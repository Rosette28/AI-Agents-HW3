# Mechanism PRD: Multi-Agent Workflow Orchestration

## 1. Description & Background
The orchestration mechanism manages the lifecycle, state, and data-passing between the AI agents (Researcher, Writer, Editor). It defines the boundaries of what each agent is allowed to do, limits their tool access (via the Gatekeeper), and determines how the context flows from the initial CLI prompt down to the final document string.

## 2. Expected Inputs and Outputs
* **Input:** `topic` (string) and `language` (string: "english" or "bidi").
* **Output:** A final, fact-checked, and formatted Markdown string containing the text of a ~15-page article.

## 3. Constraints, Alternatives, and Rationale (ADR)
* **Constraint:** The agents must not enter infinite loops (hallucination loops) and must reliably produce content that spans approximately 15 pages in length.
* **Alternative 1: `Process.hierarchical`.** Appoint a "Manager" agent to dynamically delegate tasks to the Researcher, Writer, and Editor. *Rejected* because hierarchical processes consume significantly more API tokens (costing more money) and can lead to unpredictable document structures that break LaTeX compilation.
* **Selected Architecture: `Process.sequential` with Strict Context Passing.** Tasks are hardcoded in a strict 1-2-3 pipeline. 
  * Task 1 (Research) passes its output explicitly to Task 2 via the `context` parameter.
  * Task 2 (Writer) receives the facts and the `language` requirement, outputting structured Markdown.
  * Task 3 (Editor) receives the draft, checks for hallucinations against Task 1's facts, and ensures LaTeX structural readiness.

## 4. Test Scenarios & Acceptance Criteria
* **Scenario A (Language Adherence):** Pass `language="bidi"`.
  * *Success:* The Writer agent generates the text combining Hebrew and English naturally. The Editor agent does not accidentally translate the Hebrew back to English.
* **Scenario B (Tool Isolation):** The Writer agent attempts to search the web for missing information.
  * *Success:* The system denies the execution or raises an error, proving that only the Researcher agent has been granted access to the web-search tool.
* **Scenario C (Length & Depth Enforcement):** The topic is "Agentic AI".
  * *Success:* The prompt instructions effectively force the Writer to expand on sub-topics, generating sufficient tokens to fill approximately 15 pages once typeset, rather than summarizing the topic in a single page.