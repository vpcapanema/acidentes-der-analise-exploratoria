import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
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

print("Gerando gráficos interativos...")

# ===== GRÁFICO 1: TOTAL DE ACIDENTES POR ANO =====
fig1 = go.Figure()
acidentes_por_ano = df.groupby('Ano').size()
fig1.add_trace(go.Bar(
    x=acidentes_por_ano.index,
    y=acidentes_por_ano.values,
    marker_color=CORES_SIGMA,
    text=acidentes_por_ano.values,
    textposition='outside',
    name='Total de Acidentes'
))
fig1.update_layout(
    title='<b>Total de Acidentes por Ano</b>',
    xaxis_title='Ano',
    yaxis_title='Quantidade de Acidentes',
    hovermode='x unified',
    template='plotly_white',
    font=dict(size=12),
    height=500,
    xaxis=dict(tickmode='array', tickvals=acidentes_por_ano.index.tolist(), ticktext=[str(a) for a in acidentes_por_ano.index.tolist()])
)
salvar_grafico_acessivel(fig1, '01_total_acidentes_por_ano.html', 'Total de Acidentes por Ano')
print("✓ Gráfico 1 salvo")

# ===== GRÁFICO 2: VÍTIMAS POR ANO (LEVE, GRAVE, FATAL) =====
victimas_2023 = df[df['Ano']==2023][['Leve', 'Grave', 'Fatal']].sum()
victimas_2024 = df[df['Ano']==2024][['Leve', 'Grave', 'Fatal']].sum()
victimas_2025 = df[df['Ano']==2025][['Leve', 'Grave', 'Fatal']].sum()

