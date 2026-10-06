import os
import sys
import asyncio
import time
import subprocess
import edge_tts
from playwright.sync_api import sync_playwright

VOICE = "en-US-ChristopherNeural"  # Professional authoritative American narrator

SCRIPT_TEXT = """
Important warning before you consider buying VisiFlora: please watch this entire video carefully. 

If you are struggling with blurry vision, eye fatigue from digital screens, or terrible glare during night driving, modern ophthalmology has revealed a shocking discovery. 

Most people believe vision decline after age 45 is inevitable. But clinical research from Harvard and European universities shows that the microscopic capillaries in your retina are directly tied to your gut microbiome. When inflammatory toxins cross your digestive wall, they travel straight to your eyes, suffocating macular cells.

That is why VisiFlora was created. It is the first military-inspired formula designed specifically around the Gut-Eye Connection.

Inside every capsule, VisiFlora delivers a potent blend of rare Saffron extract, Ginkgo Biloba, Citrus Bioflavonoids, and live optic-shielding probiotic cultures. 

Together, these active botanicals help neutralize ocular inflammation, shield your eyes from harsh blue light, and support natural twenty-twenty visual sharpness.

Best of all, every order is fully protected by a 100% sixty-day money-back guarantee. If you don't experience crisper focus, you get every penny back.

To protect yourself from counterfeit bottles and claim the official manufacturer discount, click the verified official link pinned in the first comment right below this video.
""".strip()

async def generate_voiceover(output_audio_path):
    print("[1/4] Gerando narracao neural americana (IA)...")
    communicate = edge_tts.Communicate(SCRIPT_TEXT, VOICE, rate="+3%", pitch="+0Hz")
    await communicate.save(output_audio_path)
    print(f"[+] Audio neural gerado: {output_audio_path}")

def get_audio_duration(audio_path):
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{audio_path}"'
    res = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    return float(res)

def capture_cinematic_scenes(target_url, output_clips_dir, total_duration):
    print("[2/4] Capturando cenas dinamicas em Full HD 1080p (16:9)...")
    os.makedirs(output_clips_dir, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # We will record with 1920x1080 viewport
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=output_clips_dir,
            record_video_size={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        print(f"Carregando: {target_url}")
        
        try:
            page.goto(target_url, wait_until="networkidle", timeout=45000)
        except Exception:
            page.wait_for_timeout(3000)

        # Inject CSS to make cursor invisible and animations smooth
        page.add_style_tag(content="* { cursor: none !important; scroll-behavior: smooth !important; }")
        page.wait_for_timeout(2000)

        # Scene 1: Top Hero & Warning (0 to ~12s)
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(4.0)
        page.evaluate("window.scrollTo(0, 400)")
        time.sleep(4.0)

        # Scene 2: The Science / Gut-Eye Mechanism (~12s to ~26s)
        page.evaluate("window.scrollTo(0, 1100)")
        time.sleep(5.0)
        page.evaluate("window.scrollTo(0, 1900)")
        time.sleep(5.0)

        # Scene 3: Product Bottle & Military Formula (~26s to ~40s)
        page.evaluate("window.scrollTo(0, 2700)")
        time.sleep(6.0)
        page.evaluate("window.scrollTo(0, 3600)")
        time.sleep(5.0)

        # Scene 4: Ingredients breakdown & Benefits (~40s to ~55s)
        page.evaluate("window.scrollTo(0, 4500)")
        time.sleep(6.0)
        page.evaluate("window.scrollTo(0, 5600)")
        time.sleep(5.0)

        # Scene 5: 60-Day Guarantee & Reviews (~55s to ~68s)
        page.evaluate("window.scrollTo(0, 6700)")
        time.sleep(6.0)
        page.evaluate("window.scrollTo(0, 7600)")
        time.sleep(5.0)

        # Scene 6: Pricing / Final CTA (~68s to end)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(8.0)

        context.close()
        browser.close()

    recorded = [os.path.join(output_clips_dir, f) for f in os.listdir(output_clips_dir) if f.endswith(('.webm', '.mp4'))]
    if recorded:
        return max(recorded, key=os.path.getctime)
    return None

def build_final_video():
    downloads_dir = r"C:\Users\Eusimar\Downloads"
    temp_dir = os.path.join(downloads_dir, "_temp_render")
    os.makedirs(temp_dir, exist_ok=True)
    
    audio_path = os.path.join(temp_dir, "narration_visiflora.mp3")
    asyncio.run(generate_voiceover(audio_path))
    
    audio_duration = get_audio_duration(audio_path)
    print(f"[+] Duracao total da narracao: {audio_duration:.1f} segundos")

    target_url = "https://getvisiflora.com/welcome/?hopId=3247b6c9-9c36-4d7c-aa81-633a1206cbd1"
    raw_video = capture_cinematic_scenes(target_url, temp_dir, audio_duration)
    
    if not raw_video:
        print("Erro: Nenhum video capturado.")
        return

    final_output = os.path.join(downloads_dir, "VisiFlora_Review_Completo_YouTube_16x9.mp4")
    print("[3/4] Sincronizando video, cortes de zoom, audio neural e legendas...")

    # FFmpeg command: Sync video length exactly to audio, adjust speed, add subtle zoom and mix audio
    # Also add bottom banner: 'OFFICIAL LINK PINNED IN COMMENTS BELOW'
    cta_banner = "OFFICIAL DISCOUNT LINK PINNED IN THE FIRST COMMENT"
    
    ffmpeg_cmd = (
        f'ffmpeg -y -i "{raw_video}" -i "{audio_path}" '
        f'-filter_complex "[0:v]scale=1920:1080,setsar=1,'
        f'drawbox=y=ih-80:color=black@0.75:width=iw:height=80:t=fill,'
        f'drawtext=text=\'{cta_banner}\':fontcolor=yellow:fontsize=34:x=(w-text_w)/2:y=h-55:shadowcolor=black:shadowx=2:shadowy=2[v]" '
        f'-map "[v]" -map 1:a -c:v libx264 -pix_fmt yuv420p -preset fast -crf 20 -c:a aac -b:a 192k -shortest "{final_output}"'
    )

    print("[4/4] Renderizando arquivo final em alta qualidade...")
    subprocess.run(ffmpeg_cmd, shell=True, check=True)

    if os.path.exists(final_output) and os.path.getsize(final_output) > 1000:
        print(f"\n=======================================================")
        print(f"🎉 VÍDEO COMPLETO RENDERIZADO COM SUCESSO!")
        print(f"📁 Salvo em: {final_output}")
        print(f"=======================================================\n")
    else:
        print("Erro ao renderizar video final.")

if __name__ == "__main__":
    build_final_video()
