"""
Caixa Sublime Som — Módulo de Dados
Estrutura, categorização e cálculos de KPIs financeiros.
"""

import pandas as pd
import numpy as np
from datetime import datetime

# ──────────────────────────────────────────────
# 1. TRANSAÇÕES BRUTAS (extraídas dos relatórios)
# ──────────────────────────────────────────────

_transacoes_raw = [
    # Janeiro
    {"data": "2026-01-04", "mes": "Janeiro",   "descricao": "Oferta Ensaio",                        "entrada": 55.00,    "saida": 0},
    {"data": "2026-01-06", "mes": "Janeiro",   "descricao": "Valor do banner devocional",            "entrada": 0,        "saida": 25.00},
    {"data": "2026-01-07", "mes": "Janeiro",   "descricao": "Decoração Maricleide",                  "entrada": 0,        "saida": 100.00},
    {"data": "2026-01-11", "mes": "Janeiro",   "descricao": "Oferta Ensaio",                        "entrada": 95.32,    "saida": 0},
    {"data": "2026-01-16", "mes": "Janeiro",   "descricao": "Itens Devocional (Pulseiras e etc)",    "entrada": 0,        "saida": 42.25},
    {"data": "2026-01-21", "mes": "Janeiro",   "descricao": "Pagamento Enjadec",                     "entrada": 0,        "saida": 50.00},
    {"data": "2026-01-24", "mes": "Janeiro",   "descricao": "Lembrancinhas Devocional",              "entrada": 0,        "saida": 89.90},
    {"data": "2026-01-25", "mes": "Janeiro",   "descricao": "Arrecadação sorteio",                   "entrada": 1410.00,  "saida": 0},
    # Fevereiro
    {"data": "2026-02-01", "mes": "Fevereiro", "descricao": "Aniversário David",                     "entrada": 0,        "saida": 50.00},
    {"data": "2026-02-08", "mes": "Fevereiro", "descricao": "Joum David",                            "entrada": 0,        "saida": 500.00},
    {"data": "2026-02-08", "mes": "Fevereiro", "descricao": "Oferta ensaio",                         "entrada": 155.00,   "saida": 0},
    # Março
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
# 2. CATEGORIZAÇÃO AUTOMÁTICA
# ──────────────────────────────────────────────

_REGRAS_CATEGORIA = [
    # (palavras-chave na descrição, categoria atribuída)
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
    if row["entrada"] > 0:
        return "Entrada"
    return "Saída"


# ──────────────────────────────────────────────
# 3. DATAFRAME PRINCIPAL
# ──────────────────────────────────────────────

def get_transacoes() -> pd.DataFrame:
    df = pd.DataFrame(_transacoes_raw)
    df["data"] = pd.to_datetime(df["data"])
    df["categoria"] = df["descricao"].apply(_categorizar)
    df["tipo"] = df.apply(_tipo_fluxo, axis=1)
    df["valor"] = df["entrada"] + df["saida"]
    df["mes_num"] = df["data"].dt.month
    # Ordem fixa dos meses
    df["mes"] = pd.Categorical(df["mes"], categories=["Janeiro", "Fevereiro", "Março"], ordered=True)
    return df


# ──────────────────────────────────────────────
# 4. RESUMO MENSAL
# ──────────────────────────────────────────────

_SALDOS = {
    "Janeiro":   {"saldo_anterior": 77.34,  "saldo_final": 1330.51},
    "Fevereiro": {"saldo_anterior": 990.61, "saldo_final": 595.61},
    "Março":     {"saldo_anterior": 510.77, "saldo_final": 786.45},
}

MESES_ORDEM = ["Janeiro", "Fevereiro", "Março"]


def get_resumo_mensal() -> pd.DataFrame:
    df = get_transacoes()
    resumo = df.groupby("mes", observed=False).agg(
        total_entradas=("entrada", "sum"),
        total_saidas=("saida", "sum"),
        qtd_transacoes=("descricao", "count"),
    ).reset_index()

    resumo["saldo_anterior"] = resumo["mes"].map(lambda m: _SALDOS[m]["saldo_anterior"])
    resumo["saldo_final"] = resumo["mes"].map(lambda m: _SALDOS[m]["saldo_final"])
    resumo["resultado_mensal"] = resumo["total_entradas"] - resumo["total_saidas"]
    resumo["indice_cobertura"] = resumo["total_entradas"] / resumo["total_saidas"]
    resumo["mes_label"] = resumo["mes"].astype(str)

    return resumo


# ──────────────────────────────────────────────
# 5. KPIs EXECUTIVOS
# ──────────────────────────────────────────────

def get_kpis() -> dict:
    df = get_transacoes()
    resumo = get_resumo_mensal()

    total_entradas = df["entrada"].sum()
    total_saidas = df["saida"].sum()
    resultado_liquido = total_entradas - total_saidas
    saldo_atual = _SALDOS["Março"]["saldo_final"]
    media_entradas_mensal = total_entradas / 3
    media_saidas_mensal = total_saidas / 3
    reserva_em_meses = saldo_atual / media_saidas_mensal if media_saidas_mensal > 0 else 0

    # Variação do saldo mês a mês
    saldo_fev = _SALDOS["Fevereiro"]["saldo_final"]
    saldo_mar = _SALDOS["Março"]["saldo_final"]
    variacao_saldo_ultimo = ((saldo_mar - saldo_fev) / saldo_fev * 100) if saldo_fev else 0

    # Concentração de receita (maior entrada única / total entradas)
    maior_entrada = df.loc[df["entrada"] > 0, "entrada"].max()
    concentracao_receita = (maior_entrada / total_entradas * 100) if total_entradas else 0

    # Receita recorrente (ofertas de ensaio) vs eventual
    ofertas_ensaio = df.loc[df["descricao"].str.lower().str.contains("oferta"), "entrada"].sum()
    pct_recorrente = (ofertas_ensaio / total_entradas * 100) if total_entradas else 0

    # Empréstimo pendente
    emprestimo_pendente = 320.00  # David - simpósio

    # Índice de cobertura trimestral
    indice_cobertura_tri = total_entradas / total_saidas if total_saidas else 0

    # Ticket médio de saída
    saidas_df = df[df["saida"] > 0]
    ticket_medio_saida = saidas_df["saida"].mean()

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
# 6. SAÍDAS POR CATEGORIA
# ──────────────────────────────────────────────

def get_saidas_por_categoria() -> pd.DataFrame:
    df = get_transacoes()
    saidas = df[df["saida"] > 0].copy()
    cat = saidas.groupby("categoria").agg(
        total=("saida", "sum"),
        qtd=("descricao", "count"),
    ).reset_index()
    cat = cat.sort_values("total", ascending=False)
    cat["percentual"] = (cat["total"] / cat["total"].sum() * 100).round(1)
    return cat


def get_entradas_por_categoria() -> pd.DataFrame:
    df = get_transacoes()
    entradas = df[df["entrada"] > 0].copy()
    cat = entradas.groupby("categoria").agg(
        total=("entrada", "sum"),
        qtd=("descricao", "count"),
    ).reset_index()
    cat = cat.sort_values("total", ascending=False)
    cat["percentual"] = (cat["total"] / cat["total"].sum() * 100).round(1)
    return cat


# ──────────────────────────────────────────────
# 7. TOP DESPESAS
# ──────────────────────────────────────────────

def get_top_despesas(n: int = 10) -> pd.DataFrame:
    df = get_transacoes()
    saidas = df[df["saida"] > 0][["data", "mes", "descricao", "saida", "categoria"]].copy()
    saidas = saidas.sort_values("saida", ascending=False).head(n).reset_index(drop=True)
    return saidas


# ──────────────────────────────────────────────
# 8. PROJEÇÃO SIMPLES (próximos 3 meses)
# ──────────────────────────────────────────────

def get_projecao() -> pd.DataFrame:
    kpis = get_kpis()
    meses_futuros = ["Abril", "Maio", "Junho"]
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