fig2 = go.Figure()
fig2.add_trace(go.Bar(x=['Leve', 'Grave', 'Fatal'], y=victimas_2023.values, name='2023', marker_color=CORES_SIGMA[0]))
fig2.add_trace(go.Bar(x=['Leve', 'Grave', 'Fatal'], y=victimas_2024.values, name='2024', marker_color=CORES_SIGMA[1]))
fig2.add_trace(go.Bar(x=['Leve', 'Grave', 'Fatal'], y=victimas_2025.values, name='2025', marker_color=CORES_SIGMA[2]))
fig2.update_layout(
    title='<b>Vítimas por Tipo de Gravidade (2023-2024-2025)</b>',
    xaxis_title='Tipo de Vítima',
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
salvar_grafico_acessivel(fig2, '02_vitimas_por_gravidade.html', 'Vítimas por Gravidade')
print("✓ Gráfico 2 salvo")

# ===== GRÁFICO 3: TOTAL DE VÍTIMAS POR ANO =====
fig3 = go.Figure()
vitimas_total = df.groupby('Ano')['Total de Vítimas'].sum()
fig3.add_trace(go.Bar(
    x=vitimas_total.index,
    y=vitimas_total.values,
    marker_color=CORES_SIGMA,
    text=vitimas_total.values,
    textposition='outside',
    name='Total de Vítimas'
))
fig3.update_layout(
    title='<b>Total de Vítimas por Ano</b>',
    xaxis_title='Ano',
    yaxis_title='Total de Vítimas',
    hovermode='x unified',
    template='plotly_white',
    font=dict(size=12),
    height=500,
    xaxis=dict(tickmode='array', tickvals=vitimas_total.index.tolist(), ticktext=[str(a) for a in vitimas_total.index.tolist()])
)
salvar_grafico_acessivel(fig3, '03_total_vitimas_por_ano.html', 'Total de Vítimas por Ano')
print("✓ Gráfico 3 salvo")

# ===== GRÁFICO 4: TIPOS DE ACIDENTES =====
tipos_2023 = df[df['Ano']==2023]['Tipo Acidente'].value_counts().head(10)
tipos_2024 = df[df['Ano']==2024]['Tipo Acidente'].value_counts().head(10)
tipos_2025 = df[df['Ano']==2025]['Tipo Acidente'].value_counts().head(10)

fig4 = make_subplots(
    rows=1, cols=3,
    subplot_titles=('Top 10 Tipos - 2023', 'Top 10 Tipos - 2024', 'Top 10 Tipos - 2025'),
    specs=[[{'type':'bar'}, {'type':'bar'}, {'type':'bar'}]]
)
fig4.add_trace(
    go.Bar(x=tipos_2023.values, y=tipos_2023.index, orientation='h', 
           marker_color=CORES_SIGMA[0], name='2023'),
    row=1, col=1
)
fig4.add_trace(
    go.Bar(x=tipos_2024.values, y=tipos_2024.index, orientation='h',
           marker_color=CORES_SIGMA[1], name='2024'),
    row=1, col=2
)
fig4.add_trace(
    go.Bar(x=tipos_2025.values, y=tipos_2025.index, orientation='h',
           marker_color=CORES_SIGMA[2], name='2025'),
    row=1, col=3
)
fig4.update_xaxes(title_text='Quantidade', row=1, col=1)
fig4.update_xaxes(title_text='Quantidade', row=1, col=2)
fig4.update_xaxes(title_text='Quantidade', row=1, col=3)
fig4.update_yaxes(title_text='Tipo de Acidente', row=1, col=1)
fig4.update_layout(
    title_text='<b>Top 10 Tipos de Acidentes por Ano (2023-2024-2025)</b>',
    height=600,
    showlegend=False,
    template='plotly_white',
    font=dict(size=10)
)
salvar_grafico_acessivel(fig4, '04_tipos_acidentes.html', 'Tipos de Acidentes')
print("✓ Gráfico 4 salvo")

# ===== GRÁFICO 5: RODOVIAS COM MAIS ACIDENTES =====
rodovias_2023 = df[df['Ano']==2023]['Rodovia'].value_counts().head(15)
rodovias_2024 = df[df['Ano']==2024]['Rodovia'].value_counts().head(15)
rodovias_2025 = df[df['Ano']==2025]['Rodovia'].value_counts().head(15)

fig5 = make_subplots(
    rows=1, cols=3,
    subplot_titles=('Top 15 Rodovias - 2023', 'Top 15 Rodovias - 2024', 'Top 15 Rodovias - 2025'),
    specs=[[{'type':'bar'}, {'type':'bar'}, {'type':'bar'}]]
)
fig5.add_trace(
    go.Bar(x=rodovias_2023.values, y=rodovias_2023.index, orientation='h',
           marker_color=CORES_SIGMA[0], name='2023'),
    row=1, col=1
)
fig5.add_trace(
    go.Bar(x=rodovias_2024.values, y=rodovias_2024.index, orientation='h',
           marker_color=CORES_SIGMA[1], name='2024'),
    row=1, col=2
)
fig5.add_trace(
    go.Bar(x=rodovias_2025.values, y=rodovias_2025.index, orientation='h',
           marker_color=CORES_SIGMA[2], name='2025'),
    row=1, col=3
)
fig5.update_xaxes(title_text='Quantidade', row=1, col=1)
fig5.update_xaxes(title_text='Quantidade', row=1, col=2)
fig5.update_xaxes(title_text='Quantidade', row=1, col=3)
fig5.update_yaxes(title_text='Rodovia', row=1, col=1)
fig5.update_layout(
    title_text='<b>Top 15 Rodovias com Mais Acidentes (2023-2024-2025)</b>',
    height=700,
    showlegend=False,
    template='plotly_white',
    font=dict(size=10)
)
salvar_grafico_acessivel(fig5, '05_rodovias_mais_acidentes.html', 'Rodovias com Mais Acidentes')
print("✓ Gráfico 5 salvo")

# ===== GRÁFICO 6: REGIÕES COM MAIS ACIDENTES =====
regioes_2023 = df[df['Ano']==2023]['Regional'].value_counts()
regioes_2024 = df[df['Ano']==2024]['Regional'].value_counts()
regioes_2025 = df[df['Ano']==2025]['Regional'].value_counts()

fig6 = go.Figure()
fig6.add_trace(go.Bar(x=regioes_2023.index, y=regioes_2023.values, name='2023', marker_color=CORES_SIGMA[0]))
fig6.add_trace(go.Bar(x=regioes_2024.index, y=regioes_2024.values, name='2024', marker_color=CORES_SIGMA[1]))
fig6.add_trace(go.Bar(x=regioes_2025.index, y=regioes_2025.values, name='2025', marker_color=CORES_SIGMA[2]))
fig6.update_layout(
    title='<b>Acidentes por Regional (2023-2024-2025)</b>',
    xaxis_title='Regional',
    yaxis_title='Quantidade de Acidentes',
    barmode='group',
    hovermode='x unified',
    template='plotly_white',
    font=dict(size=11),
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
salvar_grafico_acessivel(fig6, '06_acidentes_por_regional.html', 'Acidentes por Regional')
print("✓ Gráfico 6 salvo")

# ===== GRÁFICO 7: OCORRÊNCIAS =====
# Normalizar os nomes de ocorrência (2025 usa capitalização diferente)
df['Ocorrencia_Norm'] = df['Ocorrencia'].str.title()  # Padroniza para Title Case

# Usar as mesmas categorias (top 12 geral) para todos os anos
top_ocorrencias = df['Ocorrencia_Norm'].value_counts().head(12).index.tolist()

ocorrencias_2023 = df[df['Ano']==2023]['Ocorrencia_Norm'].value_counts().reindex(top_ocorrencias, fill_value=0)
ocorrencias_2024 = df[df['Ano']==2024]['Ocorrencia_Norm'].value_counts().reindex(top_ocorrencias, fill_value=0)
ocorrencias_2025 = df[df['Ano']==2025]['Ocorrencia_Norm'].value_counts().reindex(top_ocorrencias, fill_value=0)

fig7 = go.Figure()
fig7.add_trace(go.Bar(x=top_ocorrencias, y=ocorrencias_2023.values, name='2023', marker_color=CORES_SIGMA[0]))
fig7.add_trace(go.Bar(x=top_ocorrencias, y=ocorrencias_2024.values, name='2024', marker_color=CORES_SIGMA[1]))
fig7.add_trace(go.Bar(x=top_ocorrencias, y=ocorrencias_2025.values, name='2025', marker_color=CORES_SIGMA[2]))
fig7.update_layout(
    title='<b>Tipos de Ocorrências (Top 12) - 2023-2024-2025</b>',
    xaxis_title='Tipo de Ocorrência',
    yaxis_title='Quantidade',
    barmode='group',
    hovermode='x unified',
    template='plotly_white',
    font=dict(size=10),
    height=600,
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
salvar_grafico_acessivel(fig7, '07_tipos_ocorrencias.html', 'Tipos de Ocorrências')
print("✓ Gráfico 7 salvo")

print("\n✓ 7 gráficos gerados com sucesso!")
