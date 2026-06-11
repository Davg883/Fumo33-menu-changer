import os
import io
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ──────────────────────────────────────────────
# Brand Colour Palette
# ──────────────────────────────────────────────
GOLD = (212, 175, 55)          # #D4AF37
GOLD_BRIGHT = (242, 201, 76)   # #F2C94C
OFF_WHITE = (250, 247, 240)    # #FAF7F0
SILVER = (192, 192, 192)       # #C0C0C0
DARK_BG = (17, 17, 17)        # #111111

# ──────────────────────────────────────────────
# Font Helpers — works on Linux (Streamlit Cloud), macOS, and Windows
# ──────────────────────────────────────────────
_font_cache = {}

def _find_system_font(preferred_names, fallback="arial.ttf"):
    """Search common system font directories for a TTF/OTF file."""
    search_dirs = [
        # Linux (Streamlit Cloud uses Debian/Ubuntu)
        "/usr/share/fonts",
        "/usr/local/share/fonts",
        # macOS
        "/Library/Fonts",
        "/System/Library/Fonts",
        os.path.expanduser("~/Library/Fonts"),
        # Windows
        os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts"),
    ]
    for name in preferred_names:
        for d in search_dirs:
            if not os.path.isdir(d):
                continue
            for root, _, files in os.walk(d):
                for f in files:
                    if f.lower() == name.lower():
                        return os.path.join(root, f)
    # Last resort fallback
    for d in search_dirs:
        if not os.path.isdir(d):
            continue
        for root, _, files in os.walk(d):
            for f in files:
                if f.lower().endswith((".ttf", ".otf")):
                    return os.path.join(root, f)
    return None

def _get_font(style="sans", size=24):
    """Return a PIL ImageFont for the given style and size."""
    cache_key = (style, size)
    if cache_key in _font_cache:
        return _font_cache[cache_key]

    if style == "serif":
        # Cinzel-like: prefer a serif with uppercase character
        candidates = [
            "Cinzel-Bold.ttf", "Cinzel-Regular.ttf",
            "Georgia Bold.ttf", "georgiab.ttf", "Georgia.ttf", "georgia.ttf",
            "Times New Roman Bold.ttf", "timesbd.ttf",
            "Times New Roman.ttf", "times.ttf",
            "DejaVuSerif-Bold.ttf", "DejaVuSerif.ttf",
            "NotoSerif-Bold.ttf", "NotoSerif-Regular.ttf",
        ]
    else:
        # Outfit-like: clean modern sans-serif
        candidates = [
            "Outfit-Regular.ttf", "Outfit-Bold.ttf",
            "Calibri.ttf", "calibri.ttf",
            "Segoe UI.ttf", "segoeui.ttf",
            "Arial.ttf", "arial.ttf",
            "DejaVuSans.ttf", "DejaVuSans-Bold.ttf",
            "NotoSans-Regular.ttf", "NotoSans-Bold.ttf",
            "LiberationSans-Regular.ttf",
        ]

    path = _find_system_font(candidates)
    try:
        if path:
            font = ImageFont.truetype(path, size)
        else:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    _font_cache[cache_key] = font
    return font


# ──────────────────────────────────────────────
# Drawing Helpers
# ──────────────────────────────────────────────
def _draw_text_shadow(draw, xy, text, font, fill, shadow_offset=2, shadow_color=(0, 0, 0, 180)):
    """Draw text with a drop shadow for depth."""
    x, y = xy
    draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=fill)


