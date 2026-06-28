import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# CONFIGURACAO GLOBAL
st.set_page_config(
    page_title="People Analytics | HR Attrition",
    layout="wide",
    initial_sidebar_state="expanded",
)

# PALETA DE CORES
COR_PERIGO   = "#E24B4A"
COR_AVISO    = "#EF9F27"
COR_OK       = "#639922"
COR_AZUL     = "#378ADD"
COR_CINZA    = "#8C9BAA"

CORES_RISCO = {
    "Critico": COR_PERIGO,
    "Alto"   : COR_AVISO,
    "Medio"  : COR_AZUL,
    "Baixo"  : COR_OK,
}

# Cores do tema roxo
ROXO_BG        = "#0e1117"
ROXO_BG_CARD   = "#14101E"
ROXO_BG_CARD2  = "#1A1425"
ROXO_BORDER    = "#2A1F3D"
ROXO_BORDER_H  = "#242424"
ROXO_ACCENT    = "#595959"
ROXO_ACCENT_H  = "#FFFFFF"
ROXO_LIGHT     = "#FFFFFF"
ROXO_TEXT      = "#F5F3FF"
ROXO_TEXT_SEC  = "#A8A8A8"
ROXO_MUTED     = "#FDFDFD"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700;800&display=swap');

/* 1. TIPOGRAFIA DO APP (IGNORA ÍCONES NATIVOS) */
.stApp, h1, h2, h3, p, div, span, label, input, button, select {{
    font-family: 'Inter', sans-serif;
}}

=[data-testid="stIcon"], 
.notranslate, 
font,
i,
[style*="Material Symbols"],
[style*="Material Icons"] {{
    font-family: 'Material Symbols Outlined', 'Material Icons' !important;
}}

.stApp {{
    background: linear-gradient(135deg, {ROXO_BG} 0%, #0e1117 50%, {ROXO_BG} 100%);
}}

[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child,
.stSidebarNav {{
    overflow: hidden !important;
    overflow-x: hidden !important;
    overflow-y: hidden !important;
    max-height: 100vh !important;
}}

[data-testid="stSidebarUserContent"] {{
    padding-top: 0rem !important; 
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    overflow: hidden !important;
    overflow-x: hidden !important;
    overflow-y: hidden !important;
}}
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0e1117 0%, #0e1117 100%);
    border-right: 1px solid {ROXO_BORDER};
}}

[data-testid="stSidebar"] * {{
    color: {ROXO_TEXT} !important;
}}

[data-testid="stSidebar"] .element-container,
[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stMultiSelect,
[data-testid="stSidebar"] .stRadio,
[data-testid="stSidebar"] div[data-baseweb="select"] {{
    overflow: hidden !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
}}

[data-testid="stSidebar"] .stRadio > div {{
    background: transparent !important;
    overflow: hidden !important;
}}

[data-testid="stSidebar"] .stRadio > div [data-baseweb="radio"] {{
    background: {ROXO_BG_CARD} !important;
    border: 1px solid {ROXO_BORDER} !important;
    border-radius: 10px !important;
    padding: 3px 3px !important;
    margin-bottom: 3px !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
    box-sizing: border-box !important;
}}

[data-testid="stSidebar"] .stRadio > div [data-baseweb="radio"]:hover {{
    background: {ROXO_BG_CARD2} !important;
    border-color: {ROXO_ACCENT} !important;
}}

[data-testid="stSidebar"] .stRadio > div [data-baseweb="radio"] label {{
    color: {ROXO_TEXT_SEC} !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    cursor: pointer !important;
}}

[data-testid="stSidebar"] .stSelectbox > div > div {{
    background: {ROXO_BG_CARD} !important;
    border: 1px solid {ROXO_BORDER} !important;
    border-radius: 8px !important;
    color: {ROXO_TEXT} !important;
}}

[data-testid="stSidebar"] .stSelectbox > div > div:focus {{
    border-color: {ROXO_ACCENT} !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
}}

[data-testid="stSidebar"] .stMultiSelect > div > div {{
    background: {ROXO_BG_CARD} !important;
    border: 1px solid {ROXO_BORDER} !important;
    border-radius: 8px !important;
}}

[data-testid="stSidebar"] .stSlider > div > div {{
    background: {ROXO_BG_CARD} !important;
}}

.metric-card {{
    background: linear-gradient(145deg, {ROXO_BG_CARD} 0%, {ROXO_BG_CARD2} 100%);
    border: 1px solid {ROXO_BORDER};
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

.metric-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, {ROXO_ACCENT}, {ROXO_ACCENT_H});
    opacity: 0;
    transition: opacity 0.3s ease;
}}

.metric-card:hover {{
    transform: translateY(-3px);
    border-color: {ROXO_BORDER_H};
    box-shadow: 0 12px 40px rgba(124, 58, 237, 0.15), 0 0 0 1px rgba(124, 58, 237, 0.1);
}}

.metric-card:hover::before {{
    opacity: 1;
}}

.metric-card .label {{
    font-size: 11px;
    color: {ROXO_MUTED};
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
    font-weight: 600;
}}

.metric-card .value {{
    font-size: 30px;
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.02em;
}}

.metric-card .sub {{
    font-size: 11px;
    color: {ROXO_MUTED};
    margin-top: 6px;
    font-weight: 400;
}}

.section-title {{
    font-size: 12px;
    font-weight: 600;
    color: {ROXO_ACCENT_H};
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 28px 0 12px;
    padding-left: 12px;
    border-left: 3px solid {ROXO_ACCENT};
}}

h1 {{
    color: {ROXO_TEXT} !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}}

h2, h3 {{
    color: {ROXO_TEXT_SEC} !important;
    font-weight: 600 !important;
}}

div[data-testid="stHorizontalBlock"] {{
    gap: 14px !important;
}}

[data-testid="stDataFrame"] {{
    border: 1px solid {ROXO_BORDER} !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}}

/* 8. SCROLLBAR CUSTOMIZADA DO CONTEÚDO PRINCIPAL */
::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
}}
::-webkit-scrollbar-track {{
    background: {ROXO_BG};
}}
::-webkit-scrollbar-thumb {{
    background: {ROXO_BORDER_H};
    border-radius: 4px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: {ROXO_ACCENT};
}}

.stCaption {{
    color: {ROXO_MUTED} !important;
}}

.stDownloadButton > button {{
    background: linear-gradient(135deg, {ROXO_ACCENT}, {ROXO_ACCENT_H}) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: all 0.3s ease !important;
}}

