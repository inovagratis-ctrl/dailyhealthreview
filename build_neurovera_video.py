import os
import sys
import re
import subprocess
from pathlib import Path

VOICE = "en-US-ChristopherNeural"

# 12 Scenes aligned with strict investigative standards
SCENES = [
    {
        "id": "01",
        "file_keyword": "CENA_01",
        "tag": "EDUCATIONAL HEALTH REVIEW  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in",
        "sentences": [
            "Have you ever walked into a room only to completely forget why you went there?",
            "Or found yourself struggling to recall familiar names, feeling that stubborn, frustrating mental fog clouding your daily focus?",
            "As we pass forty and fifty, subtle memory lapses become more frequent—leading many to wonder if cognitive decline is an inevitable part of aging.",
            "Today on Daily Health Review, we take an objective look at NeuroVera—a botanical formula designed to target the cellular root causes of brain fog."
        ]
    },
    {
        "id": "02",
        "file_keyword": "CENA_02",
        "tag": "ILLUSTRATIVE MEDICAL CONCEPT  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in_macro",
        "sentences": [
            "Modern neurobiology reveals that cognitive sluggishness often stems from micro-vascular circulation slowdowns and oxidative stress on delicate brain tissue.",
            "Furthermore, the gradual depletion of acetylcholine—the vital neurotransmitter responsible for swift memory retrieval—slows communication between neural pathways.",
            "When brain synapses lack essential micronutrients, mental fatigue and slow recall naturally follow."
        ]
    },
    {
        "id": "03",
        "file_keyword": "CENA_03",
        "tag": "PRODUCT INVESTIGATION  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in",
        "sentences": [
            "This brings us to NeuroVera by Nutraville.",
            "Promoted under the philosophy 'Clarity Starts Within', NeuroVera is a standardized dietary supplement created to support memory retention and sharp mental stamina.",
            "Crucially, it is formulated without synthetic stimulants or aggressive caffeine spikes.",
            "Let us analyze its five primary active botanical ingredients."
        ]
    },
    {
        "id": "04",
        "file_keyword": "CENA_04",
        "tag": "BOTANICAL PHYTOCHEMISTRY  |  DAILY HEALTH REVIEW",
        "effect": "pan_left_right",
        "sentences": [
            "First is Schisandra Fruit Extract.",
            "Traditionally revered in herbal medicine as a master adaptogen, modern clinical research shows Schisandra contains potent lignans like schisandrin B.",
            "These bioactive compounds help shield neurons against oxidative stress and support sustained mental alertness during high-pressure cognitive tasks."
        ]
    },
    {
        "id": "05",
        "file_keyword": "CENA_05",
        "tag": "CLINICAL BOTANY  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in",
        "sentences": [
            "Next in the matrix is Gotu Kola powder, known scientifically as Centella Asiatica.",
            "Rich in triterpenoid saponins, Gotu Kola supports healthy microcirculation across delicate cerebral capillaries.",
            "By optimizing oxygen and nutrient delivery to brain cells, research indicates it aids in neural plasticity and calm mental clarity."
        ]
    },
    {
        "id": "06",
        "file_keyword": "CENA_06",
        "tag": "CELLULAR NUTRITION  |  DAILY HEALTH REVIEW",
        "effect": "zoom_out",
        "sentences": [
            "The third key element is purified Shilajit extract.",
            "Sourced from high-altitude Himalayan rock layers, Shilajit is rich in natural fulvic acid and over eighty-four trace ionic minerals.",
            "In cognitive science, fulvic acid enhances cellular mitochondrial ATP production so brain cells have the metabolic fuel required for quick thinking."
        ]
    },
    {
        "id": "07",
        "file_keyword": "CENA_07",
        "tag": "NEUROBIOLOGICAL RESEARCH  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in_macro",
        "sentences": [
            "Fourth is Lion's Mane mushroom, or Hericium Erinaceus.",
            "This unique nootropic fungus is world-famous for containing hericenones and erinacines—compounds that cross the blood-brain barrier to stimulate Nerve Growth Factor, or NGF.",
            "NGF is the essential biological protein responsible for the growth, maintenance, and structural repair of neurons."
        ]
    },
    {
        "id": "08",
        "file_keyword": "CENA_08",
        "tag": "BOTANICAL NOOTROPICS  |  DAILY HEALTH REVIEW",
        "effect": "pan_right_left",
        "sentences": [
            "Rounding out the synergistic core is Bacopa Monnieri.",
            "Extensively documented in peer-reviewed clinical trials, Bacopa's active bacosides facilitate the repair of damaged synaptic connections.",
            "Studies demonstrate significant improvements in visual information processing, rapid memory consolidation, and mental processing speed."
        ]
    },
    {
        "id": "09",
        "file_keyword": "CENA_09",
        "tag": "QUALITY ASSURANCE  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in",
        "sentences": [
            "Quality and consumer safety are non-negotiable.",
            "NeuroVera is manufactured in the United States in state-of-the-art facilities that strictly adhere to cGMP standards.",
            "The formula is non-GMO, vegan-friendly, gluten-free, and contains zero synthetic preservatives or jitter-inducing stimulants."
        ]
    },
    {
        "id": "10",
        "file_keyword": "CENA_10",
        "tag": "NUTRITIONAL PROTOCOL  |  DAILY HEALTH REVIEW",
        "effect": "pan_left_right",
        "sentences": [
            "Using NeuroVera is simple: the manufacturer recommends taking two easy-to-swallow capsules daily with a glass of water alongside your morning meal.",
            "While some individuals report noticeable alertness within two to three weeks, botanical compounds work cumulatively.",
            "Optimal cellular benefits in memory and mental endurance are typically observed with sixty to ninety days of consistent daily use."
        ]
    },
    {
        "id": "11",
        "file_keyword": "CENA_11",
        "tag": "CONSUMER PROTECTION NOTICE  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in",
        "sentences": [
            "An important consumer advisory: to guarantee authentic formulation and activate the full sixty-day money-back guarantee, always order directly from the official laboratory portal.",
            "The producer offers discounted multi-bottle bundles starting as low as twenty-nine dollars per bottle with free shipping, allowing you to test the formula risk-free."
        ]
    },
    {
        "id": "12",
        "file_keyword": "CENA_12",
        "tag": "TRANSPARENT EDITORIAL DISCLOSURE  |  DAILY HEALTH REVIEW",
        "effect": "zoom_out",
        "sentences": [
            "In conclusion, NeuroVera provides a well-balanced, research-supported botanical blend for anyone seeking to reclaim mental clarity and protect long-term cognitive vitality.",
            "You can find the direct link to the official discounted portal in the description and pinned comment below.",
            "This is an affiliate link—meaning we may earn a small commission at no additional cost to you, supporting our independent reviews.",
            "Thank you for watching Daily Health Review, and subscribe for more evidence-based health insights."
        ]
    }
]

