import os
import sys
import re
import subprocess
from PIL import Image, ImageFilter, ImageDraw, ImageFont

VOICE = "en-US-ChristopherNeural"

# 10 Corrected Scenes aligned with 100% strict compliance & mobile-ready typography
SCENES = [
    {
        "id": "01",
        "title": "FEMICORE REVIEW  •  INGREDIENTS, CLAIMS & WHAT TO KNOW",
        "effect": "zoom_in",
        "sentences": [
            "If you find yourself waking up multiple times every night to rush to the bathroom, or feeling that sudden urge whenever you cough, laugh, or go for a walk, you are definitely not alone.",
            "Bladder sensitivity and unexpected leaks can quietly disrupt daily peace of mind for millions of women.",
            "Today on Daily Health Review, we examine FemiCore—its listed ingredients, manufacturer claims, and what to know before buying."
        ]
    },
    {
        "id": "02",
        "title": "UROLOGICAL SCIENCE  •  THE URINARY MICROBIOME FACTOR",
        "effect": "zoom_in_macro",
        "sentences": [
            "For years, women were told that bladder sensitivity was simply an unavoidable part of getting older.",
            "While pelvic tone is important, recent urological research highlights the urinary microbiome as a key biological factor.",
            "Just like your digestive tract, the urinary system relies on a delicate balance of beneficial microflora."
        ]
    },
    {
        "id": "03",
        "title": "ILLUSTRATIVE URINARY HEALTH CONCEPT  •  MUCOSAL SENSITIVITY",
        "effect": "pan_left_right",
        "sentences": [
            "When microflora balance is disrupted by hormonal shifts or dietary irritants, the bladder lining can become hypersensitive.",
            "This illustrative urinary health concept shows how mucosal irritation can send false signals to the brain, prompting involuntary urgency.",
            "Maintaining a calm and balanced urinary environment is essential for everyday comfort."
        ]
    },
    {
        "id": "04",
        "title": "PRODUCT OVERVIEW  •  FEMICORE BOTANICAL BLEND",
        "effect": "zoom_in",
        "sentences": [
            "This is where FemiCore is introduced as a daily dietary supplement designed for women's bladder comfort.",
            "According to the product label, it combines natural botanicals and probiotic strains to support urinary microflora.",
            "Check the product label for the complete ingredient list and other ingredients."
        ]
    },
    {
        "id": "05",
        "title": "FORMULA ANALYSIS  •  BOTANICAL & PROBIOTIC INGREDIENTS",
        "effect": "pan_right_left",
        "sentences": [
            "Inside FemiCore is a proprietary blend of botanical ingredients and probiotic strains listed by the manufacturer.",
            "Manufacturer claims are not the same as clinical evidence for the finished formula.",
            "Individual ingredient research does not establish that FemiCore delivers the advertised results."
        ]
    },
    {
        "id": "06",
        "title": "USAGE GUIDELINES  •  MANUFACTURER MORNING PROTOCOL",
        "effect": "zoom_in",
        "sentences": [
            "Using FemiCore follows a straightforward daily routine.",
            "The manufacturer recommends taking one capsule each morning with a full glass of water.",
            "As with any dietary supplement, consistency is key, and it should complement a balanced lifestyle and proper hydration."
        ]
    },
    {
        "id": "07",
        "title": "RESULTS PERSPECTIVE  •  INDIVIDUAL EXPERIENCES VARY",
        "effect": "zoom_out",
        "sentences": [
            "When evaluating user feedback, individual experiences vary; this review does not establish a results timeline.",
            "While some individuals report feeling more comfortable over time, individual biological responses differ significantly.",
            "We recommend tracking your personal routine and discussing any persistent concerns with your physician."
        ]
    },
    {
        "id": "08",
        "title": "PACKAGE BONUSES  •  INCLUDED WITH 6-BOTTLE BUNDLE",
        "effect": "pan_left_right",
        "sentences": [
            "According to the official product page, ordering the six-bottle bundle includes free domestic shipping plus three digital bonus guides.",
            "These include Seven Days to Rekindle Passion, Reset Your Gut, and Unlock Painless Hips and Legs for mobility."
        ]
    },
    {
        "id": "09",
        "title": "REFUND POLICY  •  60-DAY MONEY-BACK GUARANTEE TERMS",
        "effect": "zoom_in",
        "sentences": [
            "Orders are backed by an advertised sixty-day money-back guarantee.",
            "To qualify for a refund according to the official policy, you must return all bottles—whether empty, partially used, or full—along with the original packing slip within sixty days."
        ]
    },
    {
        "id": "10",
        "title": "PURCHASING ADVISORY  •  MANUFACTURER'S WEBSITE & TERMS",
        "effect": "zoom_out",
        "sentences": [
            "To verify current pricing, ingredients, and purchase terms, always check the manufacturer’s website directly.",
            "You can find the direct verified link along with our full editorial review and affiliate disclosure in the description below.",
            "Thank you for watching Daily Health Review, and remember to subscribe for more balanced, evidence-based consumer reports."
        ]
    }
]

