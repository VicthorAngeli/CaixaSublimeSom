"""
╔══════════════════════════════════════════════════════════════╗
║            CAIXA SUBLIME SOM — Dashboard Financeiro         ║
║          Relatório Executivo • Janeiro – Março 2026         ║
║                    ✨ Visual Premium ✨                      ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from data import (
    get_transacoes,
    get_resumo_mensal,
    get_kpis,
    get_saidas_por_categoria,
    get_entradas_por_categoria,
    get_top_despesas,
    get_projecao,
    MESES_ORDEM,
    adicionar_transacao,
    remover_transacao,
    atualizar_saldo_inicial,
    get_saldo_inicial,
    restaurar_padrao,
    MESES_PT,
)

# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="Caixa Sublime Som — Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Paleta de cores premium
VERDE      = "#0D9F6E"
VERDE_BG   = "rgba(13,159,110,0.08)"
VERMELHO   = "#E02D3C"
VERMELHO_BG= "rgba(224,45,60,0.08)"
AZUL       = "#1E40AF"
AZUL_BG    = "rgba(30,64,175,0.08)"
LARANJA    = "#D97706"
LARANJA_BG = "rgba(217,119,6,0.08)"
SLATE      = "#1E293B"
SLATE_LIGHT= "#64748B"

CORES_GRAFICOS = ["#0D9F6E", "#3B82F6", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899", "#06B6D4", "#84CC16"]


def fmt_brl(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_pct(valor: float) -> str:
    return f"{valor:,.1f}%".replace(".", ",")


# ──────────────────────────────────────────────
# DADOS
# ──────────────────────────────────────────────

df = get_transacoes()
resumo = get_resumo_mensal()
kpis = get_kpis()
saidas_cat = get_saidas_por_categoria()
entradas_cat = get_entradas_por_categoria()
top_desp = get_top_despesas(10)
projecao = get_projecao()


# ──────────────────────────────────────────────
# PLOTLY TEMPLATE PREMIUM
# ──────────────────────────────────────────────

PLOTLY_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, -apple-system, BlinkMacSystemFont, sans-serif", color=SLATE, size=13),
    margin=dict(t=40, b=40, l=50, r=30),
    yaxis=dict(gridcolor="rgba(0,0,0,0.06)", zerolinecolor="rgba(0,0,0,0.06)"),
    xaxis=dict(gridcolor="rgba(0,0,0,0.06)", zerolinecolor="rgba(0,0,0,0.06)"),
    legend=dict(
        orientation="h", yanchor="bottom", y=1.04, xanchor="center", x=0.5,
        bgcolor="rgba(255,255,255,0.8)", bordercolor="rgba(0,0,0,0.05)", borderwidth=1,
        font=dict(size=12),
    ),
    hoverlabel=dict(bgcolor="white", font_size=13, font_family="Inter, sans-serif"),
)


# ══════════════════════════════════════════════
# CSS PREMIUM
# ══════════════════════════════════════════════

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    /* ─── BASE ─── */
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }

    .stApp {
        background: linear-gradient(180deg, #F0F4FF 0%, #F8FAFC 30%, #F8FAFC 100%);
    }

    .block-container {
        padding-top: 2rem !important;
        max-width: 1280px !important;
    }

    /* ─── ANIMATED HEADER ─── */
    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 30%, #1e3a5f 60%, #0f172a 100%);
        background-size: 200% 200%;
        animation: gradientShift 8s ease infinite;
        padding: 3rem 2.5rem 2.5rem;
        border-radius: 24px;
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(15,23,42,0.15);
    }
    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.03) 0%, transparent 60%);
        animation: rotateBg 20s linear infinite;
    }
    @keyframes rotateBg {
        0%   { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .hero h1 {
        font-size: 2.6rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 20px rgba(0,0,0,0.3);
    }
    .hero .subtitle {
        font-size: 1.05rem;
        opacity: 0.8;
        margin: 0.6rem 0 0 0;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    .hero .meta {
        display: inline-flex;
        align-items: center;
        gap: 1.5rem;
        margin-top: 1.4rem;
        position: relative;
        z-index: 1;
        flex-wrap: wrap;
        justify-content: center;
    }
    .hero .badge {
        background: rgba(255,255,255,0.12);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.15);
        padding: 0.4rem 1rem;
        border-radius: 100px;
        font-size: 0.78rem;
        font-weight: 500;
        letter-spacing: 0.3px;
    }

    /* ─── SECTION TITLES ─── */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin: 2.5rem 0 1.2rem 0;
    }
    .section-header .icon-box {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
    }
    .section-header h2 {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
        letter-spacing: -0.3px;
    }
    .section-header .section-desc {
        font-size: 0.82rem;
        color: #94a3b8;
        margin: 0;
        font-weight: 400;
    }

    /* ─── GLASS KPI CARDS ─── */
    .kpi-glass {
        background: white;
        border-radius: 16px;
        padding: 1.4rem 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 20px rgba(0,0,0,0.03);
        border: 1px solid rgba(0,0,0,0.04);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .kpi-glass:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.06), 0 8px 30px rgba(0,0,0,0.06);
        transform: translateY(-2px);
    }
    .kpi-glass .accent-bar {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        border-radius: 16px 16px 0 0;
    }
    .kpi-glass .kpi-icon {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        margin-bottom: 0.8rem;
    }
    .kpi-glass .kpi-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #94a3b8;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .kpi-glass .kpi-val {
        font-size: 1.55rem;
        font-weight: 800;
        color: #1e293b;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    .kpi-glass .kpi-val.green { color: #0D9F6E; }
    .kpi-glass .kpi-val.red   { color: #E02D3C; }
    .kpi-glass .kpi-val.blue  { color: #1E40AF; }
    .kpi-glass .kpi-sub {
        font-size: 0.78rem;
        margin-top: 0.3rem;
        font-weight: 500;
    }
    .kpi-glass .kpi-sub.up   { color: #0D9F6E; }
    .kpi-glass .kpi-sub.down { color: #E02D3C; }
    .kpi-glass .kpi-sub.muted{ color: #94a3b8; }

    /* ─── HEALTH INDICATOR CARDS ─── */
    .health-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 20px rgba(0,0,0,0.03);
        border: 1px solid rgba(0,0,0,0.04);
        text-align: center;
        transition: all 0.3s ease;
    }
    .health-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.06), 0 8px 30px rgba(0,0,0,0.06);
        transform: translateY(-2px);
    }
    .health-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
        vertical-align: middle;
    }
    .health-dot.verde    { background: #0D9F6E; box-shadow: 0 0 8px #0D9F6E; }
    .health-dot.amarelo  { background: #D97706; box-shadow: 0 0 8px #D97706; }
    .health-dot.vermelho { background: #E02D3C; box-shadow: 0 0 8px #E02D3C; }
    .health-status {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 100px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.5rem;
    }
    .health-status.verde    { background: rgba(13,159,110,0.1); color: #0D9F6E; }
    .health-status.amarelo  { background: rgba(217,119,6,0.1); color: #D97706; }
    .health-status.vermelho { background: rgba(224,45,60,0.1); color: #E02D3C; }

    /* ─── ALERT BOXES ─── */
    .alert {
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        border: 1px solid;
        display: flex;
        gap: 1rem;
        align-items: flex-start;
        transition: all 0.2s ease;
    }
    .alert:hover { transform: translateX(4px); }
    .alert .alert-icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        flex-shrink: 0;
    }
    .alert .alert-body { flex: 1; }
    .alert .alert-title {
        font-weight: 700;
        font-size: 0.9rem;
        margin: 0 0 0.3rem 0;
    }
    .alert .alert-text {
        font-size: 0.85rem;
        line-height: 1.6;
        color: #475569;
        margin: 0;
    }
    .alert.critico {
        background: rgba(224,45,60,0.04);
        border-color: rgba(224,45,60,0.15);
    }
    .alert.critico .alert-icon { background: rgba(224,45,60,0.1); }
    .alert.critico .alert-title { color: #E02D3C; }
    .alert.aviso {
        background: rgba(217,119,6,0.04);
        border-color: rgba(217,119,6,0.15);
    }
    .alert.aviso .alert-icon { background: rgba(217,119,6,0.1); }
    .alert.aviso .alert-title { color: #D97706; }
    .alert.positivo {
        background: rgba(13,159,110,0.04);
        border-color: rgba(13,159,110,0.15);
    }
    .alert.positivo .alert-icon { background: rgba(13,159,110,0.1); }
    .alert.positivo .alert-title { color: #0D9F6E; }

    /* ─── REC CARDS ─── */
    .rec-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 20px rgba(0,0,0,0.03);
        border: 1px solid rgba(0,0,0,0.04);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        border-left: 4px solid #0D9F6E;
    }
    .rec-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.06), 0 8px 30px rgba(0,0,0,0.06);
        transform: translateY(-2px);
    }
    .rec-card .rec-num {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border-radius: 8px;
        background: linear-gradient(135deg, #0D9F6E, #059669);
        color: white;
        font-size: 0.78rem;
        font-weight: 700;
        margin-right: 0.6rem;
        flex-shrink: 0;
    }
    .rec-card h4 {
        display: flex;
        align-items: center;
        margin: 0 0 0.6rem 0;
        color: #1e293b;
        font-size: 0.95rem;
    }
    .rec-card p {
        margin: 0;
        color: #475569;
        font-size: 0.88rem;
        line-height: 1.65;
    }

    /* ─── MONTH CARDS ─── */
    .month-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 20px rgba(0,0,0,0.03);
        border: 1px solid rgba(0,0,0,0.04);
        transition: all 0.3s ease;
        overflow: hidden;
        position: relative;
    }
    .month-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.06), 0 8px 30px rgba(0,0,0,0.06);
        transform: translateY(-2px);
    }
    .month-card .month-top {
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
    }
    .month-card h3 {
        text-align: center;
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0.5rem 0 1rem 0;
    }
    .month-card table { width: 100%; border-collapse: collapse; }
    .month-card td {
        padding: 0.45rem 0;
        font-size: 0.88rem;
        color: #475569;
    }
    .month-card td:last-child { text-align: right; font-weight: 600; }
    .month-card .divider { border-top: 2px solid #f1f5f9; margin: 0.3rem 0; }

    /* ─── META CARD ─── */
    .meta-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 20px rgba(0,0,0,0.03);
        border: 1px solid rgba(0,0,0,0.04);
        text-align: center;
        transition: all 0.3s ease;
    }
    .meta-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.06), 0 8px 30px rgba(0,0,0,0.06);
        transform: translateY(-2px);
    }
    .meta-card .meta-icon { font-size: 2rem; margin-bottom: 0.6rem; }
    .meta-card h4 {
        font-size: 0.95rem; font-weight: 700; color: #1e293b; margin: 0 0 0.8rem 0;
    }
    .meta-card .meta-row {
        display: flex; justify-content: space-between;
        font-size: 0.85rem; padding: 0.3rem 0; color: #475569;
    }
    .meta-card .meta-row b { color: #1e293b; }
    .meta-bar-bg {
        height: 8px; background: #f1f5f9; border-radius: 100px; margin-top: 0.8rem; overflow: hidden;
    }
    .meta-bar-fill {
        height: 100%; border-radius: 100px; transition: width 1s ease;
    }

    /* ─── PROJ CARD ─── */
    .proj-card {
        background: white;
        border-radius: 14px;
        padding: 1.1rem 1.2rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        border: 1px solid rgba(0,0,0,0.04);
        transition: all 0.2s ease;
    }
    .proj-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        transform: translateX(4px);
    }

    /* ─── TABS STYLING ─── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: white;
        border-radius: 14px;
        padding: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        border: 1px solid rgba(0,0,0,0.06);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        font-size: 0.85rem;
        color: #64748b;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0D9F6E, #059669) !important;
        color: white !important;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }
    .stTabs [data-baseweb="tab-border"] { display: none; }

    /* ─── DATAFRAME ─── */
    .stDataFrame { border-radius: 12px; overflow: hidden; }

    /* ─── PROGRESS BAR ─── */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #0D9F6E, #3B82F6) !important;
        border-radius: 100px;
    }

    /* ─── SELECTBOX ─── */
    .stSelectbox > div > div { border-radius: 10px; border-color: rgba(0,0,0,0.1); }

    /* ─── FOOTER ─── */
    .footer {
        text-align: center; padding: 2rem 0 3rem;
        color: #94a3b8; font-size: 0.8rem; line-height: 1.8;
    }
    .footer .footer-brand { font-weight: 700; color: #64748b; font-size: 0.9rem; }

    /* ─── HIDE STREAMLIT CHROME ─── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* ─── SIDEBAR ─── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        border-right: 1px solid rgba(0,0,0,0.06);
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #1e293b;
    }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# HELPER: SECTION HEADER
# ══════════════════════════════════════════════

def section_header(icon: str, title: str, desc: str, color: str = VERDE):
    st.markdown(f"""
    <div class="section-header">
        <div class="icon-box" style="background:{color}15; color:{color};">{icon}</div>
        <div>
            <h2>{title}</h2>
            <p class="section-desc">{desc}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SIDEBAR — GESTÃO DE DADOS
