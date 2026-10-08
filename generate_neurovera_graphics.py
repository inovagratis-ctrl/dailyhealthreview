import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

def get_font(size, bold=True):
    font_paths = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/seguisb.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
        "C:/Windows/Fonts/tahoma.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def create_gradient(width, height, start_col, end_col):
    base = Image.new('RGB', (width, height), start_col)
    top = Image.new('RGB', (width, height), end_col)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        for x in range(width):
            # Diagonal gradient
            factor = (x / width * 0.6) + (y / height * 0.4)
            mask_data.append(int(factor * 255))
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def draw_rounded_badge(draw, bbox, bg_color, border_color=None, border_width=2, radius=12):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=bg_color)
    if border_color and border_width > 0:
        draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, outline=border_color, width=border_width)

def generate_youtube_thumbnail():
    width, height = 1280, 720
    # Background: Premium dark medical navy gradient
    bg = create_gradient(width, height, (6, 15, 35), (10, 28, 65))
    draw = ImageDraw.Draw(bg, "RGBA")
    
    # Glowing cyan & amber accent elements / grid lines
    for i in range(0, width, 80):
        draw.line([(i, 0), (i, height)], fill=(14, 45, 95, 40), width=1)
    for j in range(0, height, 80):
        draw.line([(0, j), (width, j)], fill=(14, 45, 95, 40), width=1)
        
    # Subtle glowing circles
    glow_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)
    glow_draw.ellipse([800, 100, 1300, 600], fill=(0, 210, 255, 45))
    glow_draw.ellipse([50, 450, 450, 850], fill=(255, 170, 0, 35))
    glow_overlay = glow_overlay.filter(ImageFilter.GaussianBlur(50))
    bg = Image.alpha_composite(bg.convert('RGBA'), glow_overlay).convert('RGB')
    draw = ImageDraw.Draw(bg, "RGBA")
    
    # Left Content Area (Text & Badges)
    # Channel Tag
    font_tag = get_font(24, bold=True)
    draw_rounded_badge(draw, [60, 45, 440, 90], (2, 132, 199, 230), (56, 189, 248, 255), 2, 8)
    draw.text((75, 54), "DAILY HEALTH REVIEW", font=font_tag, fill=(255, 255, 255))
    
    # Investigative Warning Badge
    font_alert = get_font(22, bold=True)
    draw_rounded_badge(draw, [460, 45, 730, 90], (220, 38, 38, 230), (252, 165, 165, 255), 2, 8)
    draw.text((475, 54), "⚠️ 2026 HONEST REPORT", font=font_alert, fill=(255, 255, 255))

    # Main Headline 1: NEUROVERA REVIEW
    font_title1 = get_font(68, bold=True)
    draw.text((64, 124), "NEUROVERA", font=font_title1, fill=(0, 0, 0, 180)) # Shadow
    draw.text((60, 120), "NEUROVERA", font=font_title1, fill=(255, 255, 255))
    
    # Main Headline 2: The Brain Fog Truth
    font_title2 = get_font(48, bold=True)
    draw_rounded_badge(draw, [60, 215, 680, 290], (234, 179, 8, 240), (254, 240, 138, 255), 2, 10)
    draw.text((80, 227), "DOES IT CLEAR BRAIN FOG?", font=font_title2, fill=(15, 23, 42))

    # Sub-box: 5 Key Botanicals Analyzed
    font_bullet = get_font(26, bold=True)
    draw_rounded_badge(draw, [60, 320, 700, 520], (15, 23, 42, 210), (30, 58, 138, 255), 2, 12)
    bullets = [
        "🔬 Doctor & Science Formulation Breakdown",
        "🌿 Lion's Mane, Bacopa, Shilajit & Schisandra",
        "⚡ Acetylcholine & Synaptic Speed Support",
        "🛡️ 60-Day 100% Money-Back Guarantee Verified"
    ]
    for idx, b in enumerate(bullets):
        draw.text((85, 340 + idx * 42), b, font=font_bullet, fill=(241, 245, 249))

    # Bottom Call to Action Badge
    font_cta = get_font(30, bold=True)
    draw_rounded_badge(draw, [60, 550, 650, 635], (16, 185, 129, 240), (110, 231, 183, 255), 3, 12)
    draw.text((85, 568), "👉 MUST WATCH BEFORE YOU BUY!", font=font_cta, fill=(255, 255, 255))
    
    # Official Guarantee Ribbon
    font_badge = get_font(22, bold=True)
    draw_rounded_badge(draw, [60, 655, 380, 695], (30, 41, 59, 200), (71, 85, 105, 200), 1, 6)
    draw.text((75, 663), "Nutraville Lab • Verified Quality", font=font_badge, fill=(148, 163, 184))

    # Right Side: Bottle Display with Glow & Floating Badges
    bottle_path = "C:/Users/Eusimar/Downloads/VIDEO_NEUROVERA/neurovera_2bottles.png"
    if not os.path.exists(bottle_path):
        bottle_path = "C:/Users/Eusimar/Downloads/VIDEO_NEUROVERA/neurovera_bottle.png"
        
    if os.path.exists(bottle_path):
        bottle_img = Image.open(bottle_path).convert('RGBA')
        # Resize preserving aspect ratio
        aspect = bottle_img.width / bottle_img.height
        new_h = 560
        new_w = int(new_h * aspect)
        bottle_resized = bottle_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Position on the right
        pos_x = width - new_w - 40
        pos_y = 90
        
        # Paste bottle
        bg.paste(bottle_resized, (pos_x, pos_y), bottle_resized)
        
        # Overlay a Trust Seal over the bottle area
        draw = ImageDraw.Draw(bg, "RGBA")
        draw_rounded_badge(draw, [width - 320, 520, width - 40, 600], (220, 38, 38, 240), (254, 202, 202, 255), 2, 10)
        font_seal = get_font(26, bold=True)
        draw.text((width - 305, 542), "100% RISK-FREE", font=font_seal, fill=(255, 255, 255))
        
        font_seal_sub = get_font(18, bold=True)
        draw.text((width - 280, 573), "60-DAY GUARANTEE", font=font_seal_sub, fill=(254, 226, 226))

    out_path = "C:/Users/Eusimar/Downloads/thumbnail_neurovera_youtube_1280x720.png"
    bg.save(out_path, quality=95)
    print(f"YouTube Thumbnail saved to {out_path}")

