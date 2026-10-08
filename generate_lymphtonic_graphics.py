import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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
            factor = (x / width * 0.5) + (y / height * 0.5)
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
    # Background: Deep Teal / Forest Gradient
    bg = create_gradient(width, height, (4, 30, 28), (8, 55, 50))
    draw = ImageDraw.Draw(bg, "RGBA")
    
    # Subtle fluid lines / grid
    for i in range(0, width, 80):
        draw.line([(i, 0), (i, height)], fill=(13, 148, 136, 40), width=1)
    for j in range(0, height, 80):
        draw.line([(0, j), (width, j)], fill=(13, 148, 136, 40), width=1)
        
    # Glowing spots
    glow_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)
    glow_draw.ellipse([800, 100, 1300, 600], fill=(20, 184, 166, 50))
    glow_draw.ellipse([50, 450, 450, 850], fill=(245, 158, 11, 40))
    glow_overlay = glow_overlay.filter(ImageFilter.GaussianBlur(50))
    bg = Image.alpha_composite(bg.convert('RGBA'), glow_overlay).convert('RGB')
    draw = ImageDraw.Draw(bg, "RGBA")
    
    # Left Content Area (Text & Badges)
    # Channel Tag
    font_tag = get_font(24, bold=True)
    draw_rounded_badge(draw, [60, 45, 440, 90], (13, 148, 136, 230), (94, 234, 212, 255), 2, 8)
    draw.text((75, 54), "DAILY HEALTH REVIEW", font=font_tag, fill=(255, 255, 255))
    
    # Alert Badge
    font_alert = get_font(22, bold=True)
    draw_rounded_badge(draw, [460, 45, 780, 90], (220, 38, 38, 230), (252, 165, 165, 255), 2, 8)
    draw.text((475, 54), "⚠️ SWOLLEN LEGS & EDEMA REPORT", font=font_alert, fill=(255, 255, 255))

    # Main Headline 1: LYMPH TONIC REVIEW
    font_title1 = get_font(66, bold=True)
    draw.text((64, 124), "LYMPH TONIC", font=font_title1, fill=(0, 0, 0, 180)) # Shadow
    draw.text((60, 120), "LYMPH TONIC", font=font_title1, fill=(255, 255, 255))
    
    # Main Headline 2: Does It Drain Swollen Legs?
    font_title2 = get_font(44, bold=True)
    draw_rounded_badge(draw, [60, 215, 680, 290], (245, 158, 11, 240), (254, 240, 138, 255), 2, 10)
    draw.text((75, 228), "DOES IT DRAIN SWOLLEN LEGS?", font=font_title2, fill=(15, 23, 42))

    # Sub-box: 600mg Botanicals Analyzed
    font_bullet = get_font(26, bold=True)
    draw_rounded_badge(draw, [60, 320, 700, 520], (15, 23, 42, 210), (13, 148, 136, 255), 2, 12)
    bullets = [
        "🔬 Doctor & Vascular Drainage Analysis",
        "🌿 Horse Chestnut, Nattokinase & Boswellia",
        "💧 Alcohol-Free Liquid Dropper Bioavailability",
        "🛡️ 60-Day 100% Money-Back Guarantee Verified"
    ]
    for idx, b in enumerate(bullets):
        draw.text((85, 340 + idx * 42), b, font=font_bullet, fill=(241, 245, 249))

    # Bottom Call to Action Badge
    font_cta = get_font(30, bold=True)
    draw_rounded_badge(draw, [60, 550, 650, 635], (16, 185, 129, 240), (110, 231, 183, 255), 3, 12)
    draw.text((85, 568), "👉 HONEST REVIEW BEFORE BUYING!", font=font_cta, fill=(255, 255, 255))
    
    # Official Guarantee Ribbon
    font_badge = get_font(22, bold=True)
    draw_rounded_badge(draw, [60, 655, 410, 695], (30, 41, 59, 200), (71, 85, 105, 200), 1, 6)
    draw.text((75, 663), "Dr. Brenner Lab • Verified Quality", font=font_badge, fill=(148, 163, 184))

    # Right Side: Bottle Bundle Display
    bottle_path = "C:/Users/Eusimar/Downloads/VIDEO_LYMPHTONIC/lymphtonic_bottles.png"
    if os.path.exists(bottle_path):
        bottle_img = Image.open(bottle_path).convert('RGBA')
        aspect = bottle_img.width / bottle_img.height
        new_h = 560
        new_w = int(new_h * aspect)
        bottle_resized = bottle_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        pos_x = width - new_w - 20
        pos_y = 80
        bg.paste(bottle_resized, (pos_x, pos_y), bottle_resized)
        
        # Overlay a Trust Seal
        draw = ImageDraw.Draw(bg, "RGBA")
        draw_rounded_badge(draw, [width - 320, 520, width - 40, 600], (220, 38, 38, 240), (254, 202, 202, 255), 2, 10)
        font_seal = get_font(26, bold=True)
        draw.text((width - 300, 542), "100% RISK-FREE", font=font_seal, fill=(255, 255, 255))
        
        font_seal_sub = get_font(18, bold=True)
        draw.text((width - 280, 573), "60-DAY GUARANTEE", font=font_seal_sub, fill=(254, 226, 226))

    out_path = "C:/Users/Eusimar/Downloads/thumbnail_lymphtonic_youtube_1280x720.png"
    bg.save(out_path, quality=95)
    print(f"YouTube Thumbnail saved to {out_path}")

