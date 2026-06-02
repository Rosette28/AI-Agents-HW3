# Mechanism PRD: API Gatekeeper & Rate Limiting Engine

## 1. Description & Background
In a multi-agent system, autonomous agents can rapidly fire dozens of network requests to external Large Language Model (LLM) APIs and search tools. Without a centralized throttle, the system will inevitably hit HTTP 429 (Too Many Requests) errors, leading to crashed executions and lost context. 
The `ApiGatekeeper` is a mandatory core mechanism that intercepts all outgoing network requests, checks them against predefined service limits (e.g., Requests Per Minute/Hour), and transparently queues them using backpressure if limits are nearing exhaustion.

## 2. Expected Inputs and Outputs
* **Input:** A callable API request function, its payload/arguments, and the target service identifier (e.g., `service="openai"`, `service="serper"`).
* **Output:** Upon execution, it returns the exact expected response object (e.g., JSON dictionary or string) from the target API, behaving completely transparently to the calling agent.
* **Configuration Input:** Reads bounds dynamically from `config/rate_limits.json` (RPM, RPH, concurrent limits, and max retries).

## 3. Constraints, Alternatives, and Rationale (ADR)
* **Constraint:** Must not contain any hardcoded limits or API keys. Must operate synchronously or via `asyncio` without blocking the main thread indefinitely without logging.
* **Alternative 1: Fail Fast & Retry.** Let the request fail with a 429 error and use a basic `try/except` loop with `time.sleep()`. *Rejected* because it wastes network bandwidth and risks IP bans.
* **Alternative 2: Priority Queue.** Sort incoming requests by agent importance (e.g., Editor gets priority over Researcher). *Rejected* as it adds unnecessary complexity for a sequential process.
* **Selected Architecture: FIFO Wait Queue with Backpressure.** All requests enter a First-In-First-Out queue. If the RPM limit is at 95% capacity, the Gatekeeper pauses execution, logs a "Backpressure Triggered" warning, and waits until the rate limit window resets before firing the next request.

## 4. Test Scenarios & Acceptance Criteria
* **Scenario A (Limit Breach Simulation):** Mock the RPM limit to `3`. Send 5 simultaneous tool requests.
  * *Success:* The first 3 execute immediately. The final 2 are queued, wait for the timeout period, and then execute successfully without raising exceptions.
* **Scenario B (Transient Failure):** Mock an external API to return HTTP 500/502 twice, then succeed on the third try.
  * *Success:* The Gatekeeper intercepts the errors, triggers its retry logic, and returns the successful payload on attempt 3.
* **Scenario C (Max Retries Exceeded):** Mock an external API to return HTTP 403 (Unauthorized).
  * *Success:* The Gatekeeper attempts up to `max_retries`, then gracefully fails, raising a custom `GatekeeperExhaustionError` that the SDK can catch to shut down the pipeline safely.