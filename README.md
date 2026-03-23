# 🎵 Caixa Sublime Som — Dashboard Financeiro

Dashboard executivo interativo para acompanhamento financeiro do grupo **Sublime Som**.

## Visão Geral

Este dashboard transforma os dados mensais de caixa (entradas, saídas, saldo) em um painel estratégico com:

- **KPIs Executivos** — Saldo, Entradas, Saídas, Resultado Líquido, Índice de Cobertura
- **Gráficos Interativos** — Entradas vs Saídas, Evolução do Saldo, Categorias, Top Despesas
- **Indicadores de Saúde Financeira** — Semáforos de Cobertura, Reserva, Concentração
- **Alertas e Pontos de Atenção** — Empréstimos pendentes, riscos, gastos atípicos
- **Projeção de Caixa** — Estimativa para os próximos 3 meses
- **Metas Financeiras** — Reserva de segurança, receita recorrente, teto de gastos
- **Recomendações Estratégicas** — Ações práticas para melhoria financeira

## Como Executar

### Pré-requisitos

- Python 3.9 ou superior instalado
- pip (gerenciador de pacotes do Python)

### Instalação

```bash
# 1. Abrir terminal na pasta do projeto
cd CaixaSublimeSom

# 2. (Opcional) Criar ambiente virtual
python -m venv venv
venv\Scripts\activate     # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Instalar dependências
pip install -r requirements.txt
```

### Executar o Dashboard

```bash
streamlit run app.py
```

O dashboard abrirá automaticamente no navegador em `http://localhost:8501`.

## Estrutura do Projeto

```
CaixaSublimeSom/
├── app.py                  # Dashboard principal (Streamlit)
├── data.py                 # Dados, categorização e cálculos de KPIs
├── requirements.txt        # Dependências Python
├── README.md               # Este arquivo
└── .streamlit/
    └── config.toml         # Tema visual customizado
```

## Período dos Dados

- **Janeiro 2026** — 8 transações
- **Fevereiro 2026** — 3 transações
- **Março 2026** — 11 transações

## Tecnologias

- **Streamlit** — Framework de dashboards em Python
- **Plotly** — Gráficos interativos profissionais
- **Pandas** — Manipulação e análise de dados

---

*Dashboard desenvolvido para prestação de contas à liderança do grupo Sublime Som.*
