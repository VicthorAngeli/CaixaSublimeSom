"""
Caixa Sublime Som — Módulo de Dados (Dinâmico)
Dados salvos em dados.json. Se não existir, usa dados padrão.
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent / "dados.json"

MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
}

ORDEM_MESES_ANO = list(MESES_PT.values())

# ──────────────────────────────────────────────
# DADOS PADRÃO (seed) — 100% fiéis aos relatórios
# ──────────────────────────────────────────────

_SALDO_INICIAL_PADRAO = 77.34

# Saldos anteriores reais de cada mês (conforme relatórios originais).
# Entre os meses há movimentações não registradas nas transações,
# por isso os saldos NÃO podem ser simplesmente calculados.
_SALDOS_ANTERIORES_PADRAO = {
    "Janeiro": 77.34,
    "Fevereiro": 990.61,
    "Março": 510.77,
}

_TRANSACOES_PADRAO = [
    {"data": "2026-01-04", "mes": "Janeiro",   "descricao": "Oferta Ensaio",                        "entrada": 55.00,    "saida": 0},
    {"data": "2026-01-06", "mes": "Janeiro",   "descricao": "Valor do banner devocional",            "entrada": 0,        "saida": 25.00},
    {"data": "2026-01-07", "mes": "Janeiro",   "descricao": "Decoração Maricleide",                  "entrada": 0,        "saida": 100.00},
    {"data": "2026-01-11", "mes": "Janeiro",   "descricao": "Oferta Ensaio",                        "entrada": 95.32,    "saida": 0},
    {"data": "2026-01-16", "mes": "Janeiro",   "descricao": "Itens Devocional (Pulseiras e etc)",    "entrada": 0,        "saida": 42.25},
    {"data": "2026-01-21", "mes": "Janeiro",   "descricao": "Pagamento Enjadec",                     "entrada": 0,        "saida": 50.00},
    {"data": "2026-01-24", "mes": "Janeiro",   "descricao": "Lembrancinhas Devocional",              "entrada": 0,        "saida": 89.90},
    {"data": "2026-01-25", "mes": "Janeiro",   "descricao": "Arrecadação sorteio",                   "entrada": 1410.00,  "saida": 0},
    {"data": "2026-02-01", "mes": "Fevereiro", "descricao": "Aniversário David",                     "entrada": 0,        "saida": 50.00},
    {"data": "2026-02-08", "mes": "Fevereiro", "descricao": "Joum David",                            "entrada": 0,        "saida": 500.00},
    {"data": "2026-02-08", "mes": "Fevereiro", "descricao": "Oferta ensaio",                         "entrada": 155.00,   "saida": 0},
    {"data": "2026-03-01", "mes": "Março",     "descricao": "Oferta Ensaio",                         "entrada": 35.00,    "saida": 0},
    {"data": "2026-03-06", "mes": "Março",     "descricao": "David (p/ simpósio, vai devolver)",      "entrada": 0,        "saida": 320.00},
    {"data": "2026-03-08", "mes": "Março",     "descricao": "Oferta Ensaio",                         "entrada": 265.34,   "saida": 0},
    {"data": "2026-03-09", "mes": "Março",     "descricao": "Material Lava Car",                     "entrada": 0,        "saida": 84.04},
    {"data": "2026-03-14", "mes": "Março",     "descricao": "Café e almoço lava rápido",             "entrada": 0,        "saida": 72.28},
    {"data": "2026-03-14", "mes": "Março",     "descricao": "Lava Car",                              "entrada": 450.00,   "saida": 0},
    {"data": "2026-03-18", "mes": "Março",     "descricao": "Sorteio Bolo",                          "entrada": 480.00,   "saida": 0},
    {"data": "2026-03-18", "mes": "Março",     "descricao": "Lembrancinha dia das mulheres",         "entrada": 0,        "saida": 52.00},
    {"data": "2026-03-18", "mes": "Março",     "descricao": "Bolo Red",                              "entrada": 0,        "saida": 110.00},
    {"data": "2026-03-18", "mes": "Março",     "descricao": "Parte das Lembrancinhas",               "entrada": 0,        "saida": 266.34},
    {"data": "2026-03-18", "mes": "Março",     "descricao": "Pagamento Enjadec",                     "entrada": 0,        "saida": 50.00},
]

# ──────────────────────────────────────────────
# PERSISTÊNCIA (JSON)
# ──────────────────────────────────────────────

def _load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return (
            data.get("saldo_inicial", _SALDO_INICIAL_PADRAO),
            data.get("transacoes", []),
            data.get("saldos_anteriores", dict(_SALDOS_ANTERIORES_PADRAO)),
        )
    return _SALDO_INICIAL_PADRAO, list(_TRANSACOES_PADRAO), dict(_SALDOS_ANTERIORES_PADRAO)


def _save_data(saldo_inicial, transacoes, saldos_anteriores=None):
    if saldos_anteriores is None:
        _, _, saldos_anteriores = _load_data()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {
                "saldo_inicial": round(saldo_inicial, 2),
                "transacoes": transacoes,
                "saldos_anteriores": saldos_anteriores,
            },
            f, ensure_ascii=False, indent=2,
        )


def adicionar_transacao(data_str, descricao, entrada, saida):
    saldo_ini, trans, saldos_ant = _load_data()
    dt = datetime.strptime(data_str, "%Y-%m-%d")
    mes = MESES_PT[dt.month]
    trans.append({
        "data": data_str,
        "mes": mes,
        "descricao": descricao,
        "entrada": round(float(entrada), 2),
        "saida": round(float(saida), 2),
    })
    trans.sort(key=lambda t: t["data"])
    _save_data(saldo_ini, trans, saldos_ant)


def remover_transacao(idx):
    saldo_ini, trans, saldos_ant = _load_data()
    if 0 <= idx < len(trans):
        trans.pop(idx)
        _save_data(saldo_ini, trans, saldos_ant)


def atualizar_saldo_inicial(novo_saldo):
    _, trans, saldos_ant = _load_data()
    _save_data(float(novo_saldo), trans, saldos_ant)


def get_saldo_inicial():
    s, _, _ = _load_data()
    return s


def atualizar_saldo_anterior_mes(mes, valor):
    """Define o saldo anterior real de um mês específico."""
    saldo_ini, trans, saldos_ant = _load_data()
    saldos_ant[mes] = round(float(valor), 2)
    _save_data(saldo_ini, trans, saldos_ant)


def get_saldos_anteriores():
    _, _, sa = _load_data()
    return sa


def restaurar_padrao():
    if DATA_FILE.exists():
        DATA_FILE.unlink()


# ──────────────────────────────────────────────
# CATEGORIZAÇÃO AUTOMÁTICA
# ──────────────────────────────────────────────

_REGRAS_CATEGORIA = [
    (["oferta", "ensaio"],                          "Ofertas (Ensaios)"),
    (["arrecadação", "sorteio bolo", "sorteio"],    "Eventos / Arrecadações"),
    (["lava car"],                                  "Eventos / Arrecadações"),
    (["aniversário"],                               "Celebrações / Homenagens"),
    (["lembrancinha", "lembrancinhas"],              "Celebrações / Homenagens"),
    (["dia das mulheres"],                          "Celebrações / Homenagens"),
    (["decoração", "banner", "itens devocional",
     "pulseiras", "bolo red", "bolo"],              "Material / Decoração"),
    (["enjadec"],                                   "Operacional / Fixo"),
    (["material lava"],                             "Operacional / Evento"),
    (["café", "almoço"],                            "Operacional / Evento"),
    (["simpósio", "joum david", "david"],           "Empréstimos / Adiantamentos"),
]


def _categorizar(descricao: str) -> str:
    desc_lower = descricao.lower()
    for palavras, categoria in _REGRAS_CATEGORIA:
        for p in palavras:
            if p in desc_lower:
                return categoria
    return "Outros"


def _tipo_fluxo(row) -> str:
    return "Entrada" if row["entrada"] > 0 else "Saída"


# ──────────────────────────────────────────────
# DATAFRAME PRINCIPAL
# ──────────────────────────────────────────────

MESES_ORDEM = []


def get_transacoes() -> pd.DataFrame:
    _, transacoes_raw, _ = _load_data()

    if not transacoes_raw:
        MESES_ORDEM.clear()
        return pd.DataFrame(columns=[
            "data", "mes", "descricao", "entrada", "saida",
            "categoria", "tipo", "valor", "mes_num",
        ])

    df = pd.DataFrame(transacoes_raw)
    df["data"] = pd.to_datetime(df["data"])
    df["categoria"] = df["descricao"].apply(_categorizar)
    df["tipo"] = df.apply(_tipo_fluxo, axis=1)
    df["valor"] = df["entrada"] + df["saida"]
    df["mes_num"] = df["data"].dt.month

    # Ordenar meses pela primeira data
    df_sorted = df.sort_values("data")
    meses = list(dict.fromkeys(df_sorted["mes"].tolist()))

    MESES_ORDEM.clear()
    MESES_ORDEM.extend(meses)

    df["mes"] = pd.Categorical(df["mes"], categories=meses, ordered=True)
    return df


# ──────────────────────────────────────────────
# RESUMO MENSAL
# ──────────────────────────────────────────────

def get_resumo_mensal() -> pd.DataFrame:
    df = get_transacoes()
    if df.empty:
        return pd.DataFrame()

    saldo_ini = get_saldo_inicial()
    saldos_anteriores = get_saldos_anteriores()

    resumo = df.groupby("mes", observed=False).agg(
        total_entradas=("entrada", "sum"),
        total_saidas=("saida", "sum"),
        qtd_transacoes=("descricao", "count"),
    ).reset_index()

    saldo_calculado = saldo_ini
    saldos_ant_list = []
    saldos_fin_list = []
    for _, row in resumo.iterrows():
        mes_nome = str(row["mes"])
        if mes_nome in saldos_anteriores:
            sa = saldos_anteriores[mes_nome]
        else:
            sa = round(saldo_calculado, 2)
        saldos_ant_list.append(sa)
        sf = round(sa + row["total_entradas"] - row["total_saidas"], 2)
        saldos_fin_list.append(sf)
        saldo_calculado = sf

    resumo["saldo_anterior"] = saldos_ant_list
    resumo["saldo_final"] = saldos_fin_list
    resumo["resultado_mensal"] = resumo["total_entradas"] - resumo["total_saidas"]
    resumo["indice_cobertura"] = resumo.apply(
        lambda r: r["total_entradas"] / r["total_saidas"] if r["total_saidas"] > 0 else float("inf"),
        axis=1,
    )
    resumo["mes_label"] = resumo["mes"].astype(str)

    return resumo


# ──────────────────────────────────────────────
# KPIs EXECUTIVOS
# ──────────────────────────────────────────────

def get_kpis() -> dict:
    df = get_transacoes()
    resumo = get_resumo_mensal()

    _zero = {
        "saldo_atual": 0, "total_entradas": 0, "total_saidas": 0,
        "resultado_liquido": 0, "media_entradas_mensal": 0,
        "media_saidas_mensal": 0, "reserva_em_meses": 0,
        "variacao_saldo_ultimo": 0, "maior_entrada": 0,
        "concentracao_receita": 0, "pct_recorrente": 0,
        "emprestimo_pendente": 0, "indice_cobertura_tri": 0,
        "ticket_medio_saida": 0, "ofertas_ensaio_total": 0,
    }
    if df.empty:
        return _zero

    total_entradas = df["entrada"].sum()
    total_saidas = df["saida"].sum()
    resultado_liquido = total_entradas - total_saidas

    n_meses = max(len(MESES_ORDEM), 1)

    saldo_atual = resumo.iloc[-1]["saldo_final"]
    media_entradas_mensal = total_entradas / n_meses
    media_saidas_mensal = total_saidas / n_meses
    reserva_em_meses = saldo_atual / media_saidas_mensal if media_saidas_mensal > 0 else 0

    if len(resumo) >= 2:
        sp = resumo.iloc[-2]["saldo_final"]
        su = resumo.iloc[-1]["saldo_final"]
        variacao_saldo_ultimo = ((su - sp) / sp * 100) if sp else 0
    else:
        variacao_saldo_ultimo = 0

    entradas_df = df[df["entrada"] > 0]
    maior_entrada = entradas_df["entrada"].max() if len(entradas_df) > 0 else 0
    concentracao_receita = (maior_entrada / total_entradas * 100) if total_entradas else 0

    ofertas_ensaio = df.loc[
        df["descricao"].str.lower().str.contains("oferta", na=False), "entrada"
    ].sum()
    pct_recorrente = (ofertas_ensaio / total_entradas * 100) if total_entradas else 0

    emp_df = df[df["categoria"] == "Empréstimos / Adiantamentos"]
    emprestimo_pendente = emp_df["saida"].sum()

    indice_cobertura_tri = total_entradas / total_saidas if total_saidas else 0

    saidas_df = df[df["saida"] > 0]
    ticket_medio_saida = saidas_df["saida"].mean() if len(saidas_df) > 0 else 0

    return {
        "saldo_atual": saldo_atual,
        "total_entradas": total_entradas,
        "total_saidas": total_saidas,
        "resultado_liquido": resultado_liquido,
        "media_entradas_mensal": media_entradas_mensal,
        "media_saidas_mensal": media_saidas_mensal,
        "reserva_em_meses": reserva_em_meses,
        "variacao_saldo_ultimo": variacao_saldo_ultimo,
        "maior_entrada": maior_entrada,
        "concentracao_receita": concentracao_receita,
        "pct_recorrente": pct_recorrente,
        "emprestimo_pendente": emprestimo_pendente,
        "indice_cobertura_tri": indice_cobertura_tri,
        "ticket_medio_saida": ticket_medio_saida,
        "ofertas_ensaio_total": ofertas_ensaio,
    }


# ──────────────────────────────────────────────
# SAÍDAS POR CATEGORIA
# ──────────────────────────────────────────────

def get_saidas_por_categoria() -> pd.DataFrame:
    df = get_transacoes()
    if df.empty:
        return pd.DataFrame(columns=["categoria", "total", "qtd", "percentual"])
    saidas = df[df["saida"] > 0].copy()
    if saidas.empty:
        return pd.DataFrame(columns=["categoria", "total", "qtd", "percentual"])
    cat = saidas.groupby("categoria").agg(
        total=("saida", "sum"),
        qtd=("descricao", "count"),
    ).reset_index()
    cat = cat.sort_values("total", ascending=False)
    cat["percentual"] = (cat["total"] / cat["total"].sum() * 100).round(1)
    return cat


def get_entradas_por_categoria() -> pd.DataFrame:
    df = get_transacoes()
    if df.empty:
        return pd.DataFrame(columns=["categoria", "total", "qtd", "percentual"])
    entradas = df[df["entrada"] > 0].copy()
    if entradas.empty:
        return pd.DataFrame(columns=["categoria", "total", "qtd", "percentual"])
    cat = entradas.groupby("categoria").agg(
        total=("entrada", "sum"),
        qtd=("descricao", "count"),
    ).reset_index()
    cat = cat.sort_values("total", ascending=False)
    cat["percentual"] = (cat["total"] / cat["total"].sum() * 100).round(1)
    return cat


# ──────────────────────────────────────────────
# TOP DESPESAS
# ──────────────────────────────────────────────

def get_top_despesas(n: int = 10) -> pd.DataFrame:
    df = get_transacoes()
    if df.empty:
        return pd.DataFrame(columns=["data", "mes", "descricao", "saida", "categoria"])
    saidas = df[df["saida"] > 0][["data", "mes", "descricao", "saida", "categoria"]].copy()
    saidas = saidas.sort_values("saida", ascending=False).head(n).reset_index(drop=True)
    return saidas


# ──────────────────────────────────────────────
# PROJEÇÃO SIMPLES (próximos 3 meses)
# ──────────────────────────────────────────────

def get_projecao() -> pd.DataFrame:
    kpis = get_kpis()
    resumo = get_resumo_mensal()

    if resumo.empty:
        return pd.DataFrame()

    ultimo_mes = str(resumo.iloc[-1]["mes"])
    try:
        idx = ORDEM_MESES_ANO.index(ultimo_mes)
    except ValueError:
        idx = 0

    meses_futuros = [ORDEM_MESES_ANO[(idx + 1 + i) % 12] for i in range(3)]

    saldo = kpis["saldo_atual"]
    rows = []
    for mes in meses_futuros:
        entrada_proj = kpis["media_entradas_mensal"]
        saida_proj = kpis["media_saidas_mensal"]
        saldo_ant = saldo
        saldo = saldo_ant + entrada_proj - saida_proj
        rows.append({
            "mes": mes,
            "entrada_projetada": round(entrada_proj, 2),
            "saida_projetada": round(saida_proj, 2),
            "saldo_anterior": round(saldo_ant, 2),
            "saldo_projetado": round(saldo, 2),
        })
    return pd.DataFrame(rows)


# ──────────────────────────────────────────────
# DIAGNÓSTICO FINANCEIRO (problemas + soluções)
# ──────────────────────────────────────────────

def get_diagnostico() -> dict:
    """Analisa os dados e retorna problemas e soluções baseados em evidências."""
    df = get_transacoes()
    kpis = get_kpis()
    resumo = get_resumo_mensal()
    saldos_ant = get_saldos_anteriores()

    if df.empty:
        return {"problemas": [], "solucoes": [], "impacto_total_estimado": 0}

    total_entradas = kpis["total_entradas"]
    total_saidas = kpis["total_saidas"]
    n_meses = max(len(MESES_ORDEM), 1)

    problemas = []
    solucoes = []

    # ── Problema 1: Concentração de receita em eventos pontuais ──
    ofertas = df.loc[df["descricao"].str.lower().str.contains("oferta", na=False), "entrada"].sum()
    receita_eventos = total_entradas - ofertas
    pct_eventos = (receita_eventos / total_entradas * 100) if total_entradas > 0 else 0
    of_mensal = []
    for m in MESES_ORDEM:
        of_mes = df[(df["mes"] == m) & (df["descricao"].str.lower().str.contains("oferta", na=False))]["entrada"].sum()
        of_mensal.append(of_mes)
    of_min = min(of_mensal) if of_mensal else 0
    of_max = max(of_mensal) if of_mensal else 0

    if pct_eventos > 50:
        problemas.append({
            "titulo": "Receita concentrada em eventos pontuais",
            "icon": "📊",
            "gravidade": "critico",
            "texto": f"Eventos e arrecadações = <b>R$ {receita_eventos:,.2f}</b> "
                     f"(<b>{pct_eventos:.0f}%</b> da receita total). "
                     f"Ofertas de ensaio (receita recorrente) variaram de "
                     f"R$ {of_min:,.2f} a R$ {of_max:,.2f}/mês — instável e insuficiente. "
                     f"Meses sem evento geram <b>déficit</b>.",
            "evidencia": f"{pct_eventos:.0f}% eventos vs {100-pct_eventos:.0f}% recorrente",
        })
        solucoes.append({
            "titulo": "Criar contribuição mensal fixa dos membros",
            "icon": "💳",
            "texto": f"Ofertas de ensaio são instáveis (R$ {of_min:,.2f}–R$ {of_max:,.2f}/mês). "
                     f"Estabelecer cota fixa mensal (ex: R$ 20/membro). Com 15 membros = "
                     f"<b>R$ 300/mês garantidos</b>, criando base que sustenta o caixa sem depender de eventos.",
            "impacto": "+ R$ 300/mês",
        })

    # ── Problema 2: Empréstimos pessoais drenando o caixa ──
    emp_df = df[df["categoria"] == "Empréstimos / Adiantamentos"]
    emprestimo_total = emp_df["saida"].sum()
    pct_emp = (emprestimo_total / total_saidas * 100) if total_saidas > 0 else 0
    devolver = df[df["descricao"].str.lower().str.contains("devolver", na=False)]
    pendente_devolver = devolver["saida"].sum()

    if emprestimo_total > 0:
        txt_devolver = ""
        if pendente_devolver > 0:
            txt_devolver = f" Há <b>R$ {pendente_devolver:,.2f}</b> com promessa de devolução ainda pendente."
        problemas.append({
            "titulo": "Empréstimos pessoais drenando o caixa",
            "icon": "🏦",
            "gravidade": "critico" if pct_emp > 30 else "aviso",
            "texto": f"Saídas como empréstimos/adiantamentos = <b>R$ {emprestimo_total:,.2f}</b> "
                     f"(<b>{pct_emp:.0f}%</b> de todas as saídas). "
                     f"São gastos pessoais, não do grupo.{txt_devolver}",
            "evidencia": f"R$ {emprestimo_total:,.2f} = {pct_emp:.0f}% das saídas",
        })
        solucoes.append({
            "titulo": "Política rígida de empréstimos",
            "icon": "📋",
            "texto": f"Regra: máx R$ 200/empréstimo, devolução em 30 dias, aprovação coletiva &gt; R$ 100. "
                     f"<b>Cobrar imediatamente os R$ {pendente_devolver:,.2f} pendentes</b>. "
                     f"Se todos os R$ {emprestimo_total:,.2f} voltarem, saldo sobe para "
                     f"<b>R$ {kpis['saldo_atual'] + emprestimo_total:,.2f}</b>.",
            "impacto": f"+ R$ {emprestimo_total:,.2f}",
        })

    # ── Problema 3: Movimentações sem registro entre meses ──
    gap_total = 0.0
    gaps = []
    for i in range(len(resumo) - 1):
        sf = resumo.iloc[i]["saldo_final"]
        prox_mes = str(resumo.iloc[i + 1]["mes"])
        sa_prox = saldos_ant.get(prox_mes, sf)
        gap = sf - sa_prox
        if abs(gap) > 0.01:
            gaps.append((str(resumo.iloc[i]["mes"]), prox_mes, gap))
            gap_total += gap

    if abs(gap_total) > 0.01:
        detalhes = "; ".join([f"{a}→{b}: R$ {g:,.2f}" for a, b, g in gaps])
        problemas.append({
            "titulo": "Movimentações sem registro entre meses",
            "icon": "👻",
            "gravidade": "critico" if gap_total > 200 else "aviso",
            "texto": f"<b>R$ {gap_total:,.2f}</b> saíram do caixa sem transação registrada. "
                     f"Detalhes: {detalhes}. "
                     f"Dinheiro saindo sem controle = impossível prestar contas.",
            "evidencia": f"R$ {gap_total:,.2f} não rastreados",
        })
        solucoes.append({
            "titulo": "Registrar 100% das movimentações",
            "icon": "📝",
            "texto": f"Os R$ {gap_total:,.2f} não rastreados precisam parar de existir. "
                     f"<b>Toda saída e entrada — por menor que seja — deve entrar no sistema no mesmo dia.</b> "
                     f"Designar um responsável único para registro. O dashboard já tem o formulário na sidebar.",
            "impacto": f"+ R$ {gap_total:,.2f}/tri",
        })

    # ── Impacto total estimado ──
    impacto_total = 0.0
    if pct_eventos > 50:
        impacto_total += 300 * 3
    impacto_total += emprestimo_total
    impacto_total += abs(gap_total)

    return {
        "problemas": problemas,
        "solucoes": solucoes,
        "impacto_total_estimado": round(impacto_total, 2),
    }
