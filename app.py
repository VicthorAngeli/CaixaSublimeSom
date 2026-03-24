"""
Caixa Sublime Som — Relatório Financeiro Simplificado
Para liderança da igreja · Janeiro a Março 2026
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

from data import (
    get_transacoes,
    get_resumo_mensal,
    get_kpis,
    get_saidas_por_categoria,
    get_entradas_por_categoria,
    get_top_despesas,
    MESES_ORDEM,
)

st.set_page_config(
    page_title="Caixa Sublime Som",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Dados ──
df = get_transacoes()
resumo = get_resumo_mensal()
kpis = get_kpis()
saidas_cat = get_saidas_por_categoria()
entradas_cat = get_entradas_por_categoria()
top_desp = get_top_despesas(5)

VERDE = "#0D9F6E"
VERMELHO = "#E02D3C"
AZUL = "#1E40AF"
LARANJA = "#D97706"
CORES = ["#0D9F6E", "#3B82F6", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899"]


def R(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ── CSS ──
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
* { font-family: 'Inter', sans-serif !important; }
.stApp { background: #F8FAFC; }
.block-container { max-width: 1000px !important; padding-top: 1.5rem !important; }

.header {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
    padding: 2.5rem 2rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.header h1 { font-size: 2rem; font-weight: 800; margin: 0; }
.header p { opacity: 0.8; margin: 0.5rem 0 0; font-size: 1rem; }

.card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    border: 1px solid rgba(0,0,0,0.05);
    margin-bottom: 1rem;
}

.big-number {
    font-size: 2rem;
    font-weight: 800;
    margin: 0.3rem 0;
}

.explain {
    background: #F0F9FF;
    border-left: 4px solid #3B82F6;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    font-size: 0.92rem;
    line-height: 1.7;
    color: #334155;
}
.explain b { color: #1e293b; }

.alerta-vermelho {
    background: #FEF2F2;
    border-left: 4px solid #E02D3C;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    font-size: 0.92rem;
    line-height: 1.7;
}

.alerta-verde {
    background: #F0FDF4;
    border-left: 4px solid #0D9F6E;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    font-size: 0.92rem;
    line-height: 1.7;
}

.alerta-amarelo {
    background: #FFFBEB;
    border-left: 4px solid #D97706;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    font-size: 0.92rem;
    line-height: 1.7;
}

.titulo-secao {
    font-size: 1.3rem;
    font-weight: 700;
    color: #1e293b;
    margin: 2rem 0 0.8rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #e2e8f0;
}

.sugestao {
    background: white;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
    border-left: 4px solid #0D9F6E;
    box-shadow: 0 1px 6px rgba(0,0,0,0.04);
}
.sugestao h4 { margin: 0 0 0.4rem; color: #1e293b; font-size: 1rem; }
.sugestao p { margin: 0; color: #475569; font-size: 0.9rem; line-height: 1.6; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

PLOTLY = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#1e293b", size=13),
    margin=dict(t=30, b=30, l=50, r=30),
    hoverlabel=dict(bgcolor="white", font_size=13),
)


# ══════════════════════════════════════════════
# CABEÇALHO
# ══════════════════════════════════════════════

st.markdown("""
<div class="header">
    <h1>🎵 Caixa Sublime Som</h1>
    <p>Relatório Financeiro · Janeiro a Março de 2026</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# 1. RESUMO RÁPIDO — "Quanto temos no caixa?"
# ══════════════════════════════════════════════

