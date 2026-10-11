import os
import re

ADSENSE_SNIPPET = """<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3922432751903141"
     crossorigin="anonymous"></script>"""

project_dir = r"C:\Users\Eusimar\.gemini\antigravity\scratch\Projeto_ClickBank_DailyHealthReview"
updated_files = []

for root, dirs, files in os.walk(project_dir):
    # Avoid installing on /go/ redirect folders to keep 100% AdSense compliance
    if "\\go\\" in root or "/go/" in root:
        continue
        
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
                content = fp.read()
            
            if 'ca-pub-3922432751903141' in content:
                continue
                
            # Place after Google Analytics tag or right after <head>
            if '<!-- Google tag (gtag.js) -->' in content:
                new_content = content.replace('<!-- Google tag (gtag.js) -->', f'{ADSENSE_SNIPPET}\n<!-- Google tag (gtag.js) -->', 1)
            elif '<head>' in content:
                new_content = content.replace('<head>', f'<head>\n{ADSENSE_SNIPPET}', 1)
            elif re.search(r'<head\b[^>]*>', content, re.IGNORECASE):
                new_content = re.sub(r'(<head\b[^>]*>)', r'\1\n' + ADSENSE_SNIPPET, content, count=1, flags=re.IGNORECASE)
            elif '</head>' in content:
                new_content = content.replace('</head>', f'{ADSENSE_SNIPPET}\n</head>', 1)
            else:
                new_content = f'{ADSENSE_SNIPPET}\n{content}'
                
            with open(filepath, 'w', encoding='utf-8') as fp:
                fp.write(new_content)
            updated_files.append(filepath)

print(f"Successfully installed Google AdSense (ca-pub-3922432751903141) in {len(updated_files)} HTML pages!")
for p in updated_files:
    print(" -", os.path.relpath(p, project_dir))