def _draw_text_centered(draw, y, text, font, fill, canvas_width, shadow=True):
    """Draw horizontally-centered text at a given y position."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (canvas_width - tw) // 2
    if shadow:
        _draw_text_shadow(draw, (x, y), text, font, fill)
    else:
        draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]  # return text height


def _create_gradient_overlay(width, height, direction="bottom", base_opacity=0.6):
    """Create a gradient RGBA overlay image."""
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    if direction == "bottom":
        # Gradient from transparent top to dark bottom
        for y_pos in range(height):
            progress = y_pos / height
            # Ease-in curve for more natural gradient
            alpha = int(255 * base_opacity * (progress ** 1.5))
            alpha = min(255, alpha)
            for x_pos in range(width):
                overlay.putpixel((x_pos, y_pos), (17, 17, 17, alpha))
    elif direction == "left":
        # Gradient from dark left to transparent right
        for x_pos in range(width):
            progress = 1.0 - (x_pos / width)
            alpha = int(255 * base_opacity * (progress ** 1.3))
            alpha = min(255, alpha)
            for y_pos in range(height):
                overlay.putpixel((x_pos, y_pos), (17, 17, 17, alpha))

    return overlay


def _create_gradient_overlay_fast(width, height, direction="bottom", base_opacity=0.6):
    """Fast gradient using numpy-like line drawing instead of per-pixel."""
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    if direction == "bottom":
        for y_pos in range(height):
            progress = y_pos / height
            alpha = int(255 * base_opacity * (progress ** 1.5))
            alpha = min(255, alpha)
            draw.line([(0, y_pos), (width, y_pos)], fill=(17, 17, 17, alpha))
    elif direction == "left":
        for x_pos in range(width):
            progress = 1.0 - (x_pos / width)
            alpha = int(255 * base_opacity * (progress ** 1.3))
            alpha = min(255, alpha)
            draw.line([(x_pos, 0), (x_pos, height)], fill=(17, 17, 17, alpha))
    elif direction == "full":
        # Full darkening overlay (uniform)
        for y_pos in range(height):
            alpha = int(255 * base_opacity * 0.85)
            draw.line([(0, y_pos), (width, y_pos)], fill=(17, 17, 17, alpha))

    return overlay


def _draw_double_border(draw, width, height, padding, color=GOLD):
    """Draw an elegant double-line border frame."""
    # Outer border
    draw.rectangle(
        [padding, padding, width - padding - 1, height - padding - 1],
        outline=color + (200,), width=2
    )
    # Inner border
    inner_pad = padding + 6
    draw.rectangle(
        [inner_pad, inner_pad, width - inner_pad - 1, height - inner_pad - 1],
        outline=color + (120,), width=1
    )


def _draw_solid_border(draw, width, height, padding, color=GOLD):
    """Draw a single solid border frame."""
    draw.rectangle(
        [padding, padding, width - padding - 1, height - padding - 1],
        outline=color + (180,), width=2
    )


def _draw_badge(draw, text, xy, font, bg_color=(212, 175, 55, 40), border_color=GOLD, text_color=GOLD_BRIGHT):
    """Draw a rounded promotional badge."""
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x, pad_y = 18, 8
    rect = [x, y, x + tw + pad_x * 2, y + th + pad_y * 2]

    # Background pill
    draw.rounded_rectangle(rect, radius=20, fill=bg_color, outline=border_color + (200,), width=1)
    # Text
    draw.text((x + pad_x, y + pad_y), text, font=font, fill=text_color + (255,))
    return rect[2] - rect[0], rect[3] - rect[1]  # width, height of badge


# ──────────────────────────────────────────────
# Main Image Generator — uses PIL only (no Playwright)
# ──────────────────────────────────────────────
def generate_social_post(image_path, format_name, dish_name, description, price, badge_text,
                         overlay_opacity=0.6, border_style="double", output_path="social_post.png"):
    """
    Renders the Fumo 33 branded social post using PIL compositing.
    Formats:
      - square (1080 x 1080) — Instagram Feed / Facebook Post
      - vertical (1080 x 1920) — Instagram Story / Reel
      - landscape (1200 x 630) — Facebook Ad / Link Share
    """
    print(f"Generating social post for '{dish_name}' in format '{format_name}'...")

    # ── Dimensions ──
    dims = {
        "square":    (1080, 1080),
        "vertical":  (1080, 1920),
        "landscape": (1200, 630),
    }
    if format_name not in dims:
        raise ValueError(f"Unknown format: {format_name}")
    width, height = dims[format_name]

    # ── Font sizes scaled per format ──
    scale_factor = {"square": 1.0, "vertical": 1.3, "landscape": 0.7}[format_name]
    brand_font = _get_font("serif", int(44 * scale_factor))
    tagline_font = _get_font("sans", int(14 * scale_factor))
    badge_font = _get_font("sans", int(14 * scale_factor))
    dish_font = _get_font("serif", int(48 * scale_factor))
    price_font = _get_font("serif", int(36 * scale_factor))
    desc_font = _get_font("sans", int(20 * scale_factor))
    footer_font = _get_font("sans", int(12 * scale_factor))

    # ── Step 1: Load & resize background food image ──
    try:
        bg = Image.open(image_path).convert("RGBA")
    except Exception as e:
        print(f"Failed to open image {image_path}: {e}")
        return False

    # Cover-fit: resize maintaining aspect ratio, then centre-crop
    img_ratio = bg.width / bg.height
    target_ratio = width / height
    if img_ratio > target_ratio:
        new_h = height
        new_w = int(height * img_ratio)
    else:
        new_w = width
        new_h = int(width / img_ratio)
    bg = bg.resize((new_w, new_h), Image.LANCZOS)
    # Centre crop
    left = (new_w - width) // 2
    top = (new_h - height) // 2
    bg = bg.crop((left, top, left + width, top + height))

    # ── Step 2: Apply gradient overlay ──
    if format_name == "landscape":
        gradient = _create_gradient_overlay_fast(width, height, direction="left", base_opacity=overlay_opacity + 0.15)
    else:
        gradient = _create_gradient_overlay_fast(width, height, direction="bottom", base_opacity=overlay_opacity)
    # Also add a full-canvas light darkening for readability of top text
    top_gradient = _create_gradient_overlay_fast(width, height, direction="full", base_opacity=0.2)

    canvas = Image.alpha_composite(bg, top_gradient)
    canvas = Image.alpha_composite(canvas, gradient)

    # ── Step 3: Draw to RGBA canvas ──
    draw = ImageDraw.Draw(canvas)

    # ── Step 4: Border ──
    border_pad = int(25 * scale_factor)
    if border_style == "double":
        _draw_double_border(draw, width, height, border_pad)
    elif border_style == "solid":
        _draw_solid_border(draw, width, height, border_pad)

    content_pad = border_pad + int(20 * scale_factor)

    # ── Step 5: Layout depends on format ──
    if format_name == "landscape":
        _render_landscape(draw, canvas, width, height, content_pad,
                          brand_font, tagline_font, badge_font, dish_font,
                          price_font, desc_font, footer_font,
                          dish_name, description, price, badge_text)
    else:
        _render_portrait_or_square(draw, canvas, width, height, content_pad,
                                    brand_font, tagline_font, badge_font, dish_font,
                                    price_font, desc_font, footer_font,
                                    dish_name, description, price, badge_text, format_name)

    # ── Step 6: Save ──
    # Ensure output directory exists
    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    canvas_rgb = canvas.convert("RGB")
    canvas_rgb.save(output_path, "PNG", quality=95)
    print(f"Social post graphic compiled successfully at: {output_path}")
    return True


def _render_portrait_or_square(draw, canvas, w, h, pad,
                                brand_font, tagline_font, badge_font, dish_font,
                                price_font, desc_font, footer_font,
                                dish_name, description, price, badge_text, format_name):
    """Render the square or vertical layout: brand top-centre, dish info bottom-centre."""

    # ── Brand header (top centre) ──
    y_cursor = pad + 10
    th = _draw_text_centered(draw, y_cursor, "FUMO 33", brand_font, GOLD_BRIGHT + (255,), w)
    y_cursor += th + 4
    _draw_text_centered(draw, y_cursor, "W O O D F I R E D   K I T C H E N   &   B A R", tagline_font, GOLD + (220,), w)

    # ── Dish info block (bottom) ──
    # Calculate from bottom up
    footer_text = "📍  Ryde, Isle of Wight  •  fumo33.co.uk"
    footer_bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_h = footer_bbox[3] - footer_bbox[1]

    y_footer = h - pad - footer_h - 10

    # Dashed line above footer
    line_y = y_footer - 12
    dash_len = 8
    gap_len = 6
    x = pad + 20
    while x < w - pad - 20:
        draw.line([(x, line_y), (x + dash_len, line_y)], fill=GOLD + (80,), width=1)
        x += dash_len + gap_len

    # Footer text
    _draw_text_centered(draw, y_footer, footer_text, footer_font, (160, 160, 160, 255), w, shadow=True)

    # Description
    y_desc_bottom = line_y - 15
    desc_lines = []
    if description and str(description).strip():
        max_chars = 45 if format_name == "square" else 50
        desc_lines = textwrap.wrap(str(description).strip(), width=max_chars)

    desc_total_h = 0
    if desc_lines:
        line_h = draw.textbbox((0, 0), "Ay", font=desc_font)[3] - draw.textbbox((0, 0), "Ay", font=desc_font)[1]
        desc_total_h = len(desc_lines) * (line_h + 4)

    y_desc_start = y_desc_bottom - desc_total_h

    for i, line in enumerate(desc_lines):
        line_h = draw.textbbox((0, 0), line, font=desc_font)[3] - draw.textbbox((0, 0), line, font=desc_font)[1]
        _draw_text_centered(draw, y_desc_start + i * (line_h + 4), line, desc_font, SILVER + (230,), w)

    # Price
    price_text = f"£{price}" if price and str(price).strip() else ""
    if price_text:
        price_bbox = draw.textbbox((0, 0), price_text, font=price_font)
        price_h = price_bbox[3] - price_bbox[1]
        y_price = y_desc_start - price_h - 18
        _draw_text_centered(draw, y_price, price_text, price_font, GOLD_BRIGHT + (255,), w)
    else:
        y_price = y_desc_start - 10

    # Dish name (may wrap on 2 lines)
    name_text = str(dish_name).strip() if dish_name else ""
    if name_text:
        name_lines = textwrap.wrap(name_text, width=20)
        name_line_h = draw.textbbox((0, 0), "Ay", font=dish_font)[3] - draw.textbbox((0, 0), "Ay", font=dish_font)[1]
        name_total_h = len(name_lines) * (name_line_h + 4)
        y_name = y_price - name_total_h - 10
        for i, nl in enumerate(name_lines):
            _draw_text_centered(draw, y_name + i * (name_line_h + 4), nl, dish_font, OFF_WHITE + (255,), w)
    else:
        y_name = y_price - 10

    # Badge
    if badge_text and str(badge_text).strip():
        badge_str = str(badge_text).strip().upper()
        badge_bbox = draw.textbbox((0, 0), badge_str, font=badge_font)
        bw = badge_bbox[2] - badge_bbox[0]
        bx = (w - bw - 36) // 2
        by = y_name - 42
        _draw_badge(draw, badge_str, (bx, by), badge_font)


def _render_landscape(draw, canvas, w, h, pad,
                      brand_font, tagline_font, badge_font, dish_font,
                      price_font, desc_font, footer_font,
                      dish_name, description, price, badge_text):
    """Render the landscape (16:9) layout: content left pane, food image right."""
    pane_w = int(w * 0.45)

    # ── Brand (top-left) ──
    y_cursor = pad + 8
    _draw_text_shadow(draw, (pad + 10, y_cursor), "FUMO 33", brand_font, GOLD_BRIGHT + (255,))
    brand_h = draw.textbbox((0, 0), "FUMO 33", font=brand_font)[3]
    y_cursor += brand_h + 2
    _draw_text_shadow(draw, (pad + 10, y_cursor), "W O O D F I R E D   K I T C H E N", tagline_font, GOLD + (200,))
    tagline_h = draw.textbbox((0, 0), "Ag", font=tagline_font)[3]
    y_cursor += tagline_h + 20

    # ── Badge ──
    if badge_text and str(badge_text).strip():
        badge_str = str(badge_text).strip().upper()
        y_cursor += 10
        _draw_badge(draw, badge_str, (pad + 10, y_cursor), badge_font)
        badge_h = draw.textbbox((0, 0), badge_str, font=badge_font)[3] + 20
        y_cursor += badge_h + 15

    # ── Dish name ──
    name_text = str(dish_name).strip() if dish_name else ""
    if name_text:
        name_lines = textwrap.wrap(name_text, width=18)
        name_line_h = draw.textbbox((0, 0), "Ay", font=dish_font)[3]
        for nl in name_lines:
            _draw_text_shadow(draw, (pad + 10, y_cursor), nl, dish_font, OFF_WHITE + (255,))
            y_cursor += name_line_h + 4

    # ── Price ──
    if price and str(price).strip():
        price_text = f"£{price}"
        y_cursor += 6
        _draw_text_shadow(draw, (pad + 10, y_cursor), price_text, price_font, GOLD_BRIGHT + (255,))
        price_h = draw.textbbox((0, 0), price_text, font=price_font)[3]
        y_cursor += price_h + 10

    # ── Description ──
    if description and str(description).strip():
        desc_lines = textwrap.wrap(str(description).strip(), width=35)
        desc_line_h = draw.textbbox((0, 0), "Ay", font=desc_font)[3]
        for dl in desc_lines:
            _draw_text_shadow(draw, (pad + 10, y_cursor), dl, desc_font, SILVER + (220,))
            y_cursor += desc_line_h + 3

    # ── Footer (bottom-left) ──
    footer_text = "📍  Ryde, IOW  •  fumo33.co.uk"
    footer_h = draw.textbbox((0, 0), footer_text, font=footer_font)[3]
    y_footer = h - pad - footer_h - 10

    # Dashed divider
    line_y = y_footer - 8
    dash_len, gap_len = 6, 4
    x = pad + 10
    while x < pane_w:
        draw.line([(x, line_y), (x + dash_len, line_y)], fill=GOLD + (80,), width=1)
        x += dash_len + gap_len

    _draw_text_shadow(draw, (pad + 10, y_footer), footer_text, footer_font, (160, 160, 160, 255))


# ──────────────────────────────────────────────
# Automated Caption Generator
# ──────────────────────────────────────────────
def generate_automated_caption(tone, name, price, description, badge):
    """
    Generates structured, platform-ready social captions based on user input.
    All inputs are sanitised before template insertion.
    """
    # 1. Clean the Badge
    badge_str = str(badge).strip() if badge else ""
    badge_clean = f"[{badge_str.upper()}]" if badge_str else "[NEW DISH ALERT]"

    # 2. Clean the Name
    name_str = str(name).strip() if name else ""
    name_clean = name_str if name_str else "our newest creation"

    # 3. Clean the Price
    price_str = str(price).strip() if price else ""
    if price_str:
        # Remove any stray currency symbols
        if price_str.startswith("£"):
            price_str = price_str[1:]
        try:
            val = float(price_str)
            if val > 0:
                price_clean = f"for only £{val:.2f}"
            else:
                price_clean = "today"
        except ValueError:
            price_clean = f"for only £{price_str}"
    else:
        price_clean = "today"

    # 4. Clean the Description
    desc_str = str(description).strip() if description else ""
    desc_clean = f"\n\n{desc_str}\n" if desc_str else ""

    # 5. Build the "our" prefix to avoid "our our X" grammar bug
    our_prefix = "" if "our" in name_clean.lower() else "our "

    # 6. Normalise Tone string for reliable matching
    tone_normalized = str(tone).strip().lower()

    # ── Hype / Energetic ──
    if "hype" in tone_normalized or "energetic" in tone_normalized:
        return f"""🔥 {badge_clean} 🔥

