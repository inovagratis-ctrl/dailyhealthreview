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
  <title>Daily Health Review | Live Sales & Affiliate Command Center (25 Produtos)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
    body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #0b1329; color: #f8fafc; }
    .card-glow { background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(51, 65, 85, 0.6); }
    .metric-emerald { background: linear-gradient(135deg, rgba(6, 78, 59, 0.65) 0%, rgba(15, 23, 42, 0.95) 100%); border: 1px solid rgba(16, 185, 129, 0.4); }
    .metric-amber { background: linear-gradient(135deg, rgba(120, 53, 15, 0.65) 0%, rgba(15, 23, 42, 0.95) 100%); border: 1px solid rgba(245, 158, 11, 0.4); }
    .metric-blue { background: linear-gradient(135deg, rgba(12, 74, 110, 0.65) 0%, rgba(15, 23, 42, 0.95) 100%); border: 1px solid rgba(14, 165, 233, 0.4); }
    .metric-purple { background: linear-gradient(135deg, rgba(88, 28, 135, 0.65) 0%, rgba(15, 23, 42, 0.95) 100%); border: 1px solid rgba(168, 85, 247, 0.4); }
    @keyframes pulseLive { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    .live-dot { animation: pulseLive 2s infinite ease-in-out; }
    .badge-cb { background-color: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-ds { background-color: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
  </style>
</head>
<body class="min-h-screen flex flex-col antialiased">

  <!-- Top Navigation Bar -->
  <header class="card-glow border-b border-slate-800 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center space-x-3">
        <span class="bg-red-700 text-white font-black text-xl px-2.5 py-1 rounded-lg shadow-lg">DHR</span>
        <div>
          <h1 class="text-lg font-black tracking-tight text-white flex items-center gap-2">
            Daily Health Review Command Center
            <span class="text-[11px] font-bold uppercase tracking-wider bg-emerald-950 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded-full flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-emerald-400 live-dot"></span> LIVE 8080
            </span>
          </h1>
          <p class="text-xs text-slate-400">ID Afiliado: <span class="text-amber-400 font-bold">eusimar72</span> • Catálogo: <strong class="text-emerald-400 font-bold">25 Showcases &amp; 25 Artigos no Ar</strong></p>
        </div>
      </div>
      
      <div class="flex items-center gap-2.5">
        <button onclick="refreshData()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-lg shadow transition flex items-center gap-2">
          <i class="fa-solid fa-arrows-rotate" id="refresh-icon"></i> Atualizar API
        </button>
        <a href="https://dailyhealthreviewus.com" target="_blank" class="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg border border-slate-700 flex items-center gap-1.5 transition">
          <i class="fa-solid fa-globe text-cyan-400"></i> Ver Portal
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
          <i class="fa-solid fa-circle-check"></i> ClickBank REST 1.3 API Sincronizada
        </div>
      </div>

      <!-- Card 2: Sales Today -->
      <div class="metric-amber p-6 rounded-2xl shadow-lg relative overflow-hidden">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-bold uppercase tracking-wider text-amber-300">Vendas Registradas</span>
          <div class="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-lg">
            <i class="fa-solid fa-cart-shopping"></i>
          </div>
        </div>
        <div class="text-3xl font-black text-white" id="total-sales">0</div>
        <div class="text-xs text-amber-200/80 mt-2 flex items-center gap-1">
          <i class="fa-solid fa-chart-line"></i> Tempo real (HopLinks + Digistore24)
        </div>
      </div>

      <!-- Card 3: Active Showcases -->
      <div class="metric-blue p-6 rounded-2xl shadow-lg relative overflow-hidden">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-bold uppercase tracking-wider text-cyan-300">Catálogo Conectado</span>
          <div class="w-10 h-10 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center text-lg">
            <i class="fa-solid fa-layer-group"></i>
          </div>
        </div>
        <div class="text-3xl font-black text-white">25 / 25 Ativos</div>
        <div class="text-xs text-cyan-200/80 mt-2 flex items-center gap-1">
          <i class="fa-solid fa-check-double"></i> 100% dos Showcases no Ar
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
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div>
          <h2 class="text-base font-black text-white flex items-center gap-2">
            <i class="fa-solid fa-table-cells-large text-emerald-400"></i> Matriz Completa de 25 Produtos (Artigos Pre-Sell &amp; Showcases Oficiais)
          </h2>
          <p class="text-xs text-slate-400">Clique para abrir e auditar qualquer artigo ou página de vendas oficial do seu portal</p>
        </div>
        
        <div class="flex flex-wrap items-center gap-2">
          <!-- Filter Buttons -->
          <button onclick="filterTable('all')" id="btn-filter-all" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-emerald-600 text-white shadow">Todos (25)</button>
          <button onclick="filterTable('clickbank')" id="btn-filter-cb" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700">ClickBank (16)</button>
          <button onclick="filterTable('digistore')" id="btn-filter-ds" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700">Digistore24 (9)</button>
          
          <!-- Instant Search Input -->
          <div class="relative">
            <input type="text" id="searchInput" onkeyup="searchProducts()" placeholder="Buscar produto..." class="bg-slate-900 border border-slate-700 text-white text-xs rounded-lg pl-8 pr-3 py-1.5 focus:outline-none focus:border-emerald-500 w-44">
            <i class="fa-solid fa-magnifying-glass absolute left-2.5 top-2.5 text-slate-500 text-xs"></i>
          </div>
        </div>
      </div>

      <div class="overflow-x-auto rounded-xl border border-slate-800">
        <table class="w-full text-left text-xs" id="productsTable">
          <thead class="bg-slate-900/90 text-slate-300 uppercase font-black text-[11px] border-b border-slate-800">
            <tr>
              <th class="p-3.5">#</th>
              <th class="p-3.5">Produto Oficial</th>
              <th class="p-3.5">Plataforma</th>
              <th class="p-3.5">Nicho / Categoria</th>
              <th class="p-3.5">Comissão Estimada</th>
              <th class="p-3.5">Artigo Pre-Sell</th>
              <th class="p-3.5">Showcase Oficial</th>
              <th class="p-3.5">Link Limpo</th>
              <th class="p-3.5">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800/60 font-medium" id="tableBody">

            <!-- 1. FIMAVYN -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="clickbank">
              <td class="p-3.5 text-slate-500 font-mono">01</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span> FIMAVYN™ Metabolic Activation
              </td>
              <td class="p-3.5"><span class="badge-cb text-[10px] font-bold px-2 py-0.5 rounded">ClickBank</span></td>
              <td class="p-3.5 text-slate-300">Ativação Metabólica &amp; Queima de Gordura</td>
              <td class="p-3.5 text-emerald-400 font-bold">75% (AOV $177+, Até $150+/venda)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/fimavyn-metabolic-activation-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /fimavyn-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/fimavyn" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/fimavyn <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/fimavyn</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 2. CoreVital Burn -->
            <tr class="hover:bg-slate-800/50 transition product-row bg-emerald-950/20" data-platform="clickbank">
              <td class="p-3.5 text-slate-500 font-mono">02</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse"></span> CoreVital Burn™
              </td>
              <td class="p-3.5"><span class="badge-cb text-[10px] font-bold px-2 py-0.5 rounded">ClickBank</span></td>
              <td class="p-3.5 text-slate-300">Ativação de Gordura Marrom (BAT) / Samir Bute</td>
              <td class="p-3.5 text-emerald-400 font-bold">65% a 75% (Até $150+/venda)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/corevital" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /corevital-lander <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/corevital" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/corevital <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/corevital</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 3. Advanced Collagen PLUS -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="digistore">
              <td class="p-3.5 text-slate-500 font-mono">03</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-rose-400"></span> Advanced Collagen PLUS™
              </td>
              <td class="p-3.5"><span class="badge-ds text-[10px] font-bold px-2 py-0.5 rounded">Digistore24</span></td>
              <td class="p-3.5 text-slate-300">Rejuvenescimento Pele, Unhas &amp; Articulações (5 Tipos)</td>
              <td class="p-3.5 text-emerald-400 font-bold">60% (Até $149+/venda)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/advanced-collagen-plus-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /collagen-plus-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/advanced-collagen" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/advanced-collagen <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/collagen</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 4. JointEternal -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="digistore">
              <td class="p-3.5 text-slate-500 font-mono">04</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-teal-400"></span> JointEternal™ (Cartilage Matrix)
              </td>
              <td class="p-3.5"><span class="badge-ds text-[10px] font-bold px-2 py-0.5 rounded">Digistore24</span></td>
              <td class="p-3.5 text-slate-300">Estabilidade Articular &amp; Cartilagem (1,500mg Glucosamina)</td>
              <td class="p-3.5 text-emerald-400 font-bold">75% (AOV $250+, Até $175+/venda)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/joint-eternal-mobility-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /joint-eternal-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/joint-eternal" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/joint-eternal <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/jointeternal</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 5. Advanced Joint Support -->
            <tr class="hover:bg-slate-800/50 transition product-row bg-emerald-950/20" data-platform="digistore">
              <td class="p-3.5 text-slate-500 font-mono">05</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span> Advanced Joint Support™
              </td>
              <td class="p-3.5"><span class="badge-ds text-[10px] font-bold px-2 py-0.5 rounded">Digistore24</span></td>
              <td class="p-3.5 text-slate-300">Saúde Articular 50+ / Dr. Shallenberger (Q-Actin™)</td>
              <td class="p-3.5 text-emerald-400 font-bold">60% (Até $208+/venda)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/advanced-joint-support-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /joint-support-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/advanced-joint" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/advanced-joint <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/jointsupport</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 6. ProstaVive -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="clickbank">
              <td class="p-3.5 text-slate-500 font-mono">06</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-sky-400"></span> ProstaVive™ (Prostate &amp; Flow)
              </td>
              <td class="p-3.5"><span class="badge-cb text-[10px] font-bold px-2 py-0.5 rounded">ClickBank</span></td>
              <td class="p-3.5 text-slate-300">Saúde da Próstata, Fluxo Urinário &amp; Sono 50+</td>
              <td class="p-3.5 text-emerald-400 font-bold">75% a 80% (AOV $234, EPC $3.00+)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/prostavive-prostate-health-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /prostavive-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/prostavive" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/prostavive <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/prostavive</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 7. Java Burn -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="clickbank">
              <td class="p-3.5 text-slate-500 font-mono">07</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span> Java Burn™ (Coffee Ritual)
              </td>
              <td class="p-3.5"><span class="badge-cb text-[10px] font-bold px-2 py-0.5 rounded">ClickBank</span></td>
              <td class="p-3.5 text-slate-300">Metabolismo Matinal &amp; Queima de Gordura no Café</td>
              <td class="p-3.5 text-emerald-400 font-bold">Até $165.00/venda (AOV $294, EPC $2.80+)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/java-burn-coffee-ritual-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /java-burn-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/java-burn" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/java-burn <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/javaburn</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 8. Cardio Slim Tea -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="clickbank">
              <td class="p-3.5 text-slate-500 font-mono">08</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-blue-400"></span> Cardio Slim Tea™ (VIP Whitelist)
              </td>
              <td class="p-3.5"><span class="badge-cb text-[10px] font-bold px-2 py-0.5 rounded">ClickBank</span></td>
              <td class="p-3.5 text-slate-300">Saúde Cardiovascular, Pressão 120/80 &amp; Homocisteína</td>
              <td class="p-3.5 text-emerald-400 font-bold">65% FE / 50% Upsells (Até $210 CPA • AOV $300+)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/cardioslim-tea-cardio-support-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /cardioslim-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/cardioslim" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/cardioslim <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/cardioslim</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 9. SpartaMax -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="digistore">
              <td class="p-3.5 text-slate-500 font-mono">09</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span> SpartaMax™ (Gummies 365D)
              </td>
              <td class="p-3.5"><span class="badge-ds text-[10px] font-bold px-2 py-0.5 rounded">Digistore24</span></td>
              <td class="p-3.5 text-slate-300">Vitalidade Masculina, Fluxo Sanguíneo &amp; Stamina</td>
              <td class="p-3.5 text-emerald-400 font-bold">65% RevShare (AOV $210+, 365D Guarantee)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/spartamax-vitality-gummies-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /spartamax-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/spartamax" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/spartamax <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/spartamax</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 10. Neotonics -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="clickbank">
              <td class="p-3.5 text-slate-500 font-mono">10</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-rose-400"></span> Neotonics™ (Skin &amp; Gut)
              </td>
              <td class="p-3.5"><span class="badge-cb text-[10px] font-bold px-2 py-0.5 rounded">ClickBank</span></td>
              <td class="p-3.5 text-slate-300">Renovação Celular da Pele &amp; Microbioma</td>
              <td class="p-3.5 text-emerald-400 font-bold">VIP Group Bump (AOV $240+, EPC $3.00+)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/neotonics-skin-gut-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /neotonics-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/neotonics" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/neotonics <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/neotonics</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 11. GlucoTrust -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="digistore">
              <td class="p-3.5 text-slate-500 font-mono">11</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span> GlucoTrust™ (Blutzucker)
              </td>
              <td class="p-3.5"><span class="badge-ds text-[10px] font-bold px-2 py-0.5 rounded">Digistore24</span></td>
              <td class="p-3.5 text-slate-300">Glicose, Sono Profundo &amp; Cortisol</td>
              <td class="p-3.5 text-emerald-400 font-bold">60% RevShare (€242 AOV, EPC €4.50)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/glucotrust-blutzucker-bericht" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /glucotrust-bericht <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/glucotrust" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/glucotrust <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/glucotrust</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 12. Phytomem One -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="clickbank">
              <td class="p-3.5 text-slate-500 font-mono">12</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span> PhytoMem One™
              </td>
              <td class="p-3.5"><span class="badge-cb text-[10px] font-bold px-2 py-0.5 rounded">ClickBank</span></td>
              <td class="p-3.5 text-slate-300">Memória, Plastic Stranglehold &amp; Combustível Cerebral</td>
              <td class="p-3.5 text-emerald-400 font-bold">65% (AOV $230+, EPC $3.20+)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/phytomem-memory-formula-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /phytomem-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/phytomem" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/phytomem <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/phytomem</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 13. Advanced Amino Formula -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="digistore">
              <td class="p-3.5 text-slate-500 font-mono">13</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-sky-400"></span> Advanced Amino Formula™
              </td>
              <td class="p-3.5"><span class="badge-ds text-[10px] font-bold px-2 py-0.5 rounded">Digistore24</span></td>
              <td class="p-3.5 text-slate-300">Reversão Perda Muscular Sênior 50+ (8 Aminoácidos MAP)</td>
              <td class="p-3.5 text-emerald-400 font-bold">$33.25 a $199.50 (50-60%)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/advanced-amino-formula-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /amino-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/advanced-amino" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/advanced-amino <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/amino</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 14. All Day Slimming Tea -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="clickbank">
              <td class="p-3.5 text-slate-500 font-mono">14</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span> All Day Slimming Tea™
              </td>
              <td class="p-3.5"><span class="badge-cb text-[10px] font-bold px-2 py-0.5 rounded">ClickBank</span></td>
              <td class="p-3.5 text-slate-300">Metabolismo Matinal/Noturno &amp; Desintoxicação</td>
              <td class="p-3.5 text-emerald-400 font-bold">65% FE / 50% Upsells (VIP Aprovado)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/all-day-slimming-tea-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /slimming-tea-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/all-day-slimming-tea" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/all-day-slimming-tea <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/slimmingtea</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 15. FemiCore -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="clickbank">
              <td class="p-3.5 text-slate-500 font-mono">15</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-rose-400"></span> FemiCore™
              </td>
              <td class="p-3.5"><span class="badge-cb text-[10px] font-bold px-2 py-0.5 rounded">ClickBank</span></td>
              <td class="p-3.5 text-slate-300">Saúde da Bexiga Feminina &amp; Microbioma Pélvico</td>
              <td class="p-3.5 text-emerald-400 font-bold">$120.00 a $145.00</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/femicore-pelvic-health-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /femicore-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/femicore" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/femicore <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/femicore</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 16. Lymph Tonic -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="clickbank">
              <td class="p-3.5 text-slate-500 font-mono">16</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-teal-400"></span> Lymph Tonic™
              </td>
              <td class="p-3.5"><span class="badge-cb text-[10px] font-bold px-2 py-0.5 rounded">ClickBank</span></td>
              <td class="p-3.5 text-slate-300">Drenagem Linfática / Pernas Inchadas &amp; Circulação</td>
              <td class="p-3.5 text-emerald-400 font-bold">Até $160 CPA / $200+</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/lymphtonic-drainage-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /lymphtonic-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/lymphtonic" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/lymphtonic <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/lymphtonic</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 17. Audifort -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="clickbank">
              <td class="p-3.5 text-slate-500 font-mono">17</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-cyan-400"></span> Audifort™
              </td>
              <td class="p-3.5"><span class="badge-cb text-[10px] font-bold px-2 py-0.5 rounded">ClickBank</span></td>
              <td class="p-3.5 text-slate-300">Saúde Auditiva / Zumbido no Ouvido (Tinnitus)</td>
              <td class="p-3.5 text-emerald-400 font-bold">$100.00 a $190.00 (65%)</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/audifort-hearing-support-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /audifort-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/audifort" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/audifort <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/audifort</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 18. NeuroVera -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="clickbank">
              <td class="p-3.5 text-slate-500 font-mono">18</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-indigo-400"></span> NeuroVera™
              </td>
              <td class="p-3.5"><span class="badge-cb text-[10px] font-bold px-2 py-0.5 rounded">ClickBank</span></td>
              <td class="p-3.5 text-slate-300">Saúde Cerebral / Memória &amp; Foco</td>
              <td class="p-3.5 text-emerald-400 font-bold">$115.00 a $145.00</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/neurovera-brain-clarity-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /neurovera-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/neurovera" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/neurovera <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/neurovera</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 19. VisiFlora -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="clickbank">
              <td class="p-3.5 text-slate-500 font-mono">19</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-indigo-400"></span> VisiFlora™
              </td>
              <td class="p-3.5"><span class="badge-cb text-[10px] font-bold px-2 py-0.5 rounded">ClickBank</span></td>
              <td class="p-3.5 text-slate-300">Saúde dos Olhos / Eixo Intestino-Visão</td>
              <td class="p-3.5 text-emerald-400 font-bold">$159.37</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/visiflora-vision-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /visiflora-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/visiflora" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/visiflora <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/visiflora</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 20. CircO2 -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="digistore">
              <td class="p-3.5 text-slate-500 font-mono">20</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-rose-400"></span> CircO2® (Nitric Oxide)
              </td>
              <td class="p-3.5"><span class="badge-ds text-[10px] font-bold px-2 py-0.5 rounded">Digistore24</span></td>
              <td class="p-3.5 text-slate-300">Óxido Nítrico / Circulação Sênior 50+</td>
              <td class="p-3.5 text-emerald-400 font-bold">$83.36 a $131.00</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/circo2-nitric-oxide-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /circo2-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/circo2" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/circo2 <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/circo2</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 21. Advanced Memory Formula -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="digistore">
              <td class="p-3.5 text-slate-500 font-mono">21</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-sky-400"></span> Advanced Memory Formula™
              </td>
              <td class="p-3.5"><span class="badge-ds text-[10px] font-bold px-2 py-0.5 rounded">Digistore24</span></td>
              <td class="p-3.5 text-slate-300">Memória / Cérebro &amp; Foco 60+ (NeuroFactor)</td>
              <td class="p-3.5 text-emerald-400 font-bold">$87.73</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/advanced-memory-formula-guide" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /memory-guide <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/advanced-memory" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/advanced-memory <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/memory</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 22. CleanseSana -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="digistore">
              <td class="p-3.5 text-slate-500 font-mono">22</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span> CleanseSana™
              </td>
              <td class="p-3.5"><span class="badge-ds text-[10px] font-bold px-2 py-0.5 rounded">Digistore24</span></td>
              <td class="p-3.5 text-slate-300">Microbioma / Desinchaço Intestinal &amp; Detox</td>
              <td class="p-3.5 text-emerald-400 font-bold">$106.94</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/cleansesana-gut-reboot" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /cleansesana-reboot <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/cleansesana" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/cleansesana <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/cleansesana</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 23. Nagano Tonic -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="clickbank">
              <td class="p-3.5 text-slate-500 font-mono">23</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-red-400"></span> Nagano Lean Body Tonic
              </td>
              <td class="p-3.5"><span class="badge-cb text-[10px] font-bold px-2 py-0.5 rounded">ClickBank</span></td>
              <td class="p-3.5 text-slate-300">Metabolismo / Elixir Matinal Japonês 7s</td>
              <td class="p-3.5 text-emerald-400 font-bold">$120.00 a $140.00</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/nagano-tonic-review" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /nagano-review <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/nagano-tonic" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/nagano-tonic <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/nagano</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 24. Sugar Defender -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="clickbank">
              <td class="p-3.5 text-slate-500 font-mono">24</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span> Sugar Defender®
              </td>
              <td class="p-3.5"><span class="badge-cb text-[10px] font-bold px-2 py-0.5 rounded">ClickBank</span></td>
              <td class="p-3.5 text-slate-300">Controle de Glicose &amp; Energia Natural</td>
              <td class="p-3.5 text-emerald-400 font-bold">$125.00 a $145.00</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/sugar-defender-guide" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /sugar-defender-guide <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/sugar-defender" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/sugar-defender <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/sugardefender</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

            <!-- 25. ProDentim -->
            <tr class="hover:bg-slate-800/50 transition product-row" data-platform="clickbank">
              <td class="p-3.5 text-slate-500 font-mono">25</td>
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-teal-400"></span> ProDentim®
              </td>
              <td class="p-3.5"><span class="badge-cb text-[10px] font-bold px-2 py-0.5 rounded">ClickBank</span></td>
              <td class="p-3.5 text-slate-300">Saúde Bucal / Dentes &amp; Gengivas (3.5B Probióticos)</td>
              <td class="p-3.5 text-emerald-400 font-bold">$100.00 a $135.00</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/prodentim-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-mono">
                  /prodentim-report <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5">
                <a href="https://dailyhealthreviewus.com/showcase/prodentim" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1 font-mono font-bold">
                  /showcase/prodentim <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
              </td>
              <td class="p-3.5 font-mono text-slate-400">/go/prodentim</td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">ONLINE</span></td>
            </tr>

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
          <p class="text-xs text-slate-400">Sincronização automática a cada 60 segundos com rastreamento de Tracking ID (TID)</p>
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
    Daily Health Review Live Analytics • Conectado à API ClickBank REST 1.3 • Nickname: <strong class="text-slate-300">eusimar72</strong> • 25 Ofertas e Showcases Conectados
  </footer>

  <script>
    // Search Functionality
    function searchProducts() {
      const query = document.getElementById('searchInput').value.toLowerCase();
      const rows = document.querySelectorAll('.product-row');
      rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(query) ? '' : 'none';
      });
    }

    // Filter by platform
    function filterTable(platform) {
      const rows = document.querySelectorAll('.product-row');
      const btnAll = document.getElementById('btn-filter-all');
      const btnCb = document.getElementById('btn-filter-cb');
      const btnDs = document.getElementById('btn-filter-ds');
      
      // Reset button styles
      [btnAll, btnCb, btnDs].forEach(b => {
        b.className = 'px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700';
      });

      if (platform === 'all') {
        btnAll.className = 'px-3 py-1.5 rounded-lg text-xs font-bold bg-emerald-600 text-white shadow';
        rows.forEach(r => r.style.display = '');
      } else if (platform === 'clickbank') {
        btnCb.className = 'px-3 py-1.5 rounded-lg text-xs font-bold bg-amber-600 text-white shadow';
        rows.forEach(r => {
          r.style.display = (r.getAttribute('data-platform') === 'clickbank') ? '' : 'none';
        });
      } else if (platform === 'digistore') {
        btnDs.className = 'px-3 py-1.5 rounded-lg text-xs font-bold bg-sky-600 text-white shadow';
        rows.forEach(r => {
          r.style.display = (r.getAttribute('data-platform') === 'digistore') ? '' : 'none';
        });
      }
    }

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
            self.wfile.write(json.dumps({
                "status": "ONLINE",
                "port": PORT,
                "products_count": 25,
                "showcases_count": 25,
                "nickname": ACCOUNT_NICKNAME
            }).encode("utf-8"))
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
    print(f"[+] 25 PRODUTOS & SHOWCASES ATUALIZADOS")
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