def prepare_intro_composite_image(img_folder):
    """Pastes the authentic FemiCore bottle cleanly onto Scene 01 background on the right side without covering the woman's face."""
    bg_candidates = [f for f in os.listdir(img_folder) if f.startswith("01_") and "composite" not in f]
    if not bg_candidates:
        return
    bg_path = os.path.join(img_folder, bg_candidates[0])
    bottle_path = r"C:\Users\Eusimar\.gemini\antigravity\scratch\Projeto_ClickBank_DailyHealthReview\Imagens_Oficiais\femicore_bottle.png"
    out_path = os.path.join(img_folder, "01_Cena_FemiCore_composite.png")
    
    if os.path.exists(bottle_path) and os.path.exists(bg_path):
        try:
            bg = Image.open(bg_path).convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)
            bottle = Image.open(bottle_path).convert("RGBA")
            b_h = 550
            b_w = int(bottle.width * (b_h / bottle.height))
            bottle = bottle.resize((b_w, b_h), Image.Resampling.LANCZOS)
            
            shadow = Image.new("RGBA", bg.size, (0, 0, 0, 0))
            pos_x = 1920 - b_w - 60  # ~1395
            pos_y = 1080 - b_h - 60  # ~470
            
            s_mask = bottle.split()[3]
            s_img = Image.new("RGBA", bottle.size, (0, 0, 0, 190))
            shadow.paste(s_img, (pos_x + 12, pos_y + 16), mask=s_mask)
            shadow = shadow.filter(ImageFilter.GaussianBlur(16))
            
            combined = Image.alpha_composite(bg, shadow)
            combined.paste(bottle, (pos_x, pos_y), mask=bottle.split()[3])
            combined.convert("RGB").save(out_path, "JPEG", quality=95)
            print(f"[+] Imagem de Introdução com Frasco Real na Direita: {out_path}")
        except Exception as e:
            print(f"[-] Aviso ao compor frasco real: {e}")