.stDownloadButton > button:hover {{
    box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4) !important;
    transform: translateY(-1px) !important;
}}

.stSlider [data-baseweb="slider"] [data-testid="stTickBar"] {{
    background: {ROXO_BORDER} !important;
}}
.stSlider [data-baseweb="slider"] div[role="slider"] {{
    background-color: {ROXO_ACCENT} !important;
    border-color: {ROXO_ACCENT} !important;
}}

div[data-baseweb="select"] > div {{
    background-color: {ROXO_BG_CARD} !important;
    border-color: {ROXO_BORDER} !important;
    color: {ROXO_TEXT} !important;
}}
div[data-baseweb="popover"] > div > div {{
    background-color: {ROXO_BG_CARD} !important;
    border: 1px solid {ROXO_BORDER} !important;
}}
div[data-baseweb="popover"] div[role="option"] {{
    color: {ROXO_TEXT} !important;
}}
div[data-baseweb="popover"] div[role="option"]:hover {{
    background-color: {ROXO_BG_CARD2} !important;
}}

[aria-checked="true"] > div:first-child > div {{
    background-color: {ROXO_ACCENT} !important;
}}
</style>
""", unsafe_allow_html=True)

# GERACAO DE DADOS MOCK
@st.cache_data
def gerar_dados_mock():
    """Gera dados sinteticos no mesmo schema do IBM HR Employee Attrition."""
    np.random.seed(42)
    n = 1470

    departamentos = ["Vendas", "P&D", "RH", "TI", "Marketing", "Operações", "Financeiro"]
    cargos = ["Analista Jr.", "Analista Pl.", "Analista Sr.", "Especialista", "Diretor",
              "Representante Vendas", "Técnico", "Gerente", "Cientista", "Engenheiro"]
    niveis_cargo = ["Junior", "Pleno", "Senior", "Especialista", "Diretor"]
    estado_civil = ["Solteiro(a)", "Casado(a)", "Divorciado(a)"]
    generos = ["Masculino", "Feminino"]
    freq_viagem = ["Viaja Frequentemente", "Viaja Raramente", "Não Viaja"]
    satisfacao = ["Baixo", "Medio", "Alto", "Muito Alto"]

    df = pd.DataFrame({
        "id_funcionario": range(10001, 10001 + n),
        "idade": np.random.normal(37, 9, n).clip(18, 60).astype(int),
        "genero": np.random.choice(generos, n, p=[0.6, 0.4]),
        "estado_civil": np.random.choice(estado_civil, n, p=[0.32, 0.46, 0.22]),
        "departamento": np.random.choice(departamentos, n, p=[0.28, 0.18, 0.08, 0.15, 0.10, 0.12, 0.09]),
        "cargo": np.random.choice(cargos, n),
        "nivel_cargo": np.random.choice(niveis_cargo, n, p=[0.30, 0.30, 0.20, 0.15, 0.05]),
        "frequencia_viagem": np.random.choice(freq_viagem, n, p=[0.20, 0.55, 0.25]),
        "anos_empresa": np.random.exponential(5, n).clip(0, 40).astype(int),
        "anos_desde_ultima_promocao": np.random.exponential(2, n).clip(0, 15).astype(int),
        "renda_mensal_brl": np.random.lognormal(8.2, 0.5, n).astype(int),
        "perc_aumento_salarial": np.random.choice([0, 11, 12, 13, 14, 15, 16, 20, 22, 25], n),
        "horas_extras": np.random.choice([0, 1], n, p=[0.72, 0.28]),
        "treinamentos_ultimo_ano": np.random.poisson(3, n).clip(0, 6),
        "nivel_stock_option": np.random.choice([0, 1, 2, 3], n),
        "distancia_casa": np.random.exponential(8, n).clip(1, 30).astype(int),
    })

    # Flags derivadas
    mediana_renda = df["renda_mensal_brl"].median()
    df["flag_renda_abaixo_mediana"] = (df["renda_mensal_brl"] < mediana_renda).astype(int)
    df["flag_sem_promocao_3a"] = (df["anos_desde_ultima_promocao"] >= 3).astype(int)
    df["flag_distancia_alta"] = (df["distancia_casa"] > 15).astype(int)

    # Satisfacao
    df["satisfacao_trabalho"] = np.random.choice(satisfacao, n)
    df["satisfacao_trabalho_cod"] = df["satisfacao_trabalho"].map({"Baixo":1, "Medio":2, "Alto":3, "Muito Alto":4})
    df["satisfacao_ambiente"] = np.random.choice(satisfacao, n)
    df["satisfacao_ambiente_cod"] = df["satisfacao_ambiente"].map({"Baixo":1, "Medio":2, "Alto":3, "Muito Alto":4})
    df["satisfacao_relacionamento"] = np.random.choice(satisfacao, n)
    df["satisfacao_relacionamento_cod"] = df["satisfacao_relacionamento"].map({"Baixo":1, "Medio":2, "Alto":3, "Muito Alto":4})
    df["envolvimento_trabalho"] = np.random.choice(satisfacao, n)
    df["envolvimento_trabalho_cod"] = df["envolvimento_trabalho"].map({"Baixo":1, "Medio":2, "Alto":3, "Muito Alto":4})
    df["equilibrio_vida_trabalho"] = np.random.choice(satisfacao, n)
    df["equilibrio_vida_trabalho_cod"] = df["equilibrio_vida_trabalho"].map({"Baixo":1, "Medio":2, "Alto":3, "Muito Alto":4})
    df["avaliacao_desempenho"] = np.random.choice([3, 4], n, p=[0.15, 0.85])
    df["flag_satisfacao_baixa"] = (df["satisfacao_trabalho_cod"] <= 2).astype(int)

    # Score bem-estar
    df["score_bemestar"] = df[["satisfacao_trabalho_cod", "satisfacao_ambiente_cod",
                                "equilibrio_vida_trabalho_cod"]].mean(axis=1)

    # Faixas
    df["faixa_etaria"] = pd.cut(df["idade"], bins=[17, 25, 35, 45, 55, 99],
                                  labels=["18-25", "26-35", "36-45", "46-55", "55+"]).astype(str)
    df["faixa_renda"] = pd.qcut(df["renda_mensal_brl"], 4, labels=["Baixa", "Média-Baixa", "Média-Alta", "Alta"]).astype(str)

    # Modelo de attrition
    prob = (
        0.05
        + 0.12 * df["horas_extras"]
        + 0.08 * (df["estado_civil"] == "Solteiro(a)").astype(float)
        + 0.06 * df["flag_renda_abaixo_mediana"]
        + 0.05 * (df["frequencia_viagem"] == "Viaja Frequentemente").astype(float)
        + 0.07 * df["flag_sem_promocao_3a"]
        + 0.04 * df["flag_distancia_alta"]
        + 0.10 * df["flag_satisfacao_baixa"]
        + 0.03 * (df["anos_empresa"] < 2).astype(float)
        - 0.06 * (df["score_bemestar"] > 3).astype(float)
    ).clip(0.05, 0.85)
    df["attrition"] = (np.random.random(n) < prob).astype(int)

    # Probabilidade e risco
    df["prob_attrition"] = prob + np.random.normal(0, 0.04, n)
    df["prob_attrition"] = df["prob_attrition"].clip(0.02, 0.98)

    bins_risco = [0, 0.20, 0.40, 0.60, 1.0]
    labels_risco = ["Baixo", "Medio", "Alto", "Critico"]
    df["nivel_risco_ml"] = pd.Categorical(
        pd.cut(df["prob_attrition"], bins=bins_risco, labels=labels_risco),
        categories=labels_risco, ordered=True
    )

    # Custo reposição
    multiplicador = {"Junior": 0.5, "Pleno": 0.8, "Senior": 1.2, "Especialista": 1.5, "Diretor": 2.5}
    df["custo_reposicao_est_brl"] = (df["renda_mensal_brl"] * df["nivel_cargo"].map(multiplicador) * 12).astype(int)

    # SHAP features e ações
    features = ["horas_extras", "satisfacao_baixa", "sem_promocao", "renda_baixa",
                "distancia_alta", "viagem_freq", "solteiro", "empresa_curto"]
    df["shap_top1_feat"] = np.random.choice(features, n)
    df["shap_top2_feat"] = np.random.choice(features, n)
    df["shap_top3_feat"] = np.random.choice(features, n)

    acoes = ["Conversar 1:1", "Revisar Compensação", "Reduzir horas extras",
             "Plano de desenvolvimento", "Promover", "Mudança de time", "Aumento salarial"]
    df["acao_recomendada"] = np.random.choice(acoes, n)

    # Dim satisfação
    sat = df[["id_funcionario", "satisfacao_trabalho", "satisfacao_trabalho_cod",
              "satisfacao_ambiente", "satisfacao_ambiente_cod",
              "satisfacao_relacionamento", "satisfacao_relacionamento_cod",
              "envolvimento_trabalho", "envolvimento_trabalho_cod",
              "equilibrio_vida_trabalho", "equilibrio_vida_trabalho_cod",
              "avaliacao_desempenho"]].copy()

    # Dim cargos
    dim = df[["cargo", "departamento", "nivel_cargo"]].drop_duplicates().reset_index(drop=True)

    return df, sat, dim


df_full, sat_full, dim_cargos = gerar_dados_mock()


# SIDEBAR 
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding: 10px 0 20px;">
        <div style="font-size: 20px; font-weight: 800; color: {ROXO_TEXT};">People Analytics</div>
        <div style="font-size: 11px; color: {ROXO_MUTED}; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 4px;">HR Attrition Dashboard</div>
        <div style="width: 40px; height: 3px; background: linear-gradient(90deg, {ROXO_ACCENT}, {ROXO_ACCENT_H}); margin: 14px auto; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)

    pagina = st.radio(
        "Navegação",
        ["Visão Geral", "Demografia & Carreira", "Satisfação & Engajamento",
         "Financeiro & Compensação", "Painel de Risco"],
        label_visibility="collapsed",
    )

    st.markdown(f"""
    <div style="border-top: 1px solid {ROXO_BORDER}; margin: 16px 0 12px;"></div>
    <div style="font-size: 11px; color: {ROXO_ACCENT_H}; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700; margin-bottom: 12px;">⚙ Filtros Globais</div>
    """, unsafe_allow_html=True)

    depts = ["Todos"] + sorted(df_full["departamento"].dropna().unique().tolist())
    filtro_dept = st.selectbox("Departamento", depts)

    cargos_disp = df_full["cargo"].dropna().unique().tolist()
    if filtro_dept != "Todos":
        cargos_disp = df_full[df_full["departamento"] == filtro_dept]["cargo"].dropna().unique().tolist()
    filtro_cargo = st.multiselect("Cargo", sorted(cargos_disp), default=[])

    filtro_genero = st.multiselect(
        "Gênero", df_full["genero"].dropna().unique().tolist(), default=[]
    )

    filtro_attrition = st.selectbox("Status", ["Todos", "Saiu", "Ficou"])


# APLICAR FILTROS
df = df_full.copy()

if filtro_dept != "Todos":
    df = df[df["departamento"] == filtro_dept]
if filtro_cargo:
    df = df[df["cargo"].isin(filtro_cargo)]
if filtro_genero:
    df = df[df["genero"].isin(filtro_genero)]
if filtro_attrition == "Saiu":
    df = df[df["attrition"] == 1]
elif filtro_attrition == "Ficou":
    df = df[df["attrition"] == 0]

n_total  = len(df)
n_saiu   = df["attrition"].sum()
taxa_att = n_saiu / n_total if n_total > 0 else 0


# HELPERS
def kpi(label, valor, sub="", cor=ROXO_TEXT):
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">{label}</div>
        <div class="value" style="color:{cor}">{valor}</div>
        <div class="sub">{sub}</div>
    </div>""", unsafe_allow_html=True)


