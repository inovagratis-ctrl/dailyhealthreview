import os
import sys
import time
from playwright.sync_api import sync_playwright

def record_visiflora():
    output_dir = r"C:\Users\Eusimar\Downloads"
    os.makedirs(output_dir, exist_ok=True)
    temp_video_dir = os.path.join(output_dir, "_temp_playwright_video")
    os.makedirs(temp_video_dir, exist_ok=True)

    target_url = "https://getvisiflora.com/welcome/?hopId=3247b6c9-9c36-4d7c-aa81-633a1206cbd1"

    print("Iniciando gravacao de tela em 16:9 (1920x1080)...")
    
    with sync_playwright() as p:
        # Launch Chromium with video recording
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=temp_video_dir,
            record_video_size={"width": 1920, "height": 1080}
        )
        
        page = context.new_page()
        print(f"Acessando: {target_url}")
        
        try:
            page.goto(target_url, wait_until="networkidle", timeout=45000)
        except Exception as e:
            print(f"Aviso no carregamento inicial: {e}. Prosseguindo...")
            page.wait_for_timeout(3000)
            
        page.wait_for_timeout(2000)

        # Get total scrollable height
        total_height = page.evaluate("() => document.body.scrollHeight")
        viewport_height = 1080
        print(f"Altura total da pagina: {total_height}px")

        # Smooth scrolling down
        current_scroll = 0
        scroll_step = 8   # pixels per tick for butter-smooth motion
        
        print("Rolando a pagina suavemente para baixo...")
        while current_scroll < total_height - viewport_height:
            current_scroll += scroll_step
            page.evaluate(f"window.scrollTo(0, {current_scroll})")
            time.sleep(0.016) # ~60fps
            
            # Pause briefly at key milestones (25%, 50%, 75%, 100%)
            if current_scroll % 1500 < scroll_step:
                time.sleep(0.5)

        # Pause at the bottom / pricing section
        time.sleep(3.0)
        
        # Close context to save video
        context.close()
        browser.close()

    # Find the recorded webm/mp4 in temp dir
    recorded_files = [os.path.join(temp_video_dir, f) for f in os.listdir(temp_video_dir) if f.endswith(('.webm', '.mp4'))]
    if not recorded_files:
        print("Nenhum video encontrado.")
        return

    latest_video = max(recorded_files, key=os.path.getctime)
    final_output = os.path.join(output_dir, "video_rolagem_visiflora_16x9.mp4")

    # Convert with ffmpeg to standard high-compatibility MP4 H.264
    print("Convertendo e otimizando video para MP4 (1080p)...")
    ffmpeg_cmd = f'ffmpeg -y -i "{latest_video}" -c:v libx264 -pix_fmt yuv420p -preset fast -crf 20 "{final_output}"'
    res = os.system(ffmpeg_cmd)
    
    if os.path.exists(final_output) and os.path.getsize(final_output) > 1000:
        print(f"\n[SUCESSO] Video gravado e salvo com sucesso em:\n{final_output}")
    else:
        # If ffmpeg failed or not in path, copy original
        fallback = os.path.join(output_dir, "video_rolagem_visiflora_16x9.webm")
        os.rename(latest_video, fallback)
        print(f"\n[SUCESSO] Video salvo em:\n{fallback}")

if __name__ == "__main__":
    record_visiflora()
