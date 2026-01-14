import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Função para salvar gráfico com HTML acessível
def salvar_grafico_acessivel(fig, filename, titulo):
    """Salva o gráfico com HTML completo e tags de acessibilidade"""
    # Configurar para ser responsivo
    fig.update_layout(
        autosize=True,
        margin=dict(l=50, r=50, t=80, b=150, autoexpand=True)
    )
    html_content = fig.to_html(include_plotlyjs='cdn', full_html=False, config={'responsive': True})
    html_completo = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo} - Análise de Acidentes DER</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{ width: 100%; height: 100%; overflow: hidden; }}
        .plotly-graph-div {{ width: 100% !important; height: 100% !important; }}
        .js-plotly-plot {{ width: 100% !important; height: 100% !important; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>'''
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_completo)

# Carregar dados
df_total = pd.read_csv('dados_completos.csv')
df_total['Data Abertura'] = pd.to_datetime(df_total['Data Abertura'], errors='coerce')

# Incluir todos os três anos de análise (2023, 2024, 2025)
df = df_total[df_total['Ano'].isin([2023, 2024, 2025])].copy()

# Paleta de cores Sigma-PLI (azul institucional, verde, amarelo)
CORES_SIGMA = ['#1E3A5F', '#2E7D32', '#F9A825']  # Azul, Verde, Amarelo

print("Gerando análises de tendências regionais...")

# ===== GRÁFICO 24: HEATMAP REGIONAL - ACIDENTES E VÍTIMAS =====
regional_2023 = df[df['Ano']==2023].groupby('Regional').agg({
    'Evento': 'count',
    'Total de Vítimas': 'sum',
    'Fatal': 'sum',
    'Grave': 'sum'
})
regional_2024 = df[df['Ano']==2024].groupby('Regional').agg({
    'Evento': 'count',
    'Total de Vítimas': 'sum',
    'Fatal': 'sum',
    'Grave': 'sum'
})
regional_2025 = df[df['Ano']==2025].groupby('Regional').agg({
    'Evento': 'count',
    'Total de Vítimas': 'sum',
    'Fatal': 'sum',
    'Grave': 'sum'
})

# Métricas originais para extração dos dados
metricas = ['Evento', 'Total de Vítimas', 'Fatal', 'Grave']
# Rótulos abreviados para exibição no eixo Y
metricas_labels = ['Acidentes', 'Vítimas', 'Óbitos', 'Graves']

fig24 = make_subplots(
    rows=1, cols=3,
    subplot_titles=('2023', '2024', '2025'),
    specs=[[{'type':'heatmap'}, {'type':'heatmap'}, {'type':'heatmap'}]],
    horizontal_spacing=0.08
)

fig24.add_trace(
    go.Heatmap(z=regional_2023[metricas].T.values, 
               x=regional_2023[metricas].T.columns,
               y=metricas_labels,
               colorscale='Blues',
               colorbar=dict(x=0.28, len=0.8, thickness=10, title=dict(text="2023", font=dict(size=8)))),
    row=1, col=1
)
fig24.add_trace(
    go.Heatmap(z=regional_2024[metricas].T.values if len(regional_2024) > 0 else [[0]], 
               x=regional_2024[metricas].T.columns if len(regional_2024) > 0 else [''],
               y=metricas_labels,
               colorscale='Greens',
               colorbar=dict(x=0.64, len=0.8, thickness=10, title=dict(text="2024", font=dict(size=8)))),
    row=1, col=2
)
fig24.add_trace(
    go.Heatmap(z=regional_2025[metricas].T.values,
               x=regional_2025[metricas].T.columns,
               y=metricas_labels,
               colorscale='YlOrBr',
               colorbar=dict(x=1.0, len=0.8, thickness=10, title=dict(text="2025", font=dict(size=8)))),
    row=1, col=3
)
fig24.update_xaxes(title_text='Regional', row=1, col=1, tickangle=-45, tickfont=dict(size=7))
fig24.update_xaxes(title_text='Regional', row=1, col=2, tickangle=-45, tickfont=dict(size=7))
fig24.update_xaxes(title_text='Regional', row=1, col=3, tickangle=-45, tickfont=dict(size=7))
fig24.update_yaxes(title_text='', row=1, col=1, tickfont=dict(size=9))
fig24.update_yaxes(tickfont=dict(size=9), row=1, col=2)
fig24.update_yaxes(tickfont=dict(size=9), row=1, col=3)
fig24.update_layout(
    title_text='<b>Heatmap Regional: Acidentes e Vítimas (2023-2024-2025)</b>',
    height=400,
    font=dict(size=8),
    margin=dict(l=70, r=30, t=60, b=100)
)
salvar_grafico_acessivel(fig24, '24_heatmap_regional.html', 'Heatmap Regional')
print("✓ Gráfico 24 salvo")

# ===== GRÁFICO 25: BOX PLOT - VÍTIMAS POR REGIONAL =====
# Usando subplots para melhor visualização das legendas
regionais = sorted(df['Regional'].dropna().unique())

fig25 = make_subplots(
    rows=1, cols=3,
    subplot_titles=('2023', '2024', '2025'),
    shared_yaxes=True
)

for i, ano in enumerate([2023, 2024, 2025]):
    dados = df[df['Ano']==ano]
    for regional in regionais:
        vitimas = dados[dados['Regional']==regional]['Total de Vítimas'].dropna()
        if len(vitimas) > 0:
            fig25.add_trace(go.Box(
                y=vitimas,
                name=regional,
                boxmean='sd',
                marker_color=CORES_SIGMA[i],
                showlegend=(i == 0)  # Mostrar legenda apenas no primeiro subplot
            ), row=1, col=i+1)

fig25.update_layout(
    title='<b>Distribuição de Vítimas por Regional (2023-2024-2025)</b>',
    template='plotly_white',
    font=dict(size=10),
    height=600,
    hovermode='closest',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    )
)
fig25.update_yaxes(title_text='Total de Vítimas', row=1, col=1)
salvar_grafico_acessivel(fig25, '25_boxplot_vitimas_regional.html', 'Boxplot Vítimas por Regional')
print("✓ Gráfico 25 salvo")

# ===== GRÁFICO 26: TENDÊNCIA - TAXA DE VARIAÇÃO MENSAL =====
df['Ano-Mes'] = df['Data Abertura'].dt.to_period('M')
mensal_2023 = df[df['Ano']==2023].groupby(df[df['Ano']==2023]['Data Abertura'].dt.to_period('M')).size()
mensal_2024 = df[df['Ano']==2024].groupby(df[df['Ano']==2024]['Data Abertura'].dt.to_period('M')).size()
mensal_2025 = df[df['Ano']==2025].groupby(df[df['Ano']==2025]['Data Abertura'].dt.to_period('M')).size()

# Calcular taxa de variação 2024 vs 2023 e 2025 vs 2024
variacao_23_24 = []
variacao_24_25 = []
meses_comum = min(len(mensal_2023), len(mensal_2024), len(mensal_2025))
for i in range(1, meses_comum):
    taxa_23_24 = ((mensal_2024.iloc[i] - mensal_2023.iloc[i]) / mensal_2023.iloc[i] * 100) if mensal_2023.iloc[i] > 0 else 0
    taxa_24_25 = ((mensal_2025.iloc[i] - mensal_2024.iloc[i]) / mensal_2024.iloc[i] * 100) if mensal_2024.iloc[i] > 0 else 0
    variacao_23_24.append(taxa_23_24)
    variacao_24_25.append(taxa_24_25)

meses = [str(m) for m in mensal_2023.index[1:meses_comum]]

fig26 = go.Figure()
fig26.add_trace(go.Bar(
    x=meses,
    y=variacao_23_24,
    marker_color=CORES_SIGMA[1],
    text=[f"{v:.1f}%" for v in variacao_23_24],
    textposition='outside',
    name='Variação 2024 vs 2023'
))
fig26.add_trace(go.Bar(
    x=meses,
    y=variacao_24_25,
    marker_color=CORES_SIGMA[2],
    text=[f"{v:.1f}%" for v in variacao_24_25],
    textposition='outside',
    name='Variação 2025 vs 2024'
))
fig26.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Zero")
fig26.update_layout(
    title='<b>Taxa de Variação Mensal de Acidentes (2023-2024-2025)</b>',
    xaxis_title='Período',
    yaxis_title='Variação (%)',
    template='plotly_white',
    font=dict(size=10),
    height=550,
    hovermode='x unified',
    barmode='group',
    xaxis=dict(type='category', tickangle=-45),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.25,
        xanchor='center',
        x=0.5,
        itemwidth=80
    ),
    margin=dict(b=120)
)
salvar_grafico_acessivel(fig26, '26_tendencia_variacao_mensal.html', 'Tendência Variação Mensal')
print("✓ Gráfico 26 salvo")

# ===== GRÁFICO 27: ANÁLISE DE PERCENTIL DE VÍTIMAS =====
percentis = [10, 25, 50, 75, 90, 95, 99]
vitimas_2023 = df[df['Ano']==2023]['Total de Vítimas'].dropna()
vitimas_2024 = df[df['Ano']==2024]['Total de Vítimas'].dropna()
vitimas_2025 = df[df['Ano']==2025]['Total de Vítimas'].dropna()

percentis_2023 = [vitimas_2023.quantile(p/100) for p in percentis]
percentis_2024 = [vitimas_2024.quantile(p/100) for p in percentis]
percentis_2025 = [vitimas_2025.quantile(p/100) for p in percentis]

fig27 = go.Figure()
fig27.add_trace(go.Scatter(
    x=[f"P{p}" for p in percentis],
    y=percentis_2023,
    mode='lines+markers',
    name='2023',
    line=dict(color=CORES_SIGMA[0], width=3),
    marker=dict(size=10)
))
fig27.add_trace(go.Scatter(
    x=[f"P{p}" for p in percentis],
    y=percentis_2024,
    mode='lines+markers',
    name='2024',
    line=dict(color=CORES_SIGMA[1], width=3),
    marker=dict(size=10)
))
fig27.add_trace(go.Scatter(
    x=[f"P{p}" for p in percentis],
    y=percentis_2025,
    mode='lines+markers',
    name='2025',
    line=dict(color=CORES_SIGMA[2], width=3),
    marker=dict(size=10)
))
fig27.update_layout(
    title='<b>Análise de Percentis do Número de Vítimas (2023-2024-2025)</b>',
    xaxis_title='Percentil',
    yaxis_title='Vítimas',
    hovermode='x unified',
    template='plotly_white',
    font=dict(size=11),
    height=550,
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.12,
        xanchor='center',
        x=0.5,
        itemwidth=80
    ),
    margin=dict(b=100)
)
salvar_grafico_acessivel(fig27, '27_analise_percentis.html', 'Análise de Percentis')
print("✓ Gráfico 27 salvo")

# ===== GRÁFICO 28: MATRIZ DE FREQUÊNCIA RODOVIA x TIPO ACIDENTE =====
top_rodovias = df['Rodovia'].value_counts().head(10).index
top_tipos = df['Tipo Acidente'].value_counts().head(10).index

df_freq = df[df['Rodovia'].isin(top_rodovias) & df['Tipo Acidente'].isin(top_tipos)]
matriz_freq = pd.crosstab(df_freq['Rodovia'], df_freq['Tipo Acidente'])

# Formatar nomes das rodovias com prefixo SP- e 3 dígitos (ex: 8 => SP-008)
def formatar_rodovia(r):
    try:
        return f"SP-{int(r):03d}"
    except:
        return f"SP-{r}"

rodovias_formatadas = [formatar_rodovia(r) for r in matriz_freq.index]

fig28 = go.Figure(data=go.Heatmap(
    z=matriz_freq.values,
    x=matriz_freq.columns,
    y=rodovias_formatadas,
    colorscale='YlOrRd',
    text=matriz_freq.values,
    texttemplate='%{text}',
    textfont={"size": 7}
))
fig28.update_layout(
    title='<b>Matriz de Frequência: Top 10 Rodovias x Top 10 Tipos de Acidentes</b>',
    xaxis_title='Tipo de Acidente',
    yaxis_title='Rodovia',
    height=550,
    font=dict(size=8),
    xaxis=dict(tickangle=-45, tickfont=dict(size=7)),
    yaxis=dict(tickfont=dict(size=8)),
    margin=dict(l=80, r=30, t=60, b=120)
)
salvar_grafico_acessivel(fig28, '28_matriz_rodovia_tipo.html', 'Matriz Rodovia x Tipo')
print("✓ Gráfico 28 salvo")

# ===== GRÁFICO 29: RESUMO ESTATÍSTICO COMPARATIVO =====
stats_comparativo = pd.DataFrame({
    '2023': [
        len(df[df['Ano']==2023]),
        df[df['Ano']==2023]['Total de Vítimas'].sum(),
        df[df['Ano']==2023]['Fatal'].sum(),
        df[df['Ano']==2023]['Grave'].sum(),
        df[df['Ano']==2023]['Leve'].sum()
    ],
    '2024': [
        len(df[df['Ano']==2024]),
        df[df['Ano']==2024]['Total de Vítimas'].sum(),
        df[df['Ano']==2024]['Fatal'].sum(),
        df[df['Ano']==2024]['Grave'].sum(),
        df[df['Ano']==2024]['Leve'].sum()
    ],
    '2025': [
        len(df[df['Ano']==2025]),
        df[df['Ano']==2025]['Total de Vítimas'].sum(),
        df[df['Ano']==2025]['Fatal'].sum(),
        df[df['Ano']==2025]['Grave'].sum(),
        df[df['Ano']==2025]['Leve'].sum()
    ]
}, index=['Total Acidentes', 'Total Vítimas', 'Óbitos', 'Graves', 'Leves'])

stats_comparativo['Var 23-24 %'] = ((stats_comparativo['2024'] - stats_comparativo['2023']) / stats_comparativo['2023'] * 100).round(2)
stats_comparativo['Var 24-25 %'] = ((stats_comparativo['2025'] - stats_comparativo['2024']) / stats_comparativo['2024'] * 100).round(2)

fig29 = go.Figure(data=[
    go.Bar(name='2023', x=stats_comparativo.index, y=stats_comparativo['2023'], marker_color=CORES_SIGMA[0]),
    go.Bar(name='2024', x=stats_comparativo.index, y=stats_comparativo['2024'], marker_color=CORES_SIGMA[1]),
    go.Bar(name='2025', x=stats_comparativo.index, y=stats_comparativo['2025'], marker_color=CORES_SIGMA[2])
])
fig29.update_layout(
    title='<b>Resumo Estatístico Comparativo (2023-2024-2025)</b>',
    yaxis_title='Valor',
    barmode='group',
    template='plotly_white',
    font=dict(size=10),
    height=550,
    xaxis=dict(type='category', tickangle=-45),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.25,
        xanchor='center',
        x=0.5,
        itemwidth=80
    ),
    margin=dict(b=120)
)
salvar_grafico_acessivel(fig29, '29_resumo_estatistico.html', 'Resumo Estatístico')
print("✓ Gráfico 29 salvo")

print("\n✓ 6 gráficos de tendências regionais gerados com sucesso!")
