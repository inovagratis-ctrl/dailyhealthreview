import os
from PIL import Image, ImageDraw, ImageFont

def generate_youtube_branding():
    downloads_dir = r"C:\Users\Eusimar\Downloads"
    os.makedirs(downloads_dir, exist_ok=True)

    # 1. AVATAR / PROFILE LOGO (800x800)
    img_avatar = Image.new("RGBA", (800, 800), (11, 19, 41, 255))
    draw_avatar = ImageDraw.Draw(img_avatar)

    # Draw rounded shield / circle background
    draw_avatar.ellipse([40, 40, 760, 760], fill=(185, 28, 28, 255), outline=(245, 158, 11, 255), width=12)
    draw_avatar.ellipse([80, 80, 720, 720], fill=(15, 23, 42, 255))

    # Inner circular decoration
    draw_avatar.ellipse([110, 110, 690, 690], outline=(51, 65, 85, 255), width=4)

    # Big "DHR" Text
    try:
        font_large = ImageFont.truetype("arialbd.ttf", 150)
        font_sub = ImageFont.truetype("arialbd.ttf", 36)
        font_tiny = ImageFont.truetype("arial.ttf", 26)
    except Exception:
        font_large = font_sub = font_tiny = ImageFont.load_default()

    # Draw Cross / Caduceus symbol at top
    draw_avatar.rectangle([385, 180, 415, 260], fill=(239, 68, 68, 255))
    draw_avatar.rectangle([345, 205, 455, 235], fill=(239, 68, 68, 255))

    # Text DHR
    draw_avatar.text((400, 370), "DHR", font=font_large, fill=(255, 255, 255, 255), anchor="mm")
    
    # Subtext DAILY HEALTH REVIEW
    draw_avatar.text((400, 480), "DAILY HEALTH REVIEW", font=font_sub, fill=(245, 158, 11, 255), anchor="mm")
    draw_avatar.text((400, 535), "MEDICAL & WELLNESS REPORTS", font=font_tiny, fill=(148, 163, 184, 255), anchor="mm")

    avatar_path = os.path.join(downloads_dir, "logo_perfil_youtube_dailyhealthreview.png")
    img_avatar.save(avatar_path, "PNG")
    print(f"[+] Avatar salvo em: {avatar_path}")


    # 2. YOUTUBE BANNER (2560x1440 standard YouTube dimension)
    img_banner = Image.new("RGBA", (2560, 1440), (11, 19, 41, 255))
    draw_banner = ImageDraw.Draw(img_banner)

    # Draw background gradient bars & tech aesthetic
    for i in range(1440):
        alpha = int(15 + (i / 1440) * 35)
        draw_banner.line([(0, i), (2560, i)], fill=(15, 23, 42, 255))

    # Safe Zone for YouTube is central 1546x423 (y: 508 to 931, x: 507 to 2053)
    # Safe zone background box
    draw_banner.rounded_rectangle([450, 510, 2110, 930], radius=24, fill=(15, 23, 42, 240), outline=(51, 65, 85, 255), width=3)
    
    # Left Badge in Safe Zone
    draw_banner.ellipse([530, 580, 810, 860], fill=(185, 28, 28, 255), outline=(245, 158, 11, 255), width=6)
    draw_banner.ellipse([550, 600, 790, 840], fill=(15, 23, 42, 255))

    try:
        font_b_logo = ImageFont.truetype("arialbd.ttf", 75)
        font_b_title = ImageFont.truetype("arialbd.ttf", 64)
        font_b_sub = ImageFont.truetype("arialbd.ttf", 30)
        font_b_tag = ImageFont.truetype("arial.ttf", 26)
    except Exception:
        font_b_logo = font_b_title = font_b_sub = font_b_tag = ImageFont.load_default()

    draw_banner.text((670, 720), "DHR", font=font_b_logo, fill=(255, 255, 255, 255), anchor="mm")

    # Center Text
    draw_banner.text((860, 640), "DAILY HEALTH REVIEW", font=font_b_title, fill=(255, 255, 255, 255))
    draw_banner.text((860, 725), "EVIDENCE-BASED HEALTH REPORTS & INDEPENDENT REVIEWS", font=font_b_sub, fill=(245, 158, 11, 255))
    
    # Badges / Pill tags
    tags_text = "Metabolism Protocols  •  Retinal Health  •  Cardiovascular Vitality  •  Microbiome Science"
    draw_banner.text((860, 795), tags_text, font=font_b_tag, fill=(148, 163, 184, 255))

    banner_path = os.path.join(downloads_dir, "banner_canal_youtube_dailyhealthreview.png")
    img_banner.save(banner_path, "PNG")
    print(f"[+] Banner salvo em: {banner_path}")

if __name__ == "__main__":
    generate_youtube_branding()