def secao(txt):
    st.markdown(f'<p class="section-title">{txt}</p>', unsafe_allow_html=True)


def layout_plotly(fig, h=340, leg_y=1.12):
    """Aplica tema escuro roxo nos graficos."""
    fig.update_layout(
        height=h,
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=ROXO_TEXT, family="Inter, sans-serif"),
        legend=dict(
            orientation="h", yanchor="bottom", y=leg_y, xanchor="center", x=0.5,
            bgcolor="rgba(10,6,18,0.8)",
            bordercolor=ROXO_BORDER,
            borderwidth=1,
            font=dict(size=11, color=ROXO_TEXT_SEC),
        ),
    )
    fig.update_xaxes(
        gridcolor="rgba(42,31,61,0.5)",
        zerolinecolor=ROXO_BORDER,
        tickfont=dict(size=10, color=ROXO_MUTED),
        title_font=dict(size=11, color=ROXO_TEXT_SEC),
    )
    fig.update_yaxes(
        gridcolor="rgba(42,31,61,0.5)",
        zerolinecolor=ROXO_BORDER,
        tickfont=dict(size=10, color=ROXO_MUTED),
        title_font=dict(size=11, color=ROXO_TEXT_SEC),
    )
    return fig


# Labels visíveis para exibição
LABEL_RISCO = {
    "Critico": "Crítico",
    "Alto"   : "Alto",
    "Medio"  : "Médio",
    "Baixo"  : "Baixo",
}


