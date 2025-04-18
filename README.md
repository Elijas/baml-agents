# baml‑agents

**12‑Factor AI Agents: BAML‑powered structured generation with plug‑and‑play MCP tools**

```bash
pip install baml‑agents
```

## What you get

- **Robust architecture** – follows the [12‑Factor Agents](https://github.com/humanlayer/12-factor-agents) and the [12-Factor Tools](https://github.com/humanlayer/12-factor-agents/issues?q=author%3Aelijas%20%2312factortools%20sort%3Acreated-asc) principles.
- **Structured generation** – BAML enforces structured outputs.
- **Zero‑friction tools** – Use LLMs to call local (Python) or remote (MCP) tools through a unified interface.

## Getting Started

Explore the `notebooks/` folder for practical examples.

#### Prerequisites to running notebooks

- Have Python 3.10 or later
- Install [uv](https://docs.astral.sh/uv/) CLI
- Run `uv sync --dev` (Installs all dependencies (including dev tools))
- Run `uv run baml-cli generate` (Generates necessary BAML code)

## Design Decisions
**Why wrap tools in the MCP-compatible format?**

Even if your tools are purely internal, wrapping them in MCP offers significant design advantages:

- **Transport‑agnostic integration**  
  MCP typically uses _http/sse_ or _stdio_ for separate‑process communication, but we can also support direct in‑process Python function calls—providing a zero‑overhead, low‑latency integration without the need for external servers.

- **Hot‑swappable deployments**  
  Seamlessly switch between in‑process (inner) and remote (outer) tool implementations without modifying prompts or model code.

- **Framework‑agnostic agents**  
  Easily replace or upgrade your agent core (e.g., switching LLM backends or orchestration frameworks) without rewriting tool interfaces.

- **Cross‑project reuse**  
  Define tools once within an MCP server and reuse them across multiple applications and teams, avoiding redundant logic.

- **Effortless externalization at scale**  
  As your demand grows, migrate tools from local execution to dedicated services or clusters without altering client code or model configurations.

## Frequently Asked Questions
**Q: What is BAML?**

A: BAML ([Boundary Markup Language](https://github.com/BoundaryML/baml)) is a domain-specific language designed for interacting with Large Language Models (LLMs). It allows you to define LLM functions, specify input/output structures (often using types like Pydantic), manage prompts, and configure model parameters in a clear, testable, and version-controlled way. `baml-agents` leverages BAML for its structured generation capabilities.

**Q: What is MCP?**

A: MCP ([Machine Communication Protocol](https://github.com/humanlayer/mcp)) is a specification for standardizing how AI agents or LLMs interact with external tools (also known as functions or capabilities). It defines a common interface, typically using simple text-based protocols like HTTP/SSE or stdio, allowing tools to be developed, deployed, and consumed independently of the specific agent or LLM framework. `baml-agents` uses MCP to provide a flexible and standardized way to integrate tools.

**Q: How do BAML, MCP, and `baml-agents` relate?**

Answer:
- **BAML** is used *within* `baml-agents` to define the agent's core logic and ensure structured interactions with the LLM.
- **MCP** is used by `baml-agents` as the *interface* for calling external tools, promoting decoupling and reusability.
- **`baml-agents`** is the library that *integrates* BAML for generation and MCP for tools, providing a cohesive framework built around the 12-Factor Agent principles.

**Q: Why is `uv` required for running the notebooks? Can I just use `pip`?**

A: You can install the core `baml-agents` library using `pip install baml-agents` for use in your own projects. However, the example notebooks rely on a specific development setup managed by `uv`. We use `uv sync --dev` to install *all* project dependencies (including development tools like linters, formatters, and Jupyter) listed in `pyproject.toml`, ensuring a consistent environment. `uv run` is used to execute scripts defined in `pyproject.toml`, like the `baml-cli generate` step. While you could potentially replicate this setup manually with `pip` and `venv`, using `uv` streamlines the development and example-running process significantly.

**Q: What does the `baml-cli generate` command do?**

A: The BAML CLI (`baml-cli`) reads your `.baml` files (which define your LLM functions, types, and prompts) and generates corresponding Python code. This typically includes type-safe client interfaces, Pydantic models for inputs/outputs, and boilerplate code needed to call the BAML runtime. Running `generate` ensures your Python code is synchronized with your BAML definitions.

**Q: What are the "12-Factor Agent" principles?**

A: They are a set of best practices adapted from the [original 12-Factor App methodology](https://12factor.net/), tailored for building robust, scalable, and maintainable AI agents. Key ideas include managing configuration via the environment, treating backing services (like LLMs or Vector DBs) as attached resources, explicit dependency declaration, stateless processes, and standardized logs. You can read the full specification [here](https://github.com/humanlayer/12-factor-agents).

