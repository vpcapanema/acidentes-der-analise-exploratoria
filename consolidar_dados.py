"""
Script para consolidar dados de acidentes de 2023, 2024 e 2025
"""
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("CONSOLIDAÇÃO DE DADOS - ACIDENTES DER 2023-2024-2025")
print("=" * 60)

# Carregar dados de cada ano da planilha correta
print("\nCarregando dados...")
df2023 = pd.read_excel('Acidentes_DER_2023.xlsx', sheet_name='Base de Dados')
df2024 = pd.read_excel('Acidentes_DER_2024.xlsx', sheet_name='Base de Dados')
df2025 = pd.read_excel('Acidentes_DER_2025.xlsx', sheet_name='Base de dados ')

print(f"2023: {len(df2023):,} registros")
print(f"2024: {len(df2024):,} registros")
print(f"2025: {len(df2025):,} registros")

# Padronizar colunas
# 2024 tem ' Ocorrência' com espaço e 'Data' em vez de 'Nova data'
df2024 = df2024.rename(columns={
    ' Ocorrência': 'Ocorrencia',
    'Data': 'Nova data'
})

# 2025 tem colunas extras UBA
# Manter todas as colunas importantes

# Adicionar coluna Ano
df2023['Ano'] = 2023
df2024['Ano'] = 2024
df2025['Ano'] = 2025

# Selecionar colunas comuns
colunas_base = ['Evento', 'Rodovia', 'Km', 'Sentido', 'Ocorrencia', 'Tipo Acidente', 
                'Leve', 'Grave', 'Fatal', 'Data Abertura', 'Regional', 'Nova data', 
                'Total de Vítimas', 'Ano']

# Garantir que todas as colunas existam
for col in colunas_base:
    if col not in df2023.columns:
        df2023[col] = None
    if col not in df2024.columns:
        df2024[col] = None
    if col not in df2025.columns:
        df2025[col] = None

# Adicionar colunas UBA para 2025 (se existirem)
if 'UBA' in df2025.columns:
    colunas_extra = ['UBA', 'UBA sigla']
    for col in colunas_extra:
        if col not in df2023.columns:
            df2023[col] = None
        if col not in df2024.columns:
            df2024[col] = None

# Consolidar dados
df_total = pd.concat([df2023, df2024, df2025], ignore_index=True)

# Converter datas
df_total['Data Abertura'] = pd.to_datetime(df_total['Data Abertura'], errors='coerce')
df_total['Nova data'] = pd.to_datetime(df_total['Nova data'], errors='coerce')

# Salvar arquivo consolidado
df_total.to_csv('dados_completos.csv', index=False)

print("\n" + "=" * 60)
print("RESUMO DA CONSOLIDAÇÃO")
print("=" * 60)
print(f"\nTotal de registros consolidados: {len(df_total):,}")
print(f"\nDistribuição por ano:")
print(df_total['Ano'].value_counts().sort_index())
print(f"\nArquivo salvo: dados_completos.csv")
print("=" * 60)
