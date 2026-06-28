# People Analytics — HR Employee Attrition

Pipeline de dados e machine learning para análise e previsão de rotatividade de funcionários, com saída pronta para consumo no Power BI.

---

## Visão geral

O projeto transforma o dataset público **IBM HR Employee Attrition** (1.470 funcionários, 35 variáveis) em uma base analítica completa, cobrindo desde a limpeza básica até um modelo preditivo explicável de risco de saída.

```
archive.zip (CSV bruto)
        │
        ▼
┌───────────────────────┐
│  1. ETL_HR_Attrition  │   limpeza, tradução, métricas derivadas
│       .ipynb          │   e modelagem em estrela
└───────────┬───────────┘
            │  output/*.csv
            ▼
┌───────────────────────┐
│  2. ML_HR_Attrition   │   EDA direcionada, Random Forest + SMOTE,
│       .ipynb          │   SHAP, score de risco calibrado
└───────────┬───────────┘
            │  fato_funcionarios_ml.csv
            ▼
┌───────────────────────┐
│      Power BI         │   dashboard de attrition e painel
│                       │   de risco operacional
└───────────────────────┘
```

---

## Estrutura de arquivos

| Arquivo | Descrição |
|---|---|
| `HR-Employee-Attrition.csv` | Dataset bruto original |
| `ETL_HR_Attrition.ipynb` | Notebook de limpeza, transformação e modelagem estrela |
| `ML_HR_Attrition.ipynb` | Notebook de EDA, treino do modelo e geração do score de risco |
| `output/fato_funcionarios.csv` | Tabela fato — saída do ETL (39 colunas) |
| `output/dim_cargos.csv` | Dimensão de cargos e departamentos |
| `output/dim_satisfacao.csv` | Dimensão de índices de satisfação |
| `output/fato_funcionarios_ml.csv` | Tabela fato enriquecida com probabilidade de attrition e SHAP |
| `output/_manifesto_carga.csv` | Log da última execução do ETL |
| `output/plot_*.png` | Gráficos de avaliação e interpretabilidade do modelo |

---

## Notebook 1 — ETL (`ETL_HR_Attrition.ipynb`)

**Entrada:** `HR-Employee-Attrition.csv`
**Saída:** `output/fato_funcionarios.csv`, `dim_cargos.csv`, `dim_satisfacao.csv`

### Etapas

1. **Extração** — leitura do CSV e snapshot inicial (tipos, nulos, cardinalidade)
2. **Validação** — checagens automáticas: colunas obrigatórias, duplicidade de ID, faixas de valores esperadas, categorias inesperadas. Erros críticos interrompem o pipeline.
3. **Transformação**
   - Remoção de colunas constantes (`EmployeeCount`, `Over18`, `StandardHours`)
   - Renomeação de todas as colunas para português (snake_case)
   - Conversão de tipos (categóricas, booleanas, ordinais)
   - Decodificação de 8 escalas ordinais (1–4 → "Baixo"/"Médio"/"Alto"/"Muito Alto" etc.)
4. **Enriquecimento**
   - Flags de risco: horas extras, sem promoção há 3+ anos, distância alta, satisfação baixa, renda abaixo da mediana
   - `score_risco` (0–5) e `nivel_risco` (Baixo/Médio/Alto) — regra heurística baseada nas flags
   - Faixas etárias e de renda (quartis)
   - Métricas de tenure: % da carreira na empresa atual, tempo médio por empresa anterior, índice de estagnação no cargo
   - `custo_reposicao_est` — custo estimado de reposição por nível de cargo (50%–200% do salário anual)
5. **Exportação** — modelo estrela com 1 tabela fato + 2 dimensões, mais manifesto de carga

### Resultado

- Taxa de attrition: **16,1%** (237 de 1.470 funcionários)
- Zero valores nulos
- 53 colunas no DataFrame transformado, 39 exportadas na tabela fato

---

## Notebook 2 — ML (`ML_HR_Attrition.ipynb`)

**Entrada:** `output/fato_funcionarios.csv` + `dim_satisfacao.csv`
**Saída:** `output/fato_funcionarios_ml.csv`

### Etapas

1. **Carga e merge** das tabelas do ETL
2. **EDA direcionada**
   - Distribuição da variável target (desbalanceamento 84/16)
   - Correlação entre os 5 índices de satisfação
   - Taxa de attrition por grupo (horas extras, estado civil, cargo, viagem)
