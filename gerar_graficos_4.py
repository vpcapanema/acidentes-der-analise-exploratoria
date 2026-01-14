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

print("Gerando gráficos de análise de padrões...")

# ===== GRÁFICO 19: CORRELAÇÃO ENTRE VARIÁVEIS =====
from scipy.stats import pearsonr

df_numeric = df[['Km', 'Leve', 'Grave', 'Fatal', 'Total de Vítimas']].dropna()

# Calcular matriz de correlação
corr_matrix = df_numeric.corr()

fig19 = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=corr_matrix.columns,
    y=corr_matrix.columns,
    colorscale='RdBu',
    zmid=0,
    text=corr_matrix.values.round(3),
    texttemplate='%{text}',
    textfont={"size": 10},
    colorbar=dict(title="Correlação")
))
fig19.update_layout(
    title='<b>Matriz de Correlação de Variáveis</b>',
    height=500,
    font=dict(size=11)
)
salvar_grafico_acessivel(fig19, '19_matriz_correlacao.html', 'Matriz de Correlação')
print("✓ Gráfico 19 salvo")

# ===== GRÁFICO 20: TOP 20 RODOVIAS MAIS PERIGOSAS (ÍNDICE COMPOSTO) =====
# Calcular índice de periculosidade
rodovia_stats = df.groupby('Rodovia').agg({
    'Evento': 'count',  # total de acidentes
    'Fatal': 'sum',
    'Grave': 'sum',
    'Total de Vítimas': 'sum'
}).rename(columns={'Evento': 'Total_Acidentes'})

# Índice composto: acidentes + 5*graves + 20*fatais
rodovia_stats['Indice_Periculosidade'] = (
    rodovia_stats['Total_Acidentes'] * 1 +
    rodovia_stats['Grave'] * 5 +
    rodovia_stats['Fatal'] * 20
)

top_perigosas = rodovia_stats.nlargest(20, 'Indice_Periculosidade')
# Função para formatar rodovia no padrão DER (SP-XXX)
def formatar_rodovia(r):
    try:
        return f"SP-{int(r):03d}"
    except:
        return f"SP-{r}"
# Adicionar prefixo SP- aos nomes das rodovias
top_perigosas_labels = [formatar_rodovia(r) for r in top_perigosas.index]

fig20 = go.Figure()
fig20.add_trace(go.Bar(
    x=top_perigosas['Indice_Periculosidade'],
    y=top_perigosas_labels,
    orientation='h',
    marker=dict(
        color=top_perigosas['Total de Vítimas'],
        colorscale='Reds',
        showscale=True,
        colorbar=dict(title="Total de<br>Vítimas")
    ),
    text=[f"{int(v)}" for v in top_perigosas['Indice_Periculosidade']],
    textposition='outside'
))
fig20.update_layout(
    title='<b>Top 20 Rodovias Mais Perigosas (Índice Composto)</b>',
    xaxis_title='Índice de Periculosidade',
    yaxis_title='Rodovia',
    template='plotly_white',
    font=dict(size=10),
    height=700
)
salvar_grafico_acessivel(fig20, '20_top_rodovias_perigosas.html', 'Rodovias Mais Perigosas')
print("✓ Gráfico 20 salvo")

# ===== GRÁFICO 21: TAXA DE MORTALIDADE POR RODOVIA =====
rodovia_taxa = df.groupby('Rodovia').agg({
    'Fatal': 'sum',
    'Evento': 'count'
}).rename(columns={'Evento': 'Total'})

# Filtrar rodovias com pelo menos 100 acidentes
rodovia_taxa = rodovia_taxa[rodovia_taxa['Total'] >= 100]
rodovia_taxa['Taxa_Mortalidade'] = (rodovia_taxa['Fatal'] / rodovia_taxa['Total'] * 100)
top_taxa = rodovia_taxa.nlargest(20, 'Taxa_Mortalidade')
# Adicionar prefixo SP- aos nomes das rodovias (formato padrão DER)
top_taxa_labels = [formatar_rodovia(r) for r in top_taxa.index]

fig21 = go.Figure()
fig21.add_trace(go.Bar(
    x=top_taxa['Taxa_Mortalidade'],
    y=top_taxa_labels,
    orientation='h',
    marker=dict(
        color=top_taxa['Total'],
        colorscale='Oranges',
        showscale=True,
        colorbar=dict(title="Total de<br>Acidentes")
    ),
    text=[f"{v:.2f}%" for v in top_taxa['Taxa_Mortalidade']],
    textposition='outside'
))
fig21.update_layout(
    title='<b>Taxa de Mortalidade por Rodovia (com ≥100 acidentes)</b>',
    xaxis_title='Taxa de Mortalidade (%)',
    yaxis_title='Rodovia',
    template='plotly_white',
    font=dict(size=10),
    height=700
)
salvar_grafico_acessivel(fig21, '21_taxa_mortalidade_rodovia.html', 'Taxa de Mortalidade por Rodovia')
print("✓ Gráfico 21 salvo")

# ===== GRÁFICO 22: ANÁLISE SAZONAL =====
df['Mes'] = df['Data Abertura'].dt.month
meses_pt = {1:'Janeiro', 2:'Fevereiro', 3:'Março', 4:'Abril', 5:'Maio', 6:'Junho',
            7:'Julho', 8:'Agosto', 9:'Setembro', 10:'Outubro', 11:'Novembro', 12:'Dezembro'}
