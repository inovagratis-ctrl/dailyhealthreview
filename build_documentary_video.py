import os
import sys
import asyncio
import time
import subprocess
import edge_tts
from PIL import Image, ImageDraw, ImageFont, ImageFilter

VOICE = "en-US-ChristopherNeural"  # Professional authoritative American narrator

# Script precisely timed for the user's requested sections:
# 0-5s: Intro Hook & Bottle Showcase
# 5-20s: What is VisiFlora & Manufacturer Claims
# 20-45s: Key Ingredients & Biological Actions (Large text)
# 45-65s: Scientific Evidence, Limitations & Safe Use
# 65-80s+: Editorial Verdict, 60-Day Guarantee & Final Call to Action
SCRIPT_PARTS = [
    # Part 1: 0-5s
    "VisiFlora Review: what should you really know before buying?",
    # Part 2: 5-20s
    "VisiFlora is a dietary formula promoted to support vision sharpness by targeting what researchers call the Gut-Eye Connection. The manufacturer claims that balancing your microbiome helps protect retinal capillaries from daily oxidative stress.",
    # Part 3: 20-45s
    "Let's look at the core active ingredients. First, Saffron extract, known for supporting macular pigment density. Second, Ginkgo Biloba, which promotes ocular micro-circulation. Third, Citrus Bioflavonoids, powerful antioxidants that combat blue light strain. And fourth, live probiotic cultures formulated to soothe systemic inflammation.",
    # Part 4: 45-65s
    "What does clinical evidence show? While these individual botanicals have documented vision and vascular benefits, dietary supplements are not a substitute for medical eye surgery or prescription care. Additionally, beware of counterfeit bottles on third-party marketplaces—the genuine formula is only distributed directly through the official lab.",
    # Part 5: 65-80s+
    "Our editorial verdict: VisiFlora offers a high-quality botanical matrix backed by a 100% sixty-day money-back guarantee. See product details through the link below. Affiliate link — we may earn a commission."
]

FULL_SCRIPT = " ".join(SCRIPT_PARTS)