# ══════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 📋 Gestão de Dados")
    st.markdown("---")

    # ── Saldo Inicial ──
    with st.expander("💰 Saldo Inicial", expanded=False):
        _saldo_ini = get_saldo_inicial()
        novo_saldo = st.number_input(
            "Saldo antes da 1ª transação (R$)",
            value=_saldo_ini, step=0.01, format="%.2f", key="saldo_ini_input",
        )
        if st.button("Salvar Saldo Inicial", key="btn_saldo", use_container_width=True):
            if novo_saldo != _saldo_ini:
                atualizar_saldo_inicial(novo_saldo)
                st.rerun()

    # ── Nova Transação ──
    st.markdown("### ➕ Nova Transação")
    with st.form("nova_transacao", clear_on_submit=True):
        col_d, col_t = st.columns([2, 1])
        with col_d:
            data_input = st.date_input("Data")
        with col_t:
            tipo_input = st.selectbox("Tipo", ["Entrada", "Saída"])
        descricao_input = st.text_input("Descrição")
        valor_input = st.number_input("Valor (R$)", min_value=0.0, step=0.01, format="%.2f")
        submitted = st.form_submit_button("✅ Adicionar", use_container_width=True)

        if submitted:
            if not descricao_input:
                st.error("Preencha a descrição")
            elif valor_input <= 0:
                st.error("Valor deve ser maior que zero")
            else:
                entrada = valor_input if tipo_input == "Entrada" else 0
                saida = valor_input if tipo_input == "Saída" else 0
                adicionar_transacao(
                    data_input.strftime("%Y-%m-%d"),
                    descricao_input, entrada, saida,
                )
                st.rerun()

    # ── Importar CSV ──
    st.markdown("---")
    with st.expander("📤 Importar CSV"):
        st.caption("Colunas: `data`, `descricao`, `entrada`, `saida`")
        uploaded = st.file_uploader("Selecionar arquivo", type=["csv"], key="csv_upload")
        if uploaded:
            try:
                df_csv = pd.read_csv(uploaded)
                df_csv.columns = df_csv.columns.str.lower().str.strip()
                required = {"data", "descricao", "entrada", "saida"}
                if required.issubset(set(df_csv.columns)):
                    for _, row in df_csv.iterrows():
                        adicionar_transacao(
                            str(row["data"]), str(row["descricao"]),
                            float(row.get("entrada", 0) or 0),
                            float(row.get("saida", 0) or 0),
                        )
                    st.success(f"✅ {len(df_csv)} transações importadas!")
                    st.rerun()
                else:
                    st.error("Colunas necessárias: data, descricao, entrada, saida")
            except Exception as e:
                st.error(f"Erro ao importar: {e}")

    # ── Exportar / Restaurar ──
    st.markdown("---")
    if not df.empty:
        df_exp = df[["data", "mes", "descricao", "entrada", "saida"]].copy()
        df_exp["data"] = df_exp["data"].dt.strftime("%Y-%m-%d")
        st.download_button(
            "📥 Exportar CSV", df_exp.to_csv(index=False),
            "caixa_sublime_som.csv", "text/csv",
            use_container_width=True,
        )

    st.markdown("---")
    if st.button("🔄 Restaurar Dados Padrão", use_container_width=True):
        restaurar_padrao()
        st.rerun()

    st.caption(f"{len(df)} transações · {len(MESES_ORDEM)} meses")