def prepare_scene3_cleaned_image(img_folder):
    """Inpaints the entire horizontal text band across full screen to eliminate all fragments of 'Pelvic floor repair / cellular healing'."""
    import cv2
    import numpy as np
    
    raw_candidates = [f for f in os.listdir(img_folder) if f.startswith("03_") and "cleaned" not in f and "inpainted" not in f]
    if not raw_candidates:
        return
    img_path = os.path.join(img_folder, raw_candidates[0])
    out_path = os.path.join(img_folder, "03_Cena_FemiCore_cleaned.png")
    
    try:
        img = cv2.imread(img_path)
        img = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_LANCZOS4)
        
        # Inpaint entire horizontal band where text existed
        mask = np.zeros((1080, 1920), dtype=np.uint8)
        mask[140:310, 0:1920] = 255
        
        inpainted = cv2.inpaint(img, mask, inpaintRadius=15, flags=cv2.INPAINT_TELEA)
        
        pil_img = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img, 'RGBA')
        
        badge_w = 560
        badge_h = 50
        badge_x = (1920 - badge_w) // 2
        badge_y = 175
        
        draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=12, fill=(11, 17, 32, 225), outline=(251, 113, 133, 240), width=2)
        
        try:
            font = ImageFont.truetype('arialbd.ttf', 22)
        except:
            font = ImageFont.load_default()
            
        text = 'ILLUSTRATIVE CONCEPT'
        bbox = font.getbbox(text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((badge_x + (badge_w - tw)//2, badge_y + (badge_h - th)//2 - 2), text, font=font, fill=(255, 255, 255, 255))
        
        pil_img.save(out_path, 'PNG')
        print(f"[+] Imagem da Cena 03 100% limpa (faixa completa) com badge 'ILLUSTRATIVE CONCEPT': {out_path}")
    except Exception as e:
        print(f"[-] Aviso ao limpar Cena 03: {e}")

def prepare_scene5_and_6_cleaned_images(img_folder):
    """Removes D-MANNOSE text and any supplement bottles from Scene 05 and Scene 06."""
    import cv2
    import numpy as np
    
    # Scene 05: Clean laboratory glassware & extract
    raw5 = [f for f in os.listdir(img_folder) if f.startswith("05_") and "cleaned" not in f]
    if raw5:
        try:
            img5 = cv2.imread(os.path.join(img_folder, raw5[0]))
            img5_1080 = cv2.resize(img5, (1920, 1080), interpolation=cv2.INTER_LANCZOS4)
            lab_left = img5_1080[:, 0:960]
            lab_right_clean = cv2.flip(lab_left, 1)
            clean_lab = img5_1080.copy()
            clean_lab[:, 960:] = lab_right_clean
            out5 = os.path.join(img_folder, "05_Cena_FemiCore_cleaned.png")
            cv2.imwrite(out5, clean_lab)
            print(f"[+] Imagem da Cena 05 limpa (sem frasco): {out5}")
        except Exception as e:
            print(f"[-] Aviso ao limpar Cena 05: {e}")

    # Scene 06: Clean macro botanicals without any label or supplement bottle
    raw6 = [f for f in os.listdir(img_folder) if f.startswith("06_") and "cleaned" not in f]
    if raw6:
        try:
            img6 = cv2.imread(os.path.join(img_folder, raw6[0]))
            img6_1080 = cv2.resize(img6, (1920, 1080), interpolation=cv2.INTER_LANCZOS4)
            gray6 = cv2.cvtColor(img6_1080, cv2.COLOR_BGR2GRAY)
            _, th6 = cv2.threshold(gray6, 175, 255, cv2.THRESH_BINARY)
            kernel = np.ones((11,11), np.uint8)
            mask6 = cv2.dilate(th6, kernel, iterations=3)
            mask6_final = np.zeros((1080, 1920), dtype=np.uint8)
            mask6_final[250:950, 100:1800] = mask6[250:950, 100:1800]
            clean_botanical = cv2.inpaint(img6_1080, mask6_final, inpaintRadius=15, flags=cv2.INPAINT_TELEA)
            out6 = os.path.join(img_folder, "06_Cena_FemiCore_cleaned.png")
            cv2.imwrite(out6, clean_botanical)
            print(f"[+] Imagem da Cena 06 limpa (sem rótulos D-Mannose): {out6}")
        except Exception as e:
            print(f"[-] Aviso ao limpar Cena 06: {e}")

def find_image_file_strict(folder, scene_id):
    if scene_id == "01":
        comp = os.path.join(folder, "01_Cena_FemiCore_composite.png")
        if os.path.exists(comp):
            return comp
    if scene_id == "03":
        cleaned = os.path.join(folder, "03_Cena_FemiCore_cleaned.png")
        if os.path.exists(cleaned):
            return cleaned
    if scene_id == "05":
        cleaned = os.path.join(folder, "05_Cena_FemiCore_cleaned.png")
        if os.path.exists(cleaned):
            return cleaned
    if scene_id == "06":
        cleaned = os.path.join(folder, "06_Cena_FemiCore_cleaned.png")
        if os.path.exists(cleaned):
            return cleaned
    prefix = f"{scene_id}_"
    for f in sorted(os.listdir(folder)):
        if f.startswith(prefix) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) and "composite" not in f and "cleaned" not in f:
            return os.path.join(folder, f)
    for f in sorted(os.listdir(folder)):
        if f"Cena_{scene_id}" in f and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            return os.path.join(folder, f)
    raise FileNotFoundError(f"Imagem correspondente da Cena {scene_id} não encontrada em {folder}")

def get_audio_duration(audio_path):
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{audio_path}"'
    res = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    return float(res)

def parse_time_srt(ts):
    ts = ts.replace('.', ',')
    parts = ts.split(':')
    h = int(parts[0])
    m = int(parts[1])
    s_parts = parts[2].split(',')
    s = int(s_parts[0])
    ms = int(s_parts[1]) if len(s_parts) > 1 else 0
    return h * 3600 + m * 60 + s + ms / 1000.0

def format_ass_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def create_full_video():
    img_folder = r"C:\Users\Eusimar\Downloads\out. 10 - 15_51"
    temp_dir = r"C:\Users\Eusimar\Downloads\_temp_femicore_render"
    downloads_dir = r"C:\Users\Eusimar\Downloads"
    os.makedirs(temp_dir, exist_ok=True)

    print("\n=======================================================")
    print("GERADOR DE VÍDEO REVIEW - FEMICORE (EDITORIAL COMPLIANT & MOBILE-OPTIMIZED)")
    print(f"PASTA DAS IMAGENS: {img_folder}")
    print("DAILY HEALTH REVIEW - QUALIDADE BROADCAST 1080p")
    print("=======================================================\n")

    # 1. Prepare Scene 1 with Real Bottle on the right
    prepare_intro_composite_image(img_folder)
    
    # 2. Prepare Scene 3 with full horizontal inpainting & Illustrative Concept badge
    prepare_scene3_cleaned_image(img_folder)

    # 3. Prepare Scenes 5 & 6 with pure lab & botanical macro (no third party bottles/labels)
    prepare_scene5_and_6_cleaned_images(img_folder)

    clip_paths = []
    total_running_time = 0.0
    all_ass_events = []

    # ASS Subtitle Master Header:
    # TopBarTitle: Alignment=8 (Top Center), Fontsize=44, MarginV=50, Pure Crisp White (&H00FFFFFF), Bold
    # Default: Alignment=2 (Bottom Center), Fontsize=42, MarginV=65, Dark-Pill Box (&HB50A0F1D)
    ass_master_path = os.path.join(temp_dir, "master_subtitles.ass")
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,42,&H00FFFFFF,&H000000FF,&H00000000,&HB50A0F1D,-1,0,0,0,100,100,0,0,3,7,0,2,80,80,65,1
Style: TopBarTitle,Arial,44,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,8,40,40,50,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    for idx, scene in enumerate(SCENES):
        scene_id = scene["id"]
        print(f"\n[Cena {scene_id}/10] Renderizando áudio e movimento suave de câmera...")

        img_path = find_image_file_strict(img_folder, scene_id)
        txt_path = os.path.join(temp_dir, f"text_{scene_id}.txt")
        audio_path = os.path.join(temp_dir, f"audio_{scene_id}.mp3")
        srt_path = os.path.join(temp_dir, f"sub_{scene_id}.srt")
        clip_path = os.path.join(temp_dir, f"clip_{scene_id}.mp4")

        # Write sentences
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(scene["sentences"]))

        # 1. Generate Voice + Subtitles with edge_tts CLI
        cmd_tts = [
            "python", "-m", "edge_tts",
            "--voice", VOICE,
            "--file", txt_path,
            "--write-media", audio_path,
            "--write-subtitles", srt_path
        ]
        subprocess.run(cmd_tts, check=True)

        dur = get_audio_duration(audio_path)
        clip_dur = dur + 0.3
        frames_count = int(clip_dur * 30)

        print(f"  -> Imagem usada: {os.path.basename(img_path)}")
        print(f"  -> Duração: {dur:.2f}s (Clip: {clip_dur:.2f}s, {frames_count} frames)")

        # Add Single Centered Top Bar Title (Large Bold White & Mobile-Ready)
        tag_start = format_ass_time(total_running_time)
        tag_end = format_ass_time(total_running_time + clip_dur)
        all_ass_events.append(f"Dialogue: 0,{tag_start},{tag_end},TopBarTitle,,0,0,0,,{scene['title']}")

        # 2. Parse SRT and adjust timestamps for master ASS
        if os.path.exists(srt_path):
            with open(srt_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            blocks = re.split(r'\n\s*\n', content)
            for b in blocks:
                lines = [l.strip() for l in b.split("\n") if l.strip()]
                if len(lines) >= 3 and "-->" in lines[1]:
                    t_parts = lines[1].split("-->")
                    t_start = parse_time_srt(t_parts[0].strip()) + total_running_time
                    t_end = parse_time_srt(t_parts[1].strip()) + total_running_time
                    sub_text = " ".join(lines[2:])
                    sub_text = re.sub(r'<[^>]+>', '', sub_text)
                    all_ass_events.append(f"Dialogue: 1,{format_ass_time(t_start)},{format_ass_time(t_end)},Default,,0,0,0,,{sub_text}")

        total_running_time += clip_dur

        # 3. Dynamic Smooth Motion Effects (Ultra Suave & Cinematográfico)
        effect = scene.get("effect", "zoom_in")
        if effect == "zoom_in":
            z_step = 0.08 / frames_count
            vf_motion = f"scale=3840x2160,zoompan=z='min(zoom+{z_step:.6f},1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames_count}:s=1920x1080:fps=30"
        elif effect == "zoom_in_macro":
            z_step = 0.12 / frames_count
            vf_motion = f"scale=3840x2160,zoompan=z='min(zoom+{z_step:.6f},1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames_count}:s=1920x1080:fps=30"
        elif effect == "zoom_out":
            z_step = 0.09 / frames_count
            vf_motion = f"scale=3840x2160,zoompan=z='if(lte(zoom,1.0),1.09,max(1.001,zoom-{z_step:.6f}))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames_count}:s=1920x1080:fps=30"
        elif effect == "pan_left_right":
            pan_step = 0.60 / frames_count
            vf_motion = f"scale=3840x2160,zoompan=z=1.08:x='if(lte(on,1),(iw-iw/zoom)*0.15,(x+((iw-iw/zoom)*{pan_step:.6f})))':y='ih/2-(ih/zoom/2)':d={frames_count}:s=1920x1080:fps=30"
        elif effect == "pan_right_left":
            pan_step = 0.60 / frames_count
            vf_motion = f"scale=3840x2160,zoompan=z=1.08:x='if(lte(on,1),(iw-iw/zoom)*0.85,(x-((iw-iw/zoom)*{pan_step:.6f})))':y='ih/2-(ih/zoom/2)':d={frames_count}:s=1920x1080:fps=30"
        else:
            z_step = 0.06 / frames_count
            vf_motion = f"scale=3840x2160,zoompan=z='min(zoom+{z_step:.6f},1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames_count}:s=1920x1080:fps=30"

        # SOLID 145px TOP BAR: Total coverage of top background text
        # Dark bar: 0x070B19@1.0 | Border: 0xFB7185@1.0 (Rose Pink 3px)
        vf_topbar = "drawbox=x=0:y=0:w=1920:h=145:color=0x070B19@1.0:t=fill,drawbox=x=0:y=142:w=1920:h=3:color=0xFB7185@1.0:t=fill"

        final_vf = f"{vf_motion},{vf_topbar}"

        cmd_clip = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", img_path,
            "-i", audio_path,
            "-vf", final_vf,
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-t", str(clip_dur),
            clip_path
        ]
        subprocess.run(cmd_clip, check=True)
        clip_paths.append(clip_path)

    # 4. Write Master ASS File
    with open(ass_master_path, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(all_ass_events))
    print(f"\n[+] Arquivo Master ASS criado: {ass_master_path}")

    # 5. Concatenate All Video Clips
    concat_txt_path = os.path.join(temp_dir, "concat_list.txt")
    with open(concat_txt_path, "w", encoding="utf-8") as f:
        for cp in clip_paths:
            escaped_cp = cp.replace("\\", "/")
            f.write(f"file '{escaped_cp}'\n")

    unburned_video = os.path.join(temp_dir, "unburned_full.mp4")
    print("\n[Concatenação] Unindo todos os clipes...")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_txt_path,
        "-c", "copy",
        unburned_video
    ]
    subprocess.run(cmd_concat, check=True)

    # 6. Burn Master Subtitles (Crisp 1080p, Mobile Optimized)
    final_output = os.path.join(downloads_dir, "FemiCore_Review_Completo_4Min_DailyHealthReview.mp4")
    print(f"\n[Masterização] Queimando legendas e título da barra superior...")
    ass_filter_path = ass_master_path.replace("\\", "/").replace(":", "\\:")
    cmd_burn = [
        "ffmpeg", "-y",
        "-i", unburned_video,
        "-vf", f"ass='{ass_filter_path}'",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        final_output
    ]
    subprocess.run(cmd_burn, check=True)

    total_mb = os.path.getsize(final_output) / (1024 * 1024)
    print("\n=======================================================")
    print("[+] VIDEO COMPLETO RENDERIZADO COM SUCESSO!")
    print(f"[*] ARQUIVO FINAL: {final_output}")
    print(f"[*] DURACAO TOTAL: {format_ass_time(total_running_time)}")
    print(f"[*] TAMANHO: {total_mb:.1f} MB")
    print("=======================================================\n")

if __name__ == "__main__":
    create_full_video()
