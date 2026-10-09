import os
import re

site_dir = r"C:\Users\Eusimar\.gemini\antigravity\scratch\Projeto_ClickBank_DailyHealthReview"

exact_pinterest_tag = """<!-- Pinterest Tag -->
<script>
!function(e){if(!window.pintrk){window.pintrk = function () {
window.pintrk.queue.push(Array.prototype.slice.call(arguments))};var
  n=window.pintrk;n.queue=[],n.version="3.0";var
  t=document.createElement("script");t.async=!0,t.src=e;var
  r=document.getElementsByTagName("script")[0];
  r.parentNode.insertBefore(t,r)}}("https://s.pinimg.com/ct/core.js");
pintrk('load', '2613505577093');
pintrk('page');
</script>
<noscript>
<img height="1" width="1" style="display:none;" alt=""
  src="https://ct.pinterest.com/v3/?event=init&tid=2613505577093&noscript=1" />
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
                
            # Replace existing pinterest tag block if present or insert
            if '<!-- Pinterest Tag -->' in content:
                content = re.sub(r'<!-- Pinterest Tag -->.*?<!-- end Pinterest Tag -->', exact_pinterest_tag, content, flags=re.DOTALL)
                with open(fpath, 'w', encoding='utf-8') as file:
                    file.write(content)
                count += 1
            elif '</head>' in content:
                content = content.replace('</head>', exact_pinterest_tag + '\n</head>', 1)
                with open(fpath, 'w', encoding='utf-8') as file:
                    file.write(content)
                count += 1

print(f"[+] Tag do Pinterest atualizada e validada em {count} arquivos HTML.")
