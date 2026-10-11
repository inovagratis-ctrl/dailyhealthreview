import os
import re
import subprocess

project_dir = r"C:\Users\Eusimar\.gemini\antigravity\scratch\Projeto_ClickBank_DailyHealthReview"

# 1. Update all old vercel.app domains to official custom domain dailyhealthreviewus.com
fixed_files = []
for root, dirs, files in os.walk(project_dir):
    for f in files:
        if f.endswith(('.html', '.xml', '.txt', '.json')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                c = fp.read()
            if 'dailyhealthreview.vercel.app' in c:
                new_c = c.replace('https://dailyhealthreview.vercel.app', 'https://dailyhealthreviewus.com')
                new_c = new_c.replace('dailyhealthreview.vercel.app', 'dailyhealthreviewus.com')
                with open(p, 'w', encoding='utf-8') as fp:
                    fp.write(new_c)
                fixed_files.append(p)

print(f"[+] Corrigidos dominios antigos em {len(fixed_files)} arquivos!")

# 2. Generate Master sitemap.xml with all 13 products and official pages
sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- Homepage -->
  <url>
    <loc>https://dailyhealthreviewus.com/</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>

  <!-- Pre-Sell Review Articles (13 Products) -->
  <url>
    <loc>https://dailyhealthreviewus.com/femicore-pelvic-health-report</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://dailyhealthreviewus.com/advanced-amino-formula-report</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://dailyhealthreviewus.com/all-day-slimming-tea-report</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://dailyhealthreviewus.com/lymphtonic-drainage-report</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://dailyhealthreviewus.com/audifort-hearing-support-report</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://dailyhealthreviewus.com/neurovera-brain-clarity-report</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://dailyhealthreviewus.com/visiflora-vision-report</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://dailyhealthreviewus.com/advanced-memory-formula-guide</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://dailyhealthreviewus.com/circo2-nitric-oxide-report</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://dailyhealthreviewus.com/cleansesana-gut-reboot</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://dailyhealthreviewus.com/sugar-defender-guide</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://dailyhealthreviewus.com/morning-routine</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://dailyhealthreviewus.com/nagano-tonic-review</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://dailyhealthreviewus.com/prodentim-report</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>

  <!-- Legal & Transparency Pages -->
  <url>
    <loc>https://dailyhealthreviewus.com/privacy</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.3</priority>
  </url>
  <url>
    <loc>https://dailyhealthreviewus.com/terms</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.3</priority>
  </url>
  <url>
    <loc>https://dailyhealthreviewus.com/disclosure</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.3</priority>
  </url>
  <url>
    <loc>https://dailyhealthreviewus.com/disclaimer</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.3</priority>
  </url>
  <url>
    <loc>https://dailyhealthreviewus.com/contact</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.4</priority>
  </url>
</urlset>
"""

sitemap_path = os.path.join(project_dir, "sitemap.xml")
with open(sitemap_path, "w", encoding="utf-8") as fp:
    fp.write(sitemap_xml.strip())
print(f"[+] sitemap.xml atualizado com 100% dos links e dominio oficial: {sitemap_path}")

# 3. Update robots.txt with crawl optimization
robots_txt = """User-agent: *
Allow: /
Disallow: /go/

Sitemap: https://dailyhealthreviewus.com/sitemap.xml
"""

robots_path = os.path.join(project_dir, "robots.txt")
with open(robots_path, "w", encoding="utf-8") as fp:
    fp.write(robots_txt)
print(f"[+] robots.txt atualizado com protecao /go/ e sitemap oficial: {robots_path}")
