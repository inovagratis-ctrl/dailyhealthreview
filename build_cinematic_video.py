import os
import sys
import math
import asyncio
import subprocess
import edge_tts
from PIL import Image, ImageDraw, ImageFont, ImageFilter

VOICE = "en-US-ChristopherNeural"

SCRIPT_PARTS = [
    "VisiFlora Review: what should you really know before buying?",
    "VisiFlora is a dietary formula promoted to support vision sharpness by targeting what researchers call the Gut-Eye Connection. The manufacturer claims that balancing your microbiome helps protect retinal capillaries from daily oxidative stress.",
    "Let's look at the core active ingredients. First, Saffron extract, known for supporting macular pigment density. Second, Ginkgo Biloba, which promotes ocular micro-circulation. Third, Citrus Bioflavonoids, powerful antioxidants that combat blue light strain. And fourth, live probiotic cultures formulated to soothe systemic inflammation.",
    "What does clinical evidence show? While these individual botanicals have documented vision and vascular benefits, dietary supplements are not a substitute for medical eye surgery or prescription care. Additionally, beware of counterfeit bottles on third-party marketplaces—the genuine formula is only distributed directly through the official lab.",
    "Our editorial verdict: VisiFlora offers a high-quality botanical matrix backed by a 100% sixty-day money-back guarantee. See product details through the link below. Affiliate link — we may earn a commission."
]

FULL_SCRIPT = " ".join(SCRIPT_PARTS)

def wrap_text(text, font, max_width, draw):
    words = text.split(" ")
    lines = []
    curr = ""
    for w in words:
        test = curr + (" " if curr else "") + w
        bbox = draw.textbbox((0, 0), test, font=font)
        width = bbox[2] - bbox[0]
        if width <= max_width:
            curr = test
        else:
            if curr:
                lines.append(curr)
            curr = w
    if curr:
        lines.append(curr)
    return lines

def draw_star(draw, cx, cy, r_outer, r_inner, fill_col=(250, 204, 21), outline_col=(217, 119, 6)):
    points = []
    for i in range(10):
        r = r_outer if i % 2 == 0 else r_inner
        angle = i * math.pi / 5 - math.pi / 2
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill_col, outline=outline_col)

def draw_check_badge(draw, cx, cy, r=16, bg_col=(5, 150, 105), outline_col=(52, 211, 153)):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=bg_col, outline=outline_col, width=2)
    draw.line([(cx - 7, cy), (cx - 2, cy + 5), (cx + 7, cy - 5)], fill=(255, 255, 255), width=3)

def draw_warn_badge(draw, cx, cy, r=16, bg_col=(185, 28, 28), outline_col=(248, 113, 113)):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=bg_col, outline=outline_col, width=2)
    draw.line([(cx, cy - 8), (cx, cy + 2)], fill=(255, 255, 255), width=3)
    draw.ellipse([cx - 2, cy + 5, cx + 2, cy + 9], fill=(255, 255, 255))

