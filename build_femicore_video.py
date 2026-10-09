import os
import sys
import re
import subprocess

VOICE = "en-US-ChristopherNeural"

# 10 Scenes aligned with 100% strict compliance & mobile-ready typography
SCENES = [
    {
        "id": "01",
        "title": "FEMICORE REVIEW  •  WOMEN'S BLADDER HEALTH & MICROBIOME",
        "effect": "zoom_in",
        "sentences": [
            "If you find yourself waking up multiple times every night to rush to the bathroom, or feeling that sudden, unpredictable urge whenever you cough, laugh, or go for a walk, you are definitely not alone.",
            "For millions of women, bladder sensitivity and accidental leaks can quietly take over daily freedom and peace of mind.",
            "Today on Daily Health Review, we examine FemiCore, an advanced natural formula designed to support bladder control and rebalance the urinary microbiome."
        ]
    },
    {
        "id": "02",
        "title": "UROLOGICAL SCIENCE  •  THE URINARY MICROBIOME FACTOR",
        "effect": "zoom_in_macro",
        "sentences": [
            "For years, women were told that frustrating bladder issues were just an unavoidable part of getting older or a sign of weak pelvic muscles.",
            "While pelvic tone is important, recent urological research points to a critical biological factor: an imbalance in the delicate urinary microbiome.",
            "Just like your digestive system, your bladder and urinary tract depend on a protective barrier of beneficial microflora."
        ]
    },
    {
        "id": "03",
        "title": "ROOT CAUSE  •  MUCOSAL IRRITATION & INVOLUNTARY SPASMS",
        "effect": "pan_left_right",
        "sentences": [
            "When this natural microflora balance is disrupted by hormonal shifts, stress, or dietary irritants, the bladder mucosa becomes hypersensitive.",
            "This chronic micro-irritation sends false fullness signals to your brain, triggering involuntary muscle contractions and sudden, unexpected leaks even when the bladder is not full.",
            "Restoring this protective barrier is essential for long-term bladder comfort."
        ]
    },
    {
        "id": "04",
        "title": "PRODUCT OVERVIEW  •  FEMICORE BOTANICAL FORMULA",
        "effect": "zoom_in",
        "sentences": [
            "This is where FemiCore comes in.",
            "Developed as a comprehensive daily dietary supplement, FemiCore is engineered to help soothe the bladder lining, replenish healthy urogenital flora, and support smooth muscle elasticity throughout your pelvic floor.",
            "Notably, it is crafted without harsh synthetic stimulants, fillers, or jitter-inducing chemicals."
        ]
    },
    {
        "id": "05",
        "title": "FORMULA SCIENCE  •  THE FEMICORE BOTANICAL MATRIX",
        "effect": "pan_right_left",
        "sentences": [
            "Inside every capsule of FemiCore is an optimally dosed proprietary blend of standardized botanical extracts and urogenital nutrients.",
            "These bioactives work synergistically to neutralize cellular oxidative stress in the urinary tract, reinforce the protective mucosal barrier, and nourish neuromuscular sphincter coordination for reliable holding tone."
        ]
    },
    {
        "id": "06",
        "title": "USAGE GUIDELINES  •  SIMPLE DAILY MORNING PROTOCOL",
        "effect": "zoom_in",
        "sentences": [
            "Using FemiCore is simple and fits seamlessly into any morning routine.",
            "The manufacturer recommends taking one easy-to-swallow capsule each morning with a full glass of water.",
            "Because it is non-GMO and completely stimulant-free, its gentle botanical bioactives work throughout the day without jitters or sleep interference."
        ]
    },
    {
        "id": "07",
        "title": "RESULTS TIMELINE  •  PROGRESSION OVER 30 TO 90 DAYS",
        "effect": "zoom_out",
        "sentences": [
            "With consistent daily use, most women report noticeably calmer nights and fewer false alarms within the first two weeks.",
            "Over three to six weeks, users experience improved holding capacity and renewed confidence during workouts, walks, and social outings.",
            "Consistent use over sixty to ninety days helps establish lasting urinary microbiome balance and everyday freedom."
        ]
    },
    {
        "id": "08",
        "title": "OFFICIAL BONUSES  •  INCLUDED WITH 6-BOTTLE BUNDLE",
        "effect": "pan_left_right",
        "sentences": [
            "When ordering the recommended six-bottle package directly from the manufacturer portal, you also receive free nationwide shipping plus three digital bonus guides.",
            "These include Seven Days to Rekindle Passion in Your Marriage, Reset Your Gut for optimal digestion, and Unlock Painless Hips and Legs for lower body mobility."
        ]
    },
    {
        "id": "09",
        "title": "RISK-FREE POLICY  •  100% 60-DAY MONEY-BACK GUARANTEE",
        "effect": "zoom_in",
        "sentences": [
            "To provide complete peace of mind, every order of FemiCore is protected by an unconditional sixty-day one-hundred-percent money-back guarantee.",
            "You can test the formula for two full months, and if you are not completely satisfied with your results, simply contact customer support for a prompt refund."
        ]
    },
    {
        "id": "10",
        "title": "PURCHASING ADVISORY  •  OFFICIAL LABORATORY PORTAL",
        "effect": "zoom_out",
        "sentences": [
            "To ensure you receive the genuine, lab-tested formula and avoid unauthorized third-party counterfeits, always order through the official manufacturer portal.",
            "You can find the direct verified link and our complete editorial investigation in the description and pinned comment below.",
            "Thank you for watching Daily Health Review, and remember to subscribe for more balanced, evidence-based health reports."
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
    img_folder = r"C:\Users\Eusimar\Downloads\VIDEO-FEMICORE"
    temp_dir = r"C:\Users\Eusimar\Downloads\_temp_femicore_render"
    downloads_dir = r"C:\Users\Eusimar\Downloads"
    os.makedirs(temp_dir, exist_ok=True)

    print("\n=======================================================")
    print("GERADOR DE VÍDEO REVIEW - FEMICORE (SOLID 145px TOP BAR & MOBILE-OPTIMIZED)")
    print(f"PASTA DAS IMAGENS: {img_folder}")
    print("DAILY HEALTH REVIEW - QUALIDADE BROADCAST 1080p")
    print("=======================================================\n")

    clip_paths = []
    total_running_time = 0.0
    all_ass_events = []

    # ASS Subtitle Master Header:
    # TopBarTitle: Alignment=8 (Top Center), Fontsize=34, MarginV=52, Rose Pink Accent (&H008571FB)
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
Style: TopBarTitle,Arial,34,&H008571FB,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,8,40,40,52,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    for idx, scene in enumerate(SCENES):
        scene_id = scene["id"]
        print(f"\n[Cena {scene_id}/10] Renderizando áudio e animação de câmera com barra sólida 145px...")

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

        total_running_time += clip_dur

        # 3. Dynamic Motion Effects
        effect = scene.get("effect", "zoom_in")
        if effect == "zoom_in":
            vf_motion = f"scale=8000x4500,zoompan=z='min(zoom+0.0007,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames_count}:s=1920x1080:fps=30"
        elif effect == "zoom_in_macro":
            vf_motion = f"scale=8000x4500,zoompan=z='min(zoom+0.0010,1.22)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames_count}:s=1920x1080:fps=30"
        elif effect == "zoom_out":
            vf_motion = f"scale=8000x4500,zoompan=z='if(lte(zoom,1.0),1.15,max(1.001,zoom-0.0007))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames_count}:s=1920x1080:fps=30"
        elif effect == "pan_left_right":
            vf_motion = f"scale=8000x4500,zoompan=z=1.12:x='if(lte(on,1),(iw-iw/zoom)*0.15,(x+((iw-iw/zoom)*0.70)/{frames_count}))':y='ih/2-(ih/zoom/2)':d={frames_count}:s=1920x1080:fps=30"
        elif effect == "pan_right_left":
            vf_motion = f"scale=8000x4500,zoompan=z=1.12:x='if(lte(on,1),(iw-iw/zoom)*0.85,(x-((iw-iw/zoom)*0.70)/{frames_count}))':y='ih/2-(ih/zoom/2)':d={frames_count}:s=1920x1080:fps=30"
        else:
            vf_motion = f"scale=8000x4500,zoompan=z='min(zoom+0.0006,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames_count}:s=1920x1080:fps=30"

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
