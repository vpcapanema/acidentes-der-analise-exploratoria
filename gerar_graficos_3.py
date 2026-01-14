import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy import stats
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
df_total['Nova data'] = pd.to_datetime(df_total['Nova data'], errors='coerce')

# Incluir todos os três anos de análise (2023, 2024, 2025)
df = df_total[df_total['Ano'].isin([2023, 2024, 2025])].copy()

# Paleta de cores Sigma-PLI (azul institucional, verde, amarelo)
CORES_SIGMA = ['#1E3A5F', '#2E7D32', '#F9A825']  # Azul, Verde, Amarelo

print("Gerando análises estatísticas avançadas...")

# ===== GRÁFICO 14: ESTATÍSTICAS COMPARATIVAS =====
stats_2023 = df[df['Ano']==2023].agg({
    'Leve': 'sum',
    'Grave': 'sum',
    'Fatal': 'sum',
    'Total de Vítimas': 'sum'
})
stats_2024 = df[df['Ano']==2024].agg({
    'Leve': 'sum',
    'Grave': 'sum',
    'Fatal': 'sum',
    'Total de Vítimas': 'sum'
})
stats_2025 = df[df['Ano']==2025].agg({
    'Leve': 'sum',
    'Grave': 'sum',
    'Fatal': 'sum',
    'Total de Vítimas': 'sum'
})

# Calcular variação percentual
variacao_23_24 = ((stats_2024 - stats_2023) / stats_2023 * 100).round(2)
variacao_24_25 = ((stats_2025 - stats_2024) / stats_2024 * 100).round(2)

fig14 = go.Figure()
metricas = ['Leve', 'Grave', 'Fatal', 'Total de Vítimas']
fig14.add_trace(go.Bar(
    x=metricas,
    y=stats_2023.values,
    name='2023',
    marker_color=CORES_SIGMA[0],
    text=[f"{int(v)}" for v in stats_2023.values],
    textposition='outside'
))
fig14.add_trace(go.Bar(
    x=metricas,
    y=stats_2024.values,
    name='2024',
    marker_color=CORES_SIGMA[1],
    text=[f"{int(v)}" for v in stats_2024.values],
    textposition='outside'
))
fig14.add_trace(go.Bar(
    x=metricas,
    y=stats_2025.values,
    name='2025',
    marker_color=CORES_SIGMA[2],
    text=[f"{int(v)}" for v in stats_2025.values],
    textposition='outside'
))
fig14.update_layout(
    title='<b>Comparação de Vítimas: 2023 vs 2024 vs 2025</b>',
    xaxis_title='Categoria',
    yaxis_title='Quantidade',
    barmode='group',
    hovermode='x unified',
    template='plotly_white',
    font=dict(size=12),
    height=550,
    xaxis=dict(type='category'),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.20,
        xanchor='center',
        x=0.5,
        itemwidth=80
    ),
    margin=dict(b=130)
)
salvar_grafico_acessivel(fig14, '14_comparacao_vitimas.html', 'Comparação de Vítimas')
print("✓ Gráfico 14 salvo")

# ===== GRÁFICO 15: DENSIDADE DE ACIDENTES POR KM =====
# Dividir em faixas de km
df['Faixa_KM'] = pd.cut(df['Km'], bins=range(0, 700, 50), labels=[f"{i}-{i+50}" for i in range(0, 650, 50)])

densidade_2023 = df[df['Ano']==2023]['Faixa_KM'].value_counts().sort_index()
densidade_2024 = df[df['Ano']==2024]['Faixa_KM'].value_counts().sort_index()
densidade_2025 = df[df['Ano']==2025]['Faixa_KM'].value_counts().sort_index()

fig15 = go.Figure()
fig15.add_trace(go.Bar(x=densidade_2023.index.astype(str), y=densidade_2023.values, name='2023', marker_color=CORES_SIGMA[0]))
fig15.add_trace(go.Bar(x=densidade_2024.index.astype(str), y=densidade_2024.values, name='2024', marker_color=CORES_SIGMA[1]))
fig15.add_trace(go.Bar(x=densidade_2025.index.astype(str), y=densidade_2025.values, name='2025', marker_color=CORES_SIGMA[2]))
fig15.update_layout(
    title='<b>Densidade de Acidentes por Faixa de Quilometragem (2023-2024-2025)</b>',
    xaxis_title='Faixa de Quilometragem (km)',
    yaxis_title='Quantidade de Acidentes',
    barmode='group',
    hovermode='x unified',
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
salvar_grafico_acessivel(fig15, '15_densidade_km.html', 'Densidade por Quilometragem')
print("✓ Gráfico 15 salvo")

# ===== GRÁFICO 16: ANÁLISE POR DIA DA SEMANA =====
df['Dia_Semana'] = df['Data Abertura'].dt.day_name()
dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dias_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']

dia_semana_2023 = df[df['Ano']==2023]['Dia_Semana'].value_counts().reindex(dias_ordem, fill_value=0)
dia_semana_2024 = df[df['Ano']==2024]['Dia_Semana'].value_counts().reindex(dias_ordem, fill_value=0)
dia_semana_2025 = df[df['Ano']==2025]['Dia_Semana'].value_counts().reindex(dias_ordem, fill_value=0)

fig16 = go.Figure()
fig16.add_trace(go.Bar(x=dias_pt, y=dia_semana_2023.values, name='2023', marker_color=CORES_SIGMA[0]))
fig16.add_trace(go.Bar(x=dias_pt, y=dia_semana_2024.values, name='2024', marker_color=CORES_SIGMA[1]))
fig16.add_trace(go.Bar(x=dias_pt, y=dia_semana_2025.values, name='2025', marker_color=CORES_SIGMA[2]))
fig16.update_layout(
    title='<b>Acidentes por Dia da Semana (2023-2024-2025)</b>',
    xaxis_title='Dia da Semana',
    yaxis_title='Quantidade',
    barmode='group',
    hovermode='x unified',
    template='plotly_white',
    font=dict(size=11),
    height=550,
    xaxis=dict(type='category'),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.18,
        xanchor='center',
        x=0.5,
        itemwidth=80
    ),
    margin=dict(b=130)
)
salvar_grafico_acessivel(fig16, '16_acidentes_dia_semana.html', 'Acidentes por Dia da Semana')
print("✓ Gráfico 16 salvo")

