import os

site_dir = r"C:\Users\Eusimar\.gemini\antigravity\scratch\Projeto_ClickBank_DailyHealthReview"
tag_id = "2613505577093"

pinterest_pixel_code = f"""<!-- Pinterest Tag -->
<script>
!function(e){{if(!window.pintrk){{window.pintrk = function () {{
window.pintrk.queue.push(Array.prototype.slice.call(arguments))}};var
  n=window.pintrk;n.queue=[],n.version="3.0";var
  t=document.createElement("script");t.async=!0,t.src=e;var
  r=document.getElementsByTagName("script")[0];
  r.parentNode.insertBefore(t,r)}}}}("https://s.pinimg.com/ct/core.js");
pintrk('load', '{tag_id}');
pintrk('page');
</script>
<noscript>
<img height="1" width="1" style="display:none;" alt=""
  src="https://ct.pinterest.com/v3/?event=init&tid={tag_id}&noscript=1" />
</noscript>
<!-- end Pinterest Tag -->"""

count = 0
for root, dirs, files in os.walk(site_dir):
    if '.git' in root or '__pycache__' in root or '.vercel' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            fpath = os.path.join(root, f)
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                
            if 'pintrk(' not in content:
                # Insert right before </head>
                if '</head>' in content:
                    new_content = content.replace('</head>', pinterest_pixel_code + '\n</head>', 1)
                    with open(fpath, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    count += 1

print(f"[+] Pixel do Pinterest (ID: {tag_id}) instalado com sucesso em {count} arquivos HTML!")
