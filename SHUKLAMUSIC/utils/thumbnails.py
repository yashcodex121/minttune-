import os
import re
import math

import aiofiles
import aiohttp
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from textwrap import wrap
from unidecode import unidecode
import asyncio
from SHUKLAMUSIC.platforms.Youtube import _ydl_search, seconds_to_min

from SHUKLAMUSIC import app
from config import YOUTUBE_IMG_URL


CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)


# ── colour helpers ─────────────────────────────────────────────────────────────

def cover_fit(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """Resize + crop an image to fully cover a target box without distortion
    (like CSS background-size: cover) — the whole frame is filled and the
    image's original aspect ratio is preserved."""
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    target_ratio = target_w / target_h
    if src_ratio > target_ratio:
        new_h = target_h
        new_w = int(new_h * src_ratio)
    else:
        new_w = target_w
        new_h = int(new_w / src_ratio)
    resized = img.resize((new_w, new_h), Image.LANCZOS)
    x0 = (new_w - target_w) // 2
    y0 = (new_h - target_h) // 2
    return resized.crop((x0, y0, x0 + target_w, y0 + target_h))


def clear(text, limit=34):
    words, title = text.split(" "), ""
    for w in words:
        if len(title) + len(w) < limit:
            title += " " + w
    return title.strip()


def get_bot_name():
    try:
        raw = unidecode(app.name)
    except Exception:
        raw = "Music"
    cleaned = raw.replace("_", " ")
    cleaned = re.sub(r"(?i)\b(robot|bot)\b", "", cleaned)
    return " ".join(cleaned.split()) or "Music"


# ── icon helpers (vector drawn, no external assets needed) ────────────────────

def draw_play_pause(draw, cx, cy, r, fg, bg, playing=True):
    if bg[3] != 0:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=bg)
    if playing:
        bar_w = r * 0.24
        bar_h = r * 0.9
        gap = r * 0.22
        x1 = cx - gap / 2 - bar_w
        x2 = cx + gap / 2
        draw.rounded_rectangle(
            [x1, cy - bar_h / 2, x1 + bar_w, cy + bar_h / 2],
            radius=bar_w * 0.35, fill=fg,
        )
        draw.rounded_rectangle(
            [x2, cy - bar_h / 2, x2 + bar_w, cy + bar_h / 2],
            radius=bar_w * 0.35, fill=fg,
        )
    else:
        s = r * 0.95
        draw.polygon(
            [(cx - s * 0.35, cy - s * 0.55), (cx - s * 0.35, cy + s * 0.55), (cx + s * 0.65, cy)],
            fill=fg,
        )


def draw_vinyl(canvas, cx, cy, r, cover_img):
    """Draws a spinning-record style vinyl disc with grooves + a small
    circular crop of the cover art as the label, at center (cx, cy)."""
    size = r * 2
    disc = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(disc)
    d.ellipse([0, 0, size, size], fill=(14, 14, 17, 255))

    # groove rings
    ring = r - int(r * 0.10)
    step = max(1, int(r * 0.095))
    while ring > r * 0.40:
        d.ellipse(
            [r - ring, r - ring, r + ring, r + ring],
            outline=(48, 48, 55, 255), width=max(1, int(r * 0.006)),
        )
        ring -= step

    canvas.alpha_composite(disc, (cx - r, cy - r))
    draw = ImageDraw.Draw(canvas)

    # label = small circular crop of the same cover art
    label_r = int(r * 0.34)
    label = cover_img.resize((label_r * 2, label_r * 2), Image.LANCZOS).convert("RGBA")
    lmask = Image.new("L", (label_r * 2, label_r * 2), 0)
    ImageDraw.Draw(lmask).ellipse([0, 0, label_r * 2, label_r * 2], fill=255)
    label.putalpha(lmask)
    canvas.alpha_composite(label, (cx - label_r, cy - label_r))

    # center spindle hole
    hole_r = max(3, int(r * 0.055))
    draw.ellipse([cx - hole_r, cy - hole_r, cx + hole_r, cy + hole_r], fill=(8, 8, 8, 255))
    draw.ellipse(
        [cx - hole_r * 0.4, cy - hole_r * 0.4, cx + hole_r * 0.4, cy + hole_r * 0.4],
        fill=(70, 70, 70, 255),
    )
    return draw


