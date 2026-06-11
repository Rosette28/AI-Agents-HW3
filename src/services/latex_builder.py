import jinja2

LATEX_TEMPLATE = r"""\documentclass[12pt,a4paper]{article}

% Graphical & Layout Packages
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,shapes,positioning,calc,babel}
\usepackage{graphicx}
\usepackage{float}       % REQUIRED for [htbp] placement
\usepackage{tabularx}    % REQUIRED for tabularx environments
\usepackage{multirow}    % REQUIRED for multirow in tables
\usepackage{booktabs}    % REQUIRED for \toprule, \midrule, \bottomrule
\usepackage{adjustbox}  % REQUIRED for auto-resizing tables to fit page width

% LuaLaTeX Preamble & BiDi Support
\usepackage{fontspec}
{% if language == 'bidi' %}
\usepackage[bidi=basic]{babel}
\babelprovide[import, main]{hebrew}
\babelprovide[import]{english}
% Fallback to a font name that is standard on most OS environments
\babelfont{rm}[Script=Hebrew]{Arial}
\babelfont{sf}[Script=Hebrew]{Arial}
{% else %}
\usepackage[english]{babel}
{% endif %}

% Bibliography
\usepackage[backend=biber,style=numeric]{biblatex}
\addbibresource{biblio.bib}

% Hyperlinks (load last to avoid conflicts)
\usepackage[hidelinks,unicode]{hyperref}

% Headers, Footers, and TOC formatting
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{ {{ topic }} }
\fancyhead[R]{AI Agents Report}
\fancyfoot[C]{\thepage}
\setlength{\headheight}{15pt} % Fix for fancyhdr small headheight warning


\begin{document}

% Cover Template
\begin{titlepage}
    \centering
    \vspace*{2cm}
    {\Huge \textbf{ {{ topic }} } \par}
    \vspace{1.5cm}
    
    {% if author %}
    {\Large \textbf{Author:} {{ author }} \par}
    \vspace{0.5cm}
    {% endif %}
    
    {% if course %}
    {\Large \textbf{Course:} {{ course }} \par}
    \vspace{0.5cm}
    {% endif %}
    
    {% if lecturer %}
    {\Large \textbf{Lecturer:} {{ lecturer }} \par}
    \vspace{0.5cm}
    {% endif %}
    
    {% if date %}
    {\Large \textbf{Date:} {{ date }} \par}
    {% endif %}
    \vfill
\end{titlepage}

\newpage
\tableofcontents
\newpage

% The parsed content is injected here
{{ content }}

\printbibliography

\end{document}
"""

def generate_latex_document(topic: str, language: str, content: str, cover_sheet: dict) -> str:
    """Renders the LaTeX document using Jinja2."""
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