st.markdown('<div class="titulo-secao">💰 Resumo Rápido</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explain">
    💡 <b>O que é isso?</b> — É a foto do nosso dinheiro. Mostra quanto entrou,
    quanto saiu e quanto sobrou no caixa de janeiro a março.
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="card" style="text-align:center; border-top: 4px solid {VERDE};">
        <div style="font-size:0.85rem; color:#64748b;">📥 Entrou no caixa</div>
        <div class="big-number" style="color:{VERDE};">{R(kpis["total_entradas"])}</div>
        <div style="font-size:0.85rem; color:#94a3b8;">Tudo que recebemos em 3 meses</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card" style="text-align:center; border-top: 4px solid {VERMELHO};">
        <div style="font-size:0.85rem; color:#64748b;">📤 Saiu do caixa</div>
        <div class="big-number" style="color:{VERMELHO};">{R(kpis["total_saidas"])}</div>
        <div style="font-size:0.85rem; color:#94a3b8;">Tudo que gastamos em 3 meses</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card" style="text-align:center; border-top: 4px solid {AZUL};">
        <div style="font-size:0.85rem; color:#64748b;">🏦 Sobrou (saldo atual)</div>
        <div class="big-number" style="color:{AZUL};">{R(kpis["saldo_atual"])}</div>
        <div style="font-size:0.85rem; color:#94a3b8;">Dinheiro disponível hoje</div>
    </div>
    """, unsafe_allow_html=True)

if kpis["resultado_liquido"] >= 0:
    st.markdown(f"""
    <div class="alerta-verde">
        ✅ <b>Boa notícia!</b> Entrou mais dinheiro do que saiu.
        Sobraram <b>{R(kpis["resultado_liquido"])}</b> nesses 3 meses.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="alerta-vermelho">
        ⚠️ <b>Atenção!</b> Gastamos mais do que recebemos.
        Faltaram <b>{R(abs(kpis["resultado_liquido"]))}</b> nesses 3 meses.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# 2. MÊS A MÊS — "Como foi cada mês?"
# ══════════════════════════════════════════════

st.markdown('<div class="titulo-secao">📅 Como foi cada mês?</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explain">
    💡 <b>O que é isso?</b> — Comparação do que entrou e saiu em cada mês.
    As barras <span style="color:#0D9F6E"><b>verdes</b></span> são entradas
    e as <span style="color:#E02D3C"><b>vermelhas</b></span> são saídas.
    Se a verde é maior, o mês foi positivo!
</div>
""", unsafe_allow_html=True)

fig = go.Figure()
fig.add_trace(go.Bar(
    x=resumo["mes_label"], y=resumo["total_entradas"],
    name="💰 Entrou",
    marker=dict(color=VERDE, cornerradius=6),
    text=[R(v) for v in resumo["total_entradas"]],
    textposition="outside",
    textfont=dict(size=13, color=VERDE, weight="bold"),
))
fig.add_trace(go.Bar(
    x=resumo["mes_label"], y=resumo["total_saidas"],
    name="💸 Saiu",
    marker=dict(color=VERMELHO, cornerradius=6),
    text=[R(v) for v in resumo["total_saidas"]],
    textposition="outside",
    textfont=dict(size=13, color=VERMELHO, weight="bold"),
))
fig.update_layout(
    **PLOTLY, barmode="group", height=400, bargap=0.3,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=14)),
)
st.plotly_chart(fig, width='stretch')

# Explicação por mês
c_jan, c_fev, c_mar = st.columns(3)

with c_jan:
    st.markdown(f"""
    <div class="card">
        <h3 style="text-align:center; margin:0 0 0.8rem;">🟢 Janeiro</h3>
        <div style="font-size:0.9rem; color:#475569; line-height:1.8;">
            Entrou: <b style="color:{VERDE}">{R(1560.32)}</b><br>
            Saiu: <b style="color:{VERMELHO}">{R(307.15)}</b><br>
            Sobrou: <b style="color:{VERDE}">{R(1253.17)}</b><br><br>
            📌 <em>Mês forte! O sorteio de R$ 1.410 ajudou muito.</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c_fev:
    st.markdown(f"""
    <div class="card">
        <h3 style="text-align:center; margin:0 0 0.8rem;">🔴 Fevereiro</h3>
        <div style="font-size:0.9rem; color:#475569; line-height:1.8;">
            Entrou: <b style="color:{VERDE}">{R(155.00)}</b><br>
            Saiu: <b style="color:{VERMELHO}">{R(550.00)}</b><br>
            Faltou: <b style="color:{VERMELHO}">{R(395.00)}</b><br><br>
            📌 <em>Mês difícil. Não teve evento e teve gasto grande (R$ 500).</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c_mar:
    st.markdown(f"""
    <div class="card">
        <h3 style="text-align:center; margin:0 0 0.8rem;">🟡 Março</h3>
        <div style="font-size:0.9rem; color:#475569; line-height:1.8;">
            Entrou: <b style="color:{VERDE}">{R(1230.34)}</b><br>
            Saiu: <b style="color:{VERMELHO}">{R(954.66)}</b><br>
            Sobrou: <b style="color:{VERDE}">{R(275.68)}</b><br><br>
            📌 <em>Recuperou com Lava Car + Sorteio, mas teve bastante gasto também.</em>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# 3. COM QUE GASTAMOS? — "Pra onde foi o dinheiro?"
# ══════════════════════════════════════════════

st.markdown('<div class="titulo-secao">📊 Pra onde foi o dinheiro?</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explain">
    💡 <b>O que é isso?</b> — Mostra em quais tipos de gasto o dinheiro foi usado.
    O gráfico de pizza mostra a proporção de cada categoria.
</div>
""", unsafe_allow_html=True)

col_pizza, col_lista = st.columns([1, 1])

with col_pizza:
    fig_cat = go.Figure(data=[go.Pie(
        labels=saidas_cat["categoria"], values=saidas_cat["total"],
        hole=0.55,
        marker=dict(colors=CORES, line=dict(color="white", width=3)),
        textinfo="percent",
        textposition="outside",
        textfont=dict(size=13, weight="bold"),
    )])
    fig_cat.update_layout(
        **{**PLOTLY, "margin": dict(t=10, b=10, l=10, r=10)},
        showlegend=False, height=350,
        annotations=[dict(
            text=f"<b>{R(kpis['total_saidas'])}</b><br><span style='font-size:11px;color:#94a3b8'>Total gasto</span>",
            x=0.5, y=0.5, font_size=14, showarrow=False,
        )],
    )
    st.plotly_chart(fig_cat, width='stretch')

with col_lista:
    st.markdown("<div style='padding-top:0.5rem'></div>", unsafe_allow_html=True)
    for i, (_, row) in enumerate(saidas_cat.iterrows()):
        cor = CORES[i % len(CORES)]
        pct = row['percentual']
        st.markdown(
            f"<span style='color:{cor}; font-size:1.5rem; vertical-align:middle;'>●</span> "
            f"**{row['categoria']}** — {R(row['total'])} ({pct:.0f}%)",
            unsafe_allow_html=True,
        )

st.markdown("""
<div class="explain">
    💡 <b>Traduzindo:</b> A maior parte do dinheiro foi para <b>empréstimos/adiantamentos</b> (pessoas que
    precisaram de dinheiro) e para <b>custos de eventos</b> (material, lembrancinhas, etc).
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# 4. MAIORES GASTOS — "Quais foram os gastos mais altos?"
# ══════════════════════════════════════════════

st.markdown('<div class="titulo-secao">💸 Os 5 maiores gastos</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explain">
    💡 <b>O que é isso?</b> — Lista dos gastos mais caros do trimestre,
    do maior pro menor. Ajuda a entender onde o dinheiro pesou mais.
</div>
""", unsafe_allow_html=True)

for i, (_, row) in enumerate(top_desp.iterrows(), 1):
    cor = VERMELHO if row['saida'] >= 200 else LARANJA
    st.markdown(f"""
    <div class="card" style="border-left: 4px solid {cor}; padding: 1rem 1.2rem; margin-bottom:0.6rem;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-weight:700; color:#1e293b;">#{i} {row['descricao']}</span>
                <span style="color:#94a3b8; font-size:0.85rem;"> — {row['mes']}</span>
            </div>
            <div style="font-weight:800; font-size:1.1rem; color:{cor};">{R(row['saida'])}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# 5. PONTOS DE ATENÇÃO — "O que a liderança precisa saber?"
# ══════════════════════════════════════════════

st.markdown('<div class="titulo-secao">🚨 Pontos de Atenção</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explain">
    💡 <b>O que é isso?</b> — São os pontos mais importantes que a liderança
    precisa acompanhar. Os vermelhos são urgentes, os amarelos precisam de atenção.
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="alerta-vermelho">
    🔴 <b>Dinheiro emprestado que não voltou</b><br>
    O David recebeu <b>{R(320)}</b> em março para o simpósio.
    Esse dinheiro <b>ainda não voltou</b> pro caixa.
    Precisamos combinar uma data pra devolução.
</div>

<div class="alerta-vermelho">
    🔴 <b>Sem evento = caixa no vermelho</b><br>
    Em fevereiro, não tivemos evento de arrecadação.
    Resultado: gastamos <b>{R(395)}</b> a mais do que recebemos.
    <b>Quando não tem evento, o caixa entra no negativo.</b>
</div>

<div class="alerta-amarelo">
    🟡 <b>Gasto grande sem registro claro</b><br>
    "Joum David" — {R(500)} — foi o maior gasto do trimestre.
    Não fica claro o que foi. Precisamos sempre anotar
    <b>pra quem</b> foi e <b>pra que</b> foi o dinheiro.
</div>

<div class="alerta-amarelo">
    🟡 <b>Quase todo dinheiro vem de eventos</b><br>
    De tudo que entrou, <b>80%</b> veio de sorteios e lava car.
    As ofertas de ensaio (que entram todo mês) representam só <b>20%</b>.
    Se um mês não tiver evento, a conta não fecha.
</div>

<div class="alerta-verde">
    🟢 <b>No geral, estamos no positivo!</b><br>
    Mesmo com o mês ruim de fevereiro, fechamos o trimestre com
    <b>{R(kpis["resultado_liquido"])}</b> de sobra. O caixa hoje tem <b>{R(kpis["saldo_atual"])}</b>.
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# 6. SUGESTÕES — "O que podemos fazer?"
# ══════════════════════════════════════════════

st.markdown('<div class="titulo-secao">💡 Sugestões para a Liderança</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explain">
    💡 <b>O que é isso?</b> — Ideias práticas baseadas nos números,
    pra ajudar o grupo a cuidar melhor do dinheiro.
</div>
""", unsafe_allow_html=True)

sugestoes = [
    ("📅 Fazer pelo menos 1 evento por mês",
     "Meses com evento = dinheiro sobrando. Meses sem evento = caixa negativo. "
     "Pode ser sorteio, rifa, lava car, bazar... o importante é ter todo mês."),
    ("📝 Anotar tudo direitinho",
     "Sempre escrever: quem recebeu o dinheiro, pra que foi, e quando vai devolver "
     "(se for empréstimo). Isso ajuda na prestação de contas."),
    ("🤝 Gastos acima de R$ 200 precisam de aprovação",
     "Antes de gastar mais de R$ 200, pedir ok de pelo menos 2 líderes. "
     "Isso evita surpresas no caixa."),
    ("💰 Guardar 20% de cada evento",
     f"Separar 20% de toda arrecadação de evento como reserva. "
     f"Hoje o caixa ({R(kpis['saldo_atual'])}) cobre pouco mais de 1 mês de gastos. "
     f"O ideal seria ter pelo menos 3 meses guardados."),
    ("🔄 Cobrar devoluções de empréstimos",
     "R$ 820 saíram como empréstimos no trimestre. Precisamos "
     "acompanhar semanalmente e cobrar a devolução com data combinada."),
]

for emoji_titulo, texto in sugestoes:
    st.markdown(f"""
    <div class="sugestao">
        <h4>{emoji_titulo}</h4>
        <p>{texto}</p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# 7. EXTRATO — "Quero ver todas as movimentações"
# ══════════════════════════════════════════════

st.markdown('<div class="titulo-secao">📋 Extrato Completo</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explain">
    💡 <b>O que é isso?</b> — Lista de todas as entradas e saídas do trimestre.
    Você pode clicar nas colunas pra ordenar.
</div>
""", unsafe_allow_html=True)

df_display = df[["data", "mes", "descricao", "tipo", "entrada", "saida"]].copy()
df_display["data"] = df_display["data"].dt.strftime("%d/%m/%Y")
df_display.columns = ["Data", "Mês", "O que foi", "Tipo", "Entrou (R$)", "Saiu (R$)"]

st.dataframe(
    df_display, width='stretch', hide_index=True,
    column_config={
        "Entrou (R$)": st.column_config.NumberColumn(format="R$ %.2f"),
        "Saiu (R$)": st.column_config.NumberColumn(format="R$ %.2f"),
    },
    height=min(500, len(df_display) * 40 + 60),
)


# ══════════════════════════════════════════════
# RODAPÉ
# ══════════════════════════════════════════════

st.markdown("---")
st.markdown(f"""
<div style="text-align:center; padding:1.5rem 0; color:#94a3b8; font-size:0.85rem; line-height:1.8;">
    <b style="color:#64748b;">🎵 Caixa Sublime Som</b><br>
    Relatório feito em {datetime.now().strftime("%d/%m/%Y às %H:%M")}<br>
    Período: Janeiro a Março de 2026<br><br>
    <em>Uso interno — Para a liderança do grupo Sublime Som</em>
</div>
""", unsafe_allow_html=True)