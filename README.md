# AI-Agents-HW3

## Overview

AI-Agents-HW3 is a multi-agent academic document generation platform built using CrewAI, Google Gemini, LaTeX, and a custom SDK orchestration layer.

The system automates the complete academic writing workflow:

1. Researching a topic
2. Gathering and managing sources
3. Planning document structure
4. Generating chapters
5. Reviewing and editing content
6. Validating document quality
7. Preparing LaTeX-ready output

The project follows a modular architecture that separates orchestration, validation, bibliography management, document generation, and API governance into independent components.

---

## Key Features

- Multi-agent CrewAI orchestration
- Google Gemini 2.5 Flash integration
- Automated research workflow
- Academic chapter planning
- Long-form document generation
- Automated document review
- Bibliography management
- Markdown-to-LaTeX workflow
- LaTeX document generation
- API rate limiting and retry handling
- Validation and sanitization pipeline
- Configuration-driven architecture
- Jupyter notebook performance analysis
- Automated testing with coverage enforcement

---

## Architecture

```text
User Input
    │
    ▼
CrewPipelineSDK
    │
    ├── Chapter Planner
    ├── Chapter Writer
    ├── Document Editor
    ├── Bibliography Manager
    ├── Validators
    └── Sanitizer
    │
    ▼
CrewAI Pipeline
    │
    ├── Research Agent
    ├── Writer Agent
    └── Editor Agent
    │
    ▼
LaTeX Builder
    │
    ▼
Final Academic Document
```

---

## Agent Workflow

### Research Agent

Responsible for:

- Finding relevant information
- Gathering sources
- Extracting key facts
- Supporting citation generation

### Writer Agent

Responsible for:

- Chapter generation
- Content structuring
- Language adaptation
- Academic writing

### Editor Agent

Responsible for:

- Reviewing generated content
- Improving clarity and consistency
- Validating formatting
- Preparing LaTeX-ready output

---

## SDK Layer

The project uses a custom SDK architecture located in:

```text
src/sdk/
```

Main components:

| Component | Responsibility |
|------------|----------------|
| sdk.py | Main orchestration entry point |
| chapter_planner.py | Chapter planning |
| chapter_writer.py | Chapter generation |
| document_editor.py | Document review |
| bibliography.py | Citation management |
| validators.py | Validation logic |
| sanitizer.py | Output sanitization |
| pipeline_helpers.py | Shared pipeline utilities |
| prompts.py | Prompt management |

The SDK abstracts all CrewAI implementation details from the application layer.

---

## API Gatekeeper

All external API calls pass through a centralized gatekeeper.

Features:

- Rate limiting
- Retry logic
- Backpressure handling
- Thread-safe execution
- Centralized API governance

Configuration is loaded from:

```text
config/rate_limits.json
```

---

## Configuration

Project configuration files:

```text
config/
├── setup.json
└── rate_limits.json
```

### setup.json

Stores project-level settings and version information.

### rate_limits.json

Stores:

- Requests per minute
- Requests per hour
- Maximum retries

---

## Project Structure

```text
AI-Agents-HW3
│
├── config
│   ├── rate_limits.json
│   └── setup.json
│
├── docs
│   ├── PLAN.md
│   ├── PRD.md
│   ├── PRD_api_gatekeeper.md
│   ├── PRD_crew_orchestration.md
│   ├── PRD_lualatex_bidi_compiler.md
│   ├── PRD_markdown_parser.md
│   ├── PROMPT_BOOK.md
│   └── TODO.md
│
├── notebooks
│   └── analysis.ipynb
│
├── skills
│   └── SKILL.md
│
├── src
│   ├── sdk
│   ├── services
│   ├── shared
│   └── main.py
│
├── tests
│   ├── integration
│   └── unit
│
├── biblio.bib
├── pyproject.toml
├── README.md
└── uv.lock
```

---

## Installation

### Prerequisites

- Python 3.10+
- uv package manager

### Clone Repository

```bash
git clone <repository-url>
cd AI-Agents-HW3
```

### Install Dependencies

```bash
uv sync
```

---

## Environment Variables

Create a `.env` file based on `.env-example`.

Required variables:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## Running the Application

Execute:

```bash
uv run python src/main.py
```

The system will launch the CrewAI pipeline and process the requested topic through the configured agents.

---

## Testing

Run all tests:

```bash
uv run pytest -v
```

Current testing status:

- Unit tests implemented
- Integration tests implemented
- SDK tests implemented
- Gatekeeper tests implemented
- Configuration tests implemented

Coverage requirement:

```text
Minimum required coverage: 85%
```

Current project coverage:

```text
87.43%
```

---

## Linting

Run Ruff:

```bash
uv run ruff check
```

Auto-fix issues:

```bash
uv run ruff check --fix
```

Project goal:

```text
0 linting violations
```

---

## Performance Analysis

Performance and token-cost analysis are available in:

```text
notebooks/analysis.ipynb
```

The notebook includes:

- Parameter sensitivity analysis
- Heatmap visualizations
- Token cost analysis
- Model cost comparison
- Performance evaluation

---

## Documentation

Detailed project documentation is available in:

```text
docs/
```

Including:

- Product Requirements Documents (PRDs)
- Development Plan
- TODO Tracking
- Prompt Book
- Architecture Documentation

---

## Technologies Used

- Python 3.12+
- CrewAI
- Google Gemini 2.5 Flash
- DuckDuckGo Search
- PyTest
- Ruff
- uv
- Jupyter Notebook
- Pandas
- Matplotlib
- Seaborn
- LaTeX / LuaLaTeX

---

## Future Improvements

Potential future enhancements:

- Additional research tools
- Multi-model support
- Advanced citation management
- PDF export automation
- Web interface
- Agent performance analytics
- Enhanced document validation

---

## License

This project was developed as part of an academic AI Agents coursework assignment.

Educational use only.