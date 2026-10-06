import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def generate_thumbnail():
    downloads_dir = r"C:\Users\Eusimar\Downloads"
    os.makedirs(downloads_dir, exist_ok=True)
    
    bottle_path = os.path.join(downloads_dir, "visiflora_bottle.png")
    output_path = os.path.join(downloads_dir, "thumbnail_visiflora_youtube_1280x720.png")

    # Dimensions: 1280x720 (16:9 YouTube Thumbnail)
    W, H = 1280, 720
    img = Image.new("RGBA", (W, H), (11, 19, 41, 255))
    draw = ImageDraw.Draw(img)

    # Gradient / Vignette background (Deep Blue to Slate Black)
    for y in range(H):
        ratio = y / H
        r = int(11 * (1 - ratio) + 4 * ratio)
        g = int(19 * (1 - ratio) + 8 * ratio)
        b = int(41 * (1 - ratio) + 20 * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # Add subtle background grid & ocular accent circles
    draw.ellipse([650, -100, 1400, 650], outline=(30, 58, 138, 180), width=4)
    draw.ellipse([750, 0, 1300, 550], outline=(37, 99, 235, 120), width=3)

    # LEFT SIDE: Big Bold High-CTR Text & Badges
    # 1. Top Red Alert Badge
    draw.rounded_rectangle([60, 60, 480, 125], radius=16, fill=(220, 38, 38, 255))
    
    # Fonts
    try:
        font_alert = ImageFont.truetype("arialbd.ttf", 36)
        font_title_main = ImageFont.truetype("arialbd.ttf", 78)
        font_title_sub = ImageFont.truetype("arialbd.ttf", 52)
        font_box = ImageFont.truetype("arialbd.ttf", 32)
        font_rating = ImageFont.truetype("arialbd.ttf", 26)
    except Exception:
        font_alert = font_title_main = font_title_sub = font_box = font_rating = ImageFont.load_default()

    draw.text((270, 92), "⚠️ URGENT WARNING!", font=font_alert, fill=(255, 255, 255, 255), anchor="mm")

    # 2. Main Question Headline
    draw.text((60, 160), "DOES IT", font=font_title_main, fill=(255, 255, 255, 255))
    draw.text((60, 245), "REALLY WORK?", font=font_title_main, fill=(250, 204, 21, 255)) # Bright Yellow

    # 3. Sub-headline
    draw.text((60, 350), "20/20 Vision or Scam?", font=font_title_sub, fill=(226, 232, 240, 255))

    # 4. Feature Checklist Card
    draw.rounded_rectangle([60, 440, 640, 640], radius=18, fill=(15, 23, 42, 230), outline=(51, 65, 85, 255), width=2)
    
    draw.text((90, 475), "✓  The 'Gut-Eye' Axis Science", font=font_box, fill=(52, 211, 153, 255))
    draw.text((90, 525), "✓  Ingredients & Side Effects", font=font_box, fill=(52, 211, 153, 255))
    draw.text((90, 575), "✓  100% 60-Day Guarantee", font=font_box, fill=(52, 211, 153, 255))

    # RIGHT SIDE: Product Bottle Placement with Glow
    if os.path.exists(bottle_path):
        bottle_img = Image.open(bottle_path).convert("RGBA")
        
        # Calculate aspect ratio to fit height ~560px
        orig_w, orig_h = bottle_img.size
        target_h = 580
        target_w = int((orig_w / orig_h) * target_h)
        bottle_resized = bottle_img.resize((target_w, target_h), Image.Resampling.LANCZOS)

        # Place bottle on right
        bottle_x = 760
        bottle_y = 70

        # Create a radial glow behind the bottle
        glow_size = (target_w + 120, target_h + 120)
        glow_img = Image.new("RGBA", glow_size, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_img)
        glow_draw.ellipse([0, 0, glow_size[0], glow_size[1]], fill=(37, 99, 235, 90))
        glow_blurred = glow_img.filter(ImageFilter.GaussianBlur(35))
        img.paste(glow_blurred, (bottle_x - 60, bottle_y - 60), glow_blurred)

        # Paste Bottle
        img.paste(bottle_resized, (bottle_x, bottle_y), bottle_resized)

    # Gold Stamp / Badge in Bottom Right Corner
    draw.ellipse([1080, 500, 1240, 660], fill=(245, 158, 11, 255), outline=(254, 240, 138, 255), width=4)
    draw.ellipse([1095, 515, 1225, 645], fill=(180, 83, 9, 255))
    
    try:
        font_seal_big = ImageFont.truetype("arialbd.ttf", 34)
        font_seal_sm = ImageFont.truetype("arialbd.ttf", 18)
    except Exception:
        font_seal_big = font_seal_sm = ImageFont.load_default()

    draw.text((1160, 560), "100%", font=font_seal_big, fill=(255, 255, 255, 255), anchor="mm")
    draw.text((1160, 600), "GUARANTEE", font=font_seal_sm, fill=(254, 240, 138, 255), anchor="mm")

    # Save to Downloads
    img.save(output_path, "PNG")
    print(f"[+] Thumbnail do YouTube salva em: {output_path}")

if __name__ == "__main__":
    generate_thumbnail()
