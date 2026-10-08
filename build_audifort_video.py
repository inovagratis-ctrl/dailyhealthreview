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
        "tag": "AUDIOLOGY HEALTH REVIEW  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in",
        "sentences": [
            "Do you constantly ask family members to repeat themselves, or lie awake at night tormented by a relentless ringing or buzzing in your ears?",
            "For millions of adults over forty, auditory decline and persistent tinnitus are among the most exhausting daily struggles.",
            "Today on Daily Health Review, we conduct an objective, clinical breakdown of Audifort—a liquid dietary formula designed to nourish auditory pathways."
        ]
    },
    {
        "id": "02",
        "file_keyword": "CENA_02",
        "tag": "ILLUSTRATIVE MEDICAL CONCEPT  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in_macro",
        "sentences": [
            "To understand hearing decline, we must look inside the inner ear's cochlea.",
            "Here, thousands of microscopic hair cells convert sound vibrations into electrical signals.",
            "When microcirculation slows and oxidative stress attacks these fragile cells, auditory signaling becomes distorted—causing both muffled hearing and phantom ringing sounds."
        ]
    },
    {
        "id": "03",
        "file_keyword": "CENA_03",
        "tag": "PRODUCT INVESTIGATION  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in",
        "sentences": [
            "This brings us to Audifort, engineered by audiological researcher Andrew Ross.",
            "Unlike generic pills, Audifort is a concentrated liquid sublingual tincture combining over twenty botanical extracts and minerals.",
            "Designed for rapid cellular absorption, it aims to support inner-ear blood flow and protect cochlear cells.",
            "Let us analyze its primary active bioactives."
        ]
    },
    {
        "id": "04",
        "file_keyword": "CENA_04",
        "tag": "AUDITORY BIOCHEMISTRY  |  DAILY HEALTH REVIEW",
        "effect": "pan_left_right",
        "sentences": [
            "First is Standardized Grape Seed Extract.",
            "Abundant in oligomeric proanthocyanidins, or OPCs, grape seed provides potent natural free-radical defense.",
            "In auditory research, OPCs help shield fragile cochlear hair cells against the cumulative oxidative degradation caused by noise and aging."
        ]
    },
    {
        "id": "05",
        "file_keyword": "CENA_05",
        "tag": "CLINICAL PHYTOTHERAPY  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in",
        "sentences": [
            "Second in the matrix is Green Tea Extract, standardized for EGCG.",
            "Scientific literature indicates EGCG supports healthy vessel flexibility, promoting steady blood flow through the microscopic auditory capillaries that deliver vital oxygen to your auditory nerve."
        ]
    },
    {
        "id": "06",
        "file_keyword": "CENA_06",
        "tag": "NUTRITIONAL BIOENERGETICS  |  DAILY HEALTH REVIEW",
        "effect": "zoom_out",
        "sentences": [
            "The third key ingredient is pure Maca Root Extract.",
            "Straining all day to understand conversations places an immense energetic drain on cognitive centers.",
            "Maca acts as a natural adaptogen, supporting sustained cellular stamina and helping the brain process auditory signals more efficiently."
        ]
    },
    {
        "id": "07",
        "file_keyword": "CENA_07",
        "tag": "OTIC CYTOPROTECTION  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in_macro",
        "sentences": [
            "Audifort also incorporates Capsicum Annuum and Gymnema Sylvestre.",
            "Natural capsaicinoids modulate healthy inflammatory pathways throughout auditory micro-vessels, while Gymnema provides cellular defense against chronic metabolic stress."
        ]
    },
    {
        "id": "08",
        "file_keyword": "CENA_08",
        "tag": "NEUROBIOLOGICAL BALANCE  |  DAILY HEALTH REVIEW",
        "effect": "pan_right_left",
        "sentences": [
            "Rounding out the synergistic blend is GABA—Gamma-Aminobutyric Acid.",
            "As the body's chief calming neurotransmitter, GABA helps soothe hyperactive neural firing in the auditory cortex.",
            "By dialing down acoustic over-stimulation, it provides relief from the anxiety and tension triggered by chronic tinnitus."
        ]
    },
    {
        "id": "09",
        "file_keyword": "CENA_09",
        "tag": "PHARMACEUTICAL QUALITY  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in",
        "sentences": [
            "Because Audifort is a sublingual liquid dropper, its micronutrients bypass the harsh digestive tract for superior bioavailability.",
            "The formula is non-GMO, non-habit forming, vegetarian, and proudly assembled in the United States in certified cGMP facilities."
        ]
    },
    {
        "id": "10",
        "file_keyword": "CENA_10",
        "tag": "DAILY PROTOCOL  |  DAILY HEALTH REVIEW",
        "effect": "pan_left_right",
        "sentences": [
            "Taking Audifort takes just ten seconds: place one full dropper under your tongue before breakfast, or mix it into your morning coffee, tea, or juice.",
            "While many users report feeling ear comfort within the first few weeks, nourishing auditory tissues is a cumulative process—making ninety to one hundred and eighty days optimal."
        ]
    },
    {
        "id": "11",
        "file_keyword": "CENA_11",
        "tag": "100% CONSUMER PROTECTION  |  DAILY HEALTH REVIEW",
        "effect": "zoom_in",
        "sentences": [
            "Audifort offers an industry-leading ninety-day, one-hundred-percent money-back guarantee.",
            "You can test the formula completely risk-free for three full months—and if you are not delighted with your hearing clarity, you can return even your empty bottles for a complete refund."
        ]
    },
    {
        "id": "12",
        "file_keyword": "CENA_12",
        "tag": "TRANSPARENT EDITORIAL DISCLOSURE  |  DAILY HEALTH REVIEW",
        "effect": "zoom_out",
        "sentences": [
            "In summary, Audifort provides a well-formulated, gentle liquid solution for anyone struggling with ear ringing, muffled sounds, or auditory strain.",
            "To secure the authentic laboratory discount and activate your ninety-day guarantee, use the verified official link in the description and pinned comment below.",
            "This is an affiliate link—we may earn a small commission at no extra cost to you. Thank you for watching Daily Health Review!"
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
    base_dir = Path("C:/Users/Eusimar/Downloads/VIDEO_AUDIFORT")
    base_dir.mkdir(parents=True, exist_ok=True)
    
    print("=== DAILY HEALTH REVIEW: AUDIFORT VIDEO COMPILER ===")
    print(f"Working Directory: {base_dir}")
    
    rendered_scenes = []
    
    for scene in SCENES:
        sid = scene["id"]
        print(f"\n--- Processing Scene {sid} ({scene['tag']}) ---")
        
        combined_text = " ".join(scene["sentences"])
        audio_file = base_dir / f"scene_{sid}_audio.mp3"
        vtt_file = base_dir / f"scene_{sid}.vtt"
        ass_file = base_dir / f"scene_{sid}.ass"
        scene_mp4 = base_dir / f"scene_{sid}.mp4"
        
        print(f"Generating TTS audio with voice {VOICE}...")
        generate_tts_and_vtt(combined_text, str(audio_file), str(vtt_file))
        
        duration = get_audio_duration(str(audio_file)) + 0.5
        print(f"Scene duration: {duration:.2f}s")
        
        entries = parse_vtt(str(vtt_file))
        create_ass_subtitles(entries, scene["tag"], duration, str(ass_file))
        
        img_candidates = list(base_dir.glob(f"*{scene['file_keyword']}*")) + list(base_dir.glob(f"*{sid}*"))
        img_candidates = [f for f in img_candidates if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]]
        
        if not img_candidates:
            fallback = base_dir / "audifort_bottle.png"
            if not fallback.exists():
                fallback = Path("C:/Users/Eusimar/.gemini/antigravity/scratch/Projeto_ClickBank_DailyHealthReview/Imagens_Oficiais/audifort_bottle.png")
            img_path = fallback
            print(f"Notice: Using fallback image: {img_path.name}")
        else:
            img_path = img_candidates[0]
            print(f"Using image: {img_path.name}")
            
        print(f"Rendering scene video with Ken Burns [{scene['effect']}]...")
        render_scene(img_path, audio_file, ass_file, scene["effect"], duration, scene_mp4)
        rendered_scenes.append(scene_mp4)
        print(f"Scene {sid} rendered successfully.")

    print("\n--- Concatenating Scenes into Master Review ---")
    concat_list = base_dir / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for sc in rendered_scenes:
            clean_path = str(sc.resolve()).replace("\\", "/")
            f.write(f"file '{clean_path}'\n")
            
    master_video = Path("C:/Users/Eusimar/Downloads/Audifort_Review_Completo_4Min_DailyHealthReview.mp4")
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
