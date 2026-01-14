#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Documentação de Gráficos
Gerado automaticamente - 13 de Janeiro de 2026
"""

graficos = {
    "VISÃO GERAL": {
        "01_total_acidentes_por_ano.html": {
            "titulo": "Total de Acidentes por Ano",
            "descricao": "Comparação visual do total de acidentes entre 2023 e 2025",
            "tipo": "Bar Chart",
            "variaveis": ["Ano", "Quantidade"]
        },
        "02_vitimas_por_gravidade.html": {
            "titulo": "Vítimas por Tipo de Gravidade",
            "descricao": "Comparação de vítimas leves, graves e fatais entre os anos",
            "tipo": "Grouped Bar Chart",
            "variaveis": ["Gravidade", "2023", "2025"]
        },
        "03_total_vitimas_por_ano.html": {
            "titulo": "Total de Vítimas por Ano",
            "descricao": "Número total de vítimas registradas em cada ano",
            "tipo": "Bar Chart",
            "variaveis": ["Ano", "Total"]
        },
        "04_tipos_acidentes.html": {
            "titulo": "Top 10 Tipos de Acidentes",
            "descricao": "Ranking dos principais tipos de acidentes registrados",
            "tipo": "Horizontal Bar Chart",
            "variaveis": ["Tipo", "Quantidade"]
        },
        "29_resumo_estatistico.html": {
            "titulo": "Resumo Estatístico Comparativo",
            "descricao": "Estatísticas-chave comparadas entre 2023 e 2025",
            "tipo": "Grouped Bar Chart",
            "variaveis": ["Métrica", "2023", "2025"]
        }
    },
    
    "ANÁLISE DE VÍTIMAS": {
        "10_severidade_acidentes.html": {
            "titulo": "Distribuição do Índice de Severidade",
            "descricao": "Box plot da distribuição de severidade dos acidentes",
            "tipo": "Box Plot",
            "variaveis": ["Índice", "Ano"]
        },
        "14_comparacao_vitimas.html": {
            "titulo": "Comparação de Vítimas 2023 vs 2025",
            "descricao": "Comparação lado a lado das categorias de vítimas",
            "tipo": "Grouped Bar Chart",
            "variaveis": ["Leve", "Grave", "Fatal", "Total"]
        },
        "23_media_vitimas_tipo_acidente.html": {
            "titulo": "Média de Vítimas por Tipo de Acidente",
            "descricao": "Top 15 tipos de acidentes com maior número médio de vítimas",
            "tipo": "Horizontal Bar Chart",
            "variaveis": ["Tipo", "Média"]
        },
        "25_boxplot_vitimas_regional.html": {
            "titulo": "Distribuição de Vítimas por Regional",
            "descricao": "Box plots comparando distribuição de vítimas por região",
            "tipo": "Box Plot",
            "variaveis": ["Regional", "Vítimas"]
        },
        "27_analise_percentis.html": {
            "titulo": "Análise de Percentis",
            "descricao": "Percentis (10, 25, 50, 75, 90, 95, 99) de vítimas",
            "tipo": "Line Chart",
            "variaveis": ["Percentil", "Vítimas"]
        }
    },
    
    "SÉRIES TEMPORAIS": {
        "08_serie_temporal_acidentes.html": {
            "titulo": "Série Temporal: Acidentes por Mês",
            "descricao": "Evolução mensal de acidentes ao longo de 2023 e 2025",
            "tipo": "Line Chart",
            "variaveis": ["Data", "Acidentes", "Ano"]
        },
        "09_serie_temporal_vitimas.html": {
            "titulo": "Série Temporal: Total de Vítimas por Mês",
            "descricao": "Evolução mensal do total de vítimas",
            "tipo": "Line Chart",
            "variaveis": ["Data", "Vítimas", "Ano"]
        },
        "16_acidentes_dia_semana.html": {
            "titulo": "Acidentes por Dia da Semana",
            "descricao": "Comparação de frequência de acidentes por dia da semana",
            "tipo": "Grouped Bar Chart",
            "variaveis": ["Dia", "2023", "2025"]
        },
        "22_analise_sazonal.html": {
            "titulo": "Análise Sazonal: Acidentes vs Óbitos",
            "descricao": "Comparação mensal de acidentes e óbitos com duplo eixo Y",
            "tipo": "Bar + Line Chart",
            "variaveis": ["Mês", "Acidentes", "Óbitos"]
        },
        "26_tendencia_variacao_mensal.html": {
            "titulo": "Taxa de Variação Mensal",
            "descricao": "Percentual de variação de acidentes 2025 vs 2023",
            "tipo": "Bar Chart",
            "variaveis": ["Período", "Variação %"]
        }
    },
    
    "ANÁLISE GEOGRÁFICA": {
        "05_rodovias_mais_acidentes.html": {
            "titulo": "Top 15 Rodovias com Mais Acidentes",
            "descricao": "Ranking das rodovias com maior volume de acidentes",
            "tipo": "Horizontal Bar Chart",
            "variaveis": ["Rodovia", "Acidentes"]
        },
        "06_acidentes_por_regional.html": {
            "titulo": "Acidentes por Regional",
            "descricao": "Distribuição de acidentes entre regionais da DER",
            "tipo": "Grouped Bar Chart",
            "variaveis": ["Regional", "2023", "2025"]
        },
        "12_distribuicao_km.html": {
            "titulo": "Distribuição de Acidentes por Quilometragem",
            "descricao": "Histograma da distribuição de acidentes ao longo dos km",
            "tipo": "Histogram",
            "variaveis": ["KM", "Frequência"]
        },
        "13_heatmap_rodovia_mes.html": {
            "titulo": "Heatmap: Acidentes por Rodovia e Mês",
            "descricao": "Mapa de calor mostrando padrões sazonais por rodovia",
            "tipo": "Heatmap",
            "variaveis": ["Rodovia", "Mês", "Acidentes"]
        },
        "15_densidade_km.html": {
            "titulo": "Densidade por Faixa de Quilometragem",
            "descricao": "Comparação de acidentes em faixas de km de 50 em 50",
            "tipo": "Grouped Bar Chart",
            "variaveis": ["Faixa KM", "2023", "2025"]
        },
        "24_heatmap_regional.html": {
            "titulo": "Heatmap Regional",
            "descricao": "Mapa de calor de acidentes e vítimas por regional",
            "tipo": "Heatmap",
            "variaveis": ["Regional", "Métrica", "Valor"]
        }
    },
    
    "PADRÕES E CORRELAÇÕES": {
        "17_scatter_km_vitimas.html": {
            "titulo": "Scatter Plot: KM vs Vítimas",
            "descricao": "Relação entre quilometragem e número de vítimas",
            "tipo": "Scatter Plot",
            "variaveis": ["KM", "Vítimas", "Rodovia"]
        },
        "18_tipos_acidentes_gravidade.html": {
            "titulo": "Tipos de Acidentes por Categoria de Gravidade",
            "descricao": "Distribuição de gravidade dentro de cada tipo de acidente",
            "tipo": "Stacked Bar Chart",
            "variaveis": ["Tipo", "Gravidade", "Quantidade"]
        },
        "19_matriz_correlacao.html": {
            "titulo": "Matriz de Correlação",
            "descricao": "Correlações estatísticas entre variáveis numéricas",
            "tipo": "Heatmap",
            "variaveis": ["Variável1", "Variável2", "Correlação"]
        },
        "07_tipos_ocorrencias.html": {
            "titulo": "Tipos de Ocorrências (Top 12)",
            "descricao": "Tipos de ocorrências registradas nos acidentes",
            "tipo": "Grouped Bar Chart",
            "variaveis": ["Ocorrência", "2023", "2025"]
        },
        "28_matriz_rodovia_tipo.html": {
            "titulo": "Matriz: Rodovia x Tipo de Acidente",
            "descricao": "Frequência de tipos de acidentes em principais rodovias",
            "tipo": "Heatmap",
            "variaveis": ["Rodovia", "Tipo", "Frequência"]
        }
    },
    
    "ANÁLISE DE RISCO": {
        "20_top_rodovias_perigosas.html": {
            "titulo": "Top 20 Rodovias Mais Perigosas",
            "descricao": "Ranking por índice composto de periculosidade",
            "tipo": "Horizontal Bar Chart",
            "variaveis": ["Rodovia", "Índice", "Vítimas"]
        },
        "21_taxa_mortalidade_rodovia.html": {
            "titulo": "Taxa de Mortalidade por Rodovia",
            "descricao": "Percentage de óbitos em relação ao total de acidentes",
            "tipo": "Horizontal Bar Chart",
            "variaveis": ["Rodovia", "Taxa %", "Total"]
        },
        "11_acidentes_por_sentido.html": {
            "titulo": "Acidentes por Sentido da Via",
            "descricao": "Comparação entre crescente e decrescente",
            "tipo": "Pie Chart",
            "variaveis": ["Sentido", "Percentual"]
        }
    }
}

# Calcular totais
total_graficos = sum(len(v) for v in graficos.values())
categorias = list(graficos.keys())

print(f"\n{'='*80}")
print(f"ÍNDICE COMPLETO DE GRÁFICOS - ANÁLISE ACIDENTES DER")
print(f"{'='*80}\n")

print(f"TOTAL: {total_graficos} Gráficos em {len(categorias)} Categorias\n")

for categoria, items in graficos.items():
    print(f"\n{'─'*80}")
    print(f"📊 {categoria} ({len(items)} gráficos)")
    print(f"{'─'*80}")
    
    for idx, (arquivo, info) in enumerate(items.items(), 1):
        print(f"\n  {idx}. {info['titulo']}")
        print(f"     Arquivo: {arquivo}")
        print(f"     Tipo: {info['tipo']}")
        print(f"     Descrição: {info['descricao']}")
        print(f"     Variáveis: {', '.join(info['variaveis'])}")

print(f"\n{'='*80}")
print(f"Documentação gerada em 13 de Janeiro de 2026")
print(f"{'='*80}\n")

# Salvar como arquivo de referência
with open('INDICE_GRAFICOS.txt', 'w', encoding='utf-8') as f:
    f.write(f"ÍNDICE COMPLETO DE GRÁFICOS - ANÁLISE ACIDENTES DER\n")
    f.write(f"{'='*80}\n\n")
    f.write(f"TOTAL: {total_graficos} Gráficos em {len(categorias)} Categorias\n\n")
    
    for categoria, items in graficos.items():
        f.write(f"\n{'─'*80}\n")
        f.write(f"📊 {categoria} ({len(items)} gráficos)\n")
        f.write(f"{'─'*80}\n")
        
        for idx, (arquivo, info) in enumerate(items.items(), 1):
            f.write(f"\n  {idx}. {info['titulo']}\n")
            f.write(f"     Arquivo: {arquivo}\n")
            f.write(f"     Tipo: {info['tipo']}\n")
            f.write(f"     Descrição: {info['descricao']}\n")
            f.write(f"     Variáveis: {', '.join(info['variaveis'])}\n")

print("✓ Índice de gráficos salvo em: INDICE_GRAFICOS.txt")