# ══════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════

_primeiro_mes = MESES_ORDEM[0][:3] if MESES_ORDEM else "?"
_ultimo_mes = MESES_ORDEM[-1][:3] if MESES_ORDEM else "?"
_n_meses = len(MESES_ORDEM)

st.markdown(f"""
<div class="hero">
    <h1>🎵 Caixa Sublime Som</h1>
    <p class="subtitle">Dashboard Financeiro Executivo</p>
    <div class="meta">
        <span class="badge">📅 {_n_meses} meses analisados</span>
        <span class="badge">📊 {_primeiro_mes} – {_ultimo_mes}</span>
        <span class="badge">🕐 {datetime.now().strftime("%d/%m/%Y %H:%M")}</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SEÇÃO 1 — KPIs EXECUTIVOS
# ══════════════════════════════════════════════

section_header("📊", "Indicadores Executivos", f"Visão consolidada — {_primeiro_mes} a {_ultimo_mes}")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    _var_arrow = "▲" if kpis["variacao_saldo_ultimo"] >= 0 else "▼"
    _var_class = "up" if kpis["variacao_saldo_ultimo"] >= 0 else "down"
    _var_ref = MESES_ORDEM[-2][:3].lower() if len(MESES_ORDEM) >= 2 else "ant"
    st.markdown(f"""
    <div class="kpi-glass">
        <div class="accent-bar" style="background: linear-gradient(90deg, {VERDE}, #059669);"></div>
        <div class="kpi-icon" style="background:{VERDE_BG};">💰</div>
        <div class="kpi-label">Saldo em Caixa</div>
        <div class="kpi-val green">{fmt_brl(kpis["saldo_atual"])}</div>
        <div class="kpi-sub {_var_class}">{_var_arrow} {fmt_pct(abs(kpis["variacao_saldo_ultimo"]))} vs {_var_ref}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-glass">
        <div class="accent-bar" style="background: linear-gradient(90deg, {VERDE}, #10B981);"></div>
        <div class="kpi-icon" style="background:{VERDE_BG};">📈</div>
        <div class="kpi-label">Total de Entradas</div>
        <div class="kpi-val green">{fmt_brl(kpis["total_entradas"])}</div>
        <div class="kpi-sub muted">Acumulado no trimestre</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-glass">
        <div class="accent-bar" style="background: linear-gradient(90deg, {VERMELHO}, #F87171);"></div>
        <div class="kpi-icon" style="background:{VERMELHO_BG};">📉</div>
        <div class="kpi-label">Total de Saídas</div>
        <div class="kpi-val red">{fmt_brl(kpis["total_saidas"])}</div>
        <div class="kpi-sub muted">Acumulado no trimestre</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    delta_class = "up" if kpis["resultado_liquido"] >= 0 else "down"
    val_class = "green" if kpis["resultado_liquido"] >= 0 else "red"
    st.markdown(f"""
    <div class="kpi-glass">
        <div class="accent-bar" style="background: linear-gradient(90deg, {AZUL}, #3B82F6);"></div>
        <div class="kpi-icon" style="background:{AZUL_BG};">🏦</div>
        <div class="kpi-label">Resultado Líquido</div>
        <div class="kpi-val {val_class}">{fmt_brl(kpis["resultado_liquido"])}</div>
        <div class="kpi-sub {delta_class}">{"▲ Superávit" if kpis["resultado_liquido"] >= 0 else "▼ Déficit"}</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    cob = kpis["indice_cobertura_tri"]
    cob_class = "green" if cob >= 1.5 else ("red" if cob < 1.0 else "blue")
    st.markdown(f"""
    <div class="kpi-glass">
        <div class="accent-bar" style="background: linear-gradient(90deg, {LARANJA}, #F59E0B);"></div>
        <div class="kpi-icon" style="background:{LARANJA_BG};">⚖️</div>
        <div class="kpi-label">Índice de Cobertura</div>
        <div class="kpi-val {cob_class}">{cob:.2f}x</div>
        <div class="kpi-sub muted">Entradas ÷ Saídas</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

col6, col7, col8, col9 = st.columns(4)

with col6:
    st.markdown(f"""
    <div class="kpi-glass">
        <div class="accent-bar" style="background: linear-gradient(90deg, #8B5CF6, #A78BFA);"></div>
        <div class="kpi-icon" style="background:rgba(139,92,246,0.08);">🛡️</div>
        <div class="kpi-label">Reserva Financeira</div>
        <div class="kpi-val">{kpis["reserva_em_meses"]:.1f} meses</div>
        <div class="kpi-sub muted">Saldo ÷ Média Saídas</div>
    </div>
    """, unsafe_allow_html=True)

with col7:
    st.markdown(f"""
    <div class="kpi-glass">
        <div class="accent-bar" style="background: linear-gradient(90deg, {VERDE}, #34D399);"></div>
        <div class="kpi-icon" style="background:{VERDE_BG};">📊</div>
        <div class="kpi-label">Média Mensal Entradas</div>
        <div class="kpi-val green">{fmt_brl(kpis["media_entradas_mensal"])}</div>
        <div class="kpi-sub muted">Por mês</div>
    </div>
    """, unsafe_allow_html=True)

with col8:
    st.markdown(f"""
    <div class="kpi-glass">
        <div class="accent-bar" style="background: linear-gradient(90deg, {VERMELHO}, #FB7185);"></div>
        <div class="kpi-icon" style="background:{VERMELHO_BG};">💸</div>
        <div class="kpi-label">Média Mensal Saídas</div>
        <div class="kpi-val red">{fmt_brl(kpis["media_saidas_mensal"])}</div>
        <div class="kpi-sub muted">Por mês</div>
    </div>
    """, unsafe_allow_html=True)

with col9:
    st.markdown(f"""
    <div class="kpi-glass">
        <div class="accent-bar" style="background: linear-gradient(90deg, #EC4899, #F472B6);"></div>
        <div class="kpi-icon" style="background:rgba(236,72,153,0.08);">🧾</div>
        <div class="kpi-label">Ticket Médio Saída</div>
        <div class="kpi-val">{fmt_brl(kpis["ticket_medio_saida"])}</div>
        <div class="kpi-sub muted">Por transação</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SEÇÃO 2 — GRÁFICOS PRINCIPAIS
# ══════════════════════════════════════════════

section_header("📈", "Análise Visual", "Desempenho financeiro detalhado por mês e categoria")

tab1, tab2, tab3, tab4 = st.tabs([
    "  Entradas vs Saídas  ",
    "  Evolução do Saldo  ",
    "  Saídas por Categoria  ",
    "  Top Despesas  ",
])

with tab1:
    fig_ev = go.Figure()
    fig_ev.add_trace(go.Bar(
        x=resumo["mes_label"], y=resumo["total_entradas"],
        name="Entradas",
        marker=dict(color=VERDE, cornerradius=6),
        text=[fmt_brl(v) for v in resumo["total_entradas"]],
        textposition="outside",
        textfont=dict(size=12, color=VERDE, weight="bold"),
    ))
    fig_ev.add_trace(go.Bar(
        x=resumo["mes_label"], y=resumo["total_saidas"],
        name="Saídas",
        marker=dict(color=VERMELHO, cornerradius=6),
        text=[fmt_brl(v) for v in resumo["total_saidas"]],
        textposition="outside",
        textfont=dict(size=12, color=VERMELHO, weight="bold"),
    ))
    fig_ev.add_trace(go.Scatter(
        x=resumo["mes_label"], y=resumo["resultado_mensal"],
        name="Resultado",
        mode="lines+markers+text",
        line=dict(color=AZUL, width=3, dash="dot"),
        marker=dict(size=10, color=AZUL, line=dict(width=2, color="white")),
        text=[fmt_brl(v) for v in resumo["resultado_mensal"]],
        textposition="top center",
        textfont=dict(size=11, color=AZUL),
    ))
    fig_ev.update_layout(**PLOTLY_LAYOUT, barmode="group", height=460, bargap=0.25)
    fig_ev.update_yaxes(title="Valor (R$)", tickformat=",.0f")
    st.plotly_chart(fig_ev, width='stretch')

    st.markdown(f"""
    <div class="alert positivo">
        <div class="alert-icon">💡</div>
        <div class="alert-body">
            <p class="alert-title">Análise do Trimestre</p>
            <p class="alert-text">
                Janeiro foi o mês mais forte, impulsionado pelo sorteio (R$ 1.410).
                Fevereiro teve <b>déficit de R$ 395</b> — o único mês negativo.
                Março recuperou com Lava Car + Sorteio, mas saídas também foram elevadas.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    saldos_data = pd.DataFrame({
        "mes": ["Início"] + list(resumo["mes_label"]),
        "saldo": [get_saldo_inicial()] + list(resumo["saldo_final"]),
    })
    fig_saldo = go.Figure()
    fig_saldo.add_trace(go.Scatter(
        x=saldos_data["mes"], y=saldos_data["saldo"],
        mode="lines+markers+text",
        fill="tozeroy",
        fillcolor="rgba(13,159,110,0.06)",
        line=dict(color=VERDE, width=3.5, shape="spline"),
        marker=dict(size=14, color=VERDE, line=dict(width=3, color="white")),
        text=[fmt_brl(v) for v in saldos_data["saldo"]],
        textposition="top center",
        textfont=dict(size=13, weight="bold", color=SLATE),
    ))
    meta_reserva = kpis["media_saidas_mensal"] * 2
    fig_saldo.add_hline(
        y=meta_reserva, line_dash="dash", line_color=LARANJA, line_width=2,
        annotation_text=f"Meta Mínima: {fmt_brl(meta_reserva)}",
        annotation_position="top right",
        annotation_font=dict(color=LARANJA, size=11, weight="bold"),
    )
    fig_saldo.update_layout(**PLOTLY_LAYOUT, height=440, showlegend=False)
    fig_saldo.update_yaxes(title="Saldo (R$)", tickformat=",.0f")
    st.plotly_chart(fig_saldo, width='stretch')

    posicao = "acima" if kpis["saldo_atual"] >= meta_reserva else "abaixo"
    st.markdown(f"""
    <div class="alert aviso">
        <div class="alert-icon">📌</div>
        <div class="alert-body">
            <p class="alert-title">Meta de Reserva</p>
            <p class="alert-text">
                A linha tracejada é a meta mínima ({fmt_brl(meta_reserva)}) = 2× média de saídas.
                Saldo atual está <b>{posicao}</b> da meta.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    col_donut, col_table = st.columns([1, 1])
    with col_donut:
        fig_cat = go.Figure(data=[go.Pie(
            labels=saidas_cat["categoria"], values=saidas_cat["total"],
            hole=0.6,
            marker=dict(colors=CORES_GRAFICOS, line=dict(color="white", width=3)),
            textinfo="percent",
            textposition="outside",
            textfont=dict(size=12, weight="bold"),
            pull=[0.02] * len(saidas_cat),
            hovertemplate="<b>%{label}</b><br>%{value:,.2f}<br>%{percent}<extra></extra>",
        )])
        fig_cat.update_layout(
            **{**PLOTLY_LAYOUT, "margin": dict(t=20, b=20, l=40, r=40)},
            showlegend=False, height=420,
            annotations=[dict(
                text=f"<b>{fmt_brl(kpis['total_saidas'])}</b><br><span style='font-size:11px;color:#94a3b8'>Total Saídas</span>",
                x=0.5, y=0.5, font_size=15, showarrow=False,
            )],
        )
        st.plotly_chart(fig_cat, width='stretch')

    with col_table:
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        st.markdown("##### Detalhamento por Categoria")
        for i, (_, row) in enumerate(saidas_cat.iterrows()):
            cor = CORES_GRAFICOS[i % len(CORES_GRAFICOS)]
            st.markdown(
                f"<span style='color:{cor};font-size:1.4rem;vertical-align:middle;'>●</span> "
                f"**{row['categoria']}** — {fmt_brl(row['total'])} "
                f"({fmt_pct(row['percentual'])}) · {int(row['qtd'])} transaç{'ão' if row['qtd'] == 1 else 'ões'}",
                unsafe_allow_html=True,
            )
            st.progress(row["percentual"] / 100)

with tab4:
    fig_top = go.Figure()
    colors_top = [VERMELHO if v >= 200 else LARANJA if v >= 100 else "#94A3B8" for v in top_desp["saida"]]
    fig_top.add_trace(go.Bar(
        y=[f"{r['descricao']} ({r['mes']})" for _, r in top_desp.iterrows()],
        x=top_desp["saida"],
        orientation="h",
        marker=dict(color=colors_top, cornerradius=4),
        text=[fmt_brl(v) for v in top_desp["saida"]],
        textposition="outside",
        textfont=dict(size=11, weight="bold"),
    ))
    fig_top.update_layout(
        **{**PLOTLY_LAYOUT, "margin": dict(t=10, b=40, l=10, r=80)},
        showlegend=False,
        height=max(380, len(top_desp) * 50),
    )
    fig_top.update_yaxes(autorange="reversed")
    fig_top.update_xaxes(title="Valor (R$)")
    st.plotly_chart(fig_top, width='stretch')

    st.markdown("""
    <div class="alert critico">
        <div class="alert-icon">⚠️</div>
        <div class="alert-body">
            <p class="alert-title">Concentração de Saídas</p>
            <p class="alert-text">
                As 3 maiores saídas (Joum David R$ 500, David Simpósio R$ 320, Parte das Lembrancinhas R$ 266)
                representam <b>60%</b> de todas as saídas do trimestre.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SEÇÃO 3 — SAÚDE FINANCEIRA
# ══════════════════════════════════════════════

section_header("🏥", "Saúde Financeira", "Diagnóstico por indicadores-chave com semáforo de risco", color="#8B5CF6")

def semaforo(valor, bom, medio):
    if valor >= bom:
        return "verde", "Saudável"
    elif valor >= medio:
        return "amarelo", "Atenção"
    else:
        return "vermelho", "Crítico"

ind1, ind2, ind3, ind4 = st.columns(4)

with ind1:
    cor, status = semaforo(kpis["indice_cobertura_tri"], 1.5, 1.0)
    st.markdown(f"""
    <div class="health-card">
        <div style="font-size:2rem; margin-bottom:0.5rem;">⚖️</div>
        <div class="kpi-label">Índice de Cobertura</div>
        <div style="font-size:2rem; font-weight:800; color:#1e293b; margin:0.3rem 0;">{kpis["indice_cobertura_tri"]:.2f}x</div>
        <div><span class="health-dot {cor}"></span> <span class="health-status {cor}">{status}</span></div>
        <p style="font-size:0.78rem; color:#94a3b8; margin-top:0.6rem;">
            {"Entradas cobrem as saídas" if kpis["indice_cobertura_tri"] >= 1 else "Saídas superam entradas"}
        </p>
    </div>
    """, unsafe_allow_html=True)

with ind2:
    cor, status = semaforo(kpis["reserva_em_meses"], 3.0, 1.5)
    st.markdown(f"""
    <div class="health-card">
        <div style="font-size:2rem; margin-bottom:0.5rem;">🛡️</div>
        <div class="kpi-label">Reserva Financeira</div>
        <div style="font-size:2rem; font-weight:800; color:#1e293b; margin:0.3rem 0;">{kpis["reserva_em_meses"]:.1f} meses</div>
        <div><span class="health-dot {cor}"></span> <span class="health-status {cor}">{status}</span></div>
        <p style="font-size:0.78rem; color:#94a3b8; margin-top:0.6rem;">Meta ideal: ≥ 3 meses</p>
    </div>
    """, unsafe_allow_html=True)

with ind3:
    conc = kpis["concentracao_receita"]
    cor_conc, status_conc = semaforo(100 - conc, 70, 50)
    st.markdown(f"""
    <div class="health-card">
        <div style="font-size:2rem; margin-bottom:0.5rem;">🎯</div>
        <div class="kpi-label">Concentração de Receita</div>
        <div style="font-size:2rem; font-weight:800; color:#1e293b; margin:0.3rem 0;">{fmt_pct(conc)}</div>
        <div><span class="health-dot {cor_conc}"></span> <span class="health-status {cor_conc}">{status_conc}</span></div>
        <p style="font-size:0.78rem; color:#94a3b8; margin-top:0.6rem;">Maior entrada = {fmt_pct(conc)} do total</p>
    </div>
    """, unsafe_allow_html=True)

with ind4:
    recorr = kpis["pct_recorrente"]
    cor_rec, status_rec = semaforo(recorr, 50, 30)
    st.markdown(f"""
    <div class="health-card">
        <div style="font-size:2rem; margin-bottom:0.5rem;">🔄</div>
        <div class="kpi-label">Receita Recorrente</div>
        <div style="font-size:2rem; font-weight:800; color:#1e293b; margin:0.3rem 0;">{fmt_pct(recorr)}</div>
        <div><span class="health-dot {cor_rec}"></span> <span class="health-status {cor_rec}">{status_rec}</span></div>
        <p style="font-size:0.78rem; color:#94a3b8; margin-top:0.6rem;">Ofertas = {fmt_brl(kpis["ofertas_ensaio_total"])}</p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SEÇÃO 4 — FLUXO DE CAIXA
# ══════════════════════════════════════════════

section_header("📋", "Fluxo de Caixa", "Extrato completo com filtros interativos", color="#3B82F6")

col_f1, col_f2, _ = st.columns([1, 1, 3])
with col_f1:
    mes_filtro = st.selectbox("Mês", ["Todos"] + MESES_ORDEM, key="filtro_mes")
with col_f2:
    tipo_filtro = st.selectbox("Tipo", ["Todos", "Entrada", "Saída"], key="filtro_tipo")

df_filtrado = df.copy()
if mes_filtro != "Todos":
    df_filtrado = df_filtrado[df_filtrado["mes"] == mes_filtro]
if tipo_filtro != "Todos":
    df_filtrado = df_filtrado[df_filtrado["tipo"] == tipo_filtro]

df_display = df_filtrado[["data", "mes", "descricao", "categoria", "entrada", "saida"]].copy()
df_display["data"] = df_display["data"].dt.strftime("%d/%m/%Y")
df_display.columns = ["Data", "Mês", "Descrição", "Categoria", "Entrada (R$)", "Saída (R$)"]

st.dataframe(
    df_display, width='stretch', hide_index=True,
    column_config={
        "Entrada (R$)": st.column_config.NumberColumn(format="R$ %.2f"),
        "Saída (R$)": st.column_config.NumberColumn(format="R$ %.2f"),
    },
    height=min(400, max(200, len(df_display) * 40 + 60)),
)

tot_ent_f = df_filtrado["entrada"].sum()
tot_sai_f = df_filtrado["saida"].sum()
res_f = tot_ent_f - tot_sai_f
res_color = VERDE if res_f >= 0 else VERMELHO

st.markdown(
    f"<div style='background:white; border-radius:10px; padding:0.8rem 1.2rem; "
    f"box-shadow:0 1px 3px rgba(0,0,0,0.04); border:1px solid rgba(0,0,0,0.04); "
    f"font-size:0.9rem; display:flex; gap:2rem; flex-wrap:wrap;'>"
    f"<span><b>{len(df_filtrado)}</b> transações</span>"
    f"<span>Entradas: <b style='color:{VERDE}'>{fmt_brl(tot_ent_f)}</b></span>"
    f"<span>Saídas: <b style='color:{VERMELHO}'>{fmt_brl(tot_sai_f)}</b></span>"
    f"<span>Resultado: <b style='color:{res_color}'>{fmt_brl(res_f)}</b></span>"
    f"</div>",
    unsafe_allow_html=True,
)


# ══════════════════════════════════════════════
# SEÇÃO 5 — RESUMO MENSAL
# ══════════════════════════════════════════════

section_header("📅", "Resumo Mensal", "Comparativo lado a lado dos meses analisados", color=LARANJA)

_month_colors = [VERDE, VERMELHO, AZUL, LARANJA, "#8B5CF6", "#EC4899", "#06B6D4", "#84CC16"]
_month_cols = st.columns(len(MESES_ORDEM)) if MESES_ORDEM else []

for _mi, (col, mes) in enumerate(zip(_month_cols, MESES_ORDEM)):
    r = resumo[resumo["mes"] == mes].iloc[0]
    mc = _month_colors[_mi % len(_month_colors)]
    cor_res = VERDE if r["resultado_mensal"] >= 0 else VERMELHO
    emoji_r = "✅" if r["resultado_mensal"] >= 0 else "⚠️"

    with col:
        st.markdown(f"""
        <div class="month-card">
            <div class="month-top" style="background: linear-gradient(90deg, {mc}, {mc}88);"></div>
            <h3>{mes}</h3>
            <table>
                <tr><td>Saldo Anterior</td><td>{fmt_brl(r["saldo_anterior"])}</td></tr>
                <tr><td style="color:{VERDE}">➕ Entradas</td><td style="color:{VERDE}">{fmt_brl(r["total_entradas"])}</td></tr>
                <tr><td style="color:{VERMELHO}">➖ Saídas</td><td style="color:{VERMELHO}">{fmt_brl(r["total_saidas"])}</td></tr>
            </table>
            <div class="divider"></div>
            <table>
                <tr><td><b>{emoji_r} Resultado</b></td><td style="color:{cor_res}; font-weight:700">{fmt_brl(r["resultado_mensal"])}</td></tr>
                <tr><td><b>Saldo Final</b></td><td style="font-weight:800; font-size:1.05rem; color:#1e293b">{fmt_brl(r["saldo_final"])}</td></tr>
                <tr><td>Transações</td><td>{int(r["qtd_transacoes"])}</td></tr>
                <tr><td>Cobertura</td><td>{r["indice_cobertura"]:.2f}x</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SEÇÃO 6 — ALERTAS
# ══════════════════════════════════════════════

section_header("🚨", "Alertas e Pontos de Atenção", "Itens que exigem acompanhamento ou decisão da liderança", color=VERMELHO)

alertas = []

if kpis["emprestimo_pendente"] > 0:
    alertas.append({"tipo": "critico", "icon": "🔴",
     "titulo": "Empréstimos / Adiantamentos Pendentes",
     "texto": f"Saídas classificadas como empréstimos somam <b>{fmt_brl(kpis['emprestimo_pendente'])}</b>. "
              f"Verificar devoluções pendentes e formalizar prazos."})

if kpis["concentracao_receita"] > 40:
    alertas.append({"tipo": "critico", "icon": "🔴",
     "titulo": "Alta Concentração de Receita em Eventos",
     "texto": f"A maior entrada individual = <b>{fmt_pct(kpis['concentracao_receita'])}</b> de toda a receita. "
              f"Receita recorrente (Ofertas) = apenas <b>{fmt_pct(kpis['pct_recorrente'])}</b>."})

for _, _rm in resumo.iterrows():
    if _rm["resultado_mensal"] < 0:
        alertas.append({"tipo": "aviso", "icon": "🟡",
         "titulo": f"{_rm['mes_label']} — Déficit Operacional",
         "texto": f"Saídas (<b>{fmt_brl(_rm['total_saidas'])}</b>) superaram entradas "
                  f"(<b>{fmt_brl(_rm['total_entradas'])}</b>) em <b>{fmt_brl(abs(_rm['resultado_mensal']))}</b>."})

if kpis["resultado_liquido"] >= 0:
    alertas.append({"tipo": "positivo", "icon": "🟢",
     "titulo": f"Resultado Positivo — Superávit de {fmt_brl(kpis['resultado_liquido'])}",
     "texto": f"O período encerra com superávit e cobertura de <b>{kpis['indice_cobertura_tri']:.2f}x</b>."})
else:
    alertas.append({"tipo": "critico", "icon": "🔴",
     "titulo": f"Resultado Negativo — Déficit de {fmt_brl(abs(kpis['resultado_liquido']))}",
     "texto": f"O período encerra com déficit. Índice de cobertura: <b>{kpis['indice_cobertura_tri']:.2f}x</b>."})

for a in alertas:
    st.markdown(f"""
    <div class="alert {a['tipo']}">
        <div class="alert-icon">{a['icon']}</div>
        <div class="alert-body">
            <p class="alert-title">{a['titulo']}</p>
            <p class="alert-text">{a['texto']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SEÇÃO 7 — PROJEÇÃO
# ══════════════════════════════════════════════

section_header("🔮", "Projeção de Caixa", "Estimativa para os próximos meses (cenário conservador)", color="#8B5CF6")

st.markdown(
    "<p style='color:#94a3b8; font-size:0.85rem; margin-bottom:1rem;'>"
    "Baseado na média simples dos 3 meses reportados. Não considera eventos extraordinários.</p>",
    unsafe_allow_html=True,
)

col_proj, col_graf_proj = st.columns([1, 2])

with col_proj:
    for _, row in projecao.iterrows():
        st.markdown(f"""
        <div class="proj-card">
            <div style="font-weight:700; font-size:0.95rem; color:#1e293b; margin-bottom:0.4rem;">
                📅 {row['mes']} <span style="font-size:0.75rem; color:#94a3b8; font-weight:400;">(projetado)</span>
            </div>
            <div style="display:flex; gap:1rem; font-size:0.85rem; margin-bottom:0.3rem;">
                <span style="color:{VERDE}">▲ {fmt_brl(row['entrada_projetada'])}</span>
                <span style="color:{VERMELHO}">▼ {fmt_brl(row['saida_projetada'])}</span>
            </div>
            <div style="font-size:1.1rem; font-weight:800; color:#1e293b;">
                Saldo: {fmt_brl(row['saldo_projetado'])}
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_graf_proj:
    hist_s = pd.DataFrame({
        "mes": list(resumo["mes_label"]),
        "saldo": list(resumo["saldo_final"]),
        "tipo": ["Realizado"] * len(resumo),
    })
    proj_s = pd.DataFrame({
        "mes": projecao["mes"],
        "saldo": projecao["saldo_projetado"],
        "tipo": ["Projetado"] * 3,
    })
    todos = pd.concat([hist_s, proj_s], ignore_index=True)

    fig_proj = go.Figure()
    real = todos[todos["tipo"] == "Realizado"]
    fig_proj.add_trace(go.Scatter(
        x=real["mes"], y=real["saldo"],
        mode="lines+markers", name="Realizado",
        line=dict(color=VERDE, width=3),
        marker=dict(size=10, color=VERDE, line=dict(width=2, color="white")),
    ))
    proj_plot = pd.concat([real.tail(1), todos[todos["tipo"] == "Projetado"]], ignore_index=True)
    fig_proj.add_trace(go.Scatter(
        x=proj_plot["mes"], y=proj_plot["saldo"],
        mode="lines+markers", name="Projetado",
        line=dict(color=LARANJA, width=3, dash="dash"),
        marker=dict(size=10, symbol="diamond", color=LARANJA, line=dict(width=2, color="white")),
    ))
    fig_proj.add_hline(
        y=kpis["media_saidas_mensal"] * 2,
        line_dash="dot", line_color="#CBD5E1", line_width=1.5,
        annotation_text="Meta Mínima", annotation_position="top right",
        annotation_font=dict(size=10, color="#94a3b8"),
    )
    fig_proj.update_layout(**PLOTLY_LAYOUT, height=380)
    fig_proj.update_yaxes(title="Saldo (R$)", tickformat=",.0f")
    st.plotly_chart(fig_proj, width='stretch')


# ══════════════════════════════════════════════
# SEÇÃO 8 — METAS
# ══════════════════════════════════════════════

section_header("🎯", "Metas Financeiras", "Objetivos sugeridos para os próximos meses", color=LARANJA)

meta_reserva_3m = kpis["media_saidas_mensal"] * 3
meta_receita_recorrente = kpis["media_saidas_mensal"] * 0.6

col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    pct = min(100, (kpis["saldo_atual"] / meta_reserva_3m) * 100)
    bar_cor = VERDE if pct >= 80 else LARANJA if pct >= 50 else VERMELHO
    st.markdown(f"""
    <div class="meta-card">
        <div class="meta-icon">🏦</div>
        <h4>Reserva de Segurança</h4>
        <div class="meta-row"><span>Meta</span><b>{fmt_brl(meta_reserva_3m)}</b></div>
        <div class="meta-row"><span>Atual</span><b>{fmt_brl(kpis["saldo_atual"])}</b></div>
        <div class="meta-row"><span>Atingimento</span><b style="color:{bar_cor}">{fmt_pct(pct)}</b></div>
        <div class="meta-bar-bg"><div class="meta-bar-fill" style="width:{pct}%; background:linear-gradient(90deg, {bar_cor}, {bar_cor}88);"></div></div>
        <p style="font-size:0.78rem; color:#94a3b8; margin-top:0.6rem;">3× média de saídas mensais</p>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    pct_r = min(100, (kpis["ofertas_ensaio_total"] / 3 / meta_receita_recorrente) * 100)
    bar_cor_r = VERDE if pct_r >= 80 else LARANJA if pct_r >= 50 else VERMELHO
    st.markdown(f"""
    <div class="meta-card">
        <div class="meta-icon">🔄</div>
        <h4>Receita Recorrente</h4>
        <div class="meta-row"><span>Meta/mês</span><b>{fmt_brl(meta_receita_recorrente)}</b></div>
        <div class="meta-row"><span>Atual (média)</span><b>{fmt_brl(kpis["ofertas_ensaio_total"] / 3)}</b></div>
        <div class="meta-row"><span>Atingimento</span><b style="color:{bar_cor_r}">{fmt_pct(pct_r)}</b></div>
        <div class="meta-bar-bg"><div class="meta-bar-fill" style="width:{pct_r}%; background:linear-gradient(90deg, {bar_cor_r}, {bar_cor_r}88);"></div></div>
        <p style="font-size:0.78rem; color:#94a3b8; margin-top:0.6rem;">60% das saídas médias</p>
    </div>
    """, unsafe_allow_html=True)

with col_m3:
    _max_saida_row = resumo.loc[resumo["total_saidas"].idxmax()] if not resumo.empty else None
    _min_saida_row = resumo.loc[resumo["total_saidas"].idxmin()] if not resumo.empty else None
    _max_saida_label = f"{_max_saida_row['mes_label'][:3]} — {fmt_brl(_max_saida_row['total_saidas'])}" if _max_saida_row is not None else "—"
    _min_saida_label = f"{_min_saida_row['mes_label'][:3]} — {fmt_brl(_min_saida_row['total_saidas'])}" if _min_saida_row is not None else "—"
    st.markdown(f"""
    <div class="meta-card">
        <div class="meta-icon">📉</div>
        <h4>Teto de Saídas</h4>
        <div class="meta-row"><span>Teto sugerido</span><b>{fmt_brl(kpis["media_saidas_mensal"])}</b></div>
        <div class="meta-row"><span>Maior mês</span><b style="color:{VERMELHO}">{_max_saida_label}</b></div>
        <div class="meta-row"><span>Menor mês</span><b style="color:{VERDE}">{_min_saida_label}</b></div>
        <div class="meta-bar-bg"><div class="meta-bar-fill" style="width:65%; background:linear-gradient(90deg, {LARANJA}, {LARANJA}88);"></div></div>
        <p style="font-size:0.78rem; color:#94a3b8; margin-top:0.6rem;">Gastos &gt; R$ 200 com aprovação</p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SEÇÃO 9 — COMPOSIÇÃO DE RECEITAS
# ══════════════════════════════════════════════

section_header("💰", "Composição das Receitas", "De onde vem o dinheiro — análise de sustentabilidade", color="#3B82F6")

col_ent_donut, col_ent_info = st.columns([1, 1])

with col_ent_donut:
    fig_ent = go.Figure(data=[go.Pie(
        labels=entradas_cat["categoria"], values=entradas_cat["total"],
        hole=0.6,
        marker=dict(colors=[VERDE, LARANJA, "#3B82F6"], line=dict(color="white", width=3)),
        textinfo="label+percent",
        textposition="outside",
        textfont=dict(size=12, weight="bold"),
    )])
    fig_ent.update_layout(
        **{**PLOTLY_LAYOUT, "margin": dict(t=20, b=20, l=40, r=40)},
        showlegend=False, height=380,
        annotations=[dict(
            text=f"<b>{fmt_brl(kpis['total_entradas'])}</b><br><span style='font-size:11px;color:#94a3b8'>Total</span>",
            x=0.5, y=0.5, font_size=15, showarrow=False,
        )],
    )
    st.plotly_chart(fig_ent, width='stretch')

with col_ent_info:
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("##### Análise de Sustentabilidade")
    st.markdown(f"""
- 🟢 **Ofertas de Ensaio (recorrente):** {fmt_brl(kpis["ofertas_ensaio_total"])} — **{fmt_pct(kpis["pct_recorrente"])}** do total
- 🟡 **Eventos/Arrecadações:** {fmt_brl(kpis["total_entradas"] - kpis["ofertas_ensaio_total"])} — **{fmt_pct(100 - kpis["pct_recorrente"])}** do total
- 🔴 **Risco:** Maior entrada única (Sorteio Jan R$ 1.410) = **{fmt_pct(kpis["concentracao_receita"])}** da receita
    """)

    st.markdown(f"""
    <div class="alert aviso">
        <div class="alert-icon">📊</div>
        <div class="alert-body">
            <p class="alert-title">Benchmark de Mercado</p>
            <p class="alert-text">
                Organizações saudáveis mantêm <b>50-60%</b> de receita recorrente.
                O Sublime Som está em <b>~{fmt_pct(kpis["pct_recorrente"])}</b>.
                Este é o principal ponto de melhoria estratégica.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SEÇÃO 10 — RECOMENDAÇÕES
# ══════════════════════════════════════════════

section_header("💼", "Recomendações Estratégicas", "Ações práticas baseadas na análise dos dados", color=VERDE)

recomendacoes = [
    ("Diversificar Fontes de Receita",
     "Atualmente, <b>79,5%</b> da receita vem de eventos pontuais. "
     "Criar pelo menos 2 fontes recorrentes: contribuição mensal voluntária, "
     "venda de produtos, rifas programadas."),
    ("Formalizar Política de Empréstimos",
     "R$ 820 saíram como empréstimos/adiantamentos no trimestre = <b>45%</b> das saídas. "
     "Definir política escrita: limite, prazo, aprovação dupla, registro assinado."),
    ("Aprovação para Gastos Acima de R$ 200",
     "Despesas elevadas (R$ 500, R$ 320, R$ 266) sem aprovação documentada. "
     "Exigir autorização escrita de 2 líderes antes da execução."),
    ("Evento de Arrecadação Todo Mês",
     "Meses com evento = superávit. Sem evento (Fev) = déficit. "
     "Criar calendário fixo: 1 evento/mês mínimo (sorteio, lava car, bazar, etc)."),
    ("Criar Fundo de Reserva",
     f"Saldo cobre apenas <b>{kpis['reserva_em_meses']:.1f} meses</b>. Meta: 3 meses. "
     f"Reservar 20% de toda arrecadação de eventos até atingir {fmt_brl(meta_reserva_3m)}."),
    ("Padronizar Classificação de Despesas",
     "Descrições genéricas dificultam análise. "
     "Adotar categorias fixas (Operacional, Eventos, Material, Pessoal) "
     "e sempre registrar beneficiário + finalidade."),
]

for i, (titulo, texto) in enumerate(recomendacoes, 1):
    st.markdown(f"""
    <div class="rec-card">
        <h4><span class="rec-num">{i}</span> {titulo}</h4>
        <p>{texto}</p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════

st.markdown("---")
st.markdown(f"""
<div class="footer">
    <span class="footer-brand">🎵 Caixa Sublime Som</span><br>
    Dashboard Financeiro Executivo<br>
    Relatório gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M")} · Período: {_primeiro_mes} – {_ultimo_mes}<br>
    Dados extraídos dos relatórios de caixa mensais<br><br>
    <em>Uso interno — Prestação de contas à liderança do grupo Sublime Som</em>
</div>
""", unsafe_allow_html=True)