def create_cinematic_scenes(project_dir, temp_dir):
    os.makedirs(temp_dir, exist_ok=True)
    W, H = 1920, 1080

    img_dir = os.path.join(project_dir, "Imagens_Oficiais")
    s1_bg_path = os.path.join(img_dir, "scene1_doctor_clinic.jpg")
    s2_bg_path = os.path.join(img_dir, "scene2_retina_macro.jpg")
    s3_bg_path = os.path.join(img_dir, "scene3_botanicals.jpg")
    bottle_path = os.path.join(img_dir, "visiflora_bottle.png")

    # Load Bottle
    bottle_img = None
    if os.path.exists(bottle_path):
        b = Image.open(bottle_path).convert("RGBA")
        bw, bh = b.size
        th = 720
        tw = int((bw / bh) * th)
        bottle_img = b.resize((tw, th), Image.Resampling.LANCZOS)

    # Fonts
    try:
        f_top = ImageFont.truetype("arialbd.ttf", 26)
        f_title = ImageFont.truetype("arialbd.ttf", 60)
        f_sub = ImageFont.truetype("arialbd.ttf", 36)
        f_body = ImageFont.truetype("arial.ttf", 28)
        f_body_b = ImageFont.truetype("arialbd.ttf", 30)
        f_card_t = ImageFont.truetype("arialbd.ttf", 32)
        f_card_sub = ImageFont.truetype("arialbd.ttf", 24)
        f_card_d = ImageFont.truetype("arial.ttf", 24)
        f_cta_main = ImageFont.truetype("arialbd.ttf", 46)
        f_cta_sub = ImageFont.truetype("arial.ttf", 28)
    except Exception:
        f_top = f_title = f_sub = f_body = f_body_b = f_card_t = f_card_sub = f_card_d = f_cta_main = f_cta_sub = ImageFont.load_default()

    def add_top_bar(draw):
        draw.rectangle([0, 0, W, 80], fill=(15, 23, 42, 235))
        draw.line([(0, 80), (W, 80)], fill=(51, 65, 85, 200), width=2)
        draw.rounded_rectangle([50, 16, 130, 64], radius=6, fill=(185, 28, 28, 255))
        draw.text((90, 40), "DHR", font=f_top, fill=(255, 255, 255, 255), anchor="mm")
        draw.text((150, 40), "DAILY HEALTH REVIEW   |   INVESTIGATIVE WELLNESS REPORT", font=f_top, fill=(226, 232, 240, 255), anchor="lm")
        draw.text((W - 50, 40), "OCTOBER 2026 EDITION", font=f_top, fill=(250, 204, 21, 255), anchor="rm")

    # =============================================================
    # SCENE 1: Doctor Clinic Background + Frosted Card + Bottle
    # =============================================================
    bg1 = Image.open(s1_bg_path).resize((W, H)).convert("RGBA")
    overlay1 = Image.new("RGBA", (W, H), (15, 23, 42, 110))
    s1 = Image.alpha_composite(bg1, overlay1)
    d1 = ImageDraw.Draw(s1)
    add_top_bar(d1)

    card1 = Image.new("RGBA", (1020, 870), (15, 23, 42, 235))
    s1.paste(card1, (70, 130), card1)
    d1_card = ImageDraw.Draw(s1)
    d1_card.rounded_rectangle([70, 130, 1090, 1000], radius=24, outline=(51, 65, 85, 255), width=2)

    d1_card.rounded_rectangle([110, 175, 480, 225], radius=10, fill=(185, 28, 28, 255))
    d1_card.text((295, 200), "CRITICAL INVESTIGATION", font=f_top, fill=(255, 255, 255, 255), anchor="mm")

    d1_card.text((110, 260), "VisiFlora™ Review", font=f_title, fill=(255, 255, 255, 255))
    d1_card.text((110, 340), "What Should You Really Know?", font=f_sub, fill=(250, 204, 21, 255))
    d1_card.line([(110, 405), (1050, 405)], fill=(51, 65, 85, 255), width=2)

    bullets1 = [
        ("•  Analysis of the 'Gut-Eye Axis' Discovery", (241, 245, 249)),
        ("•  Full Active Ingredients & Botanical Matrix", (241, 245, 249)),
        ("•  Scientific Evidence & Important Limitations", (241, 245, 249)),
        ("•  Counterfeit Product Warning for Online Buyers", (250, 204, 21)),
        ("•  100% 60-Day Money-Back Guarantee Verification", (52, 211, 153))
    ]
    y_b = 445
    for b_text, b_col in bullets1:
        d1_card.text((110, y_b), b_text, font=f_body_b, fill=(*b_col, 255))
        y_b += 75

    d1_card.rounded_rectangle([110, 860, 1050, 950], radius=14, fill=(30, 41, 59, 255))
    d1_card.text((580, 905), "Independent Clinical Assessment by Daily Health Review", font=f_top, fill=(148, 163, 184, 255), anchor="mm")

    if bottle_img:
        s1.paste(bottle_img, (1200, 210), bottle_img)

    s1_out = os.path.join(temp_dir, "cin_scene1.png")
    s1.save(s1_out)

    # =============================================================
    # SCENE 2: Real Macro Eye / Iris + Gut-Eye Axis Glass Box
    # =============================================================
    bg2 = Image.open(s2_bg_path).resize((W, H)).convert("RGBA")
    overlay2 = Image.new("RGBA", (W, H), (15, 23, 42, 120))
    s2 = Image.alpha_composite(bg2, overlay2)
    d2 = ImageDraw.Draw(s2)
    add_top_bar(d2)

    card2 = Image.new("RGBA", (1760, 480), (15, 23, 42, 240))
    s2.paste(card2, (80, 500), card2)
    d2_card = ImageDraw.Draw(s2)
    d2_card.rounded_rectangle([80, 500, 1840, 980], radius=24, outline=(59, 130, 246, 255), width=2)

    d2_card.rounded_rectangle([130, 540, 540, 595], radius=10, fill=(30, 58, 138, 255))
    d2_card.text((335, 567), "THE SCIENTIFIC MECHANISM", font=f_top, fill=(255, 255, 255, 255), anchor="mm")

    d2_card.text((130, 625), "Understanding The 'Gut-Eye Axis'", font=f_title, fill=(255, 255, 255, 255))

    bullets2 = [
        "• Clinical studies link intestinal inflammation directly to retinal capillary health.",
        "• Toxins crossing a compromised gut barrier can reach ocular tissues, worsening blurriness.",
        "• VisiFlora combines targeted eye botanicals with live flora to support visual contrast naturally."
    ]
    y_b2 = 720
    for b_idx, b_text in enumerate(bullets2):
        col = (52, 211, 153, 255) if b_idx == 2 else (226, 232, 240, 255)
        f_use = f_body_b if b_idx == 2 else f_body
        d2_card.text((130, y_b2), b_text, font=f_use, fill=col)
        y_b2 += 70

    s2_out = os.path.join(temp_dir, "cin_scene2.png")
    s2.save(s2_out)

    # =============================================================
    # SCENE 3: Real Botanicals Background + 4 Perfectly Formatted Cards
    # =============================================================
    bg3 = Image.open(s3_bg_path).resize((W, H)).convert("RGBA")
    bg3_blur = bg3.filter(ImageFilter.GaussianBlur(3))
    overlay3 = Image.new("RGBA", (W, H), (15, 23, 42, 170))
    s3 = Image.alpha_composite(bg3_blur, overlay3)
    d3 = ImageDraw.Draw(s3)
    add_top_bar(d3)

    d3.text((960, 140), "Core Active Botanical Matrix", font=f_title, fill=(255, 255, 255, 255), anchor="mm")
    d3.text((960, 205), "Standardized Natural Ingredients & Targeted Functions", font=f_sub, fill=(250, 204, 21, 255), anchor="mm")

    ing_cards = [
        ("Saffron Extract", "Macular Pigment Support", "Rich in natural crocin antioxidants that help protect delicate retinal cells from ongoing oxidative wear.", (245, 158, 11)),
        ("Ginkgo Biloba", "Micro-Circulation", "Promotes healthy blood flow through the microscopic capillaries supplying the optic nerve and macula.", (52, 211, 153)),
        ("Citrus Bioflavonoids", "Blue Light Defense", "Provides cellular antioxidant defense to help shield ocular tissues from digital screen strain and glare.", (59, 130, 246)),
        ("Optic Probiotics", "Gut-Eye Barrier Defense", "Strengthens beneficial intestinal flora to help stop systemic inflammatory toxins from reaching the eyes.", (168, 85, 247))
    ]

    coords = [(90, 270, 920, 590), (1000, 270, 1830, 590), (90, 630, 920, 950), (1000, 630, 1830, 950)]
    for idx, (title, sub, desc, border_col) in enumerate(ing_cards):
        x1, y1, x2, y2 = coords[idx]
        card_w = x2 - x1
        card_h = y2 - y1
        card_box = Image.new("RGBA", (card_w, card_h), (15, 23, 42, 240))
        s3.paste(card_box, (x1, y1), card_box)
        d3_c = ImageDraw.Draw(s3)
        d3_c.rounded_rectangle([x1, y1, x2, y2], radius=20, outline=border_col, width=2)

        # Draw circle icon dot
        d3_c.ellipse([x1 + 35, y1 + 35, x1 + 55, y1 + 55], fill=border_col)
        d3_c.text((x1 + 70, y1 + 30), title, font=f_card_t, fill=(255, 255, 255, 255))
        d3_c.text((x1 + 70, y1 + 75), sub.upper(), font=f_card_sub, fill=border_col)
        d3_c.line([(x1 + 35, y1 + 115), (x2 - 35, y1 + 115)], fill=(51, 65, 85, 200), width=1)

        # Wrapped description text
        lines = wrap_text(desc, f_card_d, card_w - 70, d3_c)
        y_txt = y1 + 135
        for l in lines:
            d3_c.text((x1 + 35, y_txt), l, font=f_card_d, fill=(226, 232, 240, 255))
            y_txt += 36

    s3_out = os.path.join(temp_dir, "cin_scene3.png")
    s3.save(s3_out)

    # =============================================================
    # SCENE 4: Doctor Clinic Background (Soft Blur) + Evidence & Warnings
    # =============================================================
    bg4 = Image.open(s1_bg_path).resize((W, H)).convert("RGBA")
    bg4_blur = bg4.filter(ImageFilter.GaussianBlur(5))
    overlay4 = Image.new("RGBA", (W, H), (15, 23, 42, 175))
    s4 = Image.alpha_composite(bg4_blur, overlay4)
    d4 = ImageDraw.Draw(s4)
    add_top_bar(d4)

    d4.text((960, 140), "Clinical Evidence & Practical Limitations", font=f_title, fill=(255, 255, 255, 255), anchor="mm")

    # Column 1: Evidence Card
    card4_1 = Image.new("RGBA", (840, 720), (15, 23, 42, 240))
    s4.paste(card4_1, (80, 220), card4_1)
    d4_c1 = ImageDraw.Draw(s4)
    d4_c1.rounded_rectangle([80, 220, 920, 940], radius=22, outline=(52, 211, 153, 255), width=2)

    draw_check_badge(d4_c1, 130, 275, r=18, bg_col=(5, 150, 105))
    d4_c1.text((165, 260), "What The Science Shows", font=f_sub, fill=(52, 211, 153, 255))
    d4_c1.line([(110, 325), (890, 325)], fill=(51, 65, 85, 255), width=2)

    col1_items = [
        "Saffron and Ginkgo botanicals have multiple peer-reviewed trials for macular support.",
        "Natural nutrients require consistent daily use (typically 30 to 60 days) to nourish tissues.",
        "High safety profile with standardized clean plant-derived compounds."
    ]
    y_c1 = 360
    for item in col1_items:
        lines = wrap_text("• " + item, f_body, 760, d4_c1)
        for l_idx, l in enumerate(lines):
            indent = 0 if l_idx == 0 else 25
            d4_c1.text((110 + indent, y_c1), l, font=f_body, fill=(226, 232, 240, 255))
            y_c1 += 38
        y_c1 += 25

    draw_check_badge(d4_c1, 140, 865, r=16, bg_col=(5, 150, 105))
    d4_c1.text((175, 850), "Gentle & non-habit forming formula", font=f_body_b, fill=(52, 211, 153, 255))

    # Column 2: Limitations Card
    card4_2 = Image.new("RGBA", (840, 720), (15, 23, 42, 240))
    s4.paste(card4_2, (1000, 220), card4_2)
    d4_c2 = ImageDraw.Draw(s4)
    d4_c2.rounded_rectangle([1000, 220, 1840, 940], radius=22, outline=(239, 68, 68, 255), width=2)

    draw_warn_badge(d4_c2, 1050, 275, r=18, bg_col=(185, 28, 28))
    d4_c2.text((1085, 260), "Important Limitations", font=f_sub, fill=(248, 113, 113, 255))
    d4_c2.line([(1030, 325), (1810, 325)], fill=(51, 65, 85, 255), width=2)

    col2_items = [
        ("Supplements do not replace professional surgery or prescribed medical care for eye diseases.", (226, 232, 240), f_body),
        ("Individual results vary based on baseline health and lifestyle factors.", (226, 232, 240), f_body),
        ("COUNTERFEIT ALERT: Third-party sellers on unverified stores are not authorized.", (250, 204, 21), f_body_b)
    ]
    y_c2 = 360
    for item_text, col, fnt in col2_items:
        lines = wrap_text("• " + item_text, fnt, 760, d4_c2)
        for l_idx, l in enumerate(lines):
            indent = 0 if l_idx == 0 else 25
            d4_c2.text((1030 + indent, y_c2), l, font=fnt, fill=(*col, 255))
            y_c2 += 38
        y_c2 += 25

    draw_warn_badge(d4_c2, 1060, 865, r=16, bg_col=(185, 28, 28))
    d4_c2.text((1095, 850), "Order exclusively through the official lab", font=f_body_b, fill=(250, 204, 21, 255))

    s4_out = os.path.join(temp_dir, "cin_scene4.png")
    s4.save(s4_out)

    # =============================================================
    # SCENE 5: Clinic Bokeh + 5 Gold Vector Stars + Bottle + Requested Closing CTA
    # =============================================================
    bg5 = Image.open(s1_bg_path).resize((W, H)).convert("RGBA")
    bg5_blur = bg5.filter(ImageFilter.GaussianBlur(8))
    overlay5 = Image.new("RGBA", (W, H), (15, 23, 42, 190))
    s5 = Image.alpha_composite(bg5_blur, overlay5)
    d5 = ImageDraw.Draw(s5)
    add_top_bar(d5)

    # Verdict Card Left
    d5.rounded_rectangle([80, 130, 1150, 710], radius=24, fill=(15, 23, 42, 245), outline=(51, 65, 85, 255), width=2)
    
    d5.rounded_rectangle([120, 170, 480, 220], radius=10, fill=(5, 150, 105, 255))
    d5.text((300, 195), "EDITORIAL VERDICT", font=f_top, fill=(255, 255, 255, 255), anchor="mm")

    d5.text((120, 255), "Rating: 4.9 / 5.0", font=f_title, fill=(250, 204, 21, 255))
    # Draw 5 Gold Vector Stars
    star_x = 640
    star_y = 285
    for s_idx in range(5):
        draw_star(d5, star_x + s_idx * 45, star_y, r_outer=18, r_inner=8, fill_col=(250, 204, 21), outline_col=(217, 119, 6))

    d5.text((120, 345), "Summary Assessment:", font=f_sub, fill=(255, 255, 255, 255))

    v_bullets = [
        "Evidence-based Gut-Eye botanical matrix",
        "Supports retinal micro-circulation & contrast",
        "Protected by a 100% 60-Day Money-Back Guarantee",
        "Over 31,000 verified users across the US"
    ]
    y_v = 425
    for vb in v_bullets:
        draw_check_badge(d5, 145, y_v + 15, r=14, bg_col=(5, 150, 105))
        d5.text((180, y_v), vb, font=f_body_b, fill=(52, 211, 153, 255))
        y_v += 65

    if bottle_img:
        s5.paste(bottle_img, (1260, 130), bottle_img)

    # EXACT FINAL REQUESTED CALL TO ACTION BOX (Prominent & Pristine)
    d5.rounded_rectangle([80, 750, 1840, 990], radius=24, fill=(185, 28, 28, 255), outline=(250, 204, 21, 255), width=3)
    d5.text((960, 825), "See product details through the link below.", font=f_cta_main, fill=(255, 255, 255, 255), anchor="mm")
    d5.text((960, 910), "Affiliate link — we may earn a commission.", font=f_cta_sub, fill=(254, 240, 138, 255), anchor="mm")

    s5_out = os.path.join(temp_dir, "cin_scene5.png")
    s5.save(s5_out)

    return s1_out, s2_out, s3_out, s4_out, s5_out

