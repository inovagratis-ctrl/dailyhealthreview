import os
import re

GA_SNIPPET = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-BE7PQXFY9F"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-BE7PQXFY9F');
</script>"""

project_dir = r"C:\Users\Eusimar\.gemini\antigravity\scratch\Projeto_ClickBank_DailyHealthReview"
updated_files = []

for root, dirs, files in os.walk(project_dir):
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
                content = fp.read()
            
            if 'G-BE7PQXFY9F' in content:
                continue
                
            # Insert right after <head> or <head ...>
            if '<head>' in content:
                new_content = content.replace('<head>', f'<head>\n{GA_SNIPPET}', 1)
            elif re.search(r'<head\b[^>]*>', content, re.IGNORECASE):
                new_content = re.sub(r'(<head\b[^>]*>)', r'\1\n' + GA_SNIPPET, content, count=1, flags=re.IGNORECASE)
            elif '</head>' in content:
                new_content = content.replace('</head>', f'{GA_SNIPPET}\n</head>', 1)
            else:
                new_content = f'{GA_SNIPPET}\n{content}'
                
            with open(filepath, 'w', encoding='utf-8') as fp:
                fp.write(new_content)
            updated_files.append(filepath)

print(f"Successfully installed Google Analytics (G-BE7PQXFY9F) in {len(updated_files)} HTML files!")
for p in updated_files:
    print(" -", os.path.relpath(p, project_dir))
