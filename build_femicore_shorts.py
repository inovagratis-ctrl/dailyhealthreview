import os
import sys
import subprocess
from PIL import Image, ImageDraw, ImageFont

def create_top_badge(text, out_path, bg_color=(15, 23, 42, 235), border_color=(251, 113, 133, 255)):
    """Generates a high-retention top badge PNG for 1080x1920 Shorts."""
    img = Image.new("RGBA", (1080, 240), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    pad_x = 40
    pad_y = 30
    draw.rounded_rectangle([pad_x, pad_y, 1080 - pad_x, 240 - pad_y], radius=24, fill=bg_color, outline=border_color, width=4)
    
    try:
        font = ImageFont.truetype("arialbd.ttf", 36)
    except:
        font = ImageFont.load_default()
        
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (1080 - tw) // 2
    ty = (240 - th) // 2 - 4
    
    draw.text((tx + 2, ty + 2), text, font=font, fill=(0, 0, 0, 200))
    draw.text((tx, ty), text, font=font, fill=(255, 255, 255, 255))
    
    img.save(out_path, "PNG")

def create_bottom_badge(text, out_path):
    """Generates bottom CTA pill for Shorts."""
    img = Image.new("RGBA", (1080, 160), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw.rounded_rectangle([60, 20, 1080 - 60, 140], radius=20, fill=(2, 6, 23, 235), outline=(56, 189, 248, 255), width=3)
    
    try:
        font = ImageFont.truetype("arialbd.ttf", 32)
    except:
        font = ImageFont.load_default()
        
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (1080 - tw) // 2
    ty = (160 - th) // 2 - 2
    
    draw.text((tx, ty), text, font=font, fill=(248, 250, 252, 255))
    img.save(out_path, "PNG")

def build_femicore_shorts():
    master_video = r"C:\Users\Eusimar\Downloads\FemiCore_Review_Completo_4Min_DailyHealthReview.mp4"
    shorts_dir = r"C:\Users\Eusimar\Downloads\Cortes_YouTube_Shorts"
    os.makedirs(shorts_dir, exist_ok=True)
    temp_dir = os.path.join(shorts_dir, "_temp_render")
    os.makedirs(temp_dir, exist_ok=True)

    print("\n=======================================================")
    print("GERADOR DE YOUTUBE SHORTS (9:16 VERTICAL 1080x1920) - FEMICORE")
    print(f"VIDEO BASE: {master_video}")
    print(f"PASTA DE SAIDA: {shorts_dir}")
    print("=======================================================\n")

    shorts_config = [
        {
            "filename": "Short_01_FemiCore_Why_Bladder_Urgency_Isnt_Just_Aging.mp4",
            "start": "00:00:00.00",
            "duration": "48.20",
            "top_text": "BLADDER HEALTH  •  MICROBIOME SECRET",
            "bottom_text": "👉 Full Review & Official Link in Comments"
        },
        {
            "filename": "Short_02_FemiCore_3_Things_Before_Buying.mp4",
            "start": "00:02:22.00",
            "duration": "51.00",
            "top_text": "⚠️ 3 FACTS BEFORE BUYING FEMICORE",
            "bottom_text": "👉 Official Manufacturer Link in Comments"
        }
    ]

    for idx, cfg in enumerate(shorts_config, 1):
        print(f"\n[Short {idx}/2] Renderizando: {cfg['filename']}...")
        
        top_badge_png = os.path.join(temp_dir, f"top_badge_{idx}.png")
        bottom_badge_png = os.path.join(temp_dir, f"bottom_badge_{idx}.png")
        
        create_top_badge(cfg["top_text"], top_badge_png)
        create_bottom_badge(cfg["bottom_text"], bottom_badge_png)
        
        out_video_path = os.path.join(shorts_dir, cfg["filename"])
        
        filter_complex = (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.12[bg]; "
            "[0:v]scale=1080:608:force_original_aspect_ratio=decrease[fg]; "
            "[bg][fg]overlay=(W-w)/2:(H-h)/2[base]; "
            "[base][1:v]overlay=(W-w)/2:150[with_top]; "
            "[with_top][2:v]overlay=(W-w)/2:1620[outv]"
        )
        
        cmd = [
            "ffmpeg", "-y",
            "-ss", cfg["start"],
            "-t", cfg["duration"],
            "-i", master_video,
            "-i", top_badge_png,
            "-i", bottom_badge_png,
            "-filter_complex", filter_complex,
            "-map", "[outv]",
            "-map", "0:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            out_video_path
        ]
        
        subprocess.run(cmd, check=True)
        size_mb = os.path.getsize(out_video_path) / (1024 * 1024)
        print(f"  [+] Renderizado com sucesso: {out_video_path} ({size_mb:.1f} MB)")

    # Clean up temp
    for f in os.listdir(temp_dir):
        try:
            os.remove(os.path.join(temp_dir, f))
        except:
            pass
    try:
        os.rmdir(temp_dir)
    except:
        pass

    # Generate complete Viral SEO Guide
    seo_txt_path = os.path.join(shorts_dir, "SEO_VIRAL_COMPLETO_2_SHORTS_FEMICORE.txt")
    seo_content = """================================================================================
🚀 SEO VIRAL & GUIA DE PUBLICAÇÃO - 2 YOUTUBE SHORTS (FEMICORE)
Daily Health Review • Prontos para Postar Amanhã
================================================================================

--------------------------------------------------------------------------------
📱 SHORT 01: Why Bladder Urgency Isn't Just Aging (Microbiome Secret)
--------------------------------------------------------------------------------
📁 Arquivo: Short_01_FemiCore_Why_Bladder_Urgency_Isnt_Just_Aging.mp4
⏱️ Duração: 48 segundos (Ideal para 100%+ de retenção)

🎯 TÍTULOS VIRAIS (Escolha 1):
Opção 1: Waking Up at Night to Pee? It’s NOT Just Aging! 💧 #Shorts
Opção 2: The Hidden Bladder Microbiome Secret Women Need to Know 🔬 #Shorts
Opção 3: Frequent Bathroom Urges? Why Your Bladder Flora Matters! 🌸 #Shorts

📝 DESCRIÇÃO COMPLETA (Copie e Cole):
If you find yourself waking up multiple times every night or dealing with unexpected bladder leaks, you are not alone! Recent urological research highlights the delicate urinary microbiome as a key biological barrier for bladder comfort. 

👉 Check our full editorial report & verified manufacturer portal:
🔗 https://dailyhealthreviewus.com/go/femicore

📌 Pinned Comment (Comentário Fixado):
"🌸 Access the full FemiCore investigation and official manufacturer portal here ➡️ https://dailyhealthreviewus.com/go/femicore"

🏷️ TAGS / PALAVRAS-CHAVE:
femicore, femicore review, bladder control for women, urinary microbiome, frequent urination at night, bladder health supplements, daily health review, women health over 40, bladder leakage natural remedies, femicore ingredients

#️⃣ HASHTAGS:
#Shorts #WomensHealth #BladderHealth #FemiCore #HealthyHabits #DailyHealthReview #WellnessTips

--------------------------------------------------------------------------------
📱 SHORT 02: 3 Facts You MUST Know Before Buying FemiCore
--------------------------------------------------------------------------------
📁 Arquivo: Short_02_FemiCore_3_Things_Before_Buying.mp4
⏱️ Duração: 51 segundos

🎯 TÍTULOS VIRAIS (Escolha 1):
Opção 1: Thinking About FemiCore? 3 Facts You MUST Know First! ⚠️ #Shorts
Opção 2: FemiCore 60-Day Guarantee Policy Explained (Watch Before Buying!) 📦 #Shorts
Opção 3: FemiCore Review 2026: Usage Routine, Guarantee & Official Portal 🔍 #Shorts

📝 DESCRIÇÃO COMPLETA (Copie e Cole):
Before trying FemiCore for bladder health, here are 3 essential consumer facts you should know:
1️⃣ Morning Routine: Take 1 capsule with water daily.
2️⃣ 60-Day Guarantee Terms: Return all bottles (even empty) with the packing slip for a refund.
3️⃣ Safe Purchasing: Always order through the verified manufacturer website to avoid third-party issues.

👉 Verified manufacturer portal & full review:
🔗 https://dailyhealthreviewus.com/go/femicore

📌 Pinned Comment (Comentário Fixado):
"⚠️ Always check current terms on the official portal before ordering ➡️ https://dailyhealthreviewus.com/go/femicore"

🏷️ TAGS / PALAVRAS-CHAVE:
femicore review 2026, femicore guarantee, how to take femicore, femicore official website, bladder support supplement, femicore before and after, femicore scam or legit, clickbank health supplements, daily health review

#️⃣ HASHTAGS:
#Shorts #FemiCore #SupplementReview #ConsumerTips #WomensHealth #BladderSupport #DailyHealthReview
================================================================================
"""

    with open(seo_txt_path, "w", encoding="utf-8") as f:
        f.write(seo_content)
    
    print("\n=======================================================")
    print("[+] 02 SHORTS VERTICAIS RENDERIZADOS COM SUCESSO!")
    print(f"[*] ARQUIVO SEO CRIADO: {seo_txt_path}")
    print("=======================================================\n")

if __name__ == "__main__":
    build_femicore_shorts()