def generate_pinterest_pin():
    width, height = 1000, 1500
    # Background gradient
    bg = create_gradient(width, height, (8, 20, 48), (15, 35, 80))
    draw = ImageDraw.Draw(bg, "RGBA")
    
    # Header Badge
    font_brand = get_font(32, bold=True)
    draw_rounded_badge(draw, [80, 60, 920, 130], (2, 132, 199, 230), (56, 189, 248, 255), 2, 12)
    draw.text((250, 75), "DAILY HEALTH REVIEW | REPORT", font=font_brand, fill=(255, 255, 255))
    
    # Catchy Title
    font_pin_title = get_font(58, bold=True)
    draw.text((80, 170), "5 Natural Botanicals That", font=font_pin_title, fill=(255, 255, 255))
    draw.text((80, 240), "CLEAR BRAIN FOG", font=font_pin_title, fill=(234, 179, 8))
    draw.text((80, 310), "& Sharpen Memory Fast", font=font_pin_title, fill=(255, 255, 255))

    # Bottle Image Placement
    bottle_path = "C:/Users/Eusimar/Downloads/VIDEO_NEUROVERA/neurovera_2bottles.png"
    if not os.path.exists(bottle_path):
        bottle_path = "C:/Users/Eusimar/Downloads/VIDEO_NEUROVERA/neurovera_bottle.png"
        
    if os.path.exists(bottle_path):
        bottle_img = Image.open(bottle_path).convert('RGBA')
        aspect = bottle_img.width / bottle_img.height
        new_h = 520
        new_w = int(new_h * aspect)
        bottle_resized = bottle_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        pos_x = (width - new_w) // 2
        bg.paste(bottle_resized, (pos_x, 400), bottle_resized)
        
    draw = ImageDraw.Draw(bg, "RGBA")
    
    # Ingredients box
    font_card = get_font(30, bold=True)
    draw_rounded_badge(draw, [80, 960, 920, 1280], (15, 23, 42, 230), (30, 58, 138, 255), 2, 16)
    cards = [
        "🌿 Lion's Mane (Nerve Growth Factor / NGF)",
        "⚡ Bacopa Monnieri (Synaptic Speed & Recall)",
        "🏔️ Shilajit Extract (Mitochondrial ATP Energy)",
        "🫐 Schisandra Berry (Brain Adaptogen & Focus)",
        "🛡️ Gotu Kola (Cerebral Microcirculation)"
    ]
    for idx, c in enumerate(cards):
        draw.text((120, 990 + idx * 56), c, font=font_card, fill=(241, 245, 249))

    # CTA Button
    font_cta = get_font(38, bold=True)
    draw_rounded_badge(draw, [80, 1320, 920, 1430], (16, 185, 129, 240), (110, 231, 183, 255), 3, 16)
    draw.text((220, 1350), "READ FULL 2026 REVIEW 👉", font=font_cta, fill=(255, 255, 255))
    
    out_path = "C:/Users/Eusimar/Downloads/pin_neurovera_pinterest_1000x1500.png"
    bg.save(out_path, quality=95)
    print(f"Pinterest Pin saved to {out_path}")

if __name__ == "__main__":
    generate_youtube_thumbnail()
    generate_pinterest_pin()
