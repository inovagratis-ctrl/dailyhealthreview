import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def make_product_scene(bg_img_path, bottle_img_path, output_path, badge_text="OFFICIAL FORMULA"):
    # Target size: 1920x1080
    w, h = 1920, 1080
    
    # Base background
    if os.path.exists(bg_img_path):
        base_bg = Image.open(bg_img_path).convert("RGBA")
        base_bg = base_bg.resize((w, h), Image.Resampling.LANCZOS)
        # Apply slight blur to background so product pops
        base_bg = base_bg.filter(ImageFilter.GaussianBlur(radius=8))
        # Dark overlay
        overlay = Image.new("RGBA", (w, h), (15, 23, 42, 140))
        canvas = Image.alpha_composite(base_bg, overlay)
    else:
        canvas = Image.new("RGBA", (w, h), (15, 23, 42, 255))
        
    draw = ImageDraw.Draw(canvas)
    
    # Load authentic bottle
    if os.path.exists(bottle_img_path):
        bottle = Image.open(bottle_img_path).convert("RGBA")
        # Resize bottle nicely to fit ~70% of height
        bw, bh = bottle.size
        target_h = int(h * 0.72)
        target_w = int(bw * (target_h / bh))
        bottle = bottle.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # Add shadow underneath bottle
        shadow = Image.new("RGBA", (target_w + 100, 80), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(shadow)
        sdraw.ellipse([20, 20, target_w + 80, 60], fill=(0, 0, 0, 160))
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=15))
        
        bx = (w - target_w) // 2
        by = (h - target_h) // 2 + 20
        canvas.paste(shadow, (bx - 50, by + target_h - 40), shadow)
        canvas.paste(bottle, (bx, by), bottle)
        
    # Save as high quality JPG
    final_rgb = canvas.convert("RGB")
    final_rgb.save(output_path, quality=95)
    print(f"[+] Imagem autêntica criada: {output_path}")

if __name__ == "__main__":
    img_folder = r"C:\Users\Eusimar\Downloads\VIDEO-NEUROVERA"
    official_dir = r"C:\Users\Eusimar\.gemini\antigravity\scratch\Projeto_ClickBank_DailyHealthReview\Imagens_Oficiais"
    
    bottle_single = os.path.join(official_dir, "neurovera_bottle.png")
    bottle_double = os.path.join(official_dir, "neurovera_2bottles.png")
    
    # Scene 03 (Product Intro)
    scene03_path = os.path.join(img_folder, "03_-_Cena_03_-_20261008085454.jpg")
    make_product_scene(scene03_path, bottle_double, scene03_path)
    
    # Scene 11 (Purchase Guide)
    scene11_path = os.path.join(img_folder, "11_-_Cena_11_-_20261008085454.jpg")
    make_product_scene(scene11_path, bottle_double, scene11_path)
    
    # Scene 12 (Closing)
    scene12_path = os.path.join(img_folder, "12_-_Cena_12_-_20261008085454.jpg")
    make_product_scene(scene12_path, bottle_single, scene12_path)
