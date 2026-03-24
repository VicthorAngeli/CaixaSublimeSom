import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from data import (
    get_transacoes, get_resumo_mensal, get_kpis,
    get_saidas_por_categoria, get_entradas_por_categoria,
    get_top_despesas, MESES_ORDEM,
)

st.set_page_config(page_title="Caixa Sublime Som", page_icon="🎵", layout="wide", initial_sidebar_state="collapsed")

df = get_transacoes()
resumo = get_resumo_mensal()
kpis = get_kpis()
saidas_cat = get_saidas_por_categoria()
entradas_cat = get_entradas_por_categoria()
top_desp = get_top_despesas(5)

VERDE = "#0D9F6E"; VERMELHO = "#E02D3C"; AZUL = "#1E40AF"; LARANJA = "#D97706"
CORES = ["#0D9F6E","#3B82F6","#F59E0B","#EF4444","#8B5CF6","#EC4899"]

def R(v): return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

PLOTLY = dict(
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#1e293b", size=13),
    margin=dict(t=30, b=30, l=50, r=30),
    hoverlabel=dict(bgcolor="white", font_size=13),
)

# ── CSS PREMIUM ──
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
* { font-family: 'Inter', sans-serif !important; }
.stApp { background: linear-gradient(180deg, #F0F4FF 0%, #F8FAFC 30%); }
.block-container { max-width: 1280px !important; padding-top: 2rem !important; }

.hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 30%, #1e3a5f 60%, #0f172a 100%);
    background-size: 200% 200%;
    animation: grad 8s ease infinite;
    padding: 2.5rem 2rem 2rem;
    border-radius: 24px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px rgba(15,23,42,0.15);
}
@keyframes grad { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
.hero h1 { font-size: 2.4rem; font-weight: 800; margin: 0; letter-spacing: -0.5px; }
.hero .sub { font-size: 1rem; opacity: 0.8; margin: 0.5rem 0 0; }
.hero .badges { display: flex; justify-content: center; gap: 1rem; margin-top: 1.2rem; flex-wrap: wrap; }
.hero .badge { background: rgba(255,255,255,0.12); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.15); padding: 0.35rem 0.9rem; border-radius: 100px; font-size: 0.78rem; font-weight: 500; }

.kpi {
    background: white; border-radius: 16px; padding: 1.4rem 1.2rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 20px rgba(0,0,0,0.03);
    border: 1px solid rgba(0,0,0,0.04); position: relative; overflow: hidden;
    transition: all 0.3s ease;
}
.kpi:hover { box-shadow: 0 8px 30px rgba(0,0,0,0.07); transform: translateY(-2px); }
.kpi .bar { position: absolute; top: 0; left: 0; right: 0; height: 3px; border-radius: 16px 16px 0 0; }
.kpi .icon { width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.15rem; margin-bottom: 0.7rem; }
.kpi .label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.8px; color: #94a3b8; font-weight: 600; margin-bottom: 0.3rem; }
.kpi .val { font-size: 1.5rem; font-weight: 800; letter-spacing: -0.5px; line-height: 1.2; }
.kpi .hint { font-size: 0.78rem; margin-top: 0.2rem; color: #94a3b8; font-weight: 500; }

.section { font-size: 1.2rem; font-weight: 700; color: #1e293b; margin: 2.2rem 0 1rem; padding-bottom: 0.4rem; border-bottom: 2px solid #e2e8f0; }

.alert {
    border-radius: 14px; padding: 1.1rem 1.3rem; margin-bottom: 0.8rem;
    border: 1px solid; display: flex; gap: 0.8rem; align-items: flex-start;
    transition: transform 0.2s; font-size: 0.9rem; line-height: 1.65;
}
.alert:hover { transform: translateX(4px); }
.alert .ic { width: 34px; height: 34px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 0.95rem; flex-shrink: 0; }
.alert .t { font-weight: 700; font-size: 0.88rem; margin: 0 0 0.2rem; }
.alert .b { flex: 1; color: #475569; }
.alert.red { background: rgba(224,45,60,0.04); border-color: rgba(224,45,60,0.15); }
.alert.red .ic { background: rgba(224,45,60,0.1); }
.alert.red .t { color: #E02D3C; }
.alert.yel { background: rgba(217,119,6,0.04); border-color: rgba(217,119,6,0.15); }
.alert.yel .ic { background: rgba(217,119,6,0.1); }
.alert.yel .t { color: #D97706; }
.alert.grn { background: rgba(13,159,110,0.04); border-color: rgba(13,159,110,0.15); }
.alert.grn .ic { background: rgba(13,159,110,0.1); }
.alert.grn .t { color: #0D9F6E; }

.month {
    background: white; border-radius: 16px; padding: 1.3rem; overflow: hidden; position: relative;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 20px rgba(0,0,0,0.03);
    border: 1px solid rgba(0,0,0,0.04); transition: all 0.3s ease;
}
.month:hover { box-shadow: 0 8px 30px rgba(0,0,0,0.07); transform: translateY(-2px); }
.month .top { position: absolute; top:0; left:0; right:0; height: 4px; }
.month h3 { text-align: center; font-size: 1.05rem; font-weight: 700; margin: 0.5rem 0 0.8rem; color: #1e293b; }
.month table { width: 100%; border-collapse: collapse; }
.month td { padding: 0.4rem 0; font-size: 0.88rem; color: #475569; }
.month td:last-child { text-align: right; font-weight: 600; }
.month .div { border-top: 2px solid #f1f5f9; margin: 0.3rem 0; }

.sug {
    background: white; border-radius: 14px; padding: 1.2rem 1.4rem; margin-bottom: 0.8rem;
    border-left: 4px solid #0D9F6E; box-shadow: 0 1px 6px rgba(0,0,0,0.04);
    transition: all 0.3s ease;
}
.sug:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.06); }
.sug h4 { margin: 0 0 0.3rem; color: #1e293b; font-size: 0.95rem; }
.sug p { margin: 0; color: #475569; font-size: 0.88rem; line-height: 1.6; }

.stTabs [data-baseweb="tab-list"] { gap:0; background: white; border-radius: 14px; padding: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); border: 1px solid rgba(0,0,0,0.06); }
.stTabs [data-baseweb="tab"] { border-radius: 10px; padding: 0.6rem 1.2rem; font-weight: 600; font-size: 0.85rem; color: #64748b; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #0D9F6E, #059669) !important; color: white !important; border-radius: 10px; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════
# HEADER
# ══════════════════════════════════════

st.markdown(f"""
<div class="hero">
    <h1>🎵 Caixa Sublime Som</h1>
    <p class="sub">Relatório Financeiro — 1º Trimestre 2026</p>
    <div class="badges">
        <span class="badge">📅 Janeiro – Março</span>
        <span class="badge">🕐 {datetime.now().strftime("%d/%m/%Y %H:%M")}</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════
# KPIs
# ══════════════════════════════════════

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="kpi"><div class="bar" style="background:linear-gradient(90deg,{VERDE},{VERDE}88)"></div>
    <div class="icon" style="background:rgba(13,159,110,0.08)">💰</div>
    <div class="label">Saldo em Caixa</div>
    <div class="val" style="color:{VERDE}">{R(kpis["saldo_atual"])}</div>
    <div class="hint">Dinheiro disponível hoje</div></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="kpi"><div class="bar" style="background:linear-gradient(90deg,{VERDE},#10B981)"></div>
    <div class="icon" style="background:rgba(13,159,110,0.08)">📈</div>
    <div class="label">Total de Entradas</div>
    <div class="val" style="color:{VERDE}">{R(kpis["total_entradas"])}</div>
    <div class="hint">Tudo que recebemos</div></div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="kpi"><div class="bar" style="background:linear-gradient(90deg,{VERMELHO},#F87171)"></div>
    <div class="icon" style="background:rgba(224,45,60,0.08)">📉</div>
    <div class="label">Total de Saídas</div>
    <div class="val" style="color:{VERMELHO}">{R(kpis["total_saidas"])}</div>
    <div class="hint">Tudo que gastamos</div></div>""", unsafe_allow_html=True)
with c4:
    cor = VERDE if kpis["resultado_liquido"] >= 0 else VERMELHO
    tag = "Sobraram" if kpis["resultado_liquido"] >= 0 else "Faltaram"
    st.markdown(f"""<div class="kpi"><div class="bar" style="background:linear-gradient(90deg,{AZUL},#3B82F6)"></div>
    <div class="icon" style="background:rgba(30,64,175,0.08)">🏦</div>
    <div class="label">Resultado do Trimestre</div>
    <div class="val" style="color:{cor}">{R(kpis["resultado_liquido"])}</div>
    <div class="hint">{tag} no período</div></div>""", unsafe_allow_html=True)


# ══════════════════════════════════════
# GRÁFICO + RESUMO MENSAL
# ══════════════════════════════════════

st.markdown('<div class="section">📊 Entradas vs Saídas por Mês</div>', unsafe_allow_html=True)

fig = go.Figure()
fig.add_trace(go.Bar(
    x=resumo["mes_label"], y=resumo["total_entradas"], name="Entrou",
    marker=dict(color=VERDE, cornerradius=6),
    text=[R(v) for v in resumo["total_entradas"]], textposition="outside",
    textfont=dict(size=13, color=VERDE, weight="bold"),
))
fig.add_trace(go.Bar(
    x=resumo["mes_label"], y=resumo["total_saidas"], name="Saiu",
    marker=dict(color=VERMELHO, cornerradius=6),
    text=[R(v) for v in resumo["total_saidas"]], textposition="outside",
    textfont=dict(size=13, color=VERMELHO, weight="bold"),
))
fig.update_layout(**PLOTLY, barmode="group", height=400, bargap=0.3,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=14)))
st.plotly_chart(fig, width='stretch')

# Cards mensais
mc = {"Janeiro": VERDE, "Fevereiro": VERMELHO, "Março": AZUL}
c_jan, c_fev, c_mar = st.columns(3)
for col, mes in zip([c_jan, c_fev, c_mar], MESES_ORDEM):
    r = resumo[resumo["mes"] == mes].iloc[0]
    cr = VERDE if r["resultado_mensal"] >= 0 else VERMELHO
    emoji = "✅" if r["resultado_mensal"] >= 0 else "⚠️"
    with col:
        st.markdown(f"""
        <div class="month">
            <div class="top" style="background:linear-gradient(90deg,{mc[mes]},{mc[mes]}88)"></div>
            <h3>{mes}</h3>
            <table>
                <tr><td style="color:{VERDE}">📥 Entrou</td><td style="color:{VERDE}">{R(r["total_entradas"])}</td></tr>
                <tr><td style="color:{VERMELHO}">📤 Saiu</td><td style="color:{VERMELHO}">{R(r["total_saidas"])}</td></tr>
            </table>
            <div class="div"></div>
            <table>
                <tr><td><b>{emoji} Resultado</b></td><td style="color:{cr};font-weight:700">{R(r["resultado_mensal"])}</td></tr>
                <tr><td><b>Saldo Final</b></td><td style="font-weight:800;font-size:1.05rem">{R(r["saldo_final"])}</td></tr>
            </table>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════
# PRA ONDE FOI O DINHEIRO
# ══════════════════════════════════════

st.markdown('<div class="section">📊 Pra onde foi o dinheiro?</div>', unsafe_allow_html=True)

col_pizza, col_top = st.columns([1, 1])

with col_pizza:
    fig_cat = go.Figure(data=[go.Pie(
        labels=saidas_cat["categoria"], values=saidas_cat["total"], hole=0.6,
        marker=dict(colors=CORES, line=dict(color="white", width=3)),
        textinfo="percent", textposition="outside", textfont=dict(size=13, weight="bold"),
    )])
    fig_cat.update_layout(
        **{**PLOTLY, "margin": dict(t=10, b=10, l=10, r=10)},
        showlegend=False, height=360,
        annotations=[dict(text=f"<b>{R(kpis['total_saidas'])}</b><br><span style='font-size:11px;color:#94a3b8'>Total</span>",
            x=0.5, y=0.5, font_size=14, showarrow=False)],
    )
    st.plotly_chart(fig_cat, width='stretch')

with col_top:
    st.markdown("<div style='padding-top:0.3rem'></div>", unsafe_allow_html=True)
    for i, (_, row) in enumerate(saidas_cat.iterrows()):
        cor = CORES[i % len(CORES)]
        st.markdown(
            f"<span style='color:{cor};font-size:1.5rem;vertical-align:middle'>●</span> "
            f"**{row['categoria']}** — {R(row['total'])} ({row['percentual']:.0f}%)",
            unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Top 3 gastos:**")
    for _, row in top_desp.head(3).iterrows():
        st.markdown(f"- 🔴 **{row['descricao']}** ({row['mes']}) — {R(row['saida'])}")


# ══════════════════════════════════════
# ALERTAS
# ══════════════════════════════════════

st.markdown('<div class="section">🚨 Pontos de Atenção</div>', unsafe_allow_html=True)

alertas = [
    ("red", "🔴", "Empréstimo pendente",
     f"David recebeu <b>{R(320)}</b> para simpósio e <b>ainda não devolveu</b>. Cobrar devolução."),
    ("red", "🔴", "Sem evento = caixa negativo",
     f"Fevereiro não teve evento: gastamos <b>{R(395)}</b> a mais do que recebemos."),
    ("yel", "🟡", "80% da receita vem de eventos",
     "Ofertas de ensaio cobrem só 20%. Se não tiver evento no mês, a conta não fecha."),
    ("yel", "🟡", "Gastos altos sem registro claro",
     f"'Joum David' ({R(500)}) — maior gasto do trimestre. Anotar sempre <b>pra quem</b> e <b>pra quê</b>."),
    ("grn", "🟢", f"Trimestre positivo: +{R(kpis['resultado_liquido'])}",
     f"Mesmo com fevereiro ruim, sobraram <b>{R(kpis['resultado_liquido'])}</b>. Saldo atual: <b>{R(kpis['saldo_atual'])}</b>."),
]

for cls, ic, titulo, texto in alertas:
    st.markdown(f"""
    <div class="alert {cls}">
        <div class="ic">{ic}</div>
        <div class="b"><div class="t">{titulo}</div>{texto}</div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════
# SUGESTÕES
# ══════════════════════════════════════

st.markdown('<div class="section">💡 Sugestões</div>', unsafe_allow_html=True)

sugs = [
    ("📅 1 evento de arrecadação por mês", "Meses com evento = dinheiro sobrando. Sem evento = caixa negativo."),
    ("📝 Anotar tudo: quem, pra quê, quando devolve", "Facilita a prestação de contas e evita dúvidas."),
    ("🤝 Gastos acima de R$ 200 com aprovação", "Pedir ok de 2 líderes antes de gastar. Sem surpresas."),
    ("💰 Guardar 20% de cada evento como reserva", f"Hoje o caixa cobre só 1 mês de gastos. Ideal: 3 meses ({R(kpis['media_saidas_mensal'] * 3)})."),
]

for titulo, texto in sugs:
    st.markdown(f"""<div class="sug"><h4>{titulo}</h4><p>{texto}</p></div>""", unsafe_allow_html=True)


# ══════════════════════════════════════
# EXTRATO (escondido em aba)
# ══════════════════════════════════════

st.markdown('<div class="section">📋 Extrato</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["  Ver extrato completo  ", "  Ocultar  "])
with tab1:
    df_d = df[["data","mes","descricao","tipo","entrada","saida"]].copy()
    df_d["data"] = df_d["data"].dt.strftime("%d/%m/%Y")
    df_d.columns = ["Data","Mês","Descrição","Tipo","Entrou (R$)","Saiu (R$)"]
    st.dataframe(df_d, width='stretch', hide_index=True,
        column_config={"Entrou (R$)": st.column_config.NumberColumn(format="R$ %.2f"),
                       "Saiu (R$)": st.column_config.NumberColumn(format="R$ %.2f")},
        height=min(450, len(df_d)*40+60))

# ── Footer ──
st.markdown("---")
st.markdown(f"""
<div style="text-align:center; padding:1.5rem 0; color:#94a3b8; font-size:0.82rem; line-height:1.8;">
    <b style="color:#64748b">🎵 Caixa Sublime Som</b><br>
    Janeiro – Março 2026 · Gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M")}<br>
    <em>Uso interno — Liderança do grupo Sublime Som</em>
</div>""", unsafe_allow_html=True)