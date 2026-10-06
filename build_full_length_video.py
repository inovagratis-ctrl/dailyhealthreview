import os
import sys
import re
import subprocess

VOICE = "en-US-ChristopherNeural"

# 12 Scenes with natural sentence breaks for optimal subtitle pacing
SCENES = [
    {
        "id": "01",
        "file_keyword": "Cena_1A",
        "effect": "zoom_in",
        "sentences": [
            "If you are over forty-five and noticing that small print, street signs, or screen glare are getting harder to focus on, you are certainly not alone.",
            "For millions of adults, morning blurriness and evening eye fatigue have become a frustrating daily struggle, leading many to search for real nutritional support."
        ]
    },
    {
        "id": "02",
        "file_keyword": "Cena_1B",
        "effect": "pan_left_right",
        "sentences": [
            "That is why VisiFlora has been gaining significant attention across the health and wellness community.",
            "Advertised as an advanced botanical formula, it claims to restore clear vision by targeting what researchers call the Gut-Eye Connection.",
            "But does it really work, or is it just another overhyped supplement?"
        ]
    },
    {
        "id": "03",
        "file_keyword": "Cena_2A",
        "effect": "zoom_in_macro",
        "sentences": [
            "To understand how VisiFlora works, we have to look at the biology of vision.",
            "Most people believe that declining eye sharpness is strictly an ocular problem.",
            "However, modern clinical science shows that your retina requires a continuous, unimpeded supply of microscopic blood flow and protective antioxidants to maintain cellular integrity."
        ]
    },
    {
        "id": "04",
        "file_keyword": "Cena_2B",
        "effect": "zoom_out",
        "sentences": [
            "Researchers have discovered that chronic low-grade inflammation originating in the digestive tract can weaken the blood-retinal barrier.",
            "When gut flora becomes imbalanced, harmful oxidative toxins can enter the bloodstream, directly irritating delicate macular tissues and worsening visual fatigue."
        ]
    },
    {
        "id": "05",
        "file_keyword": "Cena_3A",
        "effect": "zoom_in",
        "sentences": [
            "To combat this root cause, VisiFlora includes four standardized key active ingredients.",
            "First is Pure Saffron Extract.",
            "Saffron is rich in natural crocin carotenoids, which have been clinically studied in ophthalmology trials for supporting macular pigment density and improving natural contrast sensitivity in dim lighting."
        ]
    },
    {
        "id": "06",
        "file_keyword": "Cena_3B",
        "effect": "pan_right_left",
        "sentences": [
            "The second key ingredient is standardized Ginkgo Biloba extract.",
            "Known for centuries as a potent vascular tonic, Ginkgo helps promote healthy micro-circulation through the tiny capillaries that nourish the optic nerve, ensuring optimal oxygen and nutrient delivery to ocular cells."
        ]
    },
    {
        "id": "07",
        "file_keyword": "Cena_3C",
        "effect": "zoom_in",
        "sentences": [
            "Third, the formula incorporates concentrated Citrus Bioflavonoids.",
            "In our modern digital environment, our eyes face constant blue light exposure from screens and harsh artificial lighting.",
            "These bioflavonoids act as powerful natural cellular shields against daily oxidative damage."
        ]
    },
    {
        "id": "08",
        "file_keyword": "Cena_3D",
        "effect": "zoom_in_macro",
        "sentences": [
            "Fourth is the proprietary Optic Probiotic Matrix.",
            "Unlike traditional vision vitamins, VisiFlora includes live beneficial bacterial strains designed to reinforce the intestinal lining, stopping systemic inflammatory compounds before they ever reach your ocular bloodstream."
        ]
    },
    {
        "id": "09",
        "file_keyword": "Cena_4A",
        "effect": "pan_left_right",
        "sentences": [
            "Now let us discuss what you should realistically expect.",
            "VisiFlora is a natural dietary supplement, not a medical drug, and it is not a substitute for professional eye surgery or prescribed treatment.",
            "Natural plant compounds require consistent daily use, with most users noting the clearest benefits after thirty to sixty days."
        ]
    },
    {
        "id": "10",
        "file_keyword": "Cena_4B",
        "effect": "zoom_in",
        "sentences": [
            "We also have a vital consumer warning.",
            "Due to the high popularity of VisiFlora, unauthorized third-party listings on marketplaces like eBay and Amazon have surfaced with counterfeit or expired formulas.",
            "To guarantee genuine, lab-tested quality, you should only purchase directly from the official manufacturer."
        ]
    },
    {
        "id": "11",
        "file_keyword": "Cena_5A",
        "effect": "zoom_out",
        "sentences": [
            "Thousands of verified men and women across the country have reported noticeable improvements in reading comfort, reduced eye fatigue, and sharper daily clarity when combining VisiFlora with a healthy lifestyle.",
            "It is clean, non-GMO, and produced under strict GMP laboratory standards."
        ]
    },
    {
        "id": "12",
        "file_keyword": "Cena_5B",
        "effect": "zoom_in",
        "sentences": [
            "Every official bottle comes backed by an unconditional sixty-day, one-hundred-percent money-back guarantee, allowing you to test it completely risk-free.",
            "To verify current lab discounts and access the authentic formula, click the official link in the description and first pinned comment below.",
            "See product details through the link below. Affiliate link — we may earn a commission."
        ]
    }
]

