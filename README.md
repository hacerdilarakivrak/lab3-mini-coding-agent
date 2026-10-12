# Lab 3: A Mini Coding Agent

## Project Overview

This project implements a mini coding agent using Python, Ollama, and the `llama3.1:8b` language model.

The agent can inspect project files, read file contents, and run unit tests with user approval. It uses an agent loop with a maximum of 20 steps.

## Tools

- **list_files:** Lists files within the project directory.
- **read_file:** Reads the contents of a specified project file.
- **run_tests:** Runs unit tests after requesting user approval.

## Safety Features

- File access is restricted to the project directory.
- Running tests requires explicit user approval.
- The agent loop is limited to 20 steps.
- Unknown tool calls are rejected.
- The agent cannot modify project files.

## How to Run

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Make sure Ollama is running and the `llama3.1:8b` model is installed.

Start the agent:

```bash
python mini_coding_agent.py
```

Run unit tests directly:

```bash
python -m unittest discover -v
```

## Testing and Results

**Test 1 — File Inspection**

The agent successfully called `list_files` and `read_file`, listed the project files, read `README.md`, and summarized the project.

**Test 2 — Permission Denied**

When the user entered `no`, the `run_tests` tool correctly refused to execute tests. However, the language model incorrectly described the tool as unavailable.

**Test 3 — Permission Granted Before Adding Tests**

The agent executed the test command after user approval. It reported that no tests were found.

**Test 4 — Unit Tests**

Four automated unit tests passed:

- File listing
- File reading
- Blocking access outside the project
- Rejecting test execution without approval

**Test 5 — Agent-Executed Tests**

The agent called `run_tests` after receiving user approval and correctly reported:

```text
Ran 4 tests
OK
```

Exit code: `0`. No test failures.

## Conclusion

The mini coding agent successfully demonstrates an agent loop, tool calling, file inspection, unit testing, and basic safety controls. The tests also show that a language model can occasionally misinterpret a tool result, even when the tool itself behaves correctly.
