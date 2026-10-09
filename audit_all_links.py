import os
import re

site_dir = r"C:\Users\Eusimar\.gemini\antigravity\scratch\Projeto_ClickBank_DailyHealthReview"

raw_patterns = [
    re.compile(r'https?://[a-zA-Z0-9\-_]+\.hop\.clickbank\.net[^\s"\'<>]*', re.I),
    re.compile(r'https?://hop\.clickbank\.net[^\s"\'<>]*', re.I),
    re.compile(r'https?://[a-zA-Z0-9\-_]+\.pay\.clickbank\.net[^\s"\'<>]*', re.I),
    re.compile(r'https?://[a-zA-Z0-9\-_]+\.clickbank\.net[^\s"\'<>]*', re.I),
    re.compile(r'https?://(?:www\.)?clickbank\.com[^\s"\'<>]*', re.I),
    re.compile(r'https?://(?:www\.)?theneurovera\.com[^\s"\'<>]*', re.I),
    re.compile(r'https?://(?:www\.)?audifort\.com[^\s"\'<>]*', re.I),
    re.compile(r'https?://(?:www\.)?trylymphtonic\.com[^\s"\'<>]*', re.I),
    re.compile(r'https?://(?:www\.)?sugardefender\.com[^\s"\'<>]*', re.I),
    re.compile(r'https?://(?:www\.)?prodentim\.com[^\s"\'<>]*', re.I),
    re.compile(r'https?://(?:www\.)?naganotonic\.com[^\s"\'<>]*', re.I),
    re.compile(r'https?://(?:www\.)?cleansesana\.com[^\s"\'<>]*', re.I),
    re.compile(r'https?://(?:www\.)?visiflora\.com[^\s"\'<>]*', re.I),
    re.compile(r'https?://(?:www\.)?circo2\.com[^\s"\'<>]*', re.I),
    re.compile(r'https?://(?:www\.)?advancedmemoryformula\.com[^\s"\'<>]*', re.I)
]

raw_links_found = []
go_redirect_routes = {}
all_page_cta_links = {}
all_pages_scanned = []

for root, dirs, files in os.walk(site_dir):
    if '.git' in root or '__pycache__' in root or '.vercel' in root:
        continue
    for f in files:
        if f.endswith(('.html', '.js', '.json')):
            fpath = os.path.join(root, f)
            rel_path = os.path.relpath(fpath, site_dir).replace('\\', '/')
            all_pages_scanned.append(rel_path)
            
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()
                
            is_go_folder = rel_path.startswith('go/')
            
            # If inside go/, extract destination
            if is_go_folder and f == 'index.html':
                content = "".join(lines)
                m = re.search(r'url=([^\'"]+)', content, re.I)
                if not m:
                    m = re.search(r'location\.href\s*=\s*[\'"]([^\'"]+)[\'"]', content, re.I)
                target = m.group(1) if m else "UNKNOWN"
                route = '/' + os.path.dirname(rel_path)
                go_redirect_routes[route] = target
                continue
                
            # Scan each line for raw links or hrefs
            for line_idx, line in enumerate(lines, 1):
                # Check for raw affiliate / vendor links
                for pat in raw_patterns:
                    matches = pat.findall(line)
                    for match in matches:
                        raw_links_found.append({
                            'file': rel_path,
                            'line': line_idx,
                            'match': match,
                            'context': line.strip()
                        })
                        
                # Extract all hrefs
                href_matches = re.findall(r'href=[\'"]([^\'"]+)[\'"]', line, re.I)
                for href in href_matches:
                    if href.startswith('/go/'):
                        if rel_path not in all_page_cta_links:
                            all_page_cta_links[rel_path] = set()
                        all_page_cta_links[rel_path].add(href)

output_lines = []
output_lines.append("="*70)
output_lines.append("AUDITORIA COMPLETA DE LINKS - DAILY HEALTH REVIEW")
output_lines.append("="*70)
output_lines.append(f"Total de arquivos escaneados: {len(all_pages_scanned)}")

output_lines.append(f"\n1. ROTAS INTERNAS DE REDIRECIONAMENTO LIMPAS (/go/): Total = {len(go_redirect_routes)}")
for route in sorted(go_redirect_routes.keys()):
    output_lines.append(f"   {route:<20} -> {go_redirect_routes[route]}")

output_lines.append("\n" + "-"*70)
output_lines.append("2. LINKS DE CTA (/go/...) PRESENTES NAS PAGINAS DO SITE:")
for page in sorted(all_page_cta_links.keys()):
    output_lines.append(f"   [PAGINA] {page}")
    for link in sorted(all_page_cta_links[page]):
        output_lines.append(f"      |--> {link}")

output_lines.append("\n" + "="*70)
output_lines.append("3. RESULTADO DA BUSCA POR LINKS CRUS / VAZADOS NAS PAGINAS PUBLICAS:")
output_lines.append("="*70)

if raw_links_found:
    output_lines.append(f"ALERTA: Foram encontrados {len(raw_links_found)} links crus/externos fora da pasta /go/:")
    for item in raw_links_found:
        output_lines.append(f"   [ARQUIVO] {item['file']}:{item['line']}")
        output_lines.append(f"      Link: {item['match']}")
        output_lines.append(f"      Linha: {item['context'][:120]}...\n")
else:
    output_lines.append("SUCESSO: NENHUM LINK CRU DO CLICKBANK OU DE PRODUTOR EXPOSTO!")
    output_lines.append("Todas as paginas publicas usam estritamente links camuflados /go/*.")
output_lines.append("="*70)

report_text = "\n".join(output_lines)
print(report_text)

with open(os.path.join(site_dir, "relatorio_auditoria_links.txt"), "w", encoding="utf-8") as rf:
    rf.write(report_text)