def draw_waveform(draw, x, y, w, h, color, bars=40, seed=7):
    rnd = np.random.RandomState(seed)
    heights = rnd.uniform(0.18, 1.0, bars)
    gap = w / bars
    bw = gap * 0.42
    for i, hf in enumerate(heights):
        bh = h * hf
        bx = x + i * gap
        draw.rounded_rectangle(
            [bx, y - bh / 2, bx + bw, y + bh / 2], radius=bw / 2, fill=color
        )


def draw_volume_icon(draw, x, y, w, h, color, muted=True):
    body_w = w * 0.48
    draw.polygon(
        [(x, y + h * 0.30), (x + body_w * 0.5, y + h * 0.30),
         (x + body_w, y), (x + body_w, y + h),
         (x + body_w * 0.5, y + h * 0.70), (x, y + h * 0.70)],
        fill=color,
    )
    if muted:
        lw = max(2, int(h * 0.12))
        draw.line([(x + body_w + 5, y + h * 0.18), (x + w, y + h * 0.82)], fill=color, width=lw)
        draw.line([(x + body_w + 5, y + h * 0.82), (x + w, y + h * 0.18)], fill=color, width=lw)
    else:
        draw.arc(
            [x + body_w + 3, y + h * 0.15, x + body_w + w * 0.35, y + h * 0.85],
            start=290, end=70, fill=color, width=max(2, int(h * 0.10)),
        )


# ── main ──────────────────────────────────────────────────────────────────────

async def get_thumb(videoid: str) -> str:
    cache_path = os.path.join(CACHE_DIR, f"{videoid}_v7.png")
    if os.path.isfile(cache_path):
        return cache_path

    results = await asyncio.get_event_loop().run_in_executor(
        None, lambda: _ydl_search(f"https://www.youtube.com/watch?v={videoid}", 1)
    )
    try:
        if not results:
            raise ValueError("No results found.")
        data = results[0]
        title = re.sub(r"\W+", " ", data.get("title", "Unsupported Title")).title()
        thumbnail = data.get("thumbnail") or YOUTUBE_IMG_URL
        duration = seconds_to_min(int(data.get("duration") or 0))
        channel = data.get("channel") or data.get("uploader") or "Unknown Channel"
    except Exception:
        title, thumbnail, duration, channel = (
            "Unsupported Title", YOUTUBE_IMG_URL, "0:00", "Unknown Channel",
        )

    tmp_path = os.path.join(CACHE_DIR, f"thumb{videoid}.png")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    async with aiofiles.open(tmp_path, "wb") as f:
                        await f.write(await resp.read())
    except Exception:
        return YOUTUBE_IMG_URL

    try:
        cover_raw = Image.open(tmp_path).convert("RGBA")
        render_thumbnail(cover_raw, title, duration, channel, cache_path)
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass

    return cache_path


