from __future__ import annotations

from pathlib import Path
import re


TARGET_FILES = [
    "01_total_acidentes_por_ano.html",
    "02_vitimas_por_gravidade.html",
    "03_total_vitimas_por_ano.html",
    "04_tipos_acidentes.html",
    "05_rodovias_mais_acidentes.html",
    "06_acidentes_por_regional.html",
    "07_tipos_ocorrencias.html",
    "08_serie_temporal_acidentes.html",
    "09_serie_temporal_vitimas.html",
    "10_severidade_acidentes.html",
    "11_acidentes_por_sentido.html",
    "12_distribuicao_km.html",
    "13_heatmap_rodovia_mes.html",
    "14_comparacao_vitimas.html",
    "15_densidade_km.html",
    "16_acidentes_dia_semana.html",
    "17_scatter_km_vitimas.html",
    "18_tipos_acidentes_gravidade.html",
    "19_matriz_correlacao.html",
    "20_top_rodovias_perigosas.html",
    "21_taxa_mortalidade_rodovia.html",
    "22_analise_sazonal.html",
    "23_media_vitimas_tipo_acidente.html",
    "24_heatmap_regional.html",
    "25_boxplot_vitimas_regional.html",
    "26_tendencia_variacao_mensal.html",
    "27_analise_percentis.html",
    "28_matriz_rodovia_tipo.html",
    "29_resumo_estatistico.html",
]


BODY_CLASS_PATTERN = re.compile(
    r'<body([^>]*?)\sclass="([^"]*?)has-sigma-navbar([^"]*?)"([^>]*)>',
    re.IGNORECASE,
)
HEADER_PATTERN = re.compile(
    r'\s*<header\b[^>]*class="[^"]*sigma-navbar[^"]*"[^>]*>.*?</header>\s*',
    re.IGNORECASE | re.DOTALL,
)
FOOTER_PATTERN = re.compile(
    r'\s*<footer\b[^>]*class="[^"]*fad-footer[^"]*"[^>]*>.*?</footer>\s*',
    re.IGNORECASE | re.DOTALL,
)


def clean_body_tag(content: str) -> str:
    def replacer(match: re.Match[str]) -> str:
        before = match.group(1)
        left = match.group(2)
        right = match.group(3)
        after = match.group(4)
        classes = f"{left} {right}".split()
        if classes:
            return f'<body{before} class="{" ".join(classes)}"{after}>'
        return f'<body{before}{after}>'

    return BODY_CLASS_PATTERN.sub(replacer, content)


def clean_html(content: str) -> str:
    content = clean_body_tag(content)
    content = HEADER_PATTERN.sub("\n", content)
    content = FOOTER_PATTERN.sub("\n", content)
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content


def process_file(path: Path) -> str:
    original = path.read_text(encoding="utf-8")
    cleaned = clean_html(original)
    if cleaned == original:
        return "sem alteracoes"
    path.write_text(cleaned, encoding="utf-8")
    return "alterado"


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    changed = 0
    unchanged = 0
    missing = 0

    for relative_name in TARGET_FILES:
        file_path = repo_root / relative_name
        if not file_path.exists():
            print(f"[ausente] {relative_name}")
            missing += 1
            continue

        status = process_file(file_path)
        print(f"[{status}] {relative_name}")
        if status == "alterado":
            changed += 1
        else:
            unchanged += 1

    print()
    print(f"Arquivos alterados: {changed}")
    print(f"Arquivos sem alteracoes: {unchanged}")
    print(f"Arquivos ausentes: {missing}")


if __name__ == "__main__":
    main()
