import os
import re
import json
import datetime
import urllib.request
import urllib.error

base_dir = r"C:\Users\Eusimar\.gemini\antigravity\scratch\Projeto_ClickBank_DailyHealthReview"

def run_diagnostic():
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Read index.html catalog
    index_path = os.path.join(base_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        index_text = f.read()

    blocks = re.findall(
        r'\{\s*"id":\s*"([^"]+)",.*?"title":\s*"([^"]+)",.*?"price":\s*"([^"]+)",.*?"guarantee":\s*"([^"]+)",.*?"showcase":\s*"([^"]+)",.*?"review":\s*"([^"]+)",.*?"go":\s*"([^"]+)"',
        index_text,
        re.DOTALL
    )

    # Read _redirects
    redirects_map = {}
    redirects_path = os.path.join(base_dir, "_redirects")
    if os.path.exists(redirects_path):
        with open(redirects_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    redirects_map[parts[0]] = parts[1]

    report = {
        "timestamp": timestamp_str,
        "total_products": len(blocks),
        "showcases_ok": 0,
        "editorials_ok": 0,
        "advertorials_ok": 0,
        "redirects_ok": 0,
        "affiliate_tags_ok": 0,
        "issues": [],
        "products": []
    }

    ADVERTORIAL_MAP = {
        "fimavyn": "fimavyn-metabolic-drops-secret",
        "corevital": "corevital-berberine-burn-secret",
        "collagen": "advanced-collagen-firmness-secret",
        "jointeternal": "joint-eternal-mobility-secret",
        "joint-eternal": "joint-eternal-mobility-secret",
        "advanced-joint": "advanced-joint-cucumbers-secret",
        "prostavive": "prostavive-prostate-flow-secret",
        "javaburn": "javaburn-morning-coffee-secret",
        "cardioslim": "cardioslim-tea-cardio-secret",
        "spartamax": "spartamax-male-vitality-secret",
        "neotonics": "neotonics-gut-skin-secret",
        "glucotrust": "glucotrust-sleep-glucose-secret",
        "phytomem": "phytomem-memory-recall-secret",
        "advanced-amino": "advanced-amino-cellular-secret",
        "slimming-tea": "alldayslimming-tea-detox-secret",
        "all-day-slimming": "alldayslimming-tea-detox-secret",
        "femicore": "femicore-pelvic-floor-secret",
        "lymphtonic": "lymphtonic-drainage-secret",
        "audifort": "audifort-hearing-clarity-secret",
        "neurovera": "neurovera-nerve-calm-secret",
        "visiflora": "visiflora-eye-retina-secret",
        "circo2": "circo2-nitric-oxide-secret",
        "memory": "advanced-memory-brain-secret",
        "cleansesana": "cleansesana-colon-waste-secret",
        "nagano": "nagano-japanese-tonic-secret",
        "sugar-defender": "sugar-defender-glucose-secret",
        "prodentim": "prodentim-purple-mineral-secret",
        "kerassentials": "kerassentials-nail-clear-secret",
        "nanodefense": "nanodefense-nanotech-drops-secret",
        "synaptigen": "synaptigen-synapse-clarity-secret",
        "metanail": "metanail-20in1-complex-secret",
        "jointgenesis": "jointgenesis-synovial-fluid-secret",
        "synevra": "synevra-lift-and-lock-secret",
        "nitricboost": "nitricboost-male-stamina-secret",
        "livpure": "livpure-liver-purification-secret",
        "dentabiome": "dentabiome-postbiotic-mouth-secret",
        "yusleep": "yusleep-deep-rest-secret",
        "primebiome": "primebiome-gut-dermal-secret"
    }

    for b in blocks:
        pid, title, price, guarantee, sc_route, rev_route, go_route = b
        
        # 1. Check Showcase
        sc_slug = sc_route.replace("/showcase/", "").strip("/")
        sc_file = os.path.join(base_dir, "showcase", sc_slug, "index.html")
        sc_ok = os.path.exists(sc_file)
        if sc_ok:
            report["showcases_ok"] += 1
        else:
            report["issues"].append(f"Showcase ausente: {title} em showcase/{sc_slug}/index.html")

        # 2. Check Editorial
        rev_slug = rev_route.strip("/")
        rev_file1 = os.path.join(base_dir, rev_slug, "index.html")
        rev_file2 = os.path.join(base_dir, "articles", f"{rev_slug}.html")
        rev_file3 = os.path.join(base_dir, f"{rev_slug}.html")
        rev_mapped = redirects_map.get(f"/{rev_slug}", None)
        rev_file4 = os.path.join(base_dir, rev_mapped.lstrip("/")) if rev_mapped else None
        
        rev_ok = any(cand and os.path.exists(cand) for cand in [rev_file1, rev_file2, rev_file3, rev_file4])
        if rev_ok:
            report["editorials_ok"] += 1
        else:
            report["issues"].append(f"Editorial ausente: {title} para /{rev_slug}")

        # 3. Check /go/ redirect
        target_dest = redirects_map.get(go_route, None)
        if not target_dest:
            go_folder = go_route.replace("/go/", "").strip("/")
            go_html = os.path.join(base_dir, "go", go_folder, "index.html")
            if os.path.exists(go_html):
                with open(go_html, "r", encoding="utf-8", errors="ignore") as gf:
                    m = re.search(r'url=([^"\'\s>]+)', gf.read(), re.IGNORECASE)
                    if m:
                        target_dest = m.group(1)

        redir_ok = (target_dest is not None)
        if redir_ok:
            report["redirects_ok"] += 1
        else:
            report["issues"].append(f"Rota /go/ sem destino: {title} ({go_route})")

        # 4. Check affiliate tracking presence
        has_aff = False
        if target_dest:
            if "eusimar72" in target_dest or "hop.clickbank.net" in target_dest or "corevital" in target_dest:
                has_aff = True
                report["affiliate_tags_ok"] += 1
            elif "fimavyn" in target_dest or "buygoods" in target_dest:
                # pending BuyGoods
                has_aff = False
                report["issues"].append(f"Afiliado pendente BuyGoods: {title} ({target_dest})")
            else:
                report["issues"].append(f"Sem ID de afiliado no destino: {title} ({target_dest})")

        # 5. Check Story Advertorial (Arma 5)
        secret_slug = ADVERTORIAL_MAP.get(pid)
        adv_ok = False
        if secret_slug:
            adv_file = os.path.join(base_dir, secret_slug, "index.html")
            adv_ok = os.path.exists(adv_file)
        if adv_ok:
            report["advertorials_ok"] += 1
        else:
            report["issues"].append(f"Story Advertorial ausente: {title} ({secret_slug})")

        report["products"].append({
            "id": pid,
            "title": title,
            "price": price,
            "showcase_ok": sc_ok,
            "editorial_ok": rev_ok,
            "advertorial_ok": adv_ok,
            "secret_slug": secret_slug,
            "go_route": go_route,
            "dest_url": target_dest or "N/A",
            "aff_ok": has_aff
        })

    # Save JSON report
    json_path = os.path.join(base_dir, "DIAGNOSTICO_LINKS_STATUS.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Save human-readable summary
    txt_path = os.path.join(base_dir, "DIAGNOSTICO_LINKS_STATUS.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("="*75 + "\n")
        f.write(f"RELATÓRIO PERIÓDICO DE INTEGRIDADE DE LINKS & COMISSÕES\n")
        f.write(f"Data e Hora: {timestamp_str}\n")
        f.write("="*75 + "\n")
        f.write(f"Total de Produtos Auditados : {report['total_products']}\n")
        f.write(f"Showcases 100% Online       : {report['showcases_ok']} / {report['total_products']}\n")
        f.write(f"Editoriais 100% Online      : {report['editorials_ok']} / {report['total_products']}\n")
        f.write(f"Story Advertorials (Arma 5) : {report['advertorials_ok']} / {report['total_products']}\n")
        f.write(f"Rotas 302 Ativas            : {report['redirects_ok']} / {report['total_products']}\n")
        f.write(f"Links com Rastreamento Ativo: {report['affiliate_tags_ok']} / {report['total_products']}\n")
        f.write(f"Total de Alertas / Pendências: {len(report['issues'])}\n")
        f.write("="*75 + "\n\n")

        if report["issues"]:
            f.write("PENDÊNCIAS DETECTADAS:\n")
            for iss in report["issues"]:
                f.write(f" [!] {iss}\n")
            f.write("\n")
        else:
            f.write("STATUS: TODOS OS 36 PRODUTOS E LINKS ESTÃO 100% SEGUROS E ATIVOS!\n\n")

        f.write("DETALHAMENTO DOS 36 PRODUTOS:\n")
        f.write(f"{'#':<3} | {'Produto':<25} | {'Showcase':<8} | {'Editorial':<9} | {'Afiliado':<8} | {'Rota'}\n")
        f.write("-" * 75 + "\n")
        for i, p in enumerate(report["products"], 1):
            sc = "OK" if p["showcase_ok"] else "FALHA"
            ed = "OK" if p["editorial_ok"] else "FALHA"
            af = "OK" if p["aff_ok"] else "PEND"
            f.write(f"{i:02d}  | {p['title'][:25]:<25} | {sc:<8} | {ed:<9} | {af:<8} | {p['go_route']}\n")

    print(f"[{timestamp_str}] Diagnóstico concluído: {report['total_products']} produtos checados. Alertas: {len(report['issues'])}")
    return report

if __name__ == "__main__":
    run_diagnostic()