Weekend plans? Sorted. Say hello to {our_prefix}mouth-watering {name_clean}! 🤤{desc_clean}
Indulge {price_clean} at Fumo 33. This is the ultimate fuel to kickstart your weekend. 

Tables are filling fast—don't miss out. 

📍 33 Union Street, Ryde
🔗 Reserve your space: fumo33.co.uk

#Fumo33 #Ryde #IsleOfWight #IOWFood #SovereignDining #SupportLocal #IOW"""

    # ── Elegant / Sophisticated ──
    elif "elegant" in tone_normalized or "sophisticated" in tone_normalized:
        return f"""✨ {badge_clean} ✨

Introducing your new favourite: the {name_clean}. 

Crafted with precision, cooked over wood fire, and designed to deliver a refined dining experience.{desc_clean}
Available {price_clean} at Fumo 33. Pairing recommendation available from our sommelier.

Experience the art of local gastronomy.

📍 33 Union Street, Ryde
🔗 Bookings & Menu: fumo33.co.uk

#Fumo33 #Ryde #IsleOfWight #SovereignDining #BoutiqueEats #ResponsibleGastronomy"""

    # ── Local / Community Focus (default) ──
    else:
        return f"""⚓ {badge_clean} • SUPPORT LOCAL ⚓

We are proud to introduce {our_prefix}{name_clean}, built entirely on a foundation of sovereign Island sourcing.{desc_clean}
By using hand-pressed local beef, fresh vegetables, and regional bakes, we ensure that every single pound spent at Fumo 33 remains within our circular Island economy. 

Enjoy this local masterpiece {price_clean}.

📍 33 Union Street, Ryde
🔗 Support our high street: fumo33.co.uk

#Fumo33 #Ryde #IsleOfWight #SovereignDining #SupportLocal #KeepItLocal #IOWEconomy"""


# ──────────────────────────────────────────────
# CLI Test
# ──────────────────────────────────────────────
if __name__ == '__main__':
    test_img = os.path.abspath("food_images/Steak.jpg")
    if os.path.exists(test_img):
        generate_social_post(
            image_path=test_img,
            format_name="square",
            dish_name="8oz Rump Steak",
            description="Isle of Wight dry-aged rump, chargrilled over woodfire with hand-cut chips.",
            price="24.50",
            badge_text="Weekend Special",
            output_path="test_social_post.png"
        )
    else:
        print(f"Test image not found: {test_img}")