3. **Pré-processamento** — encoding de 11 categóricas, 24 numéricas e 6 binárias (41 features)
4. **Treino** — Random Forest (300 árvores) com SMOTE aplicado apenas no treino e `class_weight='balanced'`
5. **Avaliação**
   - Cross-validation 5-fold: **ROC-AUC ≈ 0,776 ± 0,014**
   - Curvas ROC, Precision-Recall e matriz de confusão
   - Análise de threshold (0,40 usado para priorizar recall)
6. **Interpretabilidade**
   - Feature importance global (top 20)
   - SHAP beeswarm e bar plot (visão global)
   - Explicação individual via SHAP para o funcionário de maior risco
7. **Exportação** — adiciona ao dataset:
   - `prob_attrition` — probabilidade individual (0–1)
   - `nivel_risco_ml` — Baixo / Médio / Alto / Crítico, calibrado por percentis reais
   - `shap_top1_feat/val`, `shap_top2_feat/val`, `shap_top3_feat/val` — os 3 fatores que mais aumentam o risco de cada funcionário
   - `acao_recomendada` — sugestão automática de ação de RH baseada no fator principal

### Por que Random Forest + SHAP

- **Random Forest** lida bem com features mistas (numéricas, categóricas codificadas, binárias) e colinearidade moderada, sem exigir normalização
- **SMOTE** corrige o desbalanceamento de classes apenas no treino, evitando vazamento de dados (data leakage)
- **SHAP** transforma a "caixa-preta" em explicações individuais — essencial para o RH entender *por que* uma pessoa está em risco, não apenas *que* está

---

## Modelo de dados para Power BI

```
        dim_cargos ──┐
                      │ (cargo)
fato_funcionarios_ml ─┤
                      │ (id_funcionario)
       dim_satisfacao ┘
```

- `fato_funcionarios_ml.csv` substitui `fato_funcionarios.csv` como tabela principal
- Relacionamentos: `cargo` → `dim_cargos.cargo` (N:1) e `id_funcionario` → `dim_satisfacao.id_funcionario` (1:1)

---

## Dashboard sugerido (5 páginas)

| Página | Foco | Principais visuais |
|---|---|---|
| **1. Visão geral** | KPIs executivos | Taxa de attrition, custo de turnover, attrition por cargo/departamento |
| **2. Demografia & carreira** | Perfil dos funcionários | Idade, tempo na empresa, promoções, viagens |
| **3. Satisfação & engajamento** | Bem-estar | Radar de satisfação, heatmap cargo × satisfação |
| **4. Financeiro** | Compensação | Renda por nível, gap salarial, stock options |
| **5. Painel de risco (ML)** | Ação do RH | Ranking por `prob_attrition`, watchlist com SHAP, `acao_recomendada` |

### Medidas DAX principais

```dax
Taxa Attrition =
    DIVIDE(
        COUNTROWS(FILTER(fato_funcionarios_ml, [attrition] = 1)),
        COUNTROWS(fato_funcionarios_ml)
    )

Custo em Risco =
    SUMX(
        FILTER(fato_funcionarios_ml, [nivel_risco_ml] IN {"Crítico","Alto"}),
        [custo_reposicao_est]
    )

Prob Média Attrition =
    AVERAGE(fato_funcionarios_ml[prob_attrition])
```

---

## Como executar

```bash
pip install pandas numpy scikit-learn shap imbalanced-learn matplotlib --break-system-packages

# 1. Rodar o ETL primeiro — gera output/
jupyter notebook ETL_HR_Attrition.ipynb

# 2. Rodar o ML — consome output/ e gera fato_funcionarios_ml.csv
jupyter notebook ML_HR_Attrition.ipynb

# 3. Power BI Desktop → Obter Dados → Texto/CSV → importar os arquivos de output/
```

---

## Próximos passos possíveis

- Re-treinar o modelo periodicamente conforme novos dados de attrition chegam
- Testar outros algoritmos (XGBoost, LightGBM) e comparar ROC-AUC
- Adicionar análise de sobrevivência (Kaplan-Meier) para estimar *quando* o risco aumenta
- Simulação what-if: impacto de reduzir horas extras ou ajustar faixas salariais na taxa de attrition prevista
- Automatizar a atualização (refresh agendado no Power BI + script de re-treino)