def find_image_file(folder, keyword):
    for f in os.listdir(folder):
        if keyword.lower() in f.lower() and f.lower().endswith(('.jpg', '.jpeg', '.png')):
            return os.path.join(folder, f)
    raise FileNotFoundError(f"Imagem com palavra-chave '{keyword}' não encontrada em {folder}")

def get_audio_duration(audio_path):
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{audio_path}"'
    res = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    return float(res)

def parse_time_srt(ts):
    # 00:00:01,234
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
    img_folder = r"C:\Users\Eusimar\Downloads\VIDEO_VISIFLORA"
    temp_dir = r"C:\Users\Eusimar\Downloads\_temp_full_4min_render"
    downloads_dir = r"C:\Users\Eusimar\Downloads"
    os.makedirs(temp_dir, exist_ok=True)

    print("\n=======================================================")
    print("GERADOR DE VÍDEO DOCUMENTÁRIO REVIEW (3.5 A 4 MINUTOS)")
    print(f"Cenas mapeadas: {len(SCENES)} fotografias reais com animação suave")
    print("=======================================================\n")

    clip_paths = []
    total_running_time = 0.0
    all_ass_events = []

    # ASS Subtitle Header with high-contrast luxury styling
    ass_master_path = os.path.join(temp_dir, "master_subtitles.ass")
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,38,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,0,0,1,3.5,2.0,2,100,100,75,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    for idx, scene in enumerate(SCENES):
        scene_id = scene["id"]
        print(f"\n[Cena {scene_id}/12] Gerando áudio, legendas e animação da câmera...")

        img_path = find_image_file(img_folder, scene["file_keyword"])
        txt_path = os.path.join(temp_dir, f"text_{scene_id}.txt")
        audio_path = os.path.join(temp_dir, f"audio_{scene_id}.mp3")
        srt_path = os.path.join(temp_dir, f"sub_{scene_id}.srt")
        clip_path = os.path.join(temp_dir, f"clip_{scene_id}.mp4")

        # Write scene sentences to txt file
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

        print(f"  -> Imagem: {os.path.basename(img_path)}")
        print(f"  -> Duração: {dur:.2f}s (Clip: {clip_dur:.2f}s, {frames_count} frames)")

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
                    # Wrap long subtitles cleanly
                    if len(sub_text) > 55:
                        words = sub_text.split(" ")
                        mid = len(words) // 2
                        sub_text = " ".join(words[:mid]) + "\\N" + " ".join(words[mid:])
                    ass_start = format_ass_time(t_start)
                    ass_end = format_ass_time(t_end)
                    all_ass_events.append(f"Dialogue: 0,{ass_start},{ass_end},Default,,0,0,0,,{sub_text}")

        total_running_time += clip_dur

        # 3. Create Ken Burns Camera Motion Filter
        effect = scene["effect"]
        if effect == "zoom_in":
            vf_motion = f"scale=3840:2160,zoompan=z='min(zoom+0.0004,1.10)':d={frames_count}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
        elif effect == "zoom_in_macro":
            vf_motion = f"scale=3840:2160,zoompan=z='min(zoom+0.0006,1.14)':d={frames_count}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
        elif effect == "zoom_out":
            vf_motion = f"scale=3840:2160,zoompan=z='if(lte(zoom,1.0),1.10,max(1.001,zoom-0.0004))':d={frames_count}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
        elif effect == "pan_left_right":
            vf_motion = f"scale=3840:2160,zoompan=z=1.08:d={frames_count}:x='(in/{frames_count})*(iw-iw/zoom)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
        else: # pan_right_left
            vf_motion = f"scale=3840:2160,zoompan=z=1.08:d={frames_count}:x='(1-(in/{frames_count}))*(iw-iw/zoom)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"

        # Generate animated clip with audio
        cmd_clip = (
            f'ffmpeg -y -loop 1 -i "{img_path}" -i "{audio_path}" -t {clip_dur} '
            f'-vf "{vf_motion}" -c:v libx264 -pix_fmt yuv420p -preset fast -crf 18 '
            f'-c:a aac -b:a 192k -shortest "{clip_path}"'
        )
        subprocess.run(cmd_clip, shell=True, check=True)
        clip_paths.append(clip_path)

    # Write Master Subtitle File
    with open(ass_master_path, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(all_ass_events) + "\n")

    print("\n=======================================================")
    print(f"Todas as 12 cenas animadas com sucesso!")
    print(f"Tempo total do vídeo: {total_running_time:.1f}s ({total_running_time/60:.2f} minutos)")
    print(f"Legendas sincronizadas mapeadas: {len(all_ass_events)} blocos de fala")
    print("=======================================================\n")

    # Concatenate all 12 clips
    concat_txt = os.path.join(temp_dir, "concat_list.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for c in clip_paths:
            f.write(f"file '{c}'\n")

    concat_no_sub = os.path.join(temp_dir, "concat_raw.mp4")
    cmd_concat = (
        f'ffmpeg -y -f concat -safe 0 -i "{concat_txt}" '
        f'-c:v copy -c:a copy "{concat_no_sub}"'
    )
    subprocess.run(cmd_concat, shell=True, check=True)

    # Burn Synchronized Subtitles into Master Output
    final_output = os.path.join(downloads_dir, "VisiFlora_Review_Completo_4Min_DailyHealthReview.mp4")
    ass_escaped = ass_master_path.replace("\\", "/").replace(":", "\\:")
    
    print("[FINAL] Queimando legendas sincronizadas de alta resolução no vídeo master...")
    cmd_final = (
        f'ffmpeg -y -i "{concat_no_sub}" -vf "ass=\'{ass_escaped}\'" '
        f'-c:v libx264 -pix_fmt yuv420p -preset medium -crf 18 -c:a copy "{final_output}"'
    )
    subprocess.run(cmd_final, shell=True, check=True)

    if os.path.exists(final_output) and os.path.getsize(final_output) > 1000:
        print("\n=======================================================")
        print("[SUCESSO TOTAL] VÍDEO DE 4 MINUTOS RENDERIZADO COM EXCELÊNCIA!")
        print(f"[ARQUIVO] Salvo em: {final_output}")
        print(f"[DURAÇÃO] {total_running_time:.1f} segundos ({total_running_time/60:.2f} minutos)")
        print("=======================================================\n")

if __name__ == "__main__":
    create_full_video()
