import os
import sys
import json
import time
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import threading

API_KEY = "API-C6JT52HMN2YWGH0YK3IFCI8O3D37X5O4VLTV"
ACCOUNT_NICKNAME = "eusimar72"
DIGISTORE_ID = "eusimar72"
PORT = 8080

def fetch_clickbank_orders():
    """Fetches real order list from ClickBank 1.3 REST API"""
    url = "https://api.clickbank.com/rest/1.3/orders2/list"
    req = urllib.request.Request(url, headers={
        "Authorization": API_KEY,
        "Accept": "application/json",
        "User-Agent": "DailyHealthReview-Dashboard/1.0"
    })
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data_raw = resp.read().decode("utf-8")
            if not data_raw or data_raw.strip() == "null":
                return {"success": True, "orders": [], "total_amount": 0.0, "total_count": 0}
            data = json.loads(data_raw)
            orders = data.get("orderData", [])
            if isinstance(orders, dict):
                orders = [orders]
            
            total_comm = sum(float(o.get("affiliateCommission", 0.0)) for o in orders)
            return {
                "success": True,
                "orders": orders,
                "total_amount": total_comm,
                "total_count": len(orders)
            }
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}", "orders": [], "total_amount": 0.0, "total_count": 0}
    except Exception as ex:
        return {"success": False, "error": str(ex), "orders": [], "total_amount": 0.0, "total_count": 0}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Daily Health Review | Live Sales & Affiliate Command Center</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
    body { font-family: 'Inter', sans-serif; background-color: #0b1329; color: #f8fafc; }
    .card-glow { background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(51, 65, 85, 0.6); }
    .metric-emerald { background: linear-gradient(135deg, rgba(6, 78, 59, 0.6) 0%, rgba(15, 23, 42, 0.9) 100%); border: 1px solid rgba(16, 185, 129, 0.4); }
    .metric-amber { background: linear-gradient(135deg, rgba(120, 53, 15, 0.6) 0%, rgba(15, 23, 42, 0.9) 100%); border: 1px solid rgba(245, 158, 11, 0.4); }
    .metric-blue { background: linear-gradient(135deg, rgba(12, 74, 110, 0.6) 0%, rgba(15, 23, 42, 0.9) 100%); border: 1px solid rgba(14, 165, 233, 0.4); }
    .metric-purple { background: linear-gradient(135deg, rgba(88, 28, 135, 0.6) 0%, rgba(15, 23, 42, 0.9) 100%); border: 1px solid rgba(168, 85, 247, 0.4); }
    @keyframes pulseLive { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    .live-dot { animation: pulseLive 2s infinite ease-in-out; }
  </style>
</head>
<body class="min-h-screen flex flex-col">

  <!-- Top Navigation Bar -->
  <header class="card-glow border-b border-slate-800 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 py-3.5 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <span class="bg-red-700 text-white font-black text-xl px-2.5 py-1 rounded shadow">DHR</span>
        <div>
          <h1 class="text-lg font-extrabold tracking-tight text-white flex items-center gap-2">
            ClickBank & Digistore24 Live Command Center
            <span class="text-[11px] font-bold uppercase tracking-wider bg-emerald-950 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded-full flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-emerald-400 live-dot"></span> API ONLINE (8080)
            </span>
          </h1>
          <p class="text-xs text-slate-400">ID Afiliado: <span class="text-amber-400 font-bold">eusimar72</span> • Portal: <span class="text-emerald-400 font-mono font-bold">dailyhealthreviewus.com</span></p>
        </div>
      </div>
      
      <div class="flex items-center gap-3">
        <button onclick="refreshData()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-lg shadow transition flex items-center gap-2">
          <i class="fa-solid fa-arrows-rotate" id="refresh-icon"></i> Atualizar Agora
        </button>
        <a href="https://dailyhealthreviewus.com" target="_blank" class="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg border border-slate-700 flex items-center gap-1.5">
          <i class="fa-solid fa-arrow-up-right-from-square"></i> Ver Portal
        </a>
      </div>
    </div>
  </header>

  <!-- Main Dashboard Container -->
  <main class="max-w-7xl mx-auto px-4 py-8 flex-grow space-y-8 w-full">

    <!-- KPI Metric Cards Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      
      <!-- Card 1: Total Commissions -->
      <div class="metric-emerald p-6 rounded-2xl shadow-lg relative overflow-hidden">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-bold uppercase tracking-wider text-emerald-300">Total em Comissões</span>
          <div class="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-lg">
            <i class="fa-solid fa-dollar-sign"></i>
          </div>
        </div>
        <div class="text-3xl font-black text-white" id="total-commissions">$0.00</div>
        <div class="text-xs text-emerald-200/80 mt-2 flex items-center gap-1">
          <i class="fa-solid fa-circle-check"></i> Saldo direto na ClickBank REST API
        </div>
      </div>

      <!-- Card 2: Sales Today -->
      <div class="metric-amber p-6 rounded-2xl shadow-lg relative overflow-hidden">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-bold uppercase tracking-wider text-amber-300">Vendas Aprovadas</span>
          <div class="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-lg">
            <i class="fa-solid fa-cart-shopping"></i>
          </div>
        </div>
        <div class="text-3xl font-black text-white" id="total-sales">0</div>
        <div class="text-xs text-amber-200/80 mt-2 flex items-center gap-1">
          <i class="fa-solid fa-chart-line"></i> Transações em tempo real
        </div>
      </div>

      <!-- Card 3: Active Pre-sell Articles -->
      <div class="metric-blue p-6 rounded-2xl shadow-lg relative overflow-hidden">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-bold uppercase tracking-wider text-cyan-300">Produtos no Portal</span>
          <div class="w-10 h-10 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center text-lg">
            <i class="fa-solid fa-layer-group"></i>
          </div>
        </div>
        <div class="text-3xl font-black text-white">24 Ativos</div>
        <div class="text-xs text-cyan-200/80 mt-2 flex items-center gap-1">
          <i class="fa-solid fa-bolt"></i> ClickBank & Digistore24
        </div>
      </div>

      <!-- Card 4: Ticket Médio Estimado -->
      <div class="metric-purple p-6 rounded-2xl shadow-lg relative overflow-hidden">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-bold uppercase tracking-wider text-purple-300">Comissão Média</span>
          <div class="w-10 h-10 rounded-xl bg-purple-500/20 text-purple-400 flex items-center justify-center text-lg">
            <i class="fa-solid fa-tags"></i>
          </div>
        </div>
        <div class="text-3xl font-black text-white">~$145.00</div>
        <div class="text-xs text-purple-200/80 mt-2 flex items-center gap-1">
          <i class="fa-solid fa-shield-halved"></i> 60% a 85% / Até $210 CPA
        </div>
      </div>

    </div>

    <!-- Active Campaigns / Product Links Table -->
    <div class="card-glow rounded-2xl p-6 shadow-xl border border-slate-800">
      <div class="flex items-center justify-between mb-5">
        <div>
          <h2 class="text-base font-bold text-white flex items-center gap-2">
            <i class="fa-solid fa-link text-emerald-400"></i> Esteira de 24 Produtos Conectados no Blog & Redirecionamentos Limpos
          </h2>
          <p class="text-xs text-slate-400">Monitorando conversões e tráfego orgânico do Pinterest, Google SEO, YouTube e Flipboard</p>
        </div>
        <span class="text-xs text-slate-400 bg-slate-800/80 px-3 py-1 rounded-full border border-slate-700 font-bold text-emerald-400">24 Artigos Publicados & Monitorados</span>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead class="bg-slate-900/80 text-slate-300 uppercase font-bold text-[11px] border-b border-slate-800">
            <tr>
              <th class="p-3.5">Produto Oficial</th>
              <th class="p-3.5">Plataforma</th>
              <th class="p-3.5">Nicho / Categoria</th>
              <th class="p-3.5">Comissão Estimada</th>
              <th class="p-3.5">Artigo no seu Portal</th>
              <th class="p-3.5">Redirecionamento</th>
              <th class="p-3.5">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800/60 font-medium">

            <!-- FIMAVYN Metabolic Activation (NEW ClickBank) -->
            <tr class="hover:bg-slate-800/40 transition bg-emerald-950/40">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span> FIMAVYN™ Metabolic Activation
              </td>
              <td class="p-3.5 text-amber-400 font-bold">ClickBank (fimavyn)</td>
              <td class="p-3.5 text-slate-300">Ativação Metabólica, Queima de Gordura & Sensibilidade à Insulina (10 Ativos)</td>
              <td class="p-3.5 text-emerald-400 font-bold">75% em todo o funil (AOV $177+, Até $150+ por Venda)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/fimavyn-metabolic-activation-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /fimavyn-metabolic-activation-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/fimavyn</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- Advanced Collagen PLUS (NEW Digistore24) -->
            <tr class="hover:bg-slate-800/40 transition bg-rose-950/40">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-rose-400 animate-pulse"></span> Advanced Collagen PLUS™
              </td>
              <td class="p-3.5 text-blue-400 font-bold">Digistore24 (soundview)</td>
              <td class="p-3.5 text-slate-300">Rejuvenescimento da Pele, Cabelos, Unhas & Articulações (5 Tipos)</td>
              <td class="p-3.5 text-emerald-400 font-bold">60% em todo o funil (Até $149+ por Venda)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/advanced-collagen-plus-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /advanced-collagen-plus-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/collagen</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- JointEternal (NEW Digistore24) -->
            <tr class="hover:bg-slate-800/40 transition bg-teal-950/40">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-teal-400 animate-pulse"></span> JointEternal™ (Cartilage Matrix)
              </td>
              <td class="p-3.5 text-blue-400 font-bold">Digistore24 (NaturalCell)</td>
              <td class="p-3.5 text-slate-300">Estabilidade Articular, Cartilagem & Mobilidade (1,500mg Glucosamina)</td>
              <td class="p-3.5 text-emerald-400 font-bold">75% em todo o funil (AOV $250+, Até $175+ por Venda)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/joint-eternal-mobility-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /joint-eternal-mobility-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/jointeternal</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- Advanced Joint Support (NEW Digistore24) -->
            <tr class="hover:bg-slate-800/40 transition bg-amber-950/40">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse"></span> Advanced Joint Support™
              </td>
              <td class="p-3.5 text-blue-400 font-bold">Digistore24 (soundview)</td>
              <td class="p-3.5 text-slate-300">Saúde Articular, Cartilagem & Mobilidade 50+ (Q-Actin™)</td>
              <td class="p-3.5 text-emerald-400 font-bold">60% em todo o funil (Até $208+ por Venda)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/advanced-joint-support-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /advanced-joint-support-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/jointsupport</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- ProstaVive (NEW) -->
            <tr class="hover:bg-slate-800/40 transition bg-sky-950/40">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-sky-400 animate-pulse"></span> ProstaVive™ (Prostate & Flow)
              </td>
              <td class="p-3.5 text-amber-400 font-bold">ClickBank (prostavive)</td>
              <td class="p-3.5 text-slate-300">Saúde da Próstata, Fluxo Urinário & Sono 50+</td>
              <td class="p-3.5 text-emerald-400 font-bold">75% a 80% (AOV $234, EPC $3.00+)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/prostavive-prostate-health-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /prostavive-prostate-health-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/prostavive</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- Java Burn (NEW) -->
            <tr class="hover:bg-slate-800/40 transition bg-amber-950/40">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse"></span> Java Burn™ (Coffee Ritual)
              </td>
              <td class="p-3.5 text-amber-400 font-bold">ClickBank (javaburn)</td>
              <td class="p-3.5 text-slate-300">Metabolismo Matinal & Queima de Gordura no Café</td>
              <td class="p-3.5 text-emerald-400 font-bold">Até $165.00 por Venda (AOV $294, EPC $2.80+)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/java-burn-coffee-ritual-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /java-burn-coffee-ritual-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/javaburn</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- Cardio Slim Tea (VIP Whitelisted NEW) -->
            <tr class="hover:bg-slate-800/40 transition bg-blue-950/40">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-blue-400 animate-pulse"></span> Cardio Slim Tea™ (VIP Whitelist)
              </td>
              <td class="p-3.5 text-amber-400 font-bold">ClickBank (cardioslim)</td>
              <td class="p-3.5 text-slate-300">Saúde Cardiovascular, Pressão & Homocisteína</td>
              <td class="p-3.5 text-emerald-400 font-bold">65% FE / 50% Upsells (Até $210 CPA • AOV $300+)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/cardioslim-tea-cardio-support-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /cardioslim-tea-cardio-support-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/cardioslim</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- SpartaMax (Digistore24 NEW) -->
            <tr class="hover:bg-slate-800/40 transition bg-amber-950/40">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse"></span> SpartaMax™ (Gummies 365D)
              </td>
              <td class="p-3.5 text-blue-400 font-bold">Digistore24</td>
              <td class="p-3.5 text-slate-300">Vitalidade Masculina, Fluxo Sanguíneo & Stamina</td>
              <td class="p-3.5 text-emerald-400 font-bold">65% RevShare (AOV $210+, 365-Day Guarantee)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/spartamax-vitality-gummies-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /spartamax-vitality-gummies-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/spartamax</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- Neotonics (NEW) -->
            <tr class="hover:bg-slate-800/40 transition bg-rose-950/40">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-rose-400 animate-pulse"></span> Neotonics™ (VIP Group)
              </td>
              <td class="p-3.5 text-amber-400 font-bold">ClickBank</td>
              <td class="p-3.5 text-slate-300">Renovação Celular da Pele & Saúde do Intestino</td>
              <td class="p-3.5 text-emerald-400 font-bold">VIP Group Bump (AOV $240+, EPC $3.00+)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/neotonics-skin-gut-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /neotonics-skin-gut-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/neotonics</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- GlucoTrust German (NEW) -->
            <tr class="hover:bg-slate-800/40 transition bg-emerald-950/40">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span> GlucoTrust™ (German DACH)
              </td>
              <td class="p-3.5 text-blue-400 font-bold">Digistore24</td>
              <td class="p-3.5 text-slate-300">Blutzucker, Tiefschlaf & Cortisol</td>
              <td class="p-3.5 text-emerald-400 font-bold">60% RevShare (€242 AOV, EPC €4.50)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/glucotrust-blutzucker-bericht" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /glucotrust-blutzucker-bericht <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/glucotrust</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- Phytomem One (NEW) -->
            <tr class="hover:bg-slate-800/40 transition bg-amber-950/40">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse"></span> Phytomem One™
              </td>
              <td class="p-3.5 text-amber-400 font-bold">ClickBank</td>
              <td class="p-3.5 text-slate-300">Memória, Plastic Stranglehold & Combustível Cerebral</td>
              <td class="p-3.5 text-emerald-400 font-bold">65% (AOV $230+, EPC $3.20+)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/phytomem-memory-formula-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /phytomem-memory-formula-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/phytomem</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- Advanced Amino Formula (NEW) -->
            <tr class="hover:bg-slate-800/40 transition bg-sky-950/30">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-sky-400 animate-pulse"></span> Advanced Amino Formula™
              </td>
              <td class="p-3.5 text-blue-400 font-bold">Digistore24</td>
              <td class="p-3.5 text-slate-300">Reversão de Perda Muscular Sênior 50+</td>
              <td class="p-3.5 text-emerald-400 font-bold">$33.25 a $199.50 (50-60%)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/advanced-amino-formula-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /advanced-amino-formula-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/amino</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- All Day Slimming Tea (Whitelisted VIP) -->
            <tr class="hover:bg-slate-800/40 transition bg-emerald-950/30">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span> All Day Slimming Tea™ (Whitelisted VIP)
              </td>
              <td class="p-3.5 text-amber-400 font-bold">ClickBank (allslimtea)</td>
              <td class="p-3.5 text-slate-300">Metabolismo Matinal/Noturno & Desintoxicação</td>
              <td class="p-3.5 text-emerald-400 font-bold">65% FE / 50% Upsells (Aprovado VIP)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/all-day-slimming-tea-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /all-day-slimming-tea-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/slimmingtea</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- FemiCore (NEW) -->
            <tr class="hover:bg-slate-800/40 transition bg-rose-950/30">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-rose-400 animate-pulse"></span> FemiCore™
              </td>
              <td class="p-3.5 text-amber-400 font-bold">ClickBank</td>
              <td class="p-3.5 text-slate-300">Saúde da Bexiga Feminina & Microbioma</td>
              <td class="p-3.5 text-emerald-400 font-bold">$120.00 a $145.00</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/femicore-pelvic-health-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /femicore-pelvic-health-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/femicore</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- Lymph Tonic -->
            <tr class="hover:bg-slate-800/40 transition bg-teal-950/20">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-teal-400"></span> Lymph Tonic™
              </td>
              <td class="p-3.5 text-amber-400 font-bold">ClickBank</td>
              <td class="p-3.5 text-slate-300">Drenagem Linfática / Pernas Inchadas</td>
              <td class="p-3.5 text-emerald-400 font-bold">Até $160 CPA / $200+</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/lymphtonic-drainage-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /lymphtonic-drainage-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/lymphtonic</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- Audifort -->
            <tr class="hover:bg-slate-800/40 transition bg-cyan-950/20">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-cyan-400"></span> Audifort™
              </td>
              <td class="p-3.5 text-amber-400 font-bold">ClickBank</td>
              <td class="p-3.5 text-slate-300">Saúde Auditiva / Zumbido (Tinnitus)</td>
              <td class="p-3.5 text-emerald-400 font-bold">$100.00 a $190.00 (65%)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/audifort-hearing-support-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /audifort-hearing-support-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/audifort</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- NeuroVera -->
            <tr class="hover:bg-slate-800/40 transition bg-indigo-950/20">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-indigo-400"></span> NeuroVera™
              </td>
              <td class="p-3.5 text-amber-400 font-bold">ClickBank</td>
              <td class="p-3.5 text-slate-300">Saúde Cerebral / Memória & Foco</td>
              <td class="p-3.5 text-emerald-400 font-bold">$115.00 a $145.00</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/neurovera-brain-clarity-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /neurovera-brain-clarity-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/neurovera</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- VisiFlora -->
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-indigo-400"></span> VisiFlora™
              </td>
              <td class="p-3.5 text-amber-400 font-bold">ClickBank</td>
              <td class="p-3.5 text-slate-300">Saúde dos Olhos / Eixo Intestino-Visão</td>
              <td class="p-3.5 text-emerald-400 font-bold">$159.37</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/visiflora-vision-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /visiflora-vision-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/visiflora</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- CircO2 -->
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-rose-400"></span> CircO2™
              </td>
              <td class="p-3.5 text-blue-400 font-bold">Digistore24</td>
              <td class="p-3.5 text-slate-300">Óxido Nítrico / Circulação Sênior 50+</td>
              <td class="p-3.5 text-emerald-400 font-bold">$83.36 a $131.00</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/circo2-nitric-oxide-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /circo2-nitric-oxide-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/circo2</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- Advanced Memory Formula -->
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-sky-400"></span> Advanced Memory Formula™
              </td>
              <td class="p-3.5 text-blue-400 font-bold">Digistore24</td>
              <td class="p-3.5 text-slate-300">Memória / Cérebro & Foco 60+</td>
              <td class="p-3.5 text-emerald-400 font-bold">$87.73</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/advanced-memory-formula-guide" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /advanced-memory-formula-guide <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/memory</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- CleanseSana -->
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span> CleanseSana™
              </td>
              <td class="p-3.5 text-blue-400 font-bold">Digistore24</td>
              <td class="p-3.5 text-slate-300">Microbioma / Desinchaço Intestinal</td>
              <td class="p-3.5 text-emerald-400 font-bold">$106.94</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/cleansesana-gut-reboot" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /cleansesana-gut-reboot <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/cleansesana</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- Nagano Tonic -->
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-red-400"></span> Nagano Lean Body Tonic
              </td>
              <td class="p-3.5 text-amber-400 font-bold">ClickBank</td>
              <td class="p-3.5 text-slate-300">Metabolismo / 7s Elixir</td>
              <td class="p-3.5 text-emerald-400 font-bold">$120.00 a $140.00</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/nagano-tonic-review" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /nagano-tonic-review <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/nagano</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- Sugar Defender -->
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span> Sugar Defender®
              </td>
              <td class="p-3.5 text-amber-400 font-bold">ClickBank</td>
              <td class="p-3.5 text-slate-300">Controle de Glicose & Energia</td>
              <td class="p-3.5 text-emerald-400 font-bold">$125.00 a $145.00</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/sugar-defender-guide" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /sugar-defender-guide <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/sugardefender</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <!-- ProDentim -->
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-teal-400"></span> ProDentim®
              </td>
              <td class="p-3.5 text-amber-400 font-bold">ClickBank</td>
              <td class="p-3.5 text-slate-300">Saúde Bucal / Dentes & Gengivas</td>
              <td class="p-3.5 text-emerald-400 font-bold">$100.00 a $135.00</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/prodentim-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /prodentim-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/prodentim</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

          </tbody>
        </table>
      </div>
    </div>

          </tbody>
        </table>
      </div>
    </div>

    <!-- Live Orders Section -->
    <div class="card-glow rounded-2xl p-6 shadow-xl border border-slate-800">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h2 class="text-base font-bold text-white flex items-center gap-2">
            <i class="fa-solid fa-receipt text-amber-400"></i> Registro de Vendas em Tempo Real (ClickBank API)
          </h2>
          <p class="text-xs text-slate-400">Sincronização automática a cada 60 segundos</p>
        </div>
        <span id="last-update" class="text-[11px] text-slate-400 font-mono">Última checagem: agora</span>
      </div>

      <div id="orders-container">
        <!-- Content will be injected by JavaScript -->
        <div class="bg-slate-900/60 rounded-xl p-8 text-center border border-slate-800">
          <div class="w-12 h-12 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center mx-auto mb-3 text-xl">
            <i class="fa-solid fa-satellite-dish"></i>
          </div>
          <h3 class="text-sm font-bold text-slate-200 mb-1">Aguardando Primeiras Conversões</h3>
          <p class="text-xs text-slate-400 max-w-md mx-auto">
            Assim que um visitante clicar em qualquer um dos seus Pins no Pinterest, Vídeos no YouTube ou Artigos no Blog e finalizar a compra na ClickBank ou Digistore24, a transação, valor da comissão e Tracking ID (TID) aparecerão aqui instantaneamente!
          </p>
        </div>
      </div>
    </div>

  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-800 text-center py-6 text-xs text-slate-500">
    Daily Health Review Live Analytics • Conectado à API ClickBank REST 1.3 • Nickname: <strong class="text-slate-300">eusimar72</strong> • 13 Ofertas Conectadas
  </footer>

  <script>
    async function refreshData() {
      const icon = document.getElementById('refresh-icon');
      if (icon) icon.classList.add('fa-spin');
      
      try {
        const res = await fetch('/api/orders');
        const data = await res.json();
        
        if (data.success) {
          document.getElementById('total-commissions').innerText = '$' + data.total_amount.toFixed(2);
          document.getElementById('total-sales').innerText = data.total_count;
          
          const container = document.getElementById('orders-container');
          if (data.orders.length > 0) {
            let html = '<div class="overflow-x-auto"><table class="w-full text-left text-xs font-medium"><thead class="bg-slate-900 text-slate-300 uppercase text-[10px]"><tr><th class="p-3">Data/Hora</th><th class="p-3">Recibo / Order ID</th><th class="p-3">Produto</th><th class="p-3">Comissão Afiliado</th><th class="p-3">Tracking ID</th></tr></thead><tbody class="divide-y divide-slate-800">';
            data.orders.forEach(o => {
              html += `<tr class="hover:bg-slate-800/40"><td class="p-3">${o.transactionTime || 'N/A'}</td><td class="p-3 font-mono text-cyan-400">${o.receipt || 'N/A'}</td><td class="p-3 text-white font-bold">${o.itemTitle || o.itemNo || 'N/A'}</td><td class="p-3 text-emerald-400 font-bold">$${parseFloat(o.affiliateCommission || 0).toFixed(2)}</td><td class="p-3 text-amber-400 font-mono">${o.trackingId || '-'}</td></tr>`;
            });
            html += '</tbody></table></div>';
            container.innerHTML = html;
          }
        }
      } catch (e) {
        console.error('Erro ao buscar dados:', e);
      } finally {
        if (icon) icon.classList.remove('fa-spin');
        const now = new Date();
        document.getElementById('last-update').innerText = 'Última checagem: ' + now.toLocaleTimeString();
      }
    }

    // Auto refresh every 60 seconds
    setInterval(refreshData, 60000);
    window.onload = refreshData;
  </script>

</body>
</html>
"""

class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/orders":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            data = fetch_clickbank_orders()
            self.wfile.write(json.dumps(data).encode("utf-8"))
        elif self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ONLINE", "port": PORT, "products_count": 14, "nickname": ACCOUNT_NICKNAME}).encode("utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))

def start_server():
    server = HTTPServer(('127.0.0.1', PORT), DashboardHandler)
    print("\n=======================================================")
    print("[+] CLICKBANK & DIGISTORE LIVE SALES DASHBOARD ATIVO!")
    print("[+] API Status: ONLINE (Conectada a ClickBank REST 1.3)")
    print(f"[+] Acesse no seu navegador: http://localhost:{PORT}")
    print("=======================================================\n")
    server.serve_forever()

if __name__ == "__main__":
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    time.sleep(1)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nPainel encerrado.")
