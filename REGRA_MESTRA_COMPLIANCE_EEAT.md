# ⚖️ REGRA MESTRA DE COMPLIANCE, FTC, FDA & E-E-A-T (DIRETRIZ PERMANENTE DO PROJETO)
> **STATUS:** LEI INEGOCIÁVEL DO PROJETO DAILY HEALTH REVIEW. NENHUMA PÁGINA, CÓDIGO OU ARTIGO PODE VIOLAR AS DIRETRIZES ABAIXO.

---

## 1. COMPLIANCE COM A FDA (FOOD & DRUG ADMINISTRATION)
* **Estrutura/Função vs Alegações de Cura (Regra de Ouro):**
  * Suplementos alimentares nos EUA operam sob o *Dietary Supplement Health and Education Act (DSHEA)*.
  * **PROIBIÇÃO ABSOLUTA:** Jamais afirmar que qualquer suplemento ou ingrediente cura, trata, previne, reverte ou diagnostica doenças (ex: "cures neuropathy", "reverses diabetes", "melts visceral fat", "restores destroyed cartilage", "cures tinnitus").
  * **LINGUAGEM PERMITIDA (Structure/Function):**
    * *"Supports healthy resting metabolic rate"*
    * *"Promotes normal cartilage elasticity and joint comfort"*
    * *"Formulated with botanicals shown to soothe peripheral nerve sensations"*
    * *"Helps maintain healthy gut microbiota and intestinal motility"*
* **Disclaimers Médicos:**
  * O disclaimer da FDA no rodapé é obrigatório, mas **não autoriza promessas de cura no corpo do texto**. A mensagem principal da página deve ser sóbria e equilibrada.

---

## 2. COMPLIANCE COM A FTC (FEDERAL TRADE COMMISSION)
* **Aviso de Afiliado Antes do Primeiro CTA (Above The Fold):**
  * Todo artigo, review editorial ou showcase comercial DEVE exibir o banner de transparência de afiliado FTC logo abaixo do cabeçalho, **antes do primeiro botão de compra**.
  * Texto padrão:  
    `Reader Transparency Disclosure: Daily Health Review provides independent evaluations supported by research. When you buy through our links, we may earn an affiliate commission at zero additional cost to you.`
* **Proibição de Provas Sociais e Estatísticas Falsas:**
  * PROIBIDO inventar contadores de pedidos que não possuam auditoria pública (ex: "2,410+ Verified Orders", "over 85% of customers select 6-bottle").
  * PROIBIDO usar porcentagens milagrosas sem ensaio clínico humano citado (ex: "reduces pain by 70%", "214% superior to glucosamine").
  * **O que usar no lugar:** Destacar a política oficial de garantia incondicional do fabricante (ex: "Backed by 60-day 100% money-back guarantee") e dados botânicos referenciados.

---

## 3. PADRONIZAÇÃO DE LINKS LEGAIS & ZERO 404
* **Rotas Canônicas Oficiais:**
  * Política de Privacidade: `/privacy/`
  * Termos de Serviço: `/terms/`
  * Aviso de Afiliados: `/disclosure/`
  * Disclaimer da FDA: `/disclaimer/`
  * Contato & Suporte: `/contact/`
* **Regra de Redirecionamento (Zero Links Mortos):**
  * Toda variação digitada por usuários, robôs ou auditores (`/privacy-policy`, `/privacy-policy/`, `/privacy-policy.html`, `/terms-of-service/`, etc.) DEVE estar mapeada com 301 permanente no `_redirects` com e sem barra final.
* **Proibição de Links para `/staging/`:**
  * Nenhuma página pública, receita da Claire ou artigo editorial pode conter links internos apontando para URLs com o prefixo `/staging/`.

---

## 4. DIRETRIZES DE E-E-A-T (EXPERIÊNCIA, EXPERTISE, AUTORIDADE E CONFIANÇA DO GOOGLE)
* **Transparência em Receitas e Guias:**
  * Ao recomendar compostos minerais (ex: magnésio glicinato), sempre explicitar a dose do mineral elementar correspondente (ex: ~200mg magnésio elementar) e adicionar aviso sobre medicamentos e condições renais.
  * Nunca prometer indução fisiológica imediata não comprovada (ex: trocar "deep REM sleep in 30 seconds" por "a relaxing 30-second bedtime elixir for restorative sleep").
* **Abordagem de Defensor do Consumidor (Consumer Advocate):**
  * O leitor maduro compra quando sente verdade. Toda avaliação deve conter pontos fortes E limitações/para quem o produto NÃO é indicado, eliminando a sensação de "landing page forçada de afiliado".