async def generate_narration(audio_path):
    print("[1/3] Gerando narracao neural de alta fidelidade...")
    communicate = edge_tts.Communicate(FULL_SCRIPT, VOICE, rate="+2%", pitch="+0Hz")
    await communicate.save(audio_path)
    print(f"[+] Audio salvo: {audio_path}")

def build_cinematic_video():
    project_dir = r"C:\Users\Eusimar\.gemini\antigravity\scratch\Projeto_ClickBank_DailyHealthReview"
    downloads_dir = r"C:\Users\Eusimar\Downloads"
    temp_dir = os.path.join(downloads_dir, "_temp_cinematic_render")
    os.makedirs(temp_dir, exist_ok=True)

    audio_path = os.path.join(temp_dir, "visiflora_cinematic_audio.mp3")
    asyncio.run(generate_narration(audio_path))

    cmd_dur = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{audio_path}"'
    total_dur = float(subprocess.check_output(cmd_dur, shell=True).decode('utf-8').strip())
    print(f"[+] Duracao da narracao: {total_dur:.1f}s")

    s1, s2, s3, s4, s5 = create_cinematic_scenes(project_dir, temp_dir)

    # Time allocations:
    d1 = 5.5
    d2 = 15.5
    d3 = 24.0
    d4 = 20.0
    d5 = max(10.0, total_dur - (d1 + d2 + d3 + d4))

    print("[2/3] Renderizando cenas fotograficas com efeitos de transicao suave...")

    c1 = os.path.join(temp_dir, "clip1.mp4")
    c2 = os.path.join(temp_dir, "clip2.mp4")
    c3 = os.path.join(temp_dir, "clip3.mp4")
    c4 = os.path.join(temp_dir, "clip4.mp4")
    c5 = os.path.join(temp_dir, "clip5.mp4")

    # Render clips with FFmpeg
    subprocess.run(f'ffmpeg -y -loop 1 -i "{s1}" -t {d1} -r 30 -pix_fmt yuv420p -vf "scale=1920:1080" "{c1}"', shell=True, check=True)
    subprocess.run(f'ffmpeg -y -loop 1 -i "{s2}" -t {d2} -r 30 -pix_fmt yuv420p -vf "scale=1920:1080" "{c2}"', shell=True, check=True)
    subprocess.run(f'ffmpeg -y -loop 1 -i "{s3}" -t {d3} -r 30 -pix_fmt yuv420p -vf "scale=1920:1080" "{c3}"', shell=True, check=True)
    subprocess.run(f'ffmpeg -y -loop 1 -i "{s4}" -t {d4} -r 30 -pix_fmt yuv420p -vf "scale=1920:1080" "{c4}"', shell=True, check=True)
    subprocess.run(f'ffmpeg -y -loop 1 -i "{s5}" -t {d5} -r 30 -pix_fmt yuv420p -vf "scale=1920:1080" "{c5}"', shell=True, check=True)

    concat_txt = os.path.join(temp_dir, "concat.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        f.write(f"file '{c1}'\nfile '{c2}'\nfile '{c3}'\nfile '{c4}'\nfile '{c5}'\n")

    final_output = os.path.join(downloads_dir, "VisiFlora_Review_Cinematico_DailyHealthReview_16x9.mp4")

    print("[3/3] Masterizando video cinematografico final...")
    ffmpeg_final = (
        f'ffmpeg -y -f concat -safe 0 -i "{concat_txt}" -i "{audio_path}" '
        f'-c:v libx264 -pix_fmt yuv420p -preset fast -crf 18 -c:a aac -b:a 192k -shortest "{final_output}"'
    )
    subprocess.run(ffmpeg_final, shell=True, check=True)

    if os.path.exists(final_output) and os.path.getsize(final_output) > 1000:
        print("\n=======================================================")
        print("[SUCESSO] VIDEO CINEMATOGRAFICO GERADO COM SUCESSO!")
        print(f"[ARQUIVO] Salvo em: {final_output}")
        print("=======================================================\n")

if __name__ == "__main__":
    build_cinematic_video()
