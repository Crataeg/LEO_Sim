# IEICE Transactions on Communications Official Format and Template

Saved on: `2026-03-24`

## Official Source Pages

- Author guide contents page:
  - `https://www.ieice.org/eng/shiori/mokuji_cs.html`
  - Local copy: `official_pages/mokuji_cs_official.html`
- Author guide detail page:
  - `https://www.ieice.org/eng/shiori/page2_cs.html`
  - Local copy: `official_pages/page2_cs_official.html`
- Official author tools / template page:
  - `https://www.ieice.org/ftp/index-e.html`
  - Local copy: `official_pages/ftp_index_e_official.html`

## Downloaded Official Files

- Official Word template:
  - URL: `https://www.ieice.org/eng/s_issue/docs/IEICE.doc`
  - Local file: `official_files/IEICE_official_word_template.doc`
- Official LaTeX package:
  - URL: `https://www.ieice.org/ftp/tex/ieice/LaTeX2e/ieice_v2.3.zip`
  - Local file: `official_files/ieice_v2.3_official.zip`
- Official manuscript guide PDF:
  - URL: `https://www.ieice.org/ftp/tex/tech_rep/LaTeX2e/readme2ej.pdf`
  - Local file: `official_files/readme2ej_official.pdf`

## Extracted LaTeX Package Contents

- `latex_extracted/ieice.cls`
- `latex_extracted/ieicetr.bst`
- `latex_extracted/template.tex`
- `latex_extracted/readme-e.pdf`
- `latex_extracted/readme-e.tex`
- `latex_extracted/readme-j.pdf`
- `latex_extracted/readme-j.tex`

Note:
- `latex_extracted/__MACOSX/` is just archive metadata and can be ignored.

## Key Official Format Points

- Journal scope page confirms `Satellite Communications` is within scope for `IEICE Transactions on Communications`.
- The official guide states that two manuscript formats are accepted:
  - `IEICE LaTeX style file`
  - `MS-Word template file`
- The guide explicitly says the format must not be modified:
  - line spacing
  - font size
  - other layout settings
- Standard manuscript length:
  - `PAPER`: 8 pages
  - `WRITTEN DISCUSSION`: 2 pages
- Maximum initial submission length:
  - `PAPER`: 15 pages
  - `WRITTEN DISCUSSION`: 4 pages
- One page is approximately `900 words`.
- Required manuscript element order includes:
  - title
  - authors and membership status
  - affiliation and correspondence address
  - summary
  - keywords
  - body
  - acknowledgments
  - references
  - appendix if any
  - author biography and photo
  - figures/tables

## Cost-Related Official Note

- IEICE explicitly recommends LaTeX because the manuscript is closer to the final printed format.
- The official guide also states that the article processing charge is lower for manuscripts prepared with the IEICE LaTeX style file than for manuscripts prepared with the Word template.
- The contents page notes a charge change after submission date `2025-07-01`.

## Practical Recommendation

- For this satellite SCI submission, use:
  - `latex_extracted/template.tex`
  - `latex_extracted/ieice.cls`
  - `latex_extracted/ieicetr.bst`
- Keep the Word template only as backup.
