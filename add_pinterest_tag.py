import os

site_dir = r"C:\Users\Eusimar\.gemini\antigravity\scratch\Projeto_ClickBank_DailyHealthReview"
pinterest_tag = '<meta name="p:domain_verify" content="f8027f14b8587a2f549f0d732aee4eb3"/>'

count = 0
for root, dirs, files in os.walk(site_dir):
    if '.git' in root or '__pycache__' in root or '.vercel' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            fpath = os.path.join(root, f)
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                
            if 'name="p:domain_verify"' not in content:
                # Insert right after <head>
                if '<head>' in content:
                    new_content = content.replace('<head>', '<head>\n  ' + pinterest_tag, 1)
                    with open(fpath, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    count += 1

print(f"[+] Sucesso! Tag do Pinterest inserida em {count} arquivos HTML.")
