# 🧠 MEMÓRIA PERMANENTE DO PROJETO — CLAIRE EVANS & DAILY HEALTH REVIEW
> **DIRETRIZ DE CONTINUIDADE:** Este documento é a memória mestra do projeto. Toda sessão com o assistente deve respeitar rigorosamente as definições, histórico e padrões arquitetados aqui.

---

## 1. PERSONA OFICIAL: CLAIRE EVANS (@claire.matureskin)
* **Perfil:** 51 anos, mentora de saúde celular, beleza e longevidade para mulheres 40+. Pele madura radiante, corte bob loiro platinado na altura dos ombros, olhos avelã calorosos, sorriso autêntico.
* **Figurino Oficial Escolhido:** **Avental de Linho Terracota / Vinho Suave (Warm Terracotta & Wine Linen Apron)** sobre camiseta de algodão cru/off-white, colar fininho de corrente dourada e pequenas argolas douradas.
* **Voz Oficial:** Microsoft Neural `en-US-MichelleNeural` (ritmo acolhedor, amigável e maduro).

---

## 2. ARQUITETURA DO FUNIL DE CONVERSÃO ESCALÁVEL (REGRA DE OURO)
* **Destino do Tráfego:** A pessoa que assiste ao vídeo da Claire é levada **À RECEITA ESPECÍFICA CORRESPONDENTE** (ou ao Hub geral `/claire`):
  * **Hub Geral Vitrine:** 👉 `https://dailyhealthreviewus.com/claire` (Vitrine infinita com cards de todas as receitas + os 4 rituais diários fixos).
  * **Páginas Individuais por Receita:** Ex: 👉 `https://dailyhealthreviewus.com/claire/flourless-blueberry-cake`
* **Lógica do Funil Escalável (Infinitas Receitas):**
  1. A seguidora assiste ao vídeo e comenta a palavra-chave (ex: `CAKE`, `RECIPE`, `BREAD`).
  2. **Instagram/TikTok:** O robô envia via DM o link direto daquela receita específica (`/claire/nome-da-receita`).
  3. **Facebook Reels / YouTube Shorts:** O link da receita específica vai no **1º comentário fixado**.
  4. **Pinterest:** O link de destino do Pin aponta diretamente para a página da receita específica.
     * **PADRÃO ÚNICO E IMUTÁVEL DE VISUAL (TEMPLATE MESTRE OFICIAL):**
       * **REGRA ABSOLUTA:** Todas as receitas futuras usam rigorosamente o mesmo modelo mestre: `claire/TEMPLATE_MESTRE_RECEITA_CLAIRE.html`. **Apenas os textos da receita, imagens dos passos e o produto afiliado correspondente são alterados; todo o layout, CSS, proporções e código são idênticos.**
       * **Header:** Logo `CLAIRE'S RECIPES` + Raminho Botânico + Menu de Conversão (All Recipes, Skin Routine, Morning Coffee, About Claire).
       * **Google AdSense:** Tag oficial aprovada (`ca-pub-3922432751903141`) presente no `<head>` de todas as páginas de receitas para monetização passiva com alto RPM nos EUA.
       * **Split Hero Proporcional (7x5):**
         * **Coluna Esquerda (7 cols):** Título em Cormorant Garamond, avaliação 4.9 (5 estrelas), Avatar grande da Claire Evans (`51 & Glowing`, selo verificado, `@claire.matureskin`), barra com 4 métricas alinhadas (**Prep, Cook, Total Time, Yield**) e botão `Jump to Recipe`.
         * **Coluna Direita (5 cols):** Foto principal do prato pronto compactada e elegante (`max-w-[300px] sm:max-w-[330px]`, `w-full h-auto object-contain block`, `loading="eager" fetchpriority="high"`), casando 1:1 com a altura do texto sem empurrar a página.
       * **Cartão de Ingredientes:** Stepper interativo de porções `[-] 6 [+]` que recalcula dinamicamente tanto as medidas americanas (cups/tbsp) quanto as métricas internacionais (gramas e ml), com checkboxes interativas.
       * **Passo a Passo (5 Etapas):** Todas as 5 fotos exibidas 100% inteiras e completas (`object-contain`), sem cortes de cabeças ou mãos.
       * **Callout Box do Produto Afiliado (Pós-Receita):** Posicionado após o passo a passo com design editorial elegante (*"Claire's Daily Wellness Pairing"*), selo de confiança e **aviso legal de transparência FTC (Affiliate Disclosure)** obrigatório:
         * Receitas Anti-Aging / Colágeno / Pele ➔ **Neotonics** (`/go/neotonics`)
         * Receitas Intestinais / Desinchaço ➔ **CleanseSana** (`/go/cleansesana`)
         * Receitas Matinais / Café / Termogênicas ➔ **Java Burn** (`/go/javaburn`)
         * Receitas / Dicas de Sorriso e Boca ➔ **ProDentim** (`/go/prodentim`)

