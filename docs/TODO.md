# Project Task Tracker (`docs/TODO.md`)

This document tracks all tasks required to complete the Automated Multi-Agent LaTeX Book Generator project.

Tasks are divided into 8 distinct phases with predefined milestones.

## Assignment Key

* **Partner 1:** Responsible for all ODD phases (1, 3, 5, 7)
* **Partner 2:** Responsible for all EVEN phases (2, 4, 6, 8)

### Status Options

* Not Started
* In Progress
* Done

---

# Phase 1: Project Setup & Initialization, Mandatory Documentation

**Milestone**

Local environments are initialized, dependencies are locked, and all mandatory PRD and planning documentation are approved.

---

## Task 1.1 — Initialize Git Repository

**Priority:** High
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

* `git init` executed
* `main` branch created

---

## Task 1.2 — Initialize Python Environment

**Priority:** High
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

* `uv init` executed
* Virtual environment active

---

## Task 1.3 — Create Mandatory Folder Structure

**Priority:** High
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

The following directories exist:

```text
src/
docs/
tests/
config/
data/
assets/
```

---

## Task 1.4.1 — Create `.gitignore`

**Priority:** High
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

* Standard Python ignore patterns added
* `.env` added

---

## Task 1.4.2 — Create `.env-example`

**Priority:** High
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

* Dummy API keys documented
* Required environment variables listed

---

## Task 1.5.1 — Configure Ruff Linter

**Priority:** High
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

`pyproject.toml` configured with:

* 100 character line limit
* Zero violations target
* E501 ignored

---

## Task 1.5.2 — Configure Pytest Coverage

**Priority:** High
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

Coverage configuration includes:

```toml
fail_under = 85
```

---

## Task 1.6 — Lock Dependencies

**Priority:** High
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

* `uv lock` executed
* `uv.lock` committed to version control

---

## Task 1.7.1 — Write Core `PRD.md`

**Priority:** High
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

Document includes:

* KPIs
* User stories
* Project timeline

---

## Task 1.7.2 — Document PRD Dynamic Inputs

**Priority:** High
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

PRD documents:

* Topic input
* Language modes
* Cover sheet metadata

---

## Task 1.8 — Write `PLAN.md`

**Priority:** High
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

Document includes:

* C4 Context model
* C4 Container model
* SDK architecture

---

## Task 1.9 — Generate `TODO.md`

**Priority:** High
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

* File created
* File populated
* File pushed

---

## Task 1.10 — Write 4 specific mechanisms PRDs

**Priority:** Medium
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

The files: 
- PRD_api_gatekeeper.md
- PRD_lualatex_bidi_compiler.md
- PRD_markdown_parser.md
- PRD_crew_orchestration.md

are created and populated

---

# Phase 2: Core Infrastructure & Configurations

**Milestone**

All JSON configurations are parsed securely, and the API Gatekeeper is built to manage external rate limits and queues.

---

## Task 2.1 — Create `setup.json`

**Priority:** High
**Assignee:** Partner 2
**Status:** Done

### Definition of Done

File exists:

```json
{
  "version": "1.00"
}
```

---

## Task 2.2 — Create `rate_limits.json`

**Priority:** High
**Assignee:** Partner 2
**Status:** Done

### Definition of Done

Configuration contains:

* RPM = 30
* RPH = 500
* Max retries = 3

---

## Task 2.3 — Create Global Version Tracker

**Priority:** Low
**Assignee:** Partner 2
**Status:** Done

### Definition of Done

Created:

```text
src/shared/version.py
```

Tracking:

```python
VERSION = "1.00"
```

---

## Task 2.4.1 — Implement Config Parser Logic

**Priority:** High
**Assignee:** Partner 2
**Status:** Done

### Definition of Done

Parser:

* Loads JSON files
* Validates configuration
* Checks version compatibility

---

## Task 2.4.2 — Implement Safe Environment Loader

**Priority:** High
**Assignee:** Partner 2
**Status:** Done

### Definition of Done

Secrets loaded via:

```python
os.environ.get(...)
```

No hardcoded credentials.

---

## Task 2.5.1 — Implement `ApiGatekeeper` Limit Checks

**Priority:** Critical
**Assignee:** Partner 2
**Status:** Done

### Definition of Done

Gatekeeper:

* Intercepts requests
* Reads limits from configuration
* Validates requests before execution

---

## Task 2.5.2 — Implement Gatekeeper Queueing

**Priority:** Critical
**Assignee:** Partner 2
**Status:** Done

### Definition of Done

Supports:

* FIFO queueing
* Retry handling
* Backpressure logic

---

# Phase 3: Agent & Tool Engineering

**Milestone**

CrewAI dependencies are installed and specialized agents are built with tools routed through the Gatekeeper.

---

## Task 3.1 — Install AI Packages

**Priority:** High
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

Installed:

```bash
uv add crewai
uv add langchain-community
```

---

## Task 3.2.1 — Define External Search Tools

**Priority:** High
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

Tool implemented using CrewAI:

```python
@tool
```

---

## Task 3.2.2 — Wire Tools to Gatekeeper

**Priority:** Critical
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

All tool execution routes through:

```python
ApiGatekeeper
```

---

## Task 3.3 — Define Researcher Agent

**Priority:** Medium
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

Agent includes:

* Goal
* Backstory
* Tool access
* Topic awareness

---

## Task 3.4 — Define Writer Agent

**Priority:** Medium
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

Agent generates:

* Structured Markdown
* Language-aware output
* Academic formatting

---

## Task 3.5 — Define Editor Agent

**Priority:** Medium
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

Agent verifies:

* Accuracy
* Formatting
* LaTeX readiness

---

## Task 3.6 — Audit File Length Limits

**Priority:** Low
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

Audit confirms:

* No Python file exceeds 150 lines

---

# Phase 4: Orchestration & SDK Implementation

**Milestone**

The Crew is orchestrated, and the centralized SDK serves as the sole entry point triggered by interactive CLI prompts.

---

## Task 4.1 — Define Research Task

**Priority:** High
**Assignee:** Partner 2
**Status:** Done

### Definition of Done

Task uses:

* `{topic}`
* `{language}`

Input variables.

---

## Task 4.2 — Define Writing Task

**Priority:** High
**Assignee:** Partner 2
**Status:** Done

### Definition of Done

Task:

* Consumes research output
* Produces structured Markdown
* Respects selected language mode

---

## Task 4.3 — Define Review Task

**Priority:** High
**Assignee:** Partner 2
**Status:** Done

### Definition of Done

Task:

* Consumes writing output
* Produces final reviewed Markdown

---

## Task 4.4 — Instantiate Crew

**Priority:** High
**Assignee:** Partner 2
**Status:** Done

### Definition of Done

Crew:

* Contains 3 agents
* Contains 3 tasks
* Uses `Process.sequential`

---

## Task 4.5.1 — Create `CrewPipelineSDK` Logic

**Priority:** Critical
**Assignee:** Partner 2
**Status:** Done

### Definition of Done

SDK:

* Encapsulates Crew kickoff
* Hides orchestration details
* Provides clean API surface

---

## Task 4.5.2 — Define SDK Parameter Signature

**Priority:** High
**Assignee:** Partner 2
**Status:** Done

### Definition of Done

`run()` accepts:

* Topic
* Language
* Optional metadata dictionary

---

## Task 4.6.1 — Implement `main.py` CLI Inputs

**Priority:** High
**Assignee:** Partner 2
**Status:** Done

### Definition of Done

User is prompted for:

* Topic
* Language
* Author
* Date
* Course
* Lecturer

---

## Task 4.6.2 — Wire CLI to SDK

**Priority:** Critical
**Assignee:** Partner 2
**Status:** Done

### Definition of Done

Validated user input successfully reaches SDK execution layer.

---

# Phase 5: Visuals & LaTeX Asset Preparation

**Milestone**

All external graphical assets and the responsive, BiDi-capable LuaLaTeX skeleton are prepared for dynamic content injection.

---

## Task 5.1 — Define Agent Skills (`SKILL.md`)

**Priority:** High  
**Assignee:** Partner 1  
**Status:** Done

### Definition of Done

- Created `skills/SKILL.md` (per Appendix A guidelines)
- Document contains strict LaTeX formatting rules
- Document contains BiDi, Math, and TikZ layout guidelines

---

## Task 5.2.1 — Build LaTeX Cover Template

**Priority:** High
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

Template includes:

* Title
* Author
* Date
* Course
* Lecturer

Fields support conditional rendering.

---

## Task 5.2.2 — Implement Cover Injection Logic

**Priority:** High
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

Injection layer:

* Uses Jinja2 or equivalent templating
* Omits empty fields
* Produces valid LaTeX in all cases

---

## Task 5.3.1 — Configure LuaLaTeX Preamble

**Priority:** Critical
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

Preamble supports:

* English documents
* BiDi documents
* Font configuration
* RTL support

---

## Task 5.3.2 — Add Graphical LaTeX Packages

**Priority:** Medium
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

Preamble includes:

* `tikz`
* `amsmath`

Additional graphics packages validated.

---

## Task 5.4 — Format TOC and Headers

**Priority:** Low
**Assignee:** Partner 1
**Status:** Done

### Definition of Done

Document includes:

* `\tableofcontents`
* Consistent headers
* Consistent footers
* `fancyhdr` configuration

---

## Task 5.5 — Initialize Empty Bibliography for Dynamic Injection

**Priority:** High  
**Assignee:** Partner 1  
**Status:** Done

### Definition of Done

- Created a completely blank `biblio.bib` file
- Ensured file is ready to receive dynamic programmatic appends from the Researcher's `append_bibtex_tool`.

---

# Phase 6: Testing (TDD) & Linting

**Milestone**

Code reliability is proven via TDD, minimum coverage of 85% is achieved, and Ruff passes with zero violations.

---

## Task 6.1.1 — Unit Test: Config Parser

**Priority:** Medium
**Assignee:** Partner 2
**Status:** Not Started

### Definition of Done

Tests verify:

* JSON loading
* Validation behavior
* Version checks

Located under:

```text
tests/unit/
```

---

## Task 6.1.2 — Unit Test: ApiGatekeeper

**Priority:** Critical
**Assignee:** Partner 2
**Status:** Not Started

### Definition of Done

Tests verify:

* Rate limiting
* Queueing
* Retry behavior
* Successful execution path

---

## Task 6.2 — Unit Test: Tool Mocking

**Priority:** High
**Assignee:** Partner 2
**Status:** Not Started

### Definition of Done

Tests verify:

* External calls are mocked
* Tools route through Gatekeeper
* No live API dependency

---

## Task 6.3 — Integration Test: SDK

**Priority:** High
**Assignee:** Partner 2
**Status:** Not Started

### Definition of Done

End-to-end test verifies:

* SDK initialization
* Crew execution
* Result handling

Using mocked Crew components.

---

## Task 6.4 — Run Coverage Audit

**Priority:** Critical
**Assignee:** Partner 2
**Status:** Not Started

### Definition of Done

Command executed:

```bash
uv run pytest tests/ --cov=src
```

Coverage report shows:

```text
>= 85%
```

---

## Task 6.5 — Run Linter Audit

**Priority:** High
**Assignee:** Partner 2
**Status:** Not Started

### Definition of Done

Command executed:

```bash
uv run ruff check --fix
```

Results show:

```text
0 violations
```

---

# Phase 7: Compilation & Quality Check

**Milestone**

The full pipeline completes, Markdown translates cleanly to LaTeX, and LuaLaTeX successfully renders the final PDF.

---

## Task 7.1 — Execute Raw Content Generation

**Priority:** Critical
**Assignee:** Partner 1
**Status:** Not Started

### Definition of Done

Command executed:

```bash
uv run python src/main.py
```

Output contains:

* Completed Markdown
* No fatal execution errors

---

## Task 7.2.1 — Inject Graphical Assets

**Priority:** High
**Assignee:** Partner 1
**Status:** Not Started

### Definition of Done

Generated document includes:

* Markdown content
* One graph
* One formatted table

Assets successfully referenced in LaTeX.

---

## Task 7.2.2 — Inject Mathematical Formula

**Priority:** Medium
**Assignee:** Partner 1
**Status:** Not Started

### Definition of Done

Document contains:

* At least one advanced equation
* Proper LaTeX equation environment

Example:

```latex
\begin{equation}
E = mc^2
\end{equation}
```

---

## Task 7.3 — Compile `.tex` File Locally

**Priority:** Critical
**Assignee:** Partner 1
**Status:** Not Started

### Definition of Done

Compilation sequence:

```bash
lualatex document.tex
biber document
lualatex document.tex
lualatex document.tex
```

Requirements:

* No fatal errors
* Bibliography resolved
* TOC resolved
* References resolved

---

## Task 7.4.1 — Visual PDF Review: Alignment

**Priority:** High
**Assignee:** Partner 1
**Status:** Not Started

### Definition of Done

Manual inspection confirms:

* Correct RTL rendering
* Correct LTR rendering
* Proper margins
* No layout corruption

---

## Task 7.4.2 — Visual PDF Review: Links

**Priority:** High
**Assignee:** Partner 1
**Status:** Not Started

### Definition of Done

Verification confirms:

* TOC links work
* Bibliography links work
* Internal references work

---

# Phase 8: Research Log & Optimization

**Milestone**

Output data is analyzed, API token costs are audited, and the project README is finalized.

---

## Task 8.1 — Document Prompt Book

**Priority:** Low
**Assignee:** Partner 2
**Status:** Not Started

### Definition of Done

Document includes:

* Prompts used
* Iteration history
* Prompt engineering notes

Stored as Markdown.

---

## Task 8.2 — Execute Parameter Sensitivity Analysis

**Priority:** High  
**Assignee:** Partner 2  
**Status:** Not Started

### Definition of Done

- Created `src/scripts/sensitivity_analysis.py`
- Script tests multiple controlled parameter changes (e.g., LLM temperature variations).
- Latency and performance are tracked and plotted.
- Output graph saved automatically.

---

## Task 8.3 — Calculate Token Costs

**Priority:** High
**Assignee:** Partner 2
**Status:** Not Started

### Definition of Done

Report contains:

* Input token totals
* Output token totals
* Estimated API costs
* Provider breakdown

Examples:

* GPT-4
* Claude

---

## Task 8.4.1 — Draft README Instructions

**Priority:** High
**Assignee:** Partner 2
**Status:** Not Started

### Definition of Done

README documents:

* Installation
* Environment setup
* Configuration
* CLI usage
* Troubleshooting

---

## Task 8.4.2 — Finalize README Audit Information

**Priority:** High
**Assignee:** Partner 2
**Status:** Not Started

### Definition of Done

README includes:

* SDK architecture summary
* Coverage evidence
* Token cost analysis
* Final audit checklist

---

# Project Completion Checklist

## Documentation

* [ ] PRD completed
* [ ] PLAN completed
* [ ] TODO completed
* [ ] README completed
* [ ] Prompt Book completed

## Development

* [ ] SDK implemented
* [ ] Agents implemented
* [ ] Gatekeeper implemented
* [ ] CLI implemented
* [ ] LaTeX engine implemented

## Quality

* [ ] Ruff passes with zero violations
* [ ] Coverage >= 85%
* [ ] All tests passing

## Output

* [ ] PDF generated
* [ ] Approximately 15 pages
* [ ] Includes graph
* [ ] Includes table
* [ ] Includes equation
* [ ] Includes bibliography
* [ ] Supports English mode
* [ ] Supports BiDi mode

## Submission

* [ ] Repository cleaned
* [ ] Documentation complete
* [ ] Example output generated
* [ ] Final audit performed

```
```

