# Prompt Book

## Phase 2 - Configuration Parser

### Prompt
Write a Python module to parse JSON configuration files from a config/
directory and safely load environment variables using os.environ.get.

### Result
Implemented:
- load_config()
- ConfigError
- Version validation
- Environment variable loading

### Improvements
- Added version consistency checks
- Added file existence validation

---

## Phase 2 - API Gatekeeper

### Prompt
Write a Python class ApiGatekeeper. It must act as a centralized manager
for all external API calls, check rate limits based on a loaded JSON
config before execution, queue requests if the limit is reached, and
implement retry logic for transient failures.

### Result
Implemented:
- Rate limiting
- Retry mechanism
- Thread-safe locking
- Backpressure handling

### Improvements
- Added cleanup mechanism
- Added request tracking per minute and per hour

---

## Phase 3 - Research Agent

### Prompt
Write Python code using CrewAI to instantiate a Market Research Analyst Agent.

### Result
Implemented researcher agent with:
- Search tool integration
- Structured role and goal
- Research-oriented backstory

---

## Phase 3 - Writer Agent

### Prompt
Write Python code for a CrewAI Senior Technical Writer Agent.

### Result
Implemented:
- Markdown generation
- Language adaptation
- Long-form content generation

---

## Phase 3 - Editor Agent

### Prompt
Write Python code for a CrewAI Senior Editor Agent.

### Result
Implemented:
- Content review
- Formatting validation
- LaTeX readiness verification

---

## Phase 6 - Testing

### Prompt
Write pytest unit tests for ApiGatekeeper and configuration parser.

### Result
Implemented:
- Config parser tests
- Gatekeeper tests
- SDK integration tests

### Improvements
- Achieved 87.43% coverage
- Eliminated warnings