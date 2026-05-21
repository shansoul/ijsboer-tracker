#!/usr/bin/env python3
"""
PDF generator voor klantoverdracht-documenten.

Gebruik:
    python3 generate-pdf.py input.md output.pdf
    python3 generate-pdf.py input.md output.pdf --bedrijf "Jouw Bedrijfsnaam"

Vereisten:
    pip install weasyprint markdown
"""

import sys
import argparse
import markdown
from weasyprint import HTML
from datetime import date

def generate_pdf(input_md: str, output_pdf: str, bedrijfsnaam: str = ""):
    with open(input_md, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_body = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code", "nl2br"]
    )

    footer_bedrijf = f"{bedrijfsnaam} · " if bedrijfsnaam else ""

    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<style>
  /* ── Pagina-instellingen ── */
  @page {{
    size: A4;
    margin: 2.8cm 2.5cm 3cm 2.5cm;
    @top-left {{
      content: "{bedrijfsnaam}";
      font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
      font-size: 8pt;
      color: #aaa;
      margin-top: 1cm;
    }}
    @bottom-left {{
      content: "{footer_bedrijf}" attr(data-title);
      font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
      font-size: 8pt;
      color: #aaa;
    }}
    @bottom-right {{
      content: "Pagina " counter(page) " van " counter(pages);
      font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
      font-size: 8pt;
      color: #aaa;
    }}
  }}

  @page :first {{
    margin-top: 4cm;
    @top-left {{ content: ""; }}
  }}

  /* ── Basisstijl ── */
  body {{
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.65;
    color: #1c1c1e;
  }}

  /* ── Titels ── */
  h1 {{
    font-size: 22pt;
    font-weight: 700;
    color: #0d2e4f;
    margin: 0 0 4px 0;
    line-height: 1.2;
  }}

  h1 + h2 {{
    font-size: 13pt;
    font-weight: 400;
    color: #3a6e9e;
    border: none;
    margin: 0 0 32px 0;
    padding: 0;
  }}

  h2 {{
    font-size: 13pt;
    font-weight: 700;
    color: #0d2e4f;
    border-bottom: 1.5px solid #c8dff0;
    padding-bottom: 5px;
    margin-top: 36px;
    margin-bottom: 12px;
  }}

  h3 {{
    font-size: 11pt;
    font-weight: 600;
    color: #1a4f7a;
    margin-top: 22px;
    margin-bottom: 6px;
  }}

  /* ── Metadata-blok na de hoofdtitel ── */
  h1 ~ p:first-of-type {{
    font-size: 9.5pt;
    color: #666;
    line-height: 1.8;
    margin-bottom: 4px;
  }}

  /* ── Horizontale lijn ── */
  hr {{
    border: none;
    border-top: 1px solid #dde8f2;
    margin: 28px 0;
  }}

  /* ── Alinea's ── */
  p {{
    margin: 0 0 10px 0;
  }}

  /* ── Tabellen ── */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0 20px 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }}

  th {{
    background: #0d2e4f;
    color: #ffffff;
    padding: 7px 11px;
    text-align: left;
    font-weight: 600;
    font-size: 9pt;
    letter-spacing: 0.02em;
  }}

  td {{
    padding: 7px 11px;
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
    border-left: 3px solid #0d2e4f;
    padding: 12px 16px;
    border-radius: 0 5px 5px 0;
    font-family: "Courier New", Courier, monospace;
    font-size: 9pt;
    white-space: pre-wrap;
    margin: 14px 0;
    page-break-inside: avoid;
  }}

  pre code {{
    background: none;
    padding: 0;
    color: inherit;
  }}

  /* ── Blockquote (notities / waarschuwingen) ── */
  blockquote {{
    border-left: 3px solid #3a8fd1;
    margin: 14px 0;
    padding: 8px 14px;
    color: #3a4a5a;
    background: #eef6fd;
    border-radius: 0 5px 5px 0;
    font-size: 9.5pt;
  }}

  blockquote p {{
    margin: 0;
  }}

  /* ── Lijsten ── */
  ul, ol {{
    padding-left: 22px;
    margin: 6px 0 12px 0;
  }}

  li {{
    margin: 4px 0;
    line-height: 1.55;
  }}

  /* ── Handtekeningregels ── */
  p:has(> strong:first-child) {{
    margin-top: 16px;
  }}

  /* ── Paginabreuk-hints ── */
  h2 {{
    page-break-after: avoid;
  }}

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
    parser.add_argument("input", help="Pad naar het markdown-bestand (bijv. overdracht.md)")
    parser.add_argument("output", help="Pad voor de uitvoer-PDF (bijv. overdracht.pdf)")
    parser.add_argument("--bedrijf", default="", help="Jouw bedrijfsnaam voor in de header/footer")
    args = parser.parse_args()

    generate_pdf(args.input, args.output, args.bedrijf)