def render_thumbnail(cover_raw: Image.Image, title: str, duration: str, channel: str, cache_path: str):
    """All the drawing logic, split out so it can be unit-tested / demoed
    without needing a network download."""
    S = 2
    def sc(v):
        return int(v * S)

    W0, H0 = 1280, 720
    W, H = sc(W0), sc(H0)

    cover_raw = ImageEnhance.Sharpness(cover_raw).enhance(1.3)
    cover_raw = ImageEnhance.Color(cover_raw).enhance(1.2)

    WHITE = (255, 255, 255, 255)
    ACCENT = (255, 140, 30, 255)   # orange, like the waveform in the sample

    # ── LAYER 1: full blurred cover fills the whole frame ───────────────
    page_bg = cover_fit(cover_raw, W, H).convert("RGBA")
    page_bg = page_bg.filter(ImageFilter.GaussianBlur(sc(45)))
    page_bg = Image.alpha_composite(page_bg, Image.new("RGBA", (W, H), (0, 0, 0, 90)))

    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    canvas.alpha_composite(page_bg)
    draw = ImageDraw.Draw(canvas)

    # ── thin divider lines splitting the frame into 3 horizontal bands ─
    line_color = (255, 255, 255, 60)
    y_top = int(H * 0.155)
    y_bot = int(H * 0.83)
    draw.line([(0, y_top), (W, y_top)], fill=line_color, width=max(1, sc(1)))
    draw.line([(0, y_bot), (W, y_bot)], fill=line_color, width=max(1, sc(1)))

    # ── middle band: square album art + vinyl overlap ──────────────────
    band_h = y_bot - y_top
    art_size = band_h
    M = sc(50)
    art_x, art_y = M, y_top

    art = cover_raw.resize((art_size, art_size), Image.LANCZOS).convert("RGBA")
    canvas.alpha_composite(art, (art_x, art_y))

    vinyl_r = art_size // 2
    vinyl_cx = art_x + art_size - int(art_size * 0.30)
    vinyl_cy = art_y + art_size // 2
    draw = draw_vinyl(canvas, vinyl_cx, vinyl_cy, vinyl_r, cover_raw)

    # ── orange waveform, right of the vinyl ─────────────────────────────
    wf_x = vinyl_cx + vinyl_r + sc(50)
    wf_w = W - M - wf_x
    wf_y = vinyl_cy
    draw_waveform(draw, wf_x, wf_y, wf_w, sc(70), ACCENT, bars=42, seed=7)

    # ── stylish title, top-left over the album art (letter-spaced caps) ─
    def load_font(path, size):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            try:
                return ImageFont.load_default(size=size)
            except Exception:
                return ImageFont.load_default()

    FONT_BOLD = "SHUKLAMUSIC/assets/font2.ttf"
    FONT_REG = "SHUKLAMUSIC/assets/font.ttf"

    fn_title = load_font(FONT_BOLD, sc(30))
    fn_time = load_font(FONT_REG, sc(26))
    fn_watermark = load_font(FONT_REG, sc(20))

    def draw_spaced(d, xy, text, font, fill, spacing_extra=3):
        x, y = xy
        for ch in text:
            d.text((x + 1, y + 1), ch, font=font, fill=(0, 0, 0, 130))
            d.text((x, y), ch, font=font, fill=fill)
            try:
                w = font.getlength(ch)
            except Exception:
                w = font.size * 0.6
            x += w + sc(spacing_extra)

    title_lines = wrap(clear(title.upper(), 20), 12)[:2]
    ty = art_y + sc(28)
    for line in title_lines:
        draw_spaced(draw, (art_x + sc(24), ty), line, fn_title, WHITE, spacing_extra=2)
        ty += sc(40)

    # ── "TEAM HELLBOTS" watermark, top-right corner ─────────────────────
    wm_text = "TEAM HELLBOTS"
    try:
        wm_w = sum(fn_watermark.getlength(c) + sc(3) for c in wm_text)
    except Exception:
        wm_w = len(wm_text) * sc(14)
    draw_spaced(
        draw, (W - M - wm_w, sc(20)), wm_text, fn_watermark, (255, 255, 255, 190), spacing_extra=3
    )

    # ── bottom band: play/pause • time • volume, then progress bar ─────
    ctrl_y = y_bot + int((H - y_bot) * 0.30)
    play_r = sc(20)
    play_cx = M + play_r
    draw_play_pause(draw, play_cx, ctrl_y, play_r, (255, 255, 255, 255), (0, 0, 0, 0), playing=False)

    time_text = f"0:03 / {duration}"
    draw.text((play_cx + play_r + sc(20), ctrl_y - sc(16)), time_text, font=fn_time, fill=WHITE)

    vol_w, vol_h = sc(34), sc(26)
    draw_volume_icon(draw, W - M - vol_w, ctrl_y - vol_h // 2, vol_w, vol_h, WHITE, muted=True)

    # progress bar, thin, near the very bottom edge
    bar_y = H - sc(26)
    bar_x0, bar_x1 = M, W - M
    played_frac = 0.02  # ~0:03 out of full duration, like the sample
    draw.rounded_rectangle(
        [bar_x0, bar_y, bar_x1, bar_y + sc(4)], radius=sc(2), fill=(255, 255, 255, 80)
    )
    thumb_x = int(bar_x0 + (bar_x1 - bar_x0) * played_frac)
    draw.ellipse(
        [thumb_x - sc(6), bar_y - sc(4), thumb_x + sc(6), bar_y + sc(10)], fill=WHITE
    )

    canvas.convert("RGB").resize((W0, H0), Image.LANCZOS).save(
        cache_path, quality=97, optimize=False
    )