# ===== GRÁFICO 17: SCATTER PLOT - KM vs VÍTIMAS =====
df_sample_2023 = df[df['Ano']==2023].dropna(subset=['Km', 'Total de Vítimas']).sample(min(1500, len(df[df['Ano']==2023])))
df_sample_2024 = df[df['Ano']==2024].dropna(subset=['Km', 'Total de Vítimas']).sample(min(1500, len(df[df['Ano']==2024])))
df_sample_2025 = df[df['Ano']==2025].dropna(subset=['Km', 'Total de Vítimas']).sample(min(1500, len(df[df['Ano']==2025])))

fig17 = go.Figure()
fig17.add_trace(go.Scatter(
    x=df_sample_2023['Km'],
    y=df_sample_2023['Total de Vítimas'],
    mode='markers',
    name='2023',
    marker=dict(size=5, color=CORES_SIGMA[0], opacity=0.6),
    text=df_sample_2023['Rodovia'],
    hovertemplate='<b>Rodovia:</b> %{text}<br><b>KM:</b> %{x}<br><b>Vítimas:</b> %{y}'
))
fig17.add_trace(go.Scatter(
    x=df_sample_2024['Km'],
    y=df_sample_2024['Total de Vítimas'],
    mode='markers',
    name='2024',
    marker=dict(size=5, color=CORES_SIGMA[1], opacity=0.6),
    text=df_sample_2024['Rodovia'],
    hovertemplate='<b>Rodovia:</b> %{text}<br><b>KM:</b> %{x}<br><b>Vítimas:</b> %{y}'
))
fig17.add_trace(go.Scatter(
    x=df_sample_2025['Km'],
    y=df_sample_2025['Total de Vítimas'],
    mode='markers',
    name='2025',
    marker=dict(size=5, color=CORES_SIGMA[2], opacity=0.6),
    text=df_sample_2025['Rodovia'],
    hovertemplate='<b>Rodovia:</b> %{text}<br><b>KM:</b> %{x}<br><b>Vítimas:</b> %{y}'
))
fig17.update_layout(
    title='<b>Relação entre Quilometragem e Número de Vítimas (2023-2024-2025)</b>',
    xaxis_title='Quilometragem (km)',
    yaxis_title='Total de Vítimas',
    hovermode='closest',
    template='plotly_white',
    font=dict(size=11),
    height=650,
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.15,
        xanchor='center',
        x=0.5,
        itemwidth=80
    ),
    margin=dict(b=120)
)
salvar_grafico_acessivel(fig17, '17_scatter_km_vitimas.html', 'Relação KM x Vítimas')
print("✓ Gráfico 17 salvo")

# ===== GRÁFICO 18: DISTRIBUIÇÃO POR TIPO DE ACIDENTE E GRAVIDADE =====
df['Gravidade_Categoria'] = 'Sem Vítimas'
df.loc[df['Leve'] > 0, 'Gravidade_Categoria'] = 'Leve'
df.loc[df['Grave'] > 0, 'Gravidade_Categoria'] = 'Grave'
df.loc[df['Fatal'] > 0, 'Gravidade_Categoria'] = 'Fatal'

top_tipos = df['Tipo Acidente'].value_counts().head(8).index
df_tipos = df[df['Tipo Acidente'].isin(top_tipos)]

fig18 = make_subplots(
    rows=1, cols=3,
    subplot_titles=('2023', '2024', '2025'),
    specs=[[{'type':'bar'}, {'type':'bar'}, {'type':'bar'}]]
)

for ano, col in [(2023, 1), (2024, 2), (2025, 3)]:
    dados = df_tipos[df_tipos['Ano']==ano]
    tipo_gravidade = pd.crosstab(dados['Tipo Acidente'], dados['Gravidade_Categoria'])
    
    for gravidade in tipo_gravidade.columns:
        fig18.add_trace(
            go.Bar(x=tipo_gravidade.index, y=tipo_gravidade[gravidade], name=gravidade, showlegend=(col==1)),
            row=1, col=col
        )

fig18.update_xaxes(title_text='Tipo de Acidente', row=1, col=1, tickangle=-45)
fig18.update_xaxes(title_text='Tipo de Acidente', row=1, col=2, tickangle=-45)
fig18.update_xaxes(title_text='Tipo de Acidente', row=1, col=3, tickangle=-45)
fig18.update_layout(
    title_text='<b>Tipos de Acidentes por Categoria de Gravidade (Top 8) - 2023-2024-2025</b>',
    height=700,
    barmode='stack',
    template='plotly_white',
    font=dict(size=10),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.25,
        xanchor='center',
        x=0.5,
        itemwidth=60
    ),
    margin=dict(b=150)
)
salvar_grafico_acessivel(fig18, '18_tipos_acidentes_gravidade.html', 'Tipos de Acidentes por Gravidade')
print("✓ Gráfico 18 salvo")

print("\n✓ 5 gráficos de análise estatística gerados com sucesso!")
