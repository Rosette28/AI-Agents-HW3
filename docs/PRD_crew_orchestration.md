# Mechanism PRD: Multi-Agent Workflow Orchestration

## 1. Description & Background
The orchestration mechanism manages the lifecycle, state, and data-passing between the AI agents (Researcher, Writer, Editor). It defines the boundaries of what each agent is allowed to do, limits their tool access (via the Gatekeeper), and determines how the context flows from the initial CLI prompt down to the final document string.

## 2. Expected Inputs and Outputs
* **Input:** `topic` (string) and `language` (string: "english" or "bidi").
* **Output:** A final, fact-checked, and formatted Markdown string containing the text of a ~15-page article.

## 3. Constraints, Alternatives, and Rationale (ADR)
* **Constraint:** The agents must reliably produce ~15 pages of content, generate their own contextual graphs, parse real web citations, and perfectly format bilingual BiDi chapters and TikZ diagrams.
* **Alternative 1: Prompt Engineering Only.** *Rejected*. Relying solely on the `system_prompt` causes the LLM to hallucinate LaTeX syntax and fail volumetric requirements (writing short summaries instead of long chapters).
* **Selected Architecture: `Process.sequential` with Dynamic Tools & Injected Skills.** * **Dynamic Tools:** Agents are provided with Python-execution tools to autonomously write to `biblio.bib` and generate `.png` graphs via Matplotlib.
  * **Injected Skills:** The Editor agent is programmatically injected with `skills/SKILL.md` (adhering to Appendix A workflows). This separates its functional "hands" (Tools) from its academic "mind" (Skills).
  * **Task Looping/Forcing:** The writing task explicitly demands exhaustive multi-chapter output to force the LLM to hit the 15-page volumetric requirement.

## 4. Test Scenarios & Acceptance Criteria
* **Scenario A (Language Adherence):** Pass `language="bidi"`.
  * *Success:* The Writer agent generates the text combining Hebrew and English naturally. The Editor agent does not accidentally translate the Hebrew back to English.
* **Scenario B (Tool Isolation):** The Writer agent attempts to search the web for missing information.
  * *Success:* The system denies the execution or raises an error, proving that only the Researcher agent has been granted access to the web-search tool.
* **Scenario C (Length & Depth Enforcement):** The topic is "Agentic AI".
  * *Success:* The prompt instructions effectively force the Writer to expand on sub-topics, generating sufficient tokens to fill approximately 15 pages once typeset, rather than summarizing the topic in a single page.