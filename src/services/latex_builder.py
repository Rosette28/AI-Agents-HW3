import jinja2

# This template handles Tasks 5.2.1, 5.2.2, 5.3.1, 5.3.2, and 5.4
LATEX_TEMPLATE = """
\\documentclass[12pt,a4paper]{article}

% Task 5.3.2: Graphical Packages
\\usepackage{amsmath}
\\usepackage{tikz}
\\usepackage{graphicx}

% Task 5.3.1: LuaLaTeX Preamble & BiDi Support
\\usepackage{fontspec}
{% if language == 'bidi' %}
\\usepackage[bidi=basic]{babel}
\\babelprovide[import, main]{hebrew}
\\babelprovide[import]{english}
% Note: You must have a Hebrew font installed on your system, such as Arial or David CLM
\\babelfont{rm}[Script=Hebrew]{Arial} 
{% else %}
\\usepackage[english]{babel}
{% endif %}

% Task 5.4: Headers, Footers, and TOC formatting
\\usepackage{fancyhdr}
\\pagestyle{fancy}
\\fancyhf{}
\\fancyhead[L]{ {{ topic }} }
\\fancyhead[R]{AI Agents Report}
\\fancyfoot[C]{\\thepage}

% Bibliography setup
\\usepackage[backend=biber,style=apa]{biblatex}
\\addbibresource{biblio.bib}

\\begin{document}

% Task 5.2.1 & 5.2.2: Cover Template & Injection Logic (Conditional Rendering)
\\begin{titlepage}
    \\centering
    \\vspace*{2cm}
    {\\Huge \\textbf{ {{ topic }} } \\par}
    \\vspace{1.5cm}
    
    {% if author %}
    {\\Large \\textbf{Author:} {{ author }} \\par}
    \\vspace{0.5cm}
    {% endif %}
    
    {% if course %}
    {\\Large \\textbf{Course:} {{ course }} \\par}
    \\vspace{0.5cm}
    {% endif %}
    
    {% if lecturer %}
    {\\Large \\textbf{Lecturer:} {{ lecturer }} \\par}
    \\vspace{0.5cm}
    {% endif %}
    
    {% if date %}
    {\\Large \\textbf{Date:} {{ date }} \\par}
    {% endif %}
    \\vfill
\\end{titlepage}

\\newpage
\\tableofcontents
\\newpage

% The Markdown-to-LaTeX parsed content will be injected here
{{ content }}

\\newpage
\\printbibliography

\\end{document}
"""

def generate_latex_document(topic: str, language: str, content: str, cover_sheet: dict) -> str:
    """Renders the LaTeX document using Jinja2, omitting any empty cover sheet fields.
    """
    template = jinja2.Template(LATEX_TEMPLATE)

    return template.render(
        topic=topic,
        language=language,
        content=content,
        author=cover_sheet.get("author"),
        course=cover_sheet.get("course"),
        lecturer=cover_sheet.get("lecturer"),
        date=cover_sheet.get("date"),
    )
