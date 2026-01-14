import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Carregar dados dos três anos
print("Carregando dados...")
df_2023 = pd.read_excel('Acidentes_DER_2023.xlsx')
df_2024 = pd.read_excel('Acidentes_DER_2024.xlsx')
df_2025 = pd.read_excel('Acidentes_DER_2025.xlsx')

# Adicionar coluna de ano
df_2023['Ano'] = 2023
df_2024['Ano'] = 2024
df_2025['Ano'] = 2025

# Concatenar todos os dados
df_total = pd.concat([df_2023, df_2024, df_2025], ignore_index=True)

# Obter informações gerais
print("\n=== ANÁLISE EXPLORATÓRIA ===\n")
print(f"Acidentes 2023: {len(df_2023)}")
print(f"Acidentes 2024: {len(df_2024)}")
print(f"Acidentes 2025: {len(df_2025)}")
print(f"Total: {len(df_total)}")

print("\n=== COLUNAS DISPONÍVEIS ===")
print(df_total.columns.tolist())

print("\n=== PRIMEIRAS LINHAS ===")
print(df_total.head(10))

print("\n=== TIPOS DE DADOS ===")
print(df_total.dtypes)

print("\n=== ESTATÍSTICAS ===")
print(df_total.describe())

print("\n=== VALORES FALTANTES ===")
print(df_total.isnull().sum())

# Salvar informações para uso posterior
df_total.to_csv('dados_completos.csv', index=False)
print("\nDados salvos em dados_completos.csv")
