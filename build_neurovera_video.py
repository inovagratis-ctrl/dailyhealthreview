import os
import sys
import re
import subprocess

VOICE = "en-US-ChristopherNeural"

# 12 Scenes aligned with 100% strict compliance & mobile-ready typography
SCENES = [
    {
        "id": "01",
        "title": "NEUROVERA REVIEW  •  EVERYDAY FOCUS & CLARITY",
        "effect": "zoom_in",
        "sentences": [
            "Have you ever walked into a room only to momentarily forget why you went there?",
            "Or found yourself searching for familiar words, feeling occasional mental sluggishness throughout your daily routine?",
            "As we age, occasional lapses in focus lead many to look for natural nutritional support.",
            "Today on Daily Health Review, we examine NeuroVera, a dietary supplement formulated with traditional botanical ingredients to support everyday focus and mental clarity."
        ]
    },
    {
        "id": "02",
        "title": "COGNITIVE WELLNESS  •  NEURAL NUTRITION & CIRCULATION",
        "effect": "zoom_in_macro",
        "sentences": [
            "Everyday cognitive performance relies on complex cellular networks, balanced neurotransmitters, and steady blood flow.",
            "Factors such as oxidative stress, daily fatigue, and nutritional gaps can influence how quickly we process information and recall details.",
            "This has led to growing interest in nootropic botanicals that provide targeted nutritional nourishment for brain health."
        ]
    },
    {
        "id": "03",
        "title": "PRODUCT OVERVIEW  •  NEUROVERA BY NUTRAVILLE",
        "effect": "zoom_in",
        "sentences": [
            "This brings us to NeuroVera by Nutraville.",
            "Marketed under the concept of everyday cognitive wellness, NeuroVera is an encapsulated dietary formula designed to support mental clarity and sustained focus.",
            "Notably, it is crafted without harsh synthetic stimulants or excessive caffeine.",
            "Let us take a closer look at the five primary botanical ingredients featured in the blend."
        ]
    },
    {
        "id": "04",
        "title": "KEY INGREDIENT  •  SCHISANDRA FRUIT EXTRACT",
        "effect": "pan_left_right",
        "sentences": [
            "First is Schisandra Fruit Extract.",
            "Traditionally used in Eastern herbal practices as an adaptogen, Schisandra is valued for helping the body adapt to daily environmental stressors.",
            "Nutritional researchers study its natural plant lignans for their antioxidant properties and potential role in supporting mental endurance."
        ]
    },
    {
        "id": "05",
        "title": "KEY INGREDIENT  •  GOTU KOLA (CENTELLA ASIATICA)",
        "effect": "zoom_in",
        "sentences": [
            "Next in the formula is Gotu Kola, known botanically as Centella Asiatica.",
            "Long recognized in traditional wellness systems, Gotu Kola is frequently studied for its triterpene compounds.",
            "It is commonly taken to support healthy circulation and promote calm, steady concentration during demanding tasks."
        ]
    },
    {
        "id": "06",
        "title": "MINERAL RESIN  •  PURIFIED SHILAJIT EXTRACT",
        "effect": "zoom_out",
        "sentences": [
            "The third ingredient is purified Shilajit extract.",
            "Sourced from mineral-rich mountainous regions, Shilajit contains natural fulvic acid along with a wide spectrum of trace minerals.",
            "In nutritional science, fulvic acid is appreciated for supporting cellular nutrient absorption and overall vitality."
        ]
    },
    {
        "id": "07",
        "title": "NOOTROPIC MUSHROOM  •  LION'S MANE EXTRACT",
        "effect": "zoom_in_macro",
        "sentences": [
            "Fourth is Lion's Mane mushroom, or Hericium Erinaceus.",
            "This distinctive mushroom has gained widespread attention in modern nootropic research for its natural bioactive compounds.",
            "It is widely used to support cognitive wellness, clarity, and normal neural health."
        ]
    },
    {
        "id": "08",
        "title": "TRADITIONAL BOTANICAL  •  BACOPA MONNIERI",
        "effect": "pan_right_left",
        "sentences": [
            "Rounding out the five key botanicals is Bacopa Monnieri.",
            "Bacopa is an ancient herb with a long history of traditional use for supporting memory recall and mental processing speed.",
            "Contemporary studies continue to evaluate how its natural bacoside compounds support cognitive performance over time."
        ]
    },
    {
        "id": "09",
        "title": "QUALITY & SOURCING  •  FORMULA TRANSPARENCY",
        "effect": "zoom_in",
        "sentences": [
            "When evaluating any dietary supplement, ingredient quality and manufacturing transparency are essential considerations.",
            "Check the product label and manufacturer's documentation for ingredient and quality information."
        ]
    },
    {
        "id": "10",
        "title": "USAGE GUIDELINES  •  MANUFACTURER PROTOCOL",
        "effect": "pan_left_right",
        "sentences": [
            "In terms of daily routine, the manufacturer suggests taking two capsules daily with water alongside a meal.",
            "As with any dietary supplement, individual experiences can vary based on personal metabolism and consistency.",
            "Nutritional botanicals are generally intended for steady daily use alongside balanced nutrition and healthy lifestyle habits."
        ]
    },
    {
        "id": "11",
        "title": "PURCHASING ADVISORY  •  OFFICIAL SUPPLIER & TERMS",
        "effect": "zoom_in",
        "sentences": [
            "For consumer safety, it is always recommended to purchase dietary supplements directly through the brand's verified website.",
            "Check current pricing, seller information, and return terms before purchasing.",
            "The official portal also details available multi-bottle packages and customer support options."
        ]
    },
    {
        "id": "12",
        "title": "FINAL SUMMARY  •  DAILY HEALTH REVIEW",
        "effect": "zoom_out",
        "sentences": [
            "In summary, NeuroVera combines five well-known traditional botanicals into a convenient daily formula for cognitive support.",
            "If you want to review full ingredient details, customer feedback, and current pricing, check the official verified link in the description and pinned comment below.",
            "As a reminder, our link is an affiliate link, which supports our channel at no extra cost to you.",
            "Thank you for watching Daily Health Review, and remember to subscribe for more balanced health and supplement evaluations."
        ]
    }
]

