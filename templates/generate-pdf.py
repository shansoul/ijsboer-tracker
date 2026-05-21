#!/usr/bin/env python3
"""
PDF generator voor klantoverdracht-documenten.

Gebruik:
    python3 generate-pdf.py input.md output.pdf
    python3 generate-pdf.py input.md output.pdf --bedrijf "Shan Brunel Consulting" --projectnaam "IJsboer Tracker"

Vereisten:
    pip install weasyprint markdown
"""

import re
import argparse
import markdown
from weasyprint import HTML


def post_process(html: str) -> str:
    # Wrap alles vóór de eerste <hr> in een cover-sectie
    parts = html.split('<hr />', 1)
    if len(parts) == 2:
        html = f'<div class="cover-section">{parts[0]}</div><hr />{parts[1]}'

    # Vervang aaneengesloten underscores door een gestileerde handtekeninglijn
    html = re.sub(r'_{4,}', '<span class="sig-line"></span>', html)

    return html


def generate_pdf(input_md: str, output_pdf: str, bedrijfsnaam: str = "", projectnaam: str = ""):
    with open(input_md, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_body = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code", "nl2br"]
    )

    html_body = post_process(html_body)

    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<style>
  /* ── Pagina-layout ── */
  @page {{
    size: A4;
    margin: 2.8cm 2.5cm 3cm 2.5cm;

    @top-center {{
      content: "{projectnaam}";
      font-family: Arial, Helvetica, sans-serif;
      font-size: 7.5pt;
      color: #aab4be;
      padding-top: 0.8cm;
      text-align: center;
    }}
    @bottom-left {{
      content: "{bedrijfsnaam}";
      font-family: Arial, Helvetica, sans-serif;
      font-size: 7.5pt;
      color: #aab4be;
    }}
    @bottom-right {{
      content: "Pagina " counter(page) " van " counter(pages);
      font-family: Arial, Helvetica, sans-serif;
      font-size: 7.5pt;
      color: #aab4be;
    }}
  }}

  @page :first {{
    margin-top: 0;
    @top-left {{ content: ""; }}
  }}

  /* ── Basis ── */
  body {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10.5pt;
    line-height: 1.65;
    color: #1c1c1e;
    margin: 0;
  }}

  /* ── Coverpagina ── */
  .cover-section {{
    background: #0d2e4f;
    color: #ffffff;
    margin: -2.8cm -2.5cm 2.8cm -2.5cm;
    padding: 3.5cm 2.5cm 2.5cm 2.5cm;
    page-break-after: avoid;
  }}

  .cover-section h1 {{
    font-size: 26pt;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 6px 0;
    line-height: 1.15;
  }}

  .cover-section h2 {{
    font-size: 13pt;
    font-weight: 400;
    color: #7fb3d6;
    border: none;
    margin: 0 0 2.2cm 0;
    padding: 0;
  }}

  .cover-section p {{
    background: rgba(255,255,255,0.08);
    border-left: 3px solid #3a8fd1;
    padding: 14px 18px;
    margin: 0;
    font-size: 10pt;
    line-height: 2;
    border-radius: 0 4px 4px 0;
  }}

  .cover-section p strong {{
    color: #7fb3d6;
    font-weight: 600;
    display: inline-block;
    min-width: 100px;
  }}

  /* ── Sectietitels met automatische nummering ── */
  body {{
    counter-reset: sectie;
  }}

  h2 {{
    counter-increment: sectie;
    font-size: 13pt;
    font-weight: 700;
    color: #0d2e4f;
    border-bottom: 1.5px solid #c8dff0;
    padding-bottom: 5px;
    margin-top: 40px;
    margin-bottom: 14px;
    page-break-after: avoid;
  }}

  h2::before {{
    content: counter(sectie) ". ";
    color: #3a8fd1;
    font-weight: 700;
  }}

  /* Bijlages geen counter-nummering */
  h2[data-bijlage]::before {{
    content: "";
  }}

  h3 {{
    font-size: 10.5pt;
    font-weight: 700;
    color: #1a4f7a;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-top: 24px;
    margin-bottom: 8px;
    page-break-after: avoid;
  }}

  hr {{
    border: none;
    border-top: 1px solid #dde8f2;
    margin: 28px 0;
  }}

  p {{
    margin: 0 0 10px 0;
  }}

  /* ── Tabellen ── */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0 22px 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }}

  th {{
    background: #1a4f7a;
    color: #ffffff;
    padding: 8px 12px;
    text-align: left;
    font-weight: 700;
    font-size: 8.5pt;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }}

  td {{
    padding: 8px 12px;
    border-bottom: 1px solid #e4eef6;
    vertical-align: top;
  }}

  tr:nth-child(even) td {{
    background: #f4f8fc;
  }}

  /* ── Code ── */
  code {{
    background: #eef3f8;
    padding: 2px 5px;
    border-radius: 3px;
    font-family: "Courier New", Courier, monospace;
    font-size: 9pt;
    color: #1a4f7a;
  }}

  pre {{
    background: #f0f5fa;
    border-left: 4px solid #1a4f7a;
    padding: 12px 16px;
    font-family: "Courier New", Courier, monospace;
    font-size: 9pt;
    white-space: pre-wrap;
    margin: 14px 0;
    page-break-inside: avoid;
    border-radius: 0 4px 4px 0;
  }}

  pre code {{
    background: none;
    padding: 0;
    color: inherit;
  }}

  /* ── Notities / waarschuwingen ── */
  blockquote {{
    border-left: 3px solid #e8a020;
    margin: 16px 0;
    padding: 10px 16px;
    color: #4a3a10;
    background: #fef8ec;
    border-radius: 0 4px 4px 0;
    font-size: 9.5pt;
  }}

  blockquote p {{
    margin: 0;
  }}

  /* ── Lijsten ── */
  ul, ol {{
    padding-left: 22px;
    margin: 6px 0 14px 0;
  }}

  li {{
    margin: 5px 0;
    line-height: 1.6;
  }}

  /* ── Handtekeninglijnen ── */
  .sig-line {{
    display: inline-block;
    width: 220px;
    border-bottom: 1px solid #1c1c1e;
    margin: 0 6px;
    vertical-align: middle;
  }}

  /* ── Paginabreuk ── */
  table, pre, blockquote {{
    page-break-inside: avoid;
  }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

    HTML(string=html).write_pdf(output_pdf)
    print(f"PDF aangemaakt: {output_pdf}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genereer PDF van een markdown overdrachtstemplate")
    parser.add_argument("input", help="Pad naar het markdown-bestand")
    parser.add_argument("output", help="Pad voor de uitvoer-PDF")
    parser.add_argument("--bedrijf", default="", help="Jouw bedrijfsnaam voor in de header")
    parser.add_argument("--projectnaam", default="", help="Projectnaam voor in de footer")
    args = parser.parse_args()

    generate_pdf(args.input, args.output, args.bedrijf, args.projectnaam)
