import os
import sys
import json
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import threading

API_KEY = "API-C6JT52HMN2YWGH0YK3IFCI8O3D37X5O4VLTV"
ACCOUNT_NICKNAME = "eusimar72"
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
  <title>Daily Health Review | ClickBank Live Sales Dashboard</title>
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
            ClickBank Live Sales Dashboard
            <span class="text-[11px] font-bold uppercase tracking-wider bg-emerald-950 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded-full flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-emerald-400 live-dot"></span> API ONLINE
            </span>
          </h1>
          <p class="text-xs text-slate-400">Conta: <span class="text-amber-400 font-bold">eusimar72</span> • Portal: <span class="text-slate-300 font-mono">dailyhealthreview.vercel.app</span></p>
        </div>
      </div>
      
      <div class="flex items-center gap-3">
        <button onclick="refreshData()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-lg shadow transition flex items-center gap-2">
          <i class="fa-solid fa-arrows-rotate" id="refresh-icon"></i> Atualizar Agora
        </button>
        <a href="https://dailyhealthreview.vercel.app" target="_blank" class="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg border border-slate-700 flex items-center gap-1.5">
          <i class="fa-solid fa-arrow-up-right-from-square"></i> Ver Blog
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
          <i class="fa-solid fa-circle-check"></i> Saldo direto na ClickBank
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
          <i class="fa-solid fa-chart-line"></i> Pedidos registrados na API
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
        <div class="text-3xl font-black text-white">3 Ativos</div>
        <div class="text-xs text-cyan-200/80 mt-2 flex items-center gap-1">
          <i class="fa-solid fa-bolt"></i> Nagano, ProDentim, Sugar Def.
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
        <div class="text-3xl font-black text-white">~$130.00</div>
        <div class="text-xs text-purple-200/80 mt-2 flex items-center gap-1">
          <i class="fa-solid fa-shield-halved"></i> 75% a 85% de comissão
        </div>
      </div>

    </div>

    <!-- Active Campaigns / Product Links Table -->
    <div class="card-glow rounded-2xl p-6 shadow-xl border border-slate-800">
      <div class="flex items-center justify-between mb-5">
        <div>
          <h2 class="text-base font-bold text-white flex items-center gap-2">
            <i class="fa-solid fa-link text-emerald-400"></i> Produtos Conectados no Blog & HopLinks
          </h2>
          <p class="text-xs text-slate-400">Monitorando conversões e tráfego orgânico do Pinterest e Google</p>
        </div>
        <span class="text-xs text-slate-400 bg-slate-800/80 px-3 py-1 rounded-full border border-slate-700">3 Links Monitorados</span>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead class="bg-slate-900/80 text-slate-300 uppercase font-bold text-[11px] border-b border-slate-800">
            <tr>
              <th class="p-3.5">Produto ClickBank</th>
              <th class="p-3.5">Nicho / Categoria</th>
              <th class="p-3.5">Comissão Média</th>
              <th class="p-3.5">Página no seu Blog (Vercel)</th>
              <th class="p-3.5">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800/60 font-medium">
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span> Nagano Lean Body Tonic
              </td>
              <td class="p-3.5 text-slate-300">Metabolismo / 7s Elixir</td>
              <td class="p-3.5 text-emerald-400 font-bold">$120.00 a $140.00</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreview.vercel.app/nagano-tonic-review" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /nagano-tonic-review <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-teal-400"></span> ProDentim®
              </td>
              <td class="p-3.5 text-slate-300">Saúde Bucal / Dentes & Gengivas</td>
              <td class="p-3.5 text-emerald-400 font-bold">$100.00 a $135.00</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreview.vercel.app/prodentim-report" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /prodentim-report <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
            </tr>

            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-3.5 font-bold text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span> Sugar Defender®
              </td>
              <td class="p-3.5 text-slate-300">Controle de Glicose & Energia</td>
              <td class="p-3.5 text-emerald-400 font-bold">$125.00 a $145.00</td>
              <td class="p-3.5">
                <a href="https://dailyhealthreview.vercel.app/sugar-defender-guide" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1">
                  /sugar-defender-guide <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
              </td>
              <td class="p-3.5"><span class="bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded">PUBLICADO</span></td>
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
            Assim que um leitor clicar em qualquer um dos seus Pins no Pinterest ou no Blog e finalizar a compra na ClickBank, a transação, valor da comissão e Tracking ID (TID) aparecerão aqui instantaneamente!
          </p>
        </div>
      </div>
    </div>

  </main>

  <!-- Footer -->
  <footer class="card-glow border-t border-slate-800 py-6 text-center text-xs text-slate-500 mt-auto">
    <p>© 2026 Daily Health Review Dashboard • Monitoramento Integrado ClickBank REST API v1.3</p>
  </footer>

  <script>
    async function refreshData() {
      const icon = document.getElementById('refresh-icon');
      icon.classList.add('fa-spin');
      
      try {
        const resp = await fetch('/api/stats');
        const data = await resp.json();
        
        document.getElementById('total-commissions').innerText = '$' + (data.total_amount || 0).toFixed(2);
        document.getElementById('total-sales').innerText = data.total_count || 0;
        
        const now = new Date();
        document.getElementById('last-update').innerText = 'Última checagem: ' + now.toLocaleTimeString();
        
        if (data.orders && data.orders.length > 0) {
          let html = '<div class="overflow-x-auto"><table class="w-full text-left text-xs">';
          html += '<thead class="bg-slate-900 text-slate-300 font-bold uppercase text-[11px]"><tr><th class="p-3">Data</th><th class="p-3">ID Pedido</th><th class="p-3">Produto</th><th class="p-3">Comissão</th><th class="p-3">Tracking ID (TID)</th></tr></thead><tbody class="divide-y divide-slate-800">';
          data.orders.forEach(o => {
            html += `<tr class="hover:bg-slate-800/50"><td class="p-3">${o.transactionTime || '-'}</td><td class="p-3 font-mono text-amber-400">${o.receipt || '-'}</td><td class="p-3 font-bold text-white">${o.itemTitle || '-'}</td><td class="p-3 font-bold text-emerald-400">$${o.affiliateCommission || '0.00'}</td><td class="p-3 font-mono text-cyan-400">${o.trackingId || '-'}</td></tr>`;
          });
          html += '</tbody></table></div>';
          document.getElementById('orders-container').innerHTML = html;
        }
      } catch (err) {
        console.error('Erro ao buscar dados:', err);
      } finally {
        setTimeout(() => icon.classList.remove('fa-spin'), 600);
      }
    }

    // Auto-refresh every 60 seconds
    setInterval(refreshData, 60000);
    // Initial fetch
    refreshData();
  </script>
</body>
</html>
"""

class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
        elif self.path == "/api/stats":
            data = fetch_clickbank_orders()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
        else:
            super().do_GET()

def start_server():
    server = HTTPServer(("localhost", PORT), DashboardHandler)
    print(f"Server started at http://localhost:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    time.sleep(1)
    url = f"http://localhost:{PORT}"
    print(f"Abrindo Dashboard no navegador: {url}")
    webbrowser.open(url)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Encerrando Dashboard.")
