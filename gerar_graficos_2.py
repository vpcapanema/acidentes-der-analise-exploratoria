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

print("Gerando gráficos avançados...")

# ===== GRÁFICO 8: SÉRIE TEMPORAL DE ACIDENTES MENSAIS =====
df['Mes'] = df['Data Abertura'].dt.month
meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

fig8 = go.Figure()
for i, ano in enumerate([2023, 2024, 2025]):
    dados_ano = df[df['Ano']==ano].groupby('Mes').size().reindex(range(1, 13), fill_value=0)
    fig8.add_trace(go.Scatter(
        x=meses_nomes,
        y=dados_ano.values,
        mode='lines+markers',
        name=str(ano),
        marker=dict(size=8, color=CORES_SIGMA[i]),
        line=dict(width=2, color=CORES_SIGMA[i])
    ))

fig8.update_layout(
    title='<b>Série Temporal: Acidentes por Mês (2023-2024-2025)</b>',
    xaxis_title='Mês',
    yaxis_title='Quantidade de Acidentes',
    hovermode='x unified',
    template='plotly_white',
    font=dict(size=11),
    height=650,
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
salvar_grafico_acessivel(fig8, '08_serie_temporal_acidentes.html', 'Série Temporal de Acidentes')
print("✓ Gráfico 8 salvo")

# ===== GRÁFICO 9: SÉRIE TEMPORAL DE VÍTIMAS MENSAIS =====
fig9 = go.Figure()
for i, ano in enumerate([2023, 2024, 2025]):
    dados_ano = df[df['Ano']==ano].groupby('Mes')['Total de Vítimas'].sum().reindex(range(1, 13), fill_value=0)
    fig9.add_trace(go.Scatter(
        x=meses_nomes,
        y=dados_ano.values,
        mode='lines+markers',
        name=str(ano),
        marker=dict(size=8, color=CORES_SIGMA[i]),
        line=dict(width=2, color=CORES_SIGMA[i])
    ))

fig9.update_layout(
    title='<b>Série Temporal: Total de Vítimas por Mês (2023-2024-2025)</b>',
    xaxis_title='Mês',
    yaxis_title='Total de Vítimas',
    hovermode='x unified',
    template='plotly_white',
    font=dict(size=11),
    height=650,
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
salvar_grafico_acessivel(fig9, '09_serie_temporal_vitimas.html', 'Série Temporal de Vítimas')
print("✓ Gráfico 9 salvo")

# ===== GRÁFICO 10: TAXA DE SEVERIDADE (GRAVES E FATAIS) =====
severidade_2023 = df[df['Ano']==2023].copy()
severidade_2024 = df[df['Ano']==2024].copy()
severidade_2025 = df[df['Ano']==2025].copy()

severidade_2023['Severidade'] = ((severidade_2023['Grave'] + severidade_2023['Fatal'] * 2) / 
                                  (severidade_2023['Leve'] + severidade_2023['Grave'] + severidade_2023['Fatal'] + 1)) * 100
severidade_2024['Severidade'] = ((severidade_2024['Grave'] + severidade_2024['Fatal'] * 2) / 
                                  (severidade_2024['Leve'] + severidade_2024['Grave'] + severidade_2024['Fatal'] + 1)) * 100
severidade_2025['Severidade'] = ((severidade_2025['Grave'] + severidade_2025['Fatal'] * 2) / 
                                  (severidade_2025['Leve'] + severidade_2025['Grave'] + severidade_2025['Fatal'] + 1)) * 100

fig10 = go.Figure()
fig10.add_trace(go.Box(
    y=severidade_2023['Severidade'],
    name='2023',
    marker_color=CORES_SIGMA[0],
    boxmean='sd'
))
fig10.add_trace(go.Box(
    y=severidade_2024['Severidade'],
    name='2024',
    marker_color=CORES_SIGMA[1],
    boxmean='sd'
))
fig10.add_trace(go.Box(
    y=severidade_2025['Severidade'],
    name='2025',
    marker_color=CORES_SIGMA[2],
    boxmean='sd'
))
fig10.update_layout(
    title='<b>Distribuição do Índice de Severidade dos Acidentes</b>',
    yaxis_title='Índice de Severidade (%)',
    hovermode='y unified',
    template='plotly_white',
    font=dict(size=11),
    height=550,
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
salvar_grafico_acessivel(fig10, '10_severidade_acidentes.html', 'Severidade dos Acidentes')
print("✓ Gráfico 10 salvo")

# ===== GRÁFICO 11: DISTRIBUIÇÃO POR SENTIDO =====
# Nota: Em 2025 houve mudança no padrão de registro - de Crescente/Decrescente para coordenadas cardeais
sentidos_2023 = df[df['Ano']==2023]['Sentido'].value_counts()
sentidos_2024 = df[df['Ano']==2024]['Sentido'].value_counts()
# Para 2025, agrupar os principais sentidos cardeais
sentidos_2025_raw = df[df['Ano']==2025]['Sentido'].value_counts()
# Manter apenas os 4 principais (Norte, Sul, Leste, Oeste)
sentidos_2025 = sentidos_2025_raw.head(4)
sentidos_2025['Outros'] = sentidos_2025_raw.iloc[4:].sum()

fig11 = make_subplots(
    rows=1, cols=3,
    subplot_titles=('2023 (Crescente/Decrescente)', '2024 (Crescente/Decrescente)', '2025 (Coordenadas Cardeais)'),
    specs=[[{'type':'pie'}, {'type':'pie'}, {'type':'pie'}]]
)

fig11.add_trace(
    go.Pie(labels=sentidos_2023.index, values=sentidos_2023.values, name='2023',
            marker=dict(colors=['#1E3A5F', '#3D5A80', '#5C7AA0'])),
    row=1, col=1
)
fig11.add_trace(
    go.Pie(labels=sentidos_2024.index, values=sentidos_2024.values, name='2024',
            marker=dict(colors=['#2E7D32', '#4E9D52', '#6EBD72'])),
    row=1, col=2
)
fig11.add_trace(
    go.Pie(labels=sentidos_2025.index, values=sentidos_2025.values, name='2025',
            marker=dict(colors=['#F9A825', '#FBC02D', '#FDD835', '#FFEB3B', '#FFF176'])),
    row=1, col=3
)
fig11.update_layout(
    title_text='<b>Acidentes por Sentido da Via (2023-2024-2025)</b><br><sup>⚠️ Em 2025 houve mudança no padrão de registro: de Crescente/Decrescente para coordenadas cardeais (Norte/Sul/Leste/Oeste)</sup>',
    height=550,
    font=dict(size=11)
)
salvar_grafico_acessivel(fig11, '11_acidentes_por_sentido.html', 'Acidentes por Sentido')
print("✓ Gráfico 11 salvo")

# ===== GRÁFICO 12: DISTRIBUIÇÃO DE KM =====
km_2023 = df[df['Ano']==2023]['Km'].dropna()
km_2024 = df[df['Ano']==2024]['Km'].dropna()
km_2025 = df[df['Ano']==2025]['Km'].dropna()

fig12 = go.Figure()
fig12.add_trace(go.Histogram(
    x=km_2023,
    nbinsx=50,
    name='2023',
    marker_color=CORES_SIGMA[0],
    opacity=0.6
))
fig12.add_trace(go.Histogram(
    x=km_2024,
    nbinsx=50,
    name='2024',
    marker_color=CORES_SIGMA[1],
    opacity=0.6
))
fig12.add_trace(go.Histogram(
    x=km_2025,
    nbinsx=50,
    name='2025',
    marker_color=CORES_SIGMA[2],
    opacity=0.6
))
fig12.update_layout(
    title='<b>Distribuição de Acidentes por Kilometragem (2023-2024-2025)</b>',
    xaxis_title='Quilometragem (km)',
    yaxis_title='Quantidade',
    barmode='overlay',
    hovermode='x unified',
    template='plotly_white',
    font=dict(size=11),
    height=550,
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
salvar_grafico_acessivel(fig12, '12_distribuicao_km.html', 'Distribuição por Quilometragem')
print("✓ Gráfico 12 salvo")

# ===== GRÁFICO 13: HEATMAP - ACIDENTES POR RODOVIA E MÊS =====
df['Mes'] = df['Data Abertura'].dt.month
df['Mes_Nome'] = df['Mes'].map({1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr', 5:'Mai', 6:'Jun',
                                 7:'Jul', 8:'Ago', 9:'Set', 10:'Out', 11:'Nov', 12:'Dez'})

# Top 15 rodovias
top_rodovias = df['Rodovia'].value_counts().head(15).index
df_heatmap = df[df['Rodovia'].isin(top_rodovias)]

heatmap_2023 = df_heatmap[df_heatmap['Ano']==2023].groupby(['Rodovia', 'Mes_Nome']).size().unstack(fill_value=0)
heatmap_2024 = df_heatmap[df_heatmap['Ano']==2024].groupby(['Rodovia', 'Mes_Nome']).size().unstack(fill_value=0)
heatmap_2025 = df_heatmap[df_heatmap['Ano']==2025].groupby(['Rodovia', 'Mes_Nome']).size().unstack(fill_value=0)

# Ordenar meses
meses_ordem = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
heatmap_2023 = heatmap_2023.reindex(columns=[m for m in meses_ordem if m in heatmap_2023.columns], fill_value=0)
heatmap_2024 = heatmap_2024.reindex(columns=[m for m in meses_ordem if m in heatmap_2024.columns], fill_value=0)
heatmap_2025 = heatmap_2025.reindex(columns=[m for m in meses_ordem if m in heatmap_2025.columns], fill_value=0)

# Formatar nomes das rodovias com prefixo SP- e 3 dígitos (ex: 8 => SP-008)
def formatar_rodovia(r):
    try:
        return f"SP-{int(r):03d}"
    except:
        return f"SP-{r}"

heatmap_2023.index = [formatar_rodovia(r) for r in heatmap_2023.index]
heatmap_2024.index = [formatar_rodovia(r) for r in heatmap_2024.index]
heatmap_2025.index = [formatar_rodovia(r) for r in heatmap_2025.index]

fig13 = make_subplots(
    rows=1, cols=3,
    subplot_titles=('2023', '2024', '2025'),
    specs=[[{'type':'heatmap'}, {'type':'heatmap'}, {'type':'heatmap'}]],
    horizontal_spacing=0.08
)

fig13.add_trace(
    go.Heatmap(z=heatmap_2023.values, x=heatmap_2023.columns, y=heatmap_2023.index,
               colorscale='Blues', name='2023', colorbar=dict(x=0.28, len=0.8, thickness=10)),
    row=1, col=1
)
fig13.add_trace(
    go.Heatmap(z=heatmap_2024.values if len(heatmap_2024) > 0 else [[0]], 
               x=heatmap_2024.columns if len(heatmap_2024.columns) > 0 else ['Jan'], 
               y=heatmap_2024.index if len(heatmap_2024) > 0 else [''],
               colorscale='Greens', name='2024', colorbar=dict(x=0.64, len=0.8, thickness=10)),
    row=1, col=2
)
fig13.add_trace(
    go.Heatmap(z=heatmap_2025.values, x=heatmap_2025.columns, y=heatmap_2025.index,
               colorscale='YlOrBr', name='2025', colorbar=dict(x=1.0, len=0.8, thickness=10)),
    row=1, col=3
)
fig13.update_xaxes(title_text='Mês', row=1, col=1, tickfont=dict(size=7), tickangle=-45)
fig13.update_xaxes(title_text='Mês', row=1, col=2, tickfont=dict(size=7), tickangle=-45)
fig13.update_xaxes(title_text='Mês', row=1, col=3, tickfont=dict(size=7), tickangle=-45)
fig13.update_yaxes(title_text='Rodovia', row=1, col=1, tickfont=dict(size=7))
fig13.update_yaxes(tickfont=dict(size=7), row=1, col=2)
fig13.update_yaxes(tickfont=dict(size=7), row=1, col=3)
fig13.update_layout(
    title_text='<b>Heatmap: Acidentes por Rodovia e Mês (Top 15 Rodovias)</b>',
    height=550,
    font=dict(size=8),
    margin=dict(l=80, r=30, t=60, b=80)
)
salvar_grafico_acessivel(fig13, '13_heatmap_rodovia_mes.html', 'Heatmap Rodovia x Mês')
print("✓ Gráfico 13 salvo")

print("\n✓ 6 gráficos avançados gerados com sucesso!")
