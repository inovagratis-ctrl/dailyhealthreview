import os
import re

site_dir = r"C:\Users\Eusimar\.gemini\antigravity\scratch\Projeto_ClickBank_DailyHealthReview"

REPLACEMENTS = [
    (re.compile(r'https?://06fe0-8qxlbmeo9jfi-fx24x4f\.hop\.clickbank\.net[^\s"\'<>]*', re.I), '/go/nagano'),
    (re.compile(r'https?://8e01330llbokexfevijb-nq74a\.hop\.clickbank\.net[^\s"\'<>]*', re.I), '/go/prodentim'),
    (re.compile(r'https?://1bb1cc1ek8qf8sbh84dll9uk5s\.hop\.clickbank\.net[^\s"\'<>]*', re.I), '/go/sugardefender'),
    (re.compile(r'https?://(?:www\.)?cleansesana\.com/cleansesana-pdp-fe#aff=eusimar72[^\s"\'<>]*', re.I), '/go/cleansesana'),
    (re.compile(r'https?://51062z5fucqiis5oqcr2mm151a\.hop\.clickbank\.net[^\s"\'<>]*', re.I), '/go/visiflora'),
    (re.compile(r'https?://6fd8bc8jpfkil09mti3fybx058\.hop\.clickbank\.net[^\s"\'<>]*', re.I), '/go/neurovera'),
    (re.compile(r'https?://6f9834zioammkt802al5tm4pf5\.hop\.clickbank\.net[^\s"\'<>]*', re.I), '/go/audifort'),
    (re.compile(r'https?://19a86z9ovajqhs57bex45l0flv\.hop\.clickbank\.net[^\s"\'<>]*', re.I), '/go/lymphtonic'),
    (re.compile(r'https?://(?:www\.)?advancedbionutritionals\.com/DS24/Nitric-Oxide-Supplements/Superhuman-At-70/HD\.htm#aff=eusimar72[^\s"\'<>]*', re.I), '/go/circo2'),
    (re.compile(r'https?://(?:www\.)?advancedbionutritionals\.com/DS24/Advanced-Memory/Nobel-Prize-Winning-Memory-Breakthroughs/HD\.htm#aff=eusimar72[^\s"\'<>]*', re.I), '/go/memory'),
]

files_updated = 0
total_replacements = 0

for root, dirs, files in os.walk(site_dir):
    if '.git' in root or '__pycache__' in root or '.vercel' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            fpath = os.path.join(root, f)
            rel_path = os.path.relpath(fpath, site_dir).replace('\\', '/')
            
            # Skip the redirect files inside go/
            if rel_path.startswith('go/'):
                continue
                
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                
            orig_content = content
            file_changes = 0
            
            for pat, repl in REPLACEMENTS:
                matches = pat.findall(content)
                if matches:
                    file_changes += len(matches)
                    content = pat.sub(repl, content)
                    
            if file_changes > 0:
                with open(fpath, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"[CORRIGIDO] {rel_path} -> {file_changes} links crus substituidos por /go/...")
                files_updated += 1
                total_replacements += file_changes

print(f"\n[+] Concluido! {total_replacements} links crus foram substituidos em {files_updated} arquivos.")