def format_ass_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def generate_tts_and_vtt(text, audio_path, vtt_path):
    cmd = [
        "edge-tts",
        f"--voice={VOICE}",
        f"--text={text}",
        f"--write-media={audio_path}",
        f"--write-subtitles={vtt_path}"
    ]
    subprocess.run(cmd, check=True, capture_output=True)

def parse_vtt(vtt_path):
    with open(vtt_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    entries = []
    pattern = r"(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})\s*\n(.*?)(?=\n\n|\n\d{2}:|\Z)"
    matches = re.findall(pattern, content, re.DOTALL)
    
    for start_str, end_str, text in matches:
        def to_sec(ts):
            parts = ts.split(":")
            h = float(parts[0])
            m = float(parts[1])
            s = float(parts[2])
            return h * 3600 + m * 60 + s
        
        cleaned_text = " ".join(text.strip().split())
        cleaned_text = re.sub(r"<[^>]+>", "", cleaned_text)
        if cleaned_text:
            entries.append((to_sec(start_str), to_sec(end_str), cleaned_text))
    return entries

def get_audio_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def create_ass_subtitles(entries, tag_text, total_duration, ass_path):
    ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Subtitle,Arial,46,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,3,10,0,2,100,100,65,1
Style: Tag,Arial,28,&H0000F0FF,&H000000FF,&H00000000,&HA0000000,-1,0,0,0,100,100,1,0,3,6,0,8,40,40,35,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 1,0:00:00.00,{format_ass_timestamp(total_duration)},Tag,,0,0,0,,[ {tag_text} ]
"""
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_header)
        for start, end, text in entries:
            f.write(f"Dialogue: 0,{format_ass_timestamp(start)},{format_ass_timestamp(end)},Subtitle,,0,0,0,,{text}\n")

def render_scene(image_path, audio_path, ass_path, effect, duration, output_path):
    fps = 30
    total_frames = int(duration * fps) + 5
    
    # Smooth Ken Burns Filter Expressions
    if effect == "zoom_in":
        vf_expr = f"scale=8000:-1,zoompan=z='min(zoom+0.0006,1.25)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps={fps}"
    elif effect == "zoom_in_macro":
        vf_expr = f"scale=8000:-1,zoompan=z='min(zoom+0.0009,1.35)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps={fps}"
    elif effect == "zoom_out":
        vf_expr = f"scale=8000:-1,zoompan=z='if(lte(zoom,1.0),1.25,max(1.001,zoom-0.0006))':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps={fps}"
    elif effect == "pan_left_right":
        vf_expr = f"scale=8000:-1,zoompan=z='1.15':d={total_frames}:x='if(lte(on,-1),(iw-iw/zoom)/2,x+0.8)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps={fps}"
    elif effect == "pan_right_left":
        vf_expr = f"scale=8000:-1,zoompan=z='1.15':d={total_frames}:x='if(lte(on,-1),(iw-iw/zoom),x-0.8)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps={fps}"
    else:
        vf_expr = f"scale=8000:-1,zoompan=z='min(zoom+0.0005,1.2)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps={fps}"

    # Format path for ASS filter (handling Windows backslashes)
    ass_filter_path = str(Path(ass_path).resolve()).replace("\\", "/").replace(":", "\\:")
    full_vf = f"{vf_expr},subtitles='{ass_filter_path}'"

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(image_path),
        "-i", str(audio_path),
        "-vf", full_vf,
        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{duration:.3f}",
        "-preset", "faster",
        str(output_path)
    ]
    subprocess.run(cmd, check=True)

def main():
    base_dir = Path("C:/Users/Eusimar/Downloads/VIDEO_NEUROVERA")
    base_dir.mkdir(parents=True, exist_ok=True)
    
    print("=== DAILY HEALTH REVIEW: NEUROVERA VIDEO COMPILER ===")
    print(f"Working Directory: {base_dir}")
    
    rendered_scenes = []
    
    for scene in SCENES:
        sid = scene["id"]
        print(f"\n--- Processing Scene {sid} ({scene['tag']}) ---")
        
        # Audio & Subtitle generation
        combined_text = " ".join(scene["sentences"])
        audio_file = base_dir / f"scene_{sid}_audio.mp3"
        vtt_file = base_dir / f"scene_{sid}.vtt"
        ass_file = base_dir / f"scene_{sid}.ass"
        scene_mp4 = base_dir / f"scene_{sid}.mp4"
        
        print(f"Generating TTS audio with voice {VOICE}...")
        generate_tts_and_vtt(combined_text, str(audio_file), str(vtt_file))
        
        duration = get_audio_duration(str(audio_file)) + 0.5  # padding
        print(f"Scene duration: {duration:.2f}s")
        
        # Subtitles
        entries = parse_vtt(str(vtt_file))
        create_ass_subtitles(entries, scene["tag"], duration, str(ass_file))
        
        # Find Scene Image
        img_candidates = list(base_dir.glob(f"*{scene['file_keyword']}*")) + list(base_dir.glob(f"*{sid}*"))
        img_candidates = [f for f in img_candidates if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]]
        
        if not img_candidates:
            # Fallback to general bottle if not generated yet
            fallback = base_dir / "neurovera_bottle.png"
            if not fallback.exists():
                fallback = Path("C:/Users/Eusimar/.gemini/antigravity/scratch/Projeto_ClickBank_DailyHealthReview/Imagens_Oficiais/neurovera_bottle.png")
            img_path = fallback
            print(f"Notice: Specific scene image not found. Using fallback: {img_path.name}")
        else:
            img_path = img_candidates[0]
            print(f"Using image: {img_path.name}")
            
        print(f"Rendering scene video with Ken Burns [{scene['effect']}]...")
        render_scene(img_path, audio_file, ass_file, scene["effect"], duration, scene_mp4)
        rendered_scenes.append(scene_mp4)
        print(f"Scene {sid} rendered successfully.")

    # Concat all scenes
    print("\n--- Concatenating Scenes into Master Review ---")
    concat_list = base_dir / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for sc in rendered_scenes:
            clean_path = str(sc.resolve()).replace("\\", "/")
            f.write(f"file '{clean_path}'\n")
            
    master_video = Path("C:/Users/Eusimar/Downloads/NeuroVera_Review_Completo_4Min_DailyHealthReview.mp4")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(master_video)
    ]
    subprocess.run(cmd_concat, check=True)
    
    total_dur = get_audio_duration(str(master_video))
    print(f"\n=======================================================")
    print(f"SUCCESS! Master Video Rendered:")
    print(f"File: {master_video}")
    print(f"Total Duration: {total_dur:.1f} seconds (~{total_dur/60:.1f} minutes)")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