---

## 3. ROBÔ DE AUTOMAÇÃO (INSTAGRAM & TIKTOK)
* **Localização no Computador:**  
  📁 `C:\Users\Eusimar\Documents\Claire Evans Instagram\Automacao_Robo`
* **Executável:** `INICIAR_ROBO.bat`
* **Script Principal:** `claire_bot.py` (desenvolvido em Python + Playwright).
* **Configuração e Mensagens:** `config.json`
* **Como Opera:**
  * Monitora notificações e comentários no Instagram (`@claire.matureskin`) e no TikTok.
  * Quando detecta palavras como `recipe`, `receita`, `bread`, `buns`, `pao`, `secret`, `ingredients`, `how`:
  * Envia automaticamente a receita formatada de 4 ingredientes dos pães de abacate + link do hub da Claire:
    `👉 https://dailyhealthreviewus.com/claire 💖 - Claire`

---

## 4. DIRETRIZES DE SEO E PUBLICAÇÃO POR REDE SOCIAL
* **Instagram (Reels):** Apenas campo de **Legenda** (não tem título). Gancho forte na primeira linha. Link na Bio. Capa **100% limpa, sem textos sobre o rosto da Claire** (`CAPA_01_CLAIRE_ORGANICA_CLEAN_9x16.jpg`).
* **TikTok:** Legenda concisa com palavras-chave estratégicas embutidas para o buscador do TikTok.
* **YouTube Shorts:** Título atrativo (< 100 caracteres com `#Shorts`). Descrição completa com link para `https://dailyhealthreviewus.com/claire`. Primeiro comentário fixado com o link.
* **Facebook Reels:** **NÃO colocar links externos na legenda do post** (para evitar penalização no alcance orgânico pelo algoritmo da Meta). O link é colocado exclusivamente no **Primeiro Comentário Fixado**.
* **Pinterest:** Título do Pin (< 100 caracteres), Descrição rica em palavras-chave com hashtags ao final, Pasta sugerida (`Healthy Gut & Anti-Inflammatory Recipes`), Link de Destino apontando para `https://dailyhealthreviewus.com/claire`, e Capa na proporção oficial 2:3 (`CAPA_04_PINTEREST_EDITORIAL_2x3.jpg`).

---

## 5. HISTÓRICO DE PRODUÇÃO DE VÍDEOS DA CLAIRE
1. **Vídeo 01:** Sorvete de Chocolate Anti-Aging (Banana congelada, cacau 100%, leite de amêndoa).
2. **Vídeo 02:** Smoothie Verde Celular Turnover (Couve, pepino, maçã verde, limão, renovação dérmica).
3. **Vídeo 03 (Atual):** Claire's 4-Ingredient Flourless Avocado & Potato Buns:
   * **Arquivo Mestre (Sem Silêncios & Com Legendas):**  
     `C:\Users\Eusimar\Downloads\Claire_Video_Cenas_32s\Claire_Flourless_Avocado_Potato_Buns_Gut_Health_Recipe_9x16.mp4` (34,3s | 720×1280 9:16).
   * **Edição de Áudio:** Cortados mais de 3,2 segundos de pausas mortas entre as cenas 1 e 2.
   * **Legendas:** Estilo Badge branco arredondado centralizado com fonte Segoe UI Bold preta em todas as 4 cenas.

---

## 6. CREDENCIAIS E LINKS PRINCIPAIS DO ECOSSISTEMA
* **Domínio Oficial:** `https://dailyhealthreviewus.com` (Hospedado na Vercel).
* **ID Afiliado Digistore24:** `eusimar72`
* **Página Hub da Claire:** `https://dailyhealthreviewus.com/claire`
* **E-mail de Notificações / Suporte:** `eusimar72@gmail.com`

---