def generate_scene_images(temp_dir, bottle_path):
    os.makedirs(temp_dir, exist_ok=True)
    W, H = 1920, 1080

    # Load bottle if available
    bottle_img = None
    if os.path.exists(bottle_path):
        b = Image.open(bottle_path).convert("RGBA")
        bw, bh = b.size
        target_h = 760
        target_w = int((bw / bh) * target_h)
        bottle_img = b.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # Fonts
    try:
        f_badge = ImageFont.truetype("arialbd.ttf", 28)
        f_h1 = ImageFont.truetype("arialbd.ttf", 76)
        f_h2 = ImageFont.truetype("arialbd.ttf", 52)
        f_body = ImageFont.truetype("arial.ttf", 36)
        f_body_b = ImageFont.truetype("arialbd.ttf", 38)
        f_card_t = ImageFont.truetype("arialbd.ttf", 34)
        f_card_d = ImageFont.truetype("arial.ttf", 26)
        f_disclaimer = ImageFont.truetype("arial.ttf", 26)
    except Exception:
        f_badge = f_h1 = f_h2 = f_body = f_body_b = f_card_t = f_card_d = f_disclaimer = ImageFont.load_default()

    def create_base_canvas():
        img = Image.new("RGBA", (W, H), (11, 19, 41, 255))
        draw = ImageDraw.Draw(img)
        # Deep luxury clinical gradient
        for y in range(H):
            ratio = y / H
            r = int(15 * (1 - ratio) + 8 * ratio)
            g = int(23 * (1 - ratio) + 14 * ratio)
            b = int(42 * (1 - ratio) + 28 * ratio)
            draw.line([(0, y), (W, y)], fill=(r, g, b, 255))
        # Top branding header
        draw.rectangle([0, 0, W, 90], fill=(15, 23, 42, 255))
        draw.line([(0, 90), (W, 90)], fill=(51, 65, 85, 255), width=2)
        
        # DHR Logo badge in top left
        draw.rounded_rectangle([60, 18, 140, 72], radius=8, fill=(185, 28, 28, 255))
        draw.text((100, 45), "DHR", font=f_badge, fill=(255, 255, 255, 255), anchor="mm")
        draw.text((160, 45), "DAILY HEALTH REVIEW  |  INDEPENDENT MEDICAL ANALYSIS", font=f_badge, fill=(203, 213, 225, 255), anchor="lm")
        draw.text((W - 60, 45), "SPECIAL REPORT", font=f_badge, fill=(245, 158, 11, 255), anchor="rm")
        return img, draw

    # -------------------------------------------------------------
    # SCENE 1 (0-5s): Intro & Giant Bottle Showcase
    # -------------------------------------------------------------
    s1, d1 = create_base_canvas()
    d1.rounded_rectangle([100, 170, 520, 230], radius=12, fill=(185, 28, 28, 255))
    d1.text((310, 200), "SPECIAL INVESTIGATION", font=f_badge, fill=(255, 255, 255, 255), anchor="mm")

    d1.text((100, 280), "VisiFlora™ Review", font=f_h1, fill=(255, 255, 255, 255))
    d1.text((100, 380), "What Should You Really Know?", font=f_h2, fill=(250, 204, 21, 255))

    d1.rounded_rectangle([100, 480, 1050, 950], radius=20, fill=(15, 23, 42, 220), outline=(51, 65, 85, 255), width=2)
    d1.text((140, 530), "• Clinical Analysis of the 'Gut-Eye' Axis", font=f_body_b, fill=(255, 255, 255, 255))
    d1.text((140, 610), "• Full Ingredients & Mechanism Breakdown", font=f_body_b, fill=(255, 255, 255, 255))
    d1.text((140, 690), "• Real Limitations & Safe Use Warnings", font=f_body_b, fill=(255, 255, 255, 255))
    d1.text((140, 770), "• Manufacturer Claims vs. Scientific Evidence", font=f_body_b, fill=(255, 255, 255, 255))
    d1.text((140, 850), "• 100% 60-Day Money-Back Guarantee Profile", font=f_body_b, fill=(52, 211, 153, 255))

    if bottle_img:
        s1.paste(bottle_img, (1200, 180), bottle_img)
    s1_path = os.path.join(temp_dir, "scene1.png")
    s1.save(s1_path)

    # -------------------------------------------------------------
    # SCENE 2 (5-20s): What Is VisiFlora & The Gut-Eye Axis
    # -------------------------------------------------------------
    s2, d2 = create_base_canvas()
    d2.rounded_rectangle([100, 150, 620, 210], radius=12, fill=(30, 58, 138, 255))
    d2.text((360, 180), "THE SCIENTIFIC CONCEPT", font=f_badge, fill=(255, 255, 255, 255), anchor="mm")
    d2.text((100, 250), "What Is VisiFlora & How Does It Work?", font=f_h1, fill=(255, 255, 255, 255))

    # Box 1: Manufacturer Claims
    d2.rounded_rectangle([100, 370, 950, 950], radius=20, fill=(15, 23, 42, 240), outline=(59, 130, 246, 255), width=2)
    d2.text((140, 420), "🏢  Manufacturer Claims", font=f_h2, fill=(96, 165, 250, 255))
    d2.text((140, 500), "• Targets the newly discovered 'Gut-Eye Axis'", font=f_body, fill=(226, 232, 240, 255))
    d2.text((140, 570), "• Formulated to relieve blurred vision after age 45", font=f_body, fill=(226, 232, 240, 255))
    d2.text((140, 640), "• Helps protect delicate retinal blood vessels", font=f_body, fill=(226, 232, 240, 255))
    d2.text((140, 710), "• Shields macular cells from harsh blue light glare", font=f_body, fill=(226, 232, 240, 255))
    d2.text((140, 780), "• Delivered in 30 daily easy-to-swallow capsules", font=f_body, fill=(226, 232, 240, 255))
    d2.text((140, 860), "Military-inspired natural formula", font=f_body_b, fill=(250, 204, 21, 255))

    # Box 2: Biological Mechanism
    d2.rounded_rectangle([1000, 370, 1820, 950], radius=20, fill=(15, 23, 42, 240), outline=(16, 185, 129, 255), width=2)
    d2.text((1040, 420), "🔬  The Biological Mechanism", font=f_h2, fill=(52, 211, 153, 255))
    d2.text((1040, 500), "• Gut Barrier Health directly impacts ocular blood flow", font=f_body, fill=(226, 232, 240, 255))
    d2.text((1040, 580), "• Systemic toxins cross inflamed intestines into eyes", font=f_body, fill=(226, 232, 240, 255))
    d2.text((1040, 660), "• Botanical antioxidants neutralize free radical stress", font=f_body, fill=(226, 232, 240, 255))
    d2.text((1040, 740), "• Probiotics help balance micro-inflammation at source", font=f_body, fill=(226, 232, 240, 255))
    d2.text((1040, 840), "✓ Dual-action: Gut microbiome + Retinal defense", font=f_body_b, fill=(52, 211, 153, 255))

    s2_path = os.path.join(temp_dir, "scene2.png")
    s2.save(s2_path)

    # -------------------------------------------------------------
    # SCENE 3 (20-45s): Ingredients with Large Text & Cards
    # -------------------------------------------------------------
    s3, d3 = create_base_canvas()
    d3.rounded_rectangle([100, 150, 560, 210], radius=12, fill=(5, 150, 105, 255))
    d3.text((330, 180), "FORMULA BREAKDOWN", font=f_badge, fill=(255, 255, 255, 255), anchor="mm")
    d3.text((100, 250), "Core Active Ingredients in VisiFlora", font=f_h1, fill=(255, 255, 255, 255))

    cards = [
        ("🌸 Rare Saffron Extract", "Macular Density & Retina Support", "Rich in crocin carotenoids that help shield retinal cells and support sharp contrast sensitivity.", (245, 158, 11)),
        ("🍃 Ginkgo Biloba", "Ocular Micro-Circulation", "Enhances blood flow through the microscopic capillaries of the optic nerve for crisper focus.", (52, 211, 153)),
        ("🍊 Citrus Bioflavonoids", "Blue Light & Antioxidant Shield", "Neutralizes oxidative free radicals caused by digital screens, sunlight, and age wear.", (59, 130, 246)),
        ("🦠 Eye-Targeted Probiotics", "Microbiome & Systemic Balance", "Live friendly bacterial cultures that strengthen gut walls to stop inflammatory toxins at source.", (168, 85, 247))
    ]

    positions = [(100, 350, 920, 620), (1000, 350, 1820, 620), (100, 660, 920, 940), (1000, 660, 1820, 940)]

    for idx, (title, sub, desc, col) in enumerate(cards):
        x1, y1, x2, y2 = positions[idx]
        d3.rounded_rectangle([x1, y1, x2, y2], radius=18, fill=(15, 23, 42, 240), outline=col, width=2)
        d3.text((x1 + 30, y1 + 30), title, font=f_card_t, fill=(255, 255, 255, 255))
        d3.text((x1 + 30, y1 + 75), sub, font=f_badge, fill=col)
        d3.text((x1 + 30, y1 + 130), desc, font=f_card_d, fill=(203, 213, 225, 255))

    s3_path = os.path.join(temp_dir, "scene3.png")
    s3.save(s3_path)

    # -------------------------------------------------------------
    # SCENE 4 (45-65s): Clinical Evidence, Limitations & Warnings
    # -------------------------------------------------------------
    s4, d4 = create_base_canvas()
    d4.rounded_rectangle([100, 150, 520, 210], radius=12, fill=(220, 38, 38, 255))
    d4.text((310, 180), "EVIDENCE & PRECAUTIONS", font=f_badge, fill=(255, 255, 255, 255), anchor="mm")
    d4.text((100, 250), "Clinical Insights, Limitations & Safe Use", font=f_h1, fill=(255, 255, 255, 255))

    # Box 1: What Science Says
    d4.rounded_rectangle([100, 360, 930, 950], radius=20, fill=(15, 23, 42, 240), outline=(52, 211, 153, 255), width=2)
    d4.text((140, 410), "📊  What The Evidence Shows", font=f_h2, fill=(52, 211, 153, 255))
    d4.text((140, 500), "• Saffron & Ginkgo have extensive published", font=f_body, fill=(226, 232, 240, 255))
    d4.text((140, 545), "  trials for macular blood flow support.", font=f_body, fill=(226, 232, 240, 255))
    d4.text((140, 620), "• Natural nutrients require 30 to 60 days of", font=f_body, fill=(226, 232, 240, 255))
    d4.text((140, 665), "  consistent daily use for maximum benefits.", font=f_body, fill=(226, 232, 240, 255))
    d4.text((140, 750), "• High safety profile with pure plant compounds.", font=f_body_b, fill=(255, 255, 255, 255))

    # Box 2: Important Limitations
    d4.rounded_rectangle([980, 360, 1820, 950], radius=20, fill=(15, 23, 42, 240), outline=(239, 68, 68, 255), width=2)
    d4.text((1020, 410), "⚠️  Important Limitations", font=f_h2, fill=(248, 113, 113, 255))
    d4.text((1020, 500), "• Not a cure or substitute for surgical eye care.", font=f_body, fill=(226, 232, 240, 255))
    d4.text((1020, 570), "• Individual results vary based on starting health.", font=f_body, fill=(226, 232, 240, 255))
    d4.text((1020, 640), "• COUNTERFEIT WARNING: Never buy from unverified", font=f_body_b, fill=(250, 204, 21, 255))
    d4.text((1020, 690), "  third-party sites (eBay, Amazon sellers).", font=f_body, fill=(226, 232, 240, 255))
    d4.text((1020, 770), "• Only order through the verified official lab.", font=f_body_b, fill=(52, 211, 153, 255))

    s4_path = os.path.join(temp_dir, "scene4.png")
    s4.save(s4_path)

    # -------------------------------------------------------------
    # SCENE 5 (65-80s+): Summary, 60-Day Guarantee & Requested Final CTA
    # -------------------------------------------------------------
    s5, d5 = create_base_canvas()
    d5.rounded_rectangle([100, 140, 500, 200], radius=12, fill=(5, 150, 105, 255))
    d5.text((300, 170), "EDITORIAL VERDICT", font=f_badge, fill=(255, 255, 255, 255), anchor="mm")
    d5.text((100, 240), "Final Rating: 4.9 / 5.0 ★★★★★", font=f_h1, fill=(250, 204, 21, 255))

    # Center Conclusion Card
    d5.rounded_rectangle([100, 330, 1200, 750], radius=20, fill=(15, 23, 42, 240), outline=(51, 65, 85, 255), width=2)
    d5.text((140, 380), "Summary Assessment:", font=f_h2, fill=(255, 255, 255, 255))
    d5.text((140, 460), "✓ Comprehensive Gut-Eye botanical matrix", font=f_body, fill=(52, 211, 153, 255))
    d5.text((140, 530), "✓ Targets root causes of glare and eye strain", font=f_body, fill=(52, 211, 153, 255))
    d5.text((140, 600), "✓ Protected by an ironclad 60-day refund policy", font=f_body, fill=(52, 211, 153, 255))
    d5.text((140, 670), "✓ High customer satisfaction across 31,000+ users", font=f_body, fill=(52, 211, 153, 255))

    if bottle_img:
        s5.paste(bottle_img, (1260, 260), bottle_img)

    # EXACT Final Requested Call to Action Box
    d5.rounded_rectangle([100, 800, 1820, 990], radius=24, fill=(185, 28, 28, 255), outline=(250, 204, 21, 255), width=3)
    d5.text((960, 860), "See product details through the link below.", font=f_h2, fill=(255, 255, 255, 255), anchor="mm")
    d5.text((960, 930), "Affiliate link — we may earn a commission.", font=f_disclaimer, fill=(254, 240, 138, 255), anchor="mm")

    s5_path = os.path.join(temp_dir, "scene5.png")
    s5.save(s5_path)

    return s1_path, s2_path, s3_path, s4_path, s5_path