def find_image_file_strict(folder, scene_id):
    prefix = f"{scene_id}_"
    for f in sorted(os.listdir(folder)):
        if f.startswith(prefix) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
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
    img_folder = r"C:\Users\Eusimar\Downloads\VIDEO-NEUROVERA"
    temp_dir = r"C:\Users\Eusimar\Downloads\_temp_neurovera_custom_render"
    downloads_dir = r"C:\Users\Eusimar\Downloads"
    os.makedirs(temp_dir, exist_ok=True)

    print("\n=======================================================")
    print("GERADOR DE VÍDEO REVIEW - NEUROVERA (SOLID 145px TOP BAR & MOBILE-OPTIMIZED)")
    print(f"PASTA DAS IMAGENS: {img_folder}")
    print("DAILY HEALTH REVIEW - QUALIDADE BROADCAST 1080p")
    print("=======================================================\n")

    clip_paths = []
    total_running_time = 0.0
    all_ass_events = []

    # ASS Subtitle Master Header:
    # TopBarTitle: Alignment=8 (Top Center), Fontsize=34 (Crisp & Large for Mobile), MarginV=52
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
Style: TopBarTitle,Arial,34,&H0038BDF8,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,8,40,40,52,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    for idx, scene in enumerate(SCENES):
        scene_id = scene["id"]
        print(f"\n[Cena {scene_id}/12] Renderizando áudio e animação de câmera com barra sólida 145px...")

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

        # Add Single Centered Top Bar Title (Large & Mobile-Ready)
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

        # 3. Ultra-Smooth Ken Burns Camera Motions + 100% Solid 145px Top Header Bar
        # The drawbox filter covers the top 145px with 100% solid opacity (color=0x070B19@1.0)
        # to completely mask all background text, with a 3px sky-blue border at y=142
        top_bar_filter = "drawbox=x=0:y=0:w=1920:h=145:color=0x070B19@1.0:t=fill,drawbox=x=0:y=142:w=1920:h=3:color=0x38BDF8@1.0:t=fill"

        if scene["effect"] == "zoom_in":
            base_vf = f"scale=8000:-1,zoompan=z='min(zoom+0.0005,1.20)':d={frames_count}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
        elif scene["effect"] == "zoom_in_macro":
            base_vf = f"scale=8000:-1,zoompan=z='min(zoom+0.0007,1.25)':d={frames_count}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
        elif scene["effect"] == "zoom_out":
            base_vf = f"scale=8000:-1,zoompan=z='if(lte(zoom,1.0),1.20,max(1.001,zoom-0.0005))':d={frames_count}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
        elif scene["effect"] == "pan_left_right":
            base_vf = f"scale=8000:-1,zoompan=z='1.12':d={frames_count}:x='if(lte(on,-1),(iw-iw/zoom)/2,x+0.6)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
        elif scene["effect"] == "pan_right_left":
            base_vf = f"scale=8000:-1,zoompan=z='1.12':d={frames_count}:x='if(lte(on,-1),(iw-iw/zoom),x-0.6)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
        else:
            base_vf = f"scale=8000:-1,zoompan=z='min(zoom+0.0004,1.15)':d={frames_count}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"

        full_vf = f"{base_vf},{top_bar_filter}"

        cmd_video = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", img_path,
            "-i", audio_path,
            "-vf", full_vf,
            "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{clip_dur:.3f}",
            "-preset", "faster",
            clip_path
        ]
        subprocess.run(cmd_video, check=True)
        clip_paths.append(clip_path)
        total_running_time += clip_dur

    # Save Master ASS Subtitles
    with open(ass_master_path, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(all_ass_events))

    print(f"\n[+] Total de duração do vídeo: {total_running_time:.2f}s (~{total_running_time/60:.1f} minutos)")
    print("[+] Concatenando todos os 12 clipes...")

    # Concatenate clips
    list_path = os.path.join(temp_dir, "concat_list.txt")
    with open(list_path, "w", encoding="utf-8") as f:
        for p in clip_paths:
            f.write(f"file '{p}'\n")

    raw_concat_video = os.path.join(temp_dir, "raw_concatenated.mp4")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_path,
        "-c", "copy",
        raw_concat_video
    ]
    subprocess.run(cmd_concat, check=True)

    # Burn Subtitles
    print("[+] Queimando legendas master com acabamento final...")
    final_output = os.path.join(downloads_dir, "NeuroVera_Review_Completo_4Min_DailyHealthReview.mp4")
    clean_ass_path = ass_master_path.replace("\\", "/").replace(":", "\\:")

    cmd_burn = [
        "ffmpeg", "-y",
        "-i", raw_concat_video,
        "-vf", f"subtitles='{clean_ass_path}'",
        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-c:a", "copy",
        final_output
    ]
    subprocess.run(cmd_burn, check=True)

    print("\n=======================================================")
    print("SUCESSO TOTAL! VÍDEO FINALIZADO COM PADRÃO BROADCAST!")
    print(f"Arquivo Final: {final_output}")
    print(f"Duração Total: {total_running_time:.2f} segundos (~{total_running_time/60:.1f} minutos)")
    print("=======================================================\n")

if __name__ == "__main__":
    create_full_video()
