# Análise de Acidentes DER - São Paulo (2023-2024-2025)

📊 **Dashboard Interativo de Análise Exploratória de Acidentes nas Rodovias Estaduais de São Paulo**

## 🌐 Acesse o Site

**[👉 Acessar Dashboard Online](https://acidentes-der-analise.onrender.com)**

## 📈 Estatísticas Gerais

| Métrica | Valor |
|---------|-------|
| **Total de Acidentes** | 39.578 |
| **Total de Vítimas** | 34.324 |
| **Óbitos** | 2.065 |
| **Anos Analisados** | 2023, 2024, 2025 |
| **Gráficos Interativos** | 29 |

## 📊 Dados por Ano

| Ano | Acidentes | Vítimas | Óbitos |
|-----|-----------|---------|--------|
| 2023 | 14.389 | 13.076 | 744 |
| 2024 | 13.882 | 13.426 | 769 |
| 2025 | 11.307 | 7.822 | 552 |

## 🗂️ Estrutura do Projeto

```
📁 acidentes-der-analise-exploratoria/
├── 📄 portal.html          # Página inicial do portal
├── 📄 index.html           # Dashboard principal com abas
├── 📄 dashboard.html       # Dashboard compacto
├── 📄 RELATORIO_EXECUTIVO.html  # Relatório executivo
├── 📄 GUIA_ACESSO.html     # Guia de navegação
├── 📊 01-29_*.html         # 29 gráficos interativos
├── 🐍 gerar_graficos_*.py  # Scripts Python
├── 📁 dados_completos.csv  # Base de dados consolidada
└── 📁 *.xlsx               # Arquivos Excel originais
```

## 🎨 Visualizações Incluídas

### 📈 Visão Geral (5 gráficos)
- Total de acidentes por ano
- Total de vítimas por ano
- Tipos de acidentes
- Acidentes por sentido da via
- Resumo estatístico comparativo

### 👥 Análise de Vítimas (6 gráficos)
- Vítimas por gravidade
- Comparação de vítimas entre anos
- Média de vítimas por tipo de acidente
- Análise de percentis
- Índice de severidade
- Distribuição por regional

### ⏱️ Séries Temporais (5 gráficos)
- Série temporal de acidentes
- Série temporal de vítimas
- Acidentes por dia da semana
- Análise sazonal
- Taxa de variação mensal

### 🗺️ Análise Geográfica (6 gráficos)
- Top rodovias com mais acidentes
- Acidentes por regional
- Heatmaps (rodovia x mês, regional)
- Distribuição por quilometragem
- Densidade por faixa de KM

### 🔍 Padrões e Correlações (5 gráficos)
- Matriz de correlação
- Scatter KM vs Vítimas
- Tipos de acidentes por gravidade
- Matriz rodovia x tipo de acidente
- Tipos de ocorrências

### ⚠️ Análise de Risco (2 gráficos)
- Top 20 rodovias mais perigosas
- Taxa de mortalidade por rodovia

## 🛠️ Tecnologias Utilizadas

- **Python** - Processamento de dados
- **Pandas** - Manipulação de dados
- **Plotly** - Gráficos interativos
- **HTML/CSS** - Interface web responsiva

## 📝 Como Executar Localmente

```bash
# Clone o repositório
git clone https://github.com/vpcapanema/acidentes-der-analise-exploratoria.git

# Entre na pasta
cd acidentes-der-analise-exploratoria

# Abra o portal no navegador
start portal.html  # Windows
open portal.html   # macOS
xdg-open portal.html  # Linux
```

## 📄 Licença

Este projeto é de uso público para fins educacionais e de análise.

---

**Desenvolvido com 💚 usando dados do DER-SP**
