Sure — here is the entire PRD formatted as a single Markdown code block for easy copy/paste:

```md
# Product Requirements Document (PRD)

## 1. Executive Summary & Purpose

The Automated Multi-Agent LaTeX Book Generator is a production-grade system designed to automate the research, synthesis, formatting, and compilation of high-quality, comprehensive academic books or articles (targeting a length of approximately 15 pages). Leveraging a multi-agent orchestration framework (CrewAI) alongside an asset compilation pipeline, the system abstracts the technical complexities of literature review and document rendering into a streamlined, programmatically controlled process.

The application serves as a tool for researchers, educators, and content creators to generate well-structured, factually verified, and beautifully typeset professional documents. By implementing a strict Software Development Kit (SDK) layout and an aggressive API Gatekeeper, the product enforces system stability, rate-limit preservation, and adherence to professional software architectural standards.

---

## 2. Product Scope & Core Capabilities

The product delivers automated multi-agent content creation paired with programmatic document typesetting. The scope is bounded by three critical functional criteria:

### Dynamic Topic Specification

- **Requirement:** The system must not rely on a fixed, hardcoded domain or topic.
- **Capability:** The user is interactively prompted to define any desired topic string at runtime. The downstream ingestion pipeline must sanitize and propagate this variable through all research and writing subtasks dynamically.

### Variable Language Support

- **Requirement:** The system must adapt its content creation, structural composition, and underlying typesetting environment to the user's linguistic preferences.
- **Capability:** The user is prompted to select between two configuration modes:
  1. **English-Only:** Standard left-to-right (LTR) execution path where research, content generation, and document compilation use native English typography.
  2. **Bilingual BiDi (Hebrew/English):** A complex bidirectional (BiDi) text layout engine. The agents generate content that blends Hebrew and English seamlessly, and the rendering engine automatically configures a bidirectional LuaLaTeX environment to ensure correct text alignment, layout, and hyphenation.

### Configurable Cover Sheet Module

- **Requirement:** Metadata regarding the document’s origin must be dynamically adjustable.
- **Capability:** Users are prompted to customize five core metadata fields at runtime: `Topic`, `Author`, `Date`, `Course`, and `Lecturer`. The template engine must support conditional logic; fields that are explicitly omitted or left blank by the user must be cleanly stripped from the final template without generating syntax errors or leaving broken spacing in the compiled output.

---

## 3. User Stories & Personas

### Personas

- **Academic Instructor:** Needs a tool to rapidly prototype bilingual or English-only course reading packets with custom administrative metadata (Course name, Lecturer name).
- **Technical Researcher:** Wants to output research papers on various topics dynamically while monitoring execution costs and API consumption limits closely.

### User Stories

- **As an Academic Instructor,** I want to input my name, course code, and a custom date when prompted upon launching the generator, so that the compiled front matter perfectly matches my institutional layout rules without requiring manual code editing.
- **As a Technical Researcher,** I want to choose an English-only mode for international submissions or a BiDi mode for localized Hebrew/English reports at runtime, so that my text formatting looks native and clean regardless of language blend.
- **As a System Administrator,** I want to be interactively prompted for a dynamic string topic when running the script so that I can reuse this utility across multiple distinct execution runs.

---

## 4. Functional Requirements

### 4.1 CLI Entry Point & Parameter Validation

- **FR-1.1:** The system must expose a unified execution script (`src/main.py`).
- **FR-1.2:** The script must interactively prompt the user at runtime for the `topic`, `language`, and optional string variables for `author`, `date`, `course`, and `lecturer` (arguments are not passed as command-line flags).
- **FR-1.3:** Input validation must fail or prompt again immediately if the language input does not exactly match permitted options (`english`, `bidi`).

### 4.2 Centralized SDK Core

- **FR-2.1:** All high-level behaviors must run through an SDK abstraction layer (`src/sdk/sdk.py`).
- **FR-2.2:** The SDK must serve as the single public entry point, completely isolating orchestration logic, tool execution, and configuration parsing away from the UI/interactive layer.

### 4.3 Multi-Agent Orchestration Engine (CrewAI)

- **FR-3.1:** The architecture must deploy three specialized agents working sequentially: a Researcher agent, a Writer agent, and a Reviewer/Editor agent.
- **FR-3.2:** The Researcher agent must utilize context variables to execute scoped web queries based on the chosen topic.
- **FR-3.3:** The Writer agent must receive the validated content and output modular, structured Markdown text adhering strictly to the user’s selected language mode.
- **FR-3.4:** The Reviewer/Editor agent must run quality assessments on the Markdown draft to verify completeness and ensure proper formatting compatibility with LaTeX escape sequences.

### 4.4 Safe API Gatekeeper & Backpressure Control

- **FR-4.1:** All tools or agents attempting network interactions with external LLM endpoints must route calls through a centralized `ApiGatekeeper` class.
- **FR-4.2:** The gatekeeper must intercept outgoing payloads and check them against current allocations specified in `config/rate_limits.json`.
- **FR-4.3:** If a rate limit threshold is imminent, the gatekeeper must transparently queue the requests and enforce an explicit backpressure or backoff period to prevent standard connection failures.

### 4.5 Dynamic Asset & LaTeX Compiler Component

- **FR-5.1:** The pipeline must programmatically convert agentic Markdown into native LaTeX markup.
- **FR-5.2:** The component must read the metadata configuration block and generate a conditional cover sheet using dynamic string interpolation.
- **FR-5.3:** If BiDi is enabled, the system must swap out the default preamble for a specialized package configuration using BiDi-compliant fonts and text direction macros.
- **FR-5.4:** The compiler must automatically bundle auxiliary assets located in the `assets/` folder (e.g., TikZ diagrams, Matplotlib graphs) into the document layout.

---

## 5. Non-Functional Requirements & Compliance

### 5.1 Performance & Quality Metrics (ISO/IEC 25010 Compliance)

- **Maintainability:** Source structures must follow modular packaging guidelines. Individual script files must not exceed 150 lines of code.
- **Reliability:** The asset compilation component must execute multiple sequential compilation steps (minimum 4 runs) to guarantee complete cross-referencing, Table of Contents population, and bibliography binding without rendering dead links.
- **Functional Suitability:** The output file must be a highly structured PDF document that matches the defined design specifications perfectly.

### 5.2 Testability & Linting Constraints

- **Coverage Target:** The test suite implemented in `tests/` must achieve a minimum code coverage threshold of 85%. Any builds falling below this mark must trigger an explicit failure state.
- **Code Cleanliness:** The project must utilize Ruff linting configurations targeting exactly zero stylistic or programmatic violations (ignoring E501 for long string prompts, with a global line cap of 100 characters).

### 5.3 Token Cost Auditing & Rate-Limit Metrics

- **Auditing:** Every session execution must log input/output token metrics programmatically.
- **Analysis:** The system must record historical costs inside a dedicated ledger format, feeding directly into runtime performance models and analytical notebooks for transparent usage tracking.

---

## 6. Key Performance Indicators (KPIs) & Acceptance Criteria

| ID | Feature Category | Metrics / Acceptance Criteria |
| --- | --- | --- |
| **KPI-1** | Target Output Scale | The compilation engine successfully generates a PDF document approximately 15 pages in length. |
| **KPI-2** | Content Integrity | The final document integrates at least 1 image graph, 1 formatted data table, and 1 complex math equation block with zero structural rendering errors. |
| **KPI-3** | Parameter Adaptability | Omitting optional cover metadata (e.g., leaving the `course` prompt blank) results in a clean document compile with no broken fields or blank placeholder labels. |
| **KPI-4** | Language Alignment | Running the pipeline with `bidi` selected at the language prompt produces right-to-left layout alignment for Hebrew sections, while keeping technical formulas or English terms structurally intact. |
| **KPI-5** | Code Coverage Quality | Executing the test run command completes with an audited statement showing `pytest-cov >= 85%`. |

---

## 7. Implementation Timeline & Milestones

- **Milestone 1 (Foundations & Safety Controls):** Repository scaffolding, pyproject alignment, configuration parser completion, and full validation of the `ApiGatekeeper` rate-limiting queues under simulation.
- **Milestone 2 (Agent & SDK Framework):** Verification of the core SDK layer. Successful execution of the interactive multi-agent pipeline taking interactive user inputs and writing files out to disk.
- **Milestone 3 (Typesetting & Formatting Layer):** Integration of conditional cover sheets and dual-mode preambles (English vs. BiDi). Successful embedding of external tables, charts, and equations.
- **Milestone 4 (Final Quality Check & Audit):** Achievement of 85% test coverage, 0-violation lint status, execution of multi-pass LuaLaTeX testing, generation of cost breakdown notebooks, and clean submission packet preparation.
```