def generate_pinterest_pin():
    width, height = 1000, 1500
    bg = create_gradient(width, height, (4, 30, 28), (8, 55, 52))
    draw = ImageDraw.Draw(bg, "RGBA")
    
    # Header Badge
    font_brand = get_font(32, bold=True)
    draw_rounded_badge(draw, [80, 60, 920, 130], (13, 148, 136, 230), (94, 234, 212, 255), 2, 12)
    draw.text((250, 75), "DAILY HEALTH REVIEW | REPORT", font=font_brand, fill=(255, 255, 255))
    
    # Catchy Title
    font_pin_title = get_font(56, bold=True)
    draw.text((80, 170), "How to Drain & Flush", font=font_pin_title, fill=(255, 255, 255))
    draw.text((80, 240), "SWOLLEN LEGS & ANKLES", font=font_pin_title, fill=(245, 158, 11))
    draw.text((80, 310), "Naturally (The Missing Pump)", font=font_pin_title, fill=(255, 255, 255))

    # Bottle Placement
    bottle_path = "C:/Users/Eusimar/Downloads/VIDEO_LYMPHTONIC/lymphtonic_bottles.png"
    if os.path.exists(bottle_path):
        bottle_img = Image.open(bottle_path).convert('RGBA')
        aspect = bottle_img.width / bottle_img.height
        new_h = 500
        new_w = int(new_h * aspect)
        bottle_resized = bottle_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        pos_x = (width - new_w) // 2
        bg.paste(bottle_resized, (pos_x, 410), bottle_resized)
        
    draw = ImageDraw.Draw(bg, "RGBA")
    
    # Ingredients box
    font_card = get_font(30, bold=True)
    draw_rounded_badge(draw, [80, 950, 920, 1280], (15, 23, 42, 230), (13, 148, 136, 255), 2, 16)
    cards = [
        "🌿 Horse Chestnut Aescin (Strengthens Lymph Valves)",
        "⚡ Nattokinase Enzyme (Cleanses Protein Fibrin Clogs)",
        "🛡️ Boswellia Serrata (5-LOX Leg Swelling Defense)",
        "✨ Standardized Curcumin (Vascular Endothelial Tone)",
        "💧 Alcohol-Free Drops (Fast Sublingual Absorption)"
    ]
    for idx, c in enumerate(cards):
        draw.text((120, 980 + idx * 56), c, font=font_card, fill=(241, 245, 249))

    # CTA Button
    font_cta = get_font(38, bold=True)
    draw_rounded_badge(draw, [80, 1320, 920, 1430], (16, 185, 129, 240), (110, 231, 183, 255), 3, 16)
    draw.text((220, 1350), "READ FULL 2026 REVIEW 👉", font=font_cta, fill=(255, 255, 255))
    
    out_path = "C:/Users/Eusimar/Downloads/pin_lymphtonic_pinterest_1000x1500.png"
    bg.save(out_path, quality=95)
    print(f"Pinterest Pin saved to {out_path}")

if __name__ == "__main__":
    generate_youtube_thumbnail()
    generate_pinterest_pin()