df['Mes_Nome'] = df['Mes'].map(meses_pt)

sazonal_2023 = df[df['Ano']==2023].groupby('Mes_Nome').agg({
    'Evento': 'count',
    'Total de Vítimas': 'sum',
    'Fatal': 'sum'
})
sazonal_2024 = df[df['Ano']==2024].groupby('Mes_Nome').agg({
    'Evento': 'count',
    'Total de Vítimas': 'sum',
    'Fatal': 'sum'
})
sazonal_2025 = df[df['Ano']==2025].groupby('Mes_Nome').agg({
    'Evento': 'count',
    'Total de Vítimas': 'sum',
    'Fatal': 'sum'
})

fig22 = make_subplots(specs=[[{"secondary_y": True}]])

fig22.add_trace(
    go.Bar(x=sazonal_2023.index, y=sazonal_2023['Evento'], name='Acidentes 2023',
           marker_color=CORES_SIGMA[0], opacity=0.7),
    secondary_y=False
)
fig22.add_trace(
    go.Bar(x=sazonal_2024.index, y=sazonal_2024['Evento'], name='Acidentes 2024',
           marker_color=CORES_SIGMA[1], opacity=0.7),
    secondary_y=False
)
fig22.add_trace(
    go.Bar(x=sazonal_2025.index, y=sazonal_2025['Evento'], name='Acidentes 2025',
           marker_color=CORES_SIGMA[2], opacity=0.7),
    secondary_y=False
)
fig22.add_trace(
    go.Scatter(x=sazonal_2023.index, y=sazonal_2023['Fatal'], name='Óbitos 2023',
               mode='lines+markers', line=dict(color='#1E3A5F', width=3, dash='solid')),
    secondary_y=True
)
fig22.add_trace(
    go.Scatter(x=sazonal_2024.index, y=sazonal_2024['Fatal'], name='Óbitos 2024',
               mode='lines+markers', line=dict(color='#2E7D32', width=3, dash='dash')),
    secondary_y=True
)
fig22.add_trace(
    go.Scatter(x=sazonal_2025.index, y=sazonal_2025['Fatal'], name='Óbitos 2025',
               mode='lines+markers', line=dict(color='#F9A825', width=3, dash='dot')),
    secondary_y=True
)

fig22.update_layout(
    title='<b>Análise Sazonal: Acidentes vs Óbitos (2023-2024-2025)</b>',
    hovermode='x unified',
    template='plotly_white',
    font=dict(size=11),
    height=700,
    barmode='group',
    xaxis=dict(type='category', tickangle=-45),
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
fig22.update_yaxes(title_text='Quantidade de Acidentes', secondary_y=False)
fig22.update_yaxes(title_text='Quantidade de Óbitos', secondary_y=True)
salvar_grafico_acessivel(fig22, '22_analise_sazonal.html', 'Análise Sazonal')
print("✓ Gráfico 22 salvo")

# ===== GRÁFICO 23: COMPARAÇÃO DE MÉDIA DE VÍTIMAS POR ACIDENTE =====
media_vitimas_2023 = df[df['Ano']==2023].groupby('Tipo Acidente')['Total de Vítimas'].mean().nlargest(15)
media_vitimas_2024 = df[df['Ano']==2024].groupby('Tipo Acidente')['Total de Vítimas'].mean().nlargest(15)
media_vitimas_2025 = df[df['Ano']==2025].groupby('Tipo Acidente')['Total de Vítimas'].mean().nlargest(15)

fig23 = make_subplots(
    rows=1, cols=3,
    subplot_titles=('2023', '2024', '2025'),
    specs=[[{'type':'bar'}, {'type':'bar'}, {'type':'bar'}]]
)

fig23.add_trace(
    go.Bar(x=media_vitimas_2023.values, y=media_vitimas_2023.index, orientation='h',
           marker_color=CORES_SIGMA[0], name='2023'),
    row=1, col=1
)
fig23.add_trace(
    go.Bar(x=media_vitimas_2024.values, y=media_vitimas_2024.index, orientation='h',
           marker_color=CORES_SIGMA[1], name='2024'),
    row=1, col=2
)
fig23.add_trace(
    go.Bar(x=media_vitimas_2025.values, y=media_vitimas_2025.index, orientation='h',
           marker_color=CORES_SIGMA[2], name='2025'),
    row=1, col=3
)
fig23.update_xaxes(title_text='Média de Vítimas', row=1, col=1)
fig23.update_xaxes(title_text='Média de Vítimas', row=1, col=2)
fig23.update_xaxes(title_text='Média de Vítimas', row=1, col=3)
fig23.update_layout(
    title_text='<b>Média de Vítimas por Tipo de Acidente (Top 15) - 2023-2024-2025</b>',
    height=600,
    showlegend=False,
    template='plotly_white',
    font=dict(size=10)
)
salvar_grafico_acessivel(fig23, '23_media_vitimas_tipo_acidente.html', 'Média de Vítimas por Tipo de Acidente')
print("✓ Gráfico 23 salvo")

print("\n✓ 5 gráficos de padrões e correlações gerados com sucesso!")