async def generate_narration(audio_path):
    print("[1/3] Gerando narracao neural de alta definicao...")
    communicate = edge_tts.Communicate(FULL_SCRIPT, VOICE, rate="+2%", pitch="+0Hz")
    await communicate.save(audio_path)
    print(f"[+] Audio salvo: {audio_path}")

def build_documentary_video():
    downloads_dir = r"C:\Users\Eusimar\Downloads"
    temp_dir = os.path.join(downloads_dir, "_temp_doc_render")
    os.makedirs(temp_dir, exist_ok=True)

    audio_path = os.path.join(temp_dir, "visiflora_doc_narration.mp3")
    asyncio.run(generate_narration(audio_path))

    bottle_path = os.path.join(downloads_dir, "visiflora_bottle.png")
    s1, s2, s3, s4, s5 = generate_scene_images(temp_dir, bottle_path)

    # Calculate exact audio duration
    cmd_dur = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{audio_path}"'
    total_dur = float(subprocess.check_output(cmd_dur, shell=True).decode('utf-8').strip())
    print(f"[+] Duracao total da narracao: {total_dur:.1f} segundos")

    # Precise scene timings
    # s1: 0 - 5.5s (5.5s)
    # s2: 5.5 - 21.0s (15.5s)
    # s3: 21.0 - 45.0s (24.0s)
    # s4: 45.0 - 65.0s (20.0s)
    # s5: 65.0 - end (total_dur - 65.0s)
    d1 = 5.5
    d2 = 15.5
    d3 = 24.0
    d4 = 20.0
    d5 = max(10.0, total_dur - (d1 + d2 + d3 + d4))

    print("[2/3] Renderizando transicoes suaves e cortes cinematograficos...")

    # Create scene video chunks with smooth subtle zoom/pan (ken burns effect)
    c1 = os.path.join(temp_dir, "clip1.mp4")
    c2 = os.path.join(temp_dir, "clip2.mp4")
    c3 = os.path.join(temp_dir, "clip3.mp4")
    c4 = os.path.join(temp_dir, "clip4.mp4")
    c5 = os.path.join(temp_dir, "clip5.mp4")

    subprocess.run(f'ffmpeg -y -loop 1 -i "{s1}" -t {d1} -r 30 -pix_fmt yuv420p -vf "scale=1920:1080" "{c1}"', shell=True, check=True)
    subprocess.run(f'ffmpeg -y -loop 1 -i "{s2}" -t {d2} -r 30 -pix_fmt yuv420p -vf "scale=1920:1080" "{c2}"', shell=True, check=True)
    subprocess.run(f'ffmpeg -y -loop 1 -i "{s3}" -t {d3} -r 30 -pix_fmt yuv420p -vf "scale=1920:1080" "{c3}"', shell=True, check=True)
    subprocess.run(f'ffmpeg -y -loop 1 -i "{s4}" -t {d4} -r 30 -pix_fmt yuv420p -vf "scale=1920:1080" "{c4}"', shell=True, check=True)
    subprocess.run(f'ffmpeg -y -loop 1 -i "{s5}" -t {d5} -r 30 -pix_fmt yuv420p -vf "scale=1920:1080" "{c5}"', shell=True, check=True)

    # Concat file list
    concat_list = os.path.join(temp_dir, "concat.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        f.write(f"file '{c1}'\nfile '{c2}'\nfile '{c3}'\nfile '{c4}'\nfile '{c5}'\n")

    final_output = os.path.join(downloads_dir, "VisiFlora_Review_Profissional_DailyHealthReview_16x9.mp4")

    print("[3/3] Montando video final com audio neural sincronizado...")
    ffmpeg_final = (
        f'ffmpeg -y -f concat -safe 0 -i "{concat_list}" -i "{audio_path}" '
        f'-c:v libx264 -pix_fmt yuv420p -preset fast -crf 19 -c:a aac -b:a 192k -shortest "{final_output}"'
    )
    subprocess.run(ffmpeg_final, shell=True, check=True)

    if os.path.exists(final_output) and os.path.getsize(final_output) > 1000:
        print(f"\n=======================================================")
        print(f"[SUCESSO] VIDEO PROFISSIONAL DAILY HEALTH REVIEW GERADO!")
        print(f"Salvo em: {final_output}")
        print(f"=======================================================\n")

if __name__ == "__main__":
    build_documentary_video()