## 7. CANAIS DE LOUVOR E ADORAÇÃO — GLÓRIA EM LOUVORES & ECOS DAS ORAÇÕES (PADRÃO OFICIAL)
> **DIRETRIZ OFICIAL:** Todo vídeo dos canais **Glória em Louvores** e **Ecos das Orações** deve seguir rigorosamente os parâmetros de áudio, renderização cinematográfica, atmosfera celestial e SEO estruturados.

* **Diretórios Mestres dos Projetos:**
  * **Glória em Louvores:** `C:\Users\Eusimar\Downloads\NOVOS LOUVORES GLORIA EM LOUVORES\VIDEO 1`
  * **Ecos das Orações:** `C:\Users\Eusimar\Downloads\NOVOS LOUVORES GLORIA EM LOUVORES\VIDEO 2 - CANAL ECOS DAS ORAÇÕES`
* **Especificações Técnicas de Vídeo:** 1920×1080 (16:9), 30 FPS, ~8 Mbps, AAC Estéreo 48kHz @ 320 kbps. Legendas em Georgia Bold 54-56pt branco-pérola sem fundo.

---

## 8. PARCERIA VIP COREVITAL BURN & CRONOGRAMA OFICIAL DO PINTEREST (REGRA PERMANENTE)
> **DIRETRIZ DE CONTINUIDADE OBRIGATÓRIA:** Esta regra é permanente e o assistente **DEVE SEMPRE LEMBRAR O USUÁRIO** com antecedência sobre o cronograma de postagens.

* **Parceiro Homologado:** Core Vital Nutraceuticals LLC (Dr. Samir Bute, MD & Ozzie Bute).
* **ClickBank Nickname:** `eusimar72` (confirmado no Commission Group VIP com **35% de comissão** por venda).
* **Oferta Oficial:** Item `BURN119` ($119.95 por 3 frascos, frete grátis nos EUA, compra única sem assinatura, garantia de 60 dias ClickBank).
* **Link Bridge:** `https://dailyhealthreviewus.com/go/corevital` (Redirecionamento 302 direto para o HopLink verificado no ClickBank).
* **Artigo Homologado:** `https://dailyhealthreviewus.com/staging/corevital-burn` (100% aprovado pela CoreVital, com dosagens exatas de 500mg Berberine HCl, 200mg Milk Thistle, 200mg Ceylon Cinnamon, 150mg Black Cumin, 100mg Ginger Root, e aviso de medicação).
* **CRONOGRAMA OFICIAL DE PUBLICAÇÃO DO PINTEREST:**
  * **Frequência Rigorosa:** **3 Pins por semana — TODA SEGUNDA, QUARTA E SEXTA-FEIRA**.
  * **Compromisso do Assistente:** O assistente **NUNCA DEVE ESQUECER** esta cadência e deve ativamente lembrar o usuário nas Segundas, Quartas e Sextas sobre a publicação do novo Pin.
* **DIRETRIZES DE CONFORMIDADE DOS PINS (REGRAS DE OURO FTC & SAMIR BUTE):**
  1. **Aviso de Afiliado Obrigatório na 1ª Linha:** A legenda deve **SEMPRE COMEÇAR** com o aviso de comissão antes de qualquer outro texto para ficar visível antes do botão "... more":
     *Padrão Oficial:* `I may earn a commission if you purchase through my link. An independent label overview from Daily Health Review. CoreVital Burn is a physician-co-founded dietary supplement with five disclosed botanical ingredients. The standard three-bottle offer is $119.95 before applicable tax, with free U.S. shipping, one-time billing and ClickBank’s 60-day return policy. Read the directions and warnings before use. #ad #affiliate #DailyHealthReview #CoreVitalBurn`
  2. **Imagem do Pin Estritamente Oficial (Sem Modificações de IA):**
     * Proibido usar artes geradas por IA que recebam o selo *"AI modified"* ou que alterem o frasco.
     * Usar exclusivamente a foto oficial limpa do frasco em fundo estúdio (`CoreVital_Burn_Official_Pin_2x3.jpg` ou `burn-one-bottle.png`), mantendo o rótulo original intacto.
     * Proibido adicionar termos não autorizados como "Clinical Heritage" ou alegações metabólicas não comprovadas.
  3. **Link de Destino:** Sempre apontar diretamente para `https://dailyhealthreviewus.com/staging/corevital-burn`.

