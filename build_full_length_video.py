import os
import sys
import re
import subprocess

VOICE = "en-US-ChristopherNeural"

# 12 Scenes refined according to strict editorial guidelines:
# 1. Clear separation of manufacturer claims vs. preliminary science
# 2. Removal of unverified marketplace accusations (focus on authentic lab portal)
# 3. Explicit disclosure that medical/lab visuals are for illustrative educational purposes
# 4. Large broadcast-style subtitles with dark pill background for mobile readability
# 5. Prominent closing affiliate disclosure
SCENES = [
    {
        "id": "01",
        "file_keyword": "Cena_1A",
        "tag": "EDUCATIONAL REPORT  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in",
        "sentences": [
            "If you are over forty-five and experiencing eye fatigue, morning blurriness, or difficulty focusing on fine print, you are certainly not alone.",
            "For millions of adults, age-related visual strain has prompted an active search for reliable nutritional and lifestyle support.",
            "Understanding what dietary options can and cannot do is essential for making informed health decisions."
        ]
    },
    {
        "id": "02",
        "file_keyword": "Cena_1B",
        "tag": "PRODUCT EVALUATION  |  DAILY HEALTH REVIEW",
        "effect": "pan_left_right",
        "sentences": [
            "Among current nutritional options, VisiFlora has received growing interest across the wellness community.",
            "Promoted as an integrative formula, the manufacturer claims it supports visual clarity by addressing the Gut-Eye Connection.",
            "In this independent review, we analyze the ingredients, the available evidence, and the essential precautions you should know before buying."
        ]
    },
    {
        "id": "03",
        "file_keyword": "Cena_2A",
        "tag": "OCULAR PHYSIOLOGY  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in_macro",
        "sentences": [
            "To evaluate these claims, it helps to look at basic ocular physiology.",
            "Visual sharpness relies heavily on micro-capillary circulation and antioxidant defense within the retina and macula.",
            "As tissues face ongoing oxidative exposure, contrast sensitivity and visual comfort can gradually decline over time."
        ]
    },
    {
        "id": "04",
        "file_keyword": "Cena_2B",
        "tag": "ILLUSTRATIVE LAB CONCEPT  |  DAILY HEALTH REVIEW",
        "effect": "zoom_out",
        "sentences": [
            "Laboratory studies suggest that chronic low-grade inflammation in the digestive tract may interact with the blood-retinal barrier.",
            "While the Gut-Eye connection is an emerging field of research, evidence on multi-ingredient dietary formulas remains preliminary.",
            "Please note that laboratory and clinical visuals in this report are for illustrative educational purposes."
        ]
    },
    {
        "id": "05",
        "file_keyword": "Cena_3A",
        "tag": "INGREDIENT ANALYSIS: SAFFRON  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in",
        "sentences": [
            "Let us examine the individual botanical components.",
            "First is Standardized Saffron Extract.",
            "Isolated crocin compounds from saffron have been documented in peer-reviewed clinical trials for supporting macular pigment optical density and dark adaptation."
        ]
    },
    {
        "id": "06",
        "file_keyword": "Cena_3B",
        "tag": "INGREDIENT ANALYSIS: GINKGO  |  DAILY HEALTH REVIEW",
        "effect": "pan_right_left",
        "sentences": [
            "The second key ingredient is Ginkgo Biloba extract.",
            "Extensively studied in vascular research, Ginkgo is recognized for promoting healthy blood flow through the microscopic capillaries that nourish the optic nerve."
        ]
    },
    {
        "id": "07",
        "file_keyword": "Cena_3C",
        "tag": "INGREDIENT ANALYSIS: BIOFLAVONOIDS  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in",
        "sentences": [
            "Third, the formula incorporates concentrated Citrus Bioflavonoids.",
            "These plant antioxidants help defend ocular tissues against routine oxidative strain caused by bright sunlight, night driving glare, and extended digital screen use."
        ]
    },
    {
        "id": "08",
        "file_keyword": "Cena_3D",
        "tag": "INGREDIENT ANALYSIS: PROBIOTICS  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in_macro",
        "sentences": [
            "Fourth is a blend of beneficial probiotic cultures.",
            "These strains are included based on the scientific hypothesis that reinforcing gut barrier integrity helps soothe systemic inflammatory markers before they reach the bloodstream."
        ]
    },
    {
        "id": "09",
        "file_keyword": "Cena_4A",
        "tag": "CLINICAL PRECAUTIONS (ILLUSTRATIVE)  |  DAILY HEALTH REVIEW",
        "effect": "pan_left_right",
        "sentences": [
            "Now for essential practical limitations.",
            "VisiFlora is a dietary supplement, not a medical drug, and it does not replace professional care, prescription glasses, or surgical intervention for eye diseases.",
            "Botanical formulas require consistent use over several weeks, and individual results will naturally vary.",
            "Always consult with an eye care specialist before starting any new supplement regimen."
        ]
    },
    {
        "id": "10",
        "file_keyword": "Cena_4B",
        "tag": "CONSUMER GUIDANCE  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in",
        "sentences": [
            "When purchasing dietary supplements, consumer safety is paramount.",
            "To ensure you receive authentic, lab-tested bottles and retain full eligibility for customer support, purchasing directly through the verified manufacturer portal is strongly advised.",
            "This guarantees access to fresh batches and protects your purchase under the official sixty-day policy."
        ]
    },
    {
        "id": "11",
        "file_keyword": "Cena_5A",
        "tag": "INTEGRATIVE WELLNESS  |  DAILY HEALTH REVIEW",
        "effect": "zoom_out",
        "sentences": [
            "In summary, VisiFlora offers a thoughtful combination of researched botanicals and microbiome support for daily ocular nutrition.",
            "It functions best as a complementary wellness addition alongside regular hydration, balanced nutrition, and routine eye examinations."
        ]
    },
    {
        "id": "12",
        "file_keyword": "Cena_5B",
        "tag": "OFFICIAL VERIFICATION & DISCLOSURE  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in",
        "sentences": [
            "Every genuine order comes backed by an unconditional sixty-day money-back guarantee, allowing you to test the formula risk-free.",
            "See product details through the link below.",
            "Affiliate link — we may earn a commission."
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
    print("GERADOR DE VÍDEO REVIEW INVESTIGATIVO (3.5 A 4 MINUTOS)")
    print("REQUISITOS EDITORIAIS E VISUAIS APLICADOS:")
    print("1. Legendas grandes com fundo escuro (pill box) de alta legibilidade")
    print("2. Separação rigorosa entre ciência preliminar e alegações do fabricante")
    print("3. Remoção de acusações de marketplaces e foco no portal oficial")
    print("4. Aviso explícito de ilustrações educativas nas cenas médicas")
    print("5. Chamada de ação final com aviso explícito de afiliado")
    print("=======================================================\n")

    clip_paths = []
    total_running_time = 0.0
    all_ass_events = []

    # ASS Subtitle Master Header:
    # BorderStyle=3 (Opaque box), Fontsize=46, Black Background Box (&HB0000000)
    ass_master_path = os.path.join(temp_dir, "master_subtitles.ass")
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,46,&H00FFFFFF,&H000000FF,&H00000000,&HB50A0F1D,-1,0,0,0,100,100,0,0,3,7,0,2,90,90,75,1
Style: TagStyle,Arial,25,&H00FAFAFA,&H000000FF,&H00000000,&HC50F172A,-1,0,0,0,100,100,0,0,3,6,0,7,50,50,40,1
Style: AffiliateMain,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&HB5991B1B,-1,0,0,0,100,100,0,0,3,8,0,2,80,80,120,1
Style: AffiliateSub,Arial,40,&H0014D7FF,&H000000FF,&H00000000,&HC50F172A,-1,0,0,0,100,100,0,0,3,7,0,2,80,80,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    for idx, scene in enumerate(SCENES):
        scene_id = scene["id"]
        print(f"\n[Cena {scene_id}/12] Gerando áudio e animação de câmera...")

        img_path = find_image_file(img_folder, scene["file_keyword"])
        txt_path = os.path.join(temp_dir, f"text_{scene_id}.txt")
        audio_path = os.path.join(temp_dir, f"audio_{scene_id}.mp3")
        srt_path = os.path.join(temp_dir, f"sub_{scene_id}.srt")
        clip_path = os.path.join(temp_dir, f"clip_{scene_id}.mp4")

        # Write sentences (one per line)
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

        # Add Scene Top Tag
        tag_start = format_ass_time(total_running_time)
        tag_end = format_ass_time(total_running_time + clip_dur)
        all_ass_events.append(f"Dialogue: 0,{tag_start},{tag_end},TagStyle,,0,0,0,,  {scene['tag']}  ")

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
                    
                    # Wrap lines if longer than 50 chars for mobile readability
                    if len(sub_text) > 48:
                        words = sub_text.split(" ")
                        mid = len(words) // 2
                        sub_text = " ".join(words[:mid]) + "\\N" + " ".join(words[mid:])

                    ass_start = format_ass_time(t_start)
                    ass_end = format_ass_time(t_end)

                    # Highlight closing affiliate sentences in Scene 12
                    if scene_id == "12" and "Affiliate link" in sub_text:
                        all_ass_events.append(f"Dialogue: 0,{ass_start},{ass_end},AffiliateSub,,0,0,0,,{sub_text}")
                    elif scene_id == "12" and "See product details" in sub_text:
                        all_ass_events.append(f"Dialogue: 0,{ass_start},{ass_end},AffiliateMain,,0,0,0,,{sub_text}")
                    else:
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
    print(f"Legendas mapeadas: {len(all_ass_events)} eventos sincronizados")
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

    # Burn Master ASS Subtitles
    final_output = os.path.join(downloads_dir, "VisiFlora_Review_Completo_4Min_DailyHealthReview.mp4")
    ass_escaped = ass_master_path.replace("\\", "/").replace(":", "\\:")
    
    print("[FINAL] Masterizando vídeo com legendas em alta definição e tarjas de leitura...")
    cmd_final = (
        f'ffmpeg -y -i "{concat_no_sub}" -vf "ass=\'{ass_escaped}\'" '
        f'-c:v libx264 -pix_fmt yuv420p -preset medium -crf 18 -c:a copy "{final_output}"'
    )
    subprocess.run(cmd_final, shell=True, check=True)

    if os.path.exists(final_output) and os.path.getsize(final_output) > 1000:
        print("\n=======================================================")
        print("[SUCESSO TOTAL] NOVO VÍDEO EDITORIAL RENDERIZADO COM SUCESSO!")
        print(f"[ARQUIVO] Salvo em: {final_output}")
        print(f"[DURAÇÃO] {total_running_time:.1f} segundos ({total_running_time/60:.2f} minutos)")
        print("=======================================================\n")

if __name__ == "__main__":
    create_full_video()