# PAGINA 1 — Visão geral
if pagina == "Visão Geral":
    st.title("Visão Geral")
    st.markdown(f"<p style='color:{ROXO_MUTED}; font-size:13px; margin-top:-12px; margin-bottom:24px;'>Panorama completo de headcount, attrition, custos de turnover e risco preditivo.</p>", unsafe_allow_html=True)

    # KPIs
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        kpi("Headcount", f"{n_total:,}", "Funcionários filtrados", ROXO_ACCENT_H)
    with c2:
        cor_att = COR_PERIGO if taxa_att > .15 else COR_AVISO if taxa_att > .10 else COR_OK
        kpi("Attrition", f"{taxa_att:.1%}", f"{n_saiu} saídas", cor_att)
    with c3:
        custo = df[df["attrition"] == 1]["custo_reposicao_est_brl"].sum()
        kpi("Custo Turnover", f"R${custo/1e6:.1f}M", "Estimativa reposição", COR_AVISO)
    with c4:
        alto = (df["nivel_risco_ml"].isin(["Alto", "Critico"])).sum()
        kpi("Em Risco", f"{alto:,}", f"{alto/n_total:.1%}" if n_total > 0 else "0,0%", COR_AVISO)
    with c5:
        bw = df["score_bemestar"].mean()
        cor_bw = COR_OK if bw >= 2.5 else COR_AVISO
        kpi("Score de Bem-Estar", f"{bw:.2f}", "Escala 1-4", cor_bw)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])

    with col_a:
        secao("Attrition por Cargo")
        att_cargo = (
            df.groupby("cargo")["attrition"]
            .agg(["sum", "count"])
            .rename(columns={"sum": "saiu", "count": "total"})
            .assign(taxa=lambda x: x["saiu"] / x["total"])
            .sort_values("taxa", ascending=True)
            .reset_index()
        )
        fig = px.bar(
            att_cargo, x="taxa", y="cargo", orientation="h",
            text=att_cargo["taxa"].map("{:.1%}".format),
            color="taxa",
            color_continuous_scale=[[0, COR_OK], [0.3, COR_AVISO], [1, COR_PERIGO]],
            labels={"taxa": "Taxa attrition", "cargo": ""},
        )
        fig.update_traces(
            textposition="outside",
            marker_line_color=ROXO_BORDER,
            marker_line_width=0.5,
            textfont=dict(color=ROXO_TEXT, size=10),
        )
        fig = layout_plotly(fig, h=340)
        st.plotly_chart(fig, config={'responsive': True}, use_container_width=True)

    with col_b:
        secao("Funcionários por Departamento")
        att_dept = (
            df.groupby("departamento")["attrition"]
            .agg(["sum", "count"])
            .rename(columns={"sum": "Saiu", "count": "Total"})
            .assign(Ficou=lambda x: x["Total"] - x["Saiu"])
            .reset_index()
        )
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=att_dept["departamento"], y=att_dept["Ficou"],
            name="Ficou", marker_color=COR_AZUL, text=att_dept["Ficou"],
            textposition="inside", textfont=dict(color="white", size=10),
        ))
        fig2.add_trace(go.Bar(
            x=att_dept["departamento"], y=att_dept["Saiu"],
            name="Saiu", marker_color=COR_PERIGO, text=att_dept["Saiu"],
            textposition="inside", textfont=dict(color="white", size=10),
        ))
        fig2.update_layout(barmode="stack")
        fig2 = layout_plotly(fig2, h=340)
        st.plotly_chart(fig2, config={'responsive': True}, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        secao("Impacto dos Fatores de Risco")
        fatores = {
            "Com horas extras": df[df["horas_extras"] == 1]["attrition"].mean(),
            "Solteiro(a)": df[df["estado_civil"] == "Solteiro(a)"]["attrition"].mean(),
            "Renda abaixo da mediana": df[df["flag_renda_abaixo_mediana"] == 1]["attrition"].mean(),
            "Viaja frequentemente": df[df["frequencia_viagem"] == "Viaja Frequentemente"]["attrition"].mean(),
            "Sem promoção há 3+ anos": df[df["flag_sem_promocao_3a"] == 1]["attrition"].mean(),
            "Distância alta (>15km)": df[df["flag_distancia_alta"] == 1]["attrition"].mean(),
            "Satisfação baixa": df[df["flag_satisfacao_baixa"] == 1]["attrition"].mean(),
        }
        fat_df = pd.DataFrame({"fator": list(fatores.keys()), "taxa": list(fatores.values())}).dropna().sort_values("taxa")
        fig3 = px.bar(
            fat_df, x="taxa", y="fator", orientation="h",
            text=fat_df["taxa"].map("{:.1%}".format),
            color="taxa",
            color_continuous_scale=[[0, COR_OK], [0.4, COR_AVISO], [1, COR_PERIGO]],
        )
        fig3.update_traces(
            textposition="outside",
            textfont=dict(color=ROXO_TEXT, size=10),
            marker_line_color=ROXO_BORDER, marker_line_width=0.5,
        )
        fig3 = layout_plotly(fig3, h=300)
        st.plotly_chart(fig3, config={'responsive': True}, use_container_width=True)

    with col_d:
        secao("Distribuição de Risco")
        risco_cnt = (
            df["nivel_risco_ml"]
            .value_counts()
            .reindex(["Baixo", "Medio", "Alto", "Critico"])
            .reset_index()
        )
        risco_cnt.columns = ["nivel", "count"]
        risco_cnt["nivel_display"] = risco_cnt["nivel"].map(LABEL_RISCO)
        fig4 = px.pie(
            risco_cnt, values="count", names="nivel_display",
            color="nivel",
            color_discrete_map={
                "Critico": COR_PERIGO, "Alto": COR_AVISO,
                "Medio": COR_AZUL, "Baixo": COR_OK,
            },
            hole=0.55,
        )
        fig4.update_traces(
            textinfo="label+percent",
            textfont=dict(size=11, color=ROXO_TEXT),
            insidetextfont=dict(color="white"),
        )
        fig4 = layout_plotly(fig4, h=300, leg_y=-0.05)
        fig4.add_annotation(
            text=f"<b>{n_total}</b><br><span style='font-size:10px; color:{ROXO_MUTED}'>total</span>",
            showarrow=False, font=dict(size=16, color=ROXO_TEXT),
            y=0.5, x=0.5,
        )
        st.plotly_chart(fig4, config={'responsive': True}, use_container_width=True)


# PAGINA 2 — DEMOGRAFIA & CARREIRA
elif pagina == "Demografia & Carreira":
    st.title("Demografia & Carreira")
    st.markdown(f"<p style='color:{ROXO_MUTED}; font-size:13px; margin-top:-12px; margin-bottom:24px;'>Perfil etário, trajetórias de carreira, estado civil e correlações demográficas com attrition.</p>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Idade Média", f"{df['idade'].mean():.1f}", "anos", ROXO_ACCENT_H)
    with c2: kpi("Tempo na Empresa", f"{df['anos_empresa'].mean():.1f}", "anos médio", COR_AZUL)
    with c3: kpi("Sem Promoção", f"{df['anos_desde_ultima_promocao'].mean():.1f}", "anos médio", COR_AVISO)
    with c4:
        pct_ot = df["horas_extras"].mean()
        cor_ot = COR_PERIGO if pct_ot > .3 else COR_AVISO
        kpi("Com Horas Extras", f"{pct_ot:.1%}", "do headcount", cor_ot)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        secao("Distribuição de Idades por Status")
        fig = px.histogram(
            df, x="idade",
            color=df["attrition"].map({0: "Ficou", 1: "Saiu"}),
            nbins=20, barmode="overlay", opacity=0.75,
            color_discrete_map={"Ficou": COR_AZUL, "Saiu": COR_PERIGO},
            labels={"idade": "Idade", "color": "Status", "count": "Funcionários"},
        )
        fig = layout_plotly(fig, h=300)
        fig.update_traces(marker_line_color=ROXO_BORDER, marker_line_width=0.5)
        st.plotly_chart(fig, config={'responsive': True}, use_container_width=True)

    with col_b:
        secao("Attrition por Estado Civil × Gênero")
        cross = (
            df.groupby(["estado_civil", "genero"])["attrition"]
            .mean().reset_index()
            .rename(columns={"attrition": "taxa"})
        )
        fig2 = px.bar(
            cross, x="estado_civil", y="taxa", color="genero", barmode="group",
            text=cross["taxa"].map("{:.1%}".format),
            color_discrete_map={"Masculino": COR_AZUL, "Feminino": "#B47FD4"},
            labels={"taxa": "Taxa attrition", "estado_civil": "", "genero": "Gênero"},
        )
        fig2.update_traces(
            textposition="outside",
            textfont=dict(color=ROXO_TEXT, size=10),
            marker_line_color=ROXO_BORDER, marker_line_width=0.5,
        )
        fig2 = layout_plotly(fig2, h=300)
        st.plotly_chart(fig2, config={'responsive': True}, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        secao("Anos na Empresa × Anos sem Promoção")
        sample = df.sample(min(600, len(df)), random_state=42)
        fig3 = px.scatter(
            sample, x="anos_empresa", y="anos_desde_ultima_promocao",
            color=sample["attrition"].map({0: "Ficou", 1: "Saiu"}),
            color_discrete_map={"Ficou": COR_AZUL, "Saiu": COR_PERIGO},
            opacity=0.6, size_max=6,
            labels={"anos_empresa": "Anos na empresa", "anos_desde_ultima_promocao": "Anos sem promoção", "color": "Status"},
        )
        fig3 = layout_plotly(fig3, h=300)
        st.plotly_chart(fig3, config={'responsive': True}, use_container_width=True)

    with col_d:
        secao("Attrition por Viagem × Nível de Cargo")
        heat_data = (
            df.groupby(["frequencia_viagem", "nivel_cargo"])["attrition"]
            .mean().unstack(fill_value=0) * 100
        )
        fig4 = px.imshow(
            heat_data.round(1),
            color_continuous_scale=[[0, "#1a1035"], [0.5, COR_AVISO], [1, COR_PERIGO]],
            text_auto=".1f",
            labels={"color": "Attrition %"},
            aspect="auto",
        )
        fig4 = layout_plotly(fig4, h=300, leg_y=1.15)
        st.plotly_chart(fig4, config={'responsive': True}, use_container_width=True)

    secao("Attrition por Faixa Etária")
    fat_etaria = (
        df.groupby("faixa_etaria")["attrition"]
        .agg(["mean", "sum", "count"])
        .rename(columns={"mean": "taxa", "sum": "saiu", "count": "total"})
        .reindex(["18-25", "26-35", "36-45", "46-55", "55+"])
        .reset_index()
    )
    fig5 = make_subplots(specs=[[{"secondary_y": True}]])
    fig5.add_trace(go.Bar(
        x=fat_etaria["faixa_etaria"], y=fat_etaria["total"],
        name="Headcount", marker_color=COR_AZUL, opacity=0.6,
        text=fat_etaria["total"], textposition="inside",
        textfont=dict(color="white", size=10),
    ))
    fig5.add_trace(go.Scatter(
        x=fat_etaria["faixa_etaria"], y=fat_etaria["taxa"],
        name="Taxa attrition", mode="lines+markers",
        line=dict(color=COR_PERIGO, width=2.5),
        marker=dict(size=8, color=COR_PERIGO, line=dict(color=ROXO_TEXT, width=1)),
    ), secondary_y=True)
    fig5 = layout_plotly(fig5, h=260)
    fig5.update_yaxes(tickformat=".0%", secondary_y=True, showgrid=False)
    st.plotly_chart(fig5, config={'responsive': True}, use_container_width=True)


# PAGINA 3 — SATISFAÇÃO & ENGAJAMENTO
elif pagina == "Satisfação & Engajamento":
    st.title("Satisfação & Engajamento")
    st.markdown(f"<p style='color:{ROXO_MUTED}; font-size:13px; margin-top:-12px; margin-bottom:24px;'>Dimensões de satisfação, work-life balance, envolvimento e sua relação com attrition.</p>", unsafe_allow_html=True)

    sat_cols = ["satisfacao_trabalho_cod", "satisfacao_ambiente_cod",
                "satisfacao_relacionamento_cod", "envolvimento_trabalho_cod",
                "equilibrio_vida_trabalho_cod"]
    sat_labels = ["Sat. Trabalho", "Sat. Ambiente", "Sat. Relacionamento",
                  "Envolvimento", "Work-Life Balance"]

    c1, c2, c3, c4 = st.columns(4)
    bw_mean = df['score_bemestar'].mean()
    with c1:
        kpi("Pontuação de Bem-Estar", f"{bw_mean:.2f}", "média escala 1-4",
            COR_OK if bw_mean >= 2.5 else COR_AVISO)
    with c2:
        kpi("Satisfação no Trabalho", f"{df['satisfacao_trabalho_cod'].mean():.2f}", "média 1-4", COR_AZUL)
    with c3:
        kpi("Work-Life Balance", f"{df['equilibrio_vida_trabalho_cod'].mean():.2f}", "média 1-4", COR_AZUL)
    with c4:
        pct_low = (df["satisfacao_trabalho_cod"] <= 2).mean()
        cor_low = COR_PERIGO if pct_low > .3 else COR_AVISO
        kpi("Satisfação Baixa", f"{pct_low:.1%}", "Pontuação ≤ 2", cor_low)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        secao("Radar de Satisfação — Ficou vs Saiu")
        medias_fica = df[df["attrition"] == 0][sat_cols].mean().tolist()
        medias_saiu = df[df["attrition"] == 1][sat_cols].mean().tolist()

        fig = go.Figure()
        for vals, nome, cor in [(medias_fica, "Ficou", COR_AZUL), (medias_saiu, "Saiu", COR_PERIGO)]:
            fig.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=sat_labels + [sat_labels[0]],
                fill="toself", name=nome,
                line_color=cor, fillcolor=cor, opacity=0.20,
                line=dict(width=2),
            ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[1, 4],
                                gridcolor="rgba(42,31,61,0.6)", tickcolor=ROXO_MUTED,
                                tickfont=dict(color=ROXO_MUTED, size=9)),
                angularaxis=dict(gridcolor="rgba(42,31,61,0.4)", tickfont=dict(color=ROXO_TEXT_SEC, size=10)),
                bgcolor="rgba(20,16,30,0.5)",
            ),
            height=340, margin=dict(l=30, r=30, t=30, b=30),
            paper_bgcolor="rgba(0,0,0,0)", font_color=ROXO_TEXT,
            legend=dict(orientation="h", y=-0.05, x=0.5, xanchor="center",
                        font=dict(color=ROXO_TEXT_SEC, size=11)),
        )
        st.plotly_chart(fig, config={'responsive': True}, use_container_width=True)

    with col_b:
        secao("Distribuição de Satisfação no Trabalho")
        sat_dist = (
            df.groupby(["satisfacao_trabalho", "attrition"])
            .size().reset_index(name="count")
        )
        sat_dist["status"] = sat_dist["attrition"].map({0: "Ficou", 1: "Saiu"})
        ordem_sat = ["Baixo", "Medio", "Alto", "Muito Alto"]
        fig2 = px.bar(
            sat_dist, x="satisfacao_trabalho", y="count", color="status",
            barmode="group",
            color_discrete_map={"Ficou": COR_AZUL, "Saiu": COR_PERIGO},
            category_orders={"satisfacao_trabalho": ordem_sat},
            labels={"satisfacao_trabalho": "Satisfação no trabalho", "count": "Funcionários", "status": ""},
        )
        fig2.update_traces(
            textfont=dict(color=ROXO_TEXT, size=10),
            marker_line_color=ROXO_BORDER, marker_line_width=0.5,
        )
        fig2 = layout_plotly(fig2, h=340)
        st.plotly_chart(fig2, config={'responsive': True}, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        secao("Cargo × Satisfação (Attrition %)")
        heat = (
            df.groupby(["cargo", "satisfacao_trabalho"])["attrition"]
            .mean().unstack(fill_value=0) * 100
        )
        heat = heat.reindex(columns=[c for c in ordem_sat if c in heat.columns])
        fig3 = px.imshow(
            heat.round(1), text_auto=".1f",
            color_continuous_scale=[[0, "#1a1035"], [0.5, COR_AVISO], [1, COR_PERIGO]],
            labels={"color": "Attrition %"},
            aspect="auto",
        )
        fig3 = layout_plotly(fig3, h=320, leg_y=1.15)
        st.plotly_chart(fig3, config={'responsive': True}, use_container_width=True)

    with col_d:
        secao("Treinamentos × Attrition")
        treino_att = (
            df.groupby("treinamentos_ultimo_ano")["attrition"]
            .agg(["mean", "count"]).reset_index()
            .rename(columns={"mean": "taxa", "count": "total"})
        )
        fig4 = make_subplots(specs=[[{"secondary_y": True}]])
        fig4.add_trace(go.Bar(
            x=treino_att["treinamentos_ultimo_ano"], y=treino_att["total"],
            name="Headcount", marker_color=COR_CINZA, opacity=0.5,
            text=treino_att["total"], textposition="inside",
            textfont=dict(color="white", size=9),
        ))
        fig4.add_trace(go.Scatter(
            x=treino_att["treinamentos_ultimo_ano"], y=treino_att["taxa"],
            name="Taxa attrition", mode="lines+markers",
            line=dict(color=COR_PERIGO, width=2.5),
            marker=dict(size=8, color=COR_PERIGO, line=dict(color=ROXO_TEXT, width=1)),
        ), secondary_y=True)
        fig4 = layout_plotly(fig4, h=320)
        fig4.update_yaxes(tickformat=".0%", secondary_y=True, showgrid=False)
        fig4.update_xaxes(title_text="Treinamentos no último ano")
        st.plotly_chart(fig4, config={'responsive': True}, use_container_width=True)

    secao("Pontuação de Bem-Estar × Renda Mensal")
    sample = df.sample(min(800, len(df)), random_state=1)
    fig5 = px.scatter(
        sample, x="score_bemestar", y="renda_mensal_brl",
        color=sample["attrition"].map({0: "Ficou", 1: "Saiu"}),
        color_discrete_map={"Ficou": COR_AZUL, "Saiu": COR_PERIGO},
        opacity=0.65,
        labels={"score_bemestar": "Pontuação de Bem-Estar", "renda_mensal_brl": "Renda mensal (R$)", "color": ""},
    )
    fig5 = layout_plotly(fig5, h=280)
    st.plotly_chart(fig5, config={'responsive': True}, use_container_width=True)


# PAGINA 4 — FINANCEIRO & COMPENSAÇÃO
elif pagina == "Financeiro & Compensação":
    st.title("Financeiro & Compensação")
    st.markdown(f"<p style='color:{ROXO_MUTED}; font-size:13px; margin-top:-12px; margin-bottom:24px;'>Análise de renda, aumentos salariais, stock options e custo estimado de turnover.</p>", unsafe_allow_html=True)

    renda_fica = df[df["attrition"] == 0]["renda_mensal_brl"].mean()
    renda_saiu = df[df["attrition"] == 1]["renda_mensal_brl"].mean()
    gap = renda_fica - renda_saiu

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Renda Mediana", f"R${df['renda_mensal_brl'].median():,.0f}", "todos os funcionários", ROXO_ACCENT_H)
    with c2: kpi("Renda — Ficou", f"R${renda_fica:,.0f}", "média mensal", COR_OK)
    with c3: kpi("Renda — Saiu", f"R${renda_saiu:,.0f}", "média mensal", COR_PERIGO)
    with c4: kpi("Diferença Salarial", f"R${gap:,.0f}", "ficou − saiu / mês", COR_AVISO)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        secao("Renda por Nível de Cargo")
        fig = px.box(
            df, x="nivel_cargo", y="renda_mensal_brl",
            color=df["attrition"].map({0: "Ficou", 1: "Saiu"}),
            color_discrete_map={"Ficou": COR_AZUL, "Saiu": COR_PERIGO},
            category_orders={"nivel_cargo": ["Junior", "Pleno", "Senior", "Especialista", "Diretor"]},
            labels={"renda_mensal_brl": "Renda mensal (R$)", "nivel_cargo": "Nível do cargo", "color": ""},
            points=False,
        )
        fig = layout_plotly(fig, h=320)
        st.plotly_chart(fig, config={'responsive': True}, use_container_width=True)

    with col_b:
        secao("Attrition por Faixa de Renda")
        faixa_att = (
            df.groupby("faixa_renda")["attrition"]
            .agg(["mean", "sum", "count"]).reset_index()
            .rename(columns={"mean": "taxa", "sum": "saiu", "count": "total"})
        )
        ordem_faixa = ["Baixa", "Média-Baixa", "Média-Alta", "Alta"]
        faixa_att = faixa_att.set_index("faixa_renda").reindex(ordem_faixa).reset_index()
        fig2 = px.bar(
            faixa_att, x="faixa_renda", y="taxa",
            text=faixa_att["taxa"].map("{:.1%}".format),
            color="taxa",
            color_continuous_scale=[[0, COR_OK], [0.5, COR_AVISO], [1, COR_PERIGO]],
            labels={"taxa": "Taxa attrition", "faixa_renda": ""},
        )
        fig2.update_traces(
            textposition="outside",
            textfont=dict(color=ROXO_TEXT, size=10),
            marker_line_color=ROXO_BORDER, marker_line_width=0.5,
        )
        fig2 = layout_plotly(fig2, h=320)
        st.plotly_chart(fig2, config={'responsive': True}, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        secao("Aumento Salarial Médio por Cargo")
        aumento = (
            df.groupby("cargo")["perc_aumento_salarial"]
            .mean().sort_values().reset_index()
        )
        fig3 = px.bar(
            aumento, x="perc_aumento_salarial", y="cargo", orientation="h",
            text=aumento["perc_aumento_salarial"].map("{:.1f}%".format),
            color="perc_aumento_salarial",
            color_continuous_scale=[[0, COR_PERIGO], [0.5, COR_AVISO], [1, COR_OK]],
            labels={"perc_aumento_salarial": "Aumento médio (%)", "cargo": ""},
        )
        fig3.update_traces(
            textposition="outside",
            textfont=dict(color=ROXO_TEXT, size=10),
            marker_line_color=ROXO_BORDER, marker_line_width=0.5,
        )
        fig3 = layout_plotly(fig3, h=300)
        st.plotly_chart(fig3, config={'responsive': True}, use_container_width=True)

    with col_d:
        secao("Stock Options × Attrition")
        stock_att = (
            df.groupby("nivel_stock_option")["attrition"]
            .agg(["mean", "count"]).reset_index()
            .rename(columns={"mean": "taxa", "count": "total"})
        )
        fig4 = px.bar(
            stock_att, x="nivel_stock_option", y="taxa",
            text=stock_att["taxa"].map("{:.1%}".format),
            color="taxa",
            color_continuous_scale=[[0, COR_OK], [0.5, COR_AVISO], [1, COR_PERIGO]],
            labels={"taxa": "Taxa attrition", "nivel_stock_option": "Nível de stock option"},
        )
        fig4.update_traces(
            textposition="outside",
            textfont=dict(color=ROXO_TEXT, size=10),
            marker_line_color=ROXO_BORDER, marker_line_width=0.5,
        )
        fig4 = layout_plotly(fig4, h=300)
        st.plotly_chart(fig4, config={'responsive': True}, use_container_width=True)

    secao("Custo Estimado de Turnover")
    custo_dept = (
        df[df["attrition"] == 1]
        .groupby(["departamento", "nivel_cargo"])["custo_reposicao_est_brl"]
        .sum().reset_index()
    )
    fig5 = px.bar(
        custo_dept, x="departamento", y="custo_reposicao_est_brl",
        color="nivel_cargo", barmode="stack",
        labels={"custo_reposicao_est_brl": "Custo estimado (R$)", "departamento": "", "nivel_cargo": "Nível"},
        color_discrete_sequence=["#4C7BB8", "#5B8FC7", "#7BA3D1", "#9BB8DB", "#BBCDE5"],
    )
    fig5 = layout_plotly(fig5, h=280)
    st.plotly_chart(fig5, config={'responsive': True}, use_container_width=True)


# PAGINA 5 — PAINEL DE RISCO
elif pagina == "Painel de Risco":
    st.title("Painel de Risco")
    st.markdown(f"""
    <p style='color:{ROXO_MUTED}; font-size:13px; margin-top:-12px; margin-bottom:24px;'>
    Probabilidade individual de attrition.
    </p>""", unsafe_allow_html=True)

    criticos = (df["nivel_risco_ml"] == "Critico").sum()
    altos = (df["nivel_risco_ml"] == "Alto").sum()
    custo_risco = df[df["nivel_risco_ml"].isin(["Critico", "Alto"])]["custo_reposicao_est_brl"].sum()
    prob_media = df["prob_attrition"].mean()

    c1, c2, c3, c4 = st.columns(4)
    cor_prob = COR_PERIGO if prob_media > .2 else COR_AVISO
    with c1:
        kpi("Prob. Média Attrition", f"{prob_media:.1%}", "todos do filtro", cor_prob)
    with c2:
        kpi("Críticos", f"{criticos:,}", f"{criticos/n_total:.1%}" if n_total > 0 else "0,0%", COR_PERIGO)
    with c3:
        kpi("Alto Risco", f"{altos:,}", f"{altos/n_total:.1%}" if n_total > 0 else "0,0%", COR_AVISO)
    with c4:
        kpi("Custo em Risco", f"R${custo_risco/1e6:.1f}M", "Crítico + Alto", COR_AVISO)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([2, 1])

    with col_a:
        secao("Distribuição de Probabilidade de Attrition")
        fig = px.histogram(
            df, x="prob_attrition",
            color="nivel_risco_ml",
            color_discrete_map=CORES_RISCO,
            nbins=40, barmode="stack", opacity=0.88,
            labels={"prob_attrition": "Probabilidade de saída", "count": "Funcionários", "nivel_risco_ml": "Risco"},
            category_orders={"nivel_risco_ml": ["Baixo", "Medio", "Alto", "Critico"]},
        )
        fig.update_traces(marker_line_color=ROXO_BORDER, marker_line_width=0.3)
        fig.add_vline(x=0.40, line_dash="dash", line_color="white", line_width=1.5,
                      annotation_text="Threshold (0.40)", annotation_position="top right",
                      annotation_font_color=ROXO_TEXT)
        fig = layout_plotly(fig, h=300)
        st.plotly_chart(fig, config={'responsive': True}, use_container_width=True)

    with col_b:
        secao("Ações Recomendadas")
        acoes = df["acao_recomendada"].value_counts().reset_index()
        acoes.columns = ["acao", "count"]
        fig2 = px.bar(
            acoes.head(7), x="count", y="acao", orientation="h",
            text="count",
            color="count",
            color_continuous_scale=[[0, COR_AZUL], [0.5, ROXO_ACCENT], [1, COR_PERIGO]],
            labels={"count": "Funcionários", "acao": ""},
        )
        fig2.update_traces(
            textposition="outside",
            textfont=dict(color=ROXO_TEXT, size=10),
            marker_line_color=ROXO_BORDER, marker_line_width=0.5,
        )
        fig2 = layout_plotly(fig2, h=300)
        st.plotly_chart(fig2, config={'responsive': True}, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        secao("Probabilidade Média por Departamento × Cargo")
        heat_ml = (
            df.groupby(["departamento", "cargo"])["prob_attrition"]
            .mean().unstack(fill_value=0) * 100
        )
        fig3 = px.imshow(
            heat_ml.round(1), text_auto=".1f",
            color_continuous_scale=[[0, "#1a1035"], [0.5, COR_AVISO], [1, COR_PERIGO]],
            labels={"color": "Prob. (%)"},
            aspect="auto",
        )
        fig3 = layout_plotly(fig3, h=300, leg_y=1.15)
        st.plotly_chart(fig3, config={'responsive': True}, use_container_width=True)

    with col_d:
        secao("Prob. Attrition × Renda Mensal")
        sample = df.sample(min(600, len(df)), random_state=7)
        fig4 = px.scatter(
            sample, x="renda_mensal_brl", y="prob_attrition",
            color="nivel_risco_ml",
            color_discrete_map=CORES_RISCO,
            opacity=0.65, size_max=6,
            category_orders={"nivel_risco_ml": ["Baixo", "Medio", "Alto", "Critico"]},
            labels={"renda_mensal_brl": "Renda mensal (R$)", "prob_attrition": "Prob. attrition", "nivel_risco_ml": "Risco"},
        )
        fig4.add_hline(y=0.40, line_dash="dash", line_color="white", line_width=1.5)
        fig4 = layout_plotly(fig4, h=300)
        st.plotly_chart(fig4, config={'responsive': True}, use_container_width=True)

    # Watchlist
    st.markdown(f"""
    <div style="border-top: 1px solid {ROXO_BORDER}; margin: 32px 0 16px;"></div>
    <div class="section-title">Watchlist — Funcionários em Risco</div>
    """, unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filtro_risco = st.multiselect(
            "Nível de risco",
            ["Critico", "Alto", "Medio", "Baixo"],
            default=["Critico", "Alto"],
            format_func=lambda x: LABEL_RISCO.get(x, x),
        )
    with col_f2:
        filtro_acao = st.selectbox(
            "Ação recomendada",
            ["Todas"] + sorted(df["acao_recomendada"].dropna().unique().tolist()),
        )
    with col_f3:
        prob_min = st.slider("Prob. mínima de saída", 0.0, 1.0, 0.30, 0.05, format="%.0f%%")

    mask = (
        df["nivel_risco_ml"].isin(filtro_risco) &
        (df["prob_attrition"] >= prob_min)
    )
    if filtro_acao != "Todas":
        mask = mask & (df["acao_recomendada"] == filtro_acao)

    watchlist = (
        df[mask][[
            "id_funcionario", "cargo", "departamento", "nivel_cargo",
            "prob_attrition", "nivel_risco_ml",
            "shap_top1_feat", "shap_top2_feat", "shap_top3_feat",
            "acao_recomendada", "renda_mensal_brl", "anos_desde_ultima_promocao",
        ]]
        .sort_values("prob_attrition", ascending=False)
        .reset_index(drop=True)
    )

    watchlist["nivel_risco_ml"] = watchlist["nivel_risco_ml"].map(LABEL_RISCO)
    watchlist["prob_attrition"] = watchlist["prob_attrition"].map("{:.1%}".format)
    watchlist["renda_mensal_brl"] = watchlist["renda_mensal_brl"].map("R${:,.0f}".format)

    watchlist.columns = [
        "ID", "Cargo", "Departamento", "Nível",
        "Prob. Saída", "Risco",
        "Fator 1", "Fator 2", "Fator 3",
        "Ação Recomendada", "Renda", "Anos s/ Promoção",
    ]

    st.dataframe(
        watchlist,
        use_container_width=True,
        height=420,
        hide_index=True,
        column_config={
            "Prob. Saída": st.column_config.TextColumn("Prob. Saída"),
            "Risco": st.column_config.TextColumn("Risco"),
            "Renda": st.column_config.TextColumn("Renda"),
        }
    )

    st.caption(f"{len(watchlist)} funcionários no filtro atual  |  Clique no cabeçalho para ordenar  |  Use os filtros acima para refinar")

    csv_out = watchlist.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "⬇  Exportar (.csv)",
        data=csv_out,
        file_name="watchlist_risco_ml.csv",
        mime="text/csv",
    )

    st.markdown(f"""
    <div style="text-align: center; padding: 24px 0; color: {ROXO_MUTED}; font-size: 11px; border-top: 1px solid {ROXO_BORDER}; margin-top: 24px;">
        People Analytics Dashboard  ·  IBM HR Employee Attrition Dataset
    </div>
    """, unsafe_allow_html=True)