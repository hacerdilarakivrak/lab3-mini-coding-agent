# Lab 3 Writeup: A Mini Coding Agent

## 1. Project Overview

In this lab, I developed a mini coding agent using Python, Ollama, and the `llama3.1:8b` language model.

The goal was to build a simple agent that can inspect project files, read their contents, and run Python unit tests through tool calling while following basic safety restrictions.

The implementation focuses on the essential components of a coding agent: an agent loop, structured tools, input validation, user approval, project context, and a maximum step limit.

## 2. Agent Loop

The agent receives a user request and sends it to the language model together with a system message containing project information and tool instructions.

When the model requests a tool, the agent identifies the tool, validates its arguments, executes the requested operation, and adds the result to the conversation history.

The updated conversation is then sent back to the model. This process continues until the model produces a final response or the maximum limit of 20 steps is reached.

The agent uses Ollama's structured tool-calling interface and sets the model temperature to 0.0 for more consistent responses.

## 3. Implemented Coding Tools

I implemented three tools:

- **list_files:** Lists files within the project directory, excluding selected temporary and environment directories.
- **read_file:** Reads the contents of a specified text file inside the project directory.
- **run_tests:** Runs Python unit tests using `unittest` after receiving explicit user approval.

Each tool has a name, description, and parameter schema so the language model can select the appropriate operation.

## 4. Harness Checks and Safety Measures

I implemented several safety controls to prevent invalid or unauthorized tool execution.

**Tool validation:** Only the three defined tools are accepted. Unknown tool names are rejected.

**Argument validation:** Tool arguments must have the expected structure and types. Missing, invalid, or unexpected arguments are rejected.

**Project-directory restrictions:** File paths are resolved and checked to ensure that the agent cannot read files outside the project directory.

**Test execution approval:** Before running tests, the agent asks for explicit user permission. If permission is denied, the test command is not executed.

**Execution restrictions:** The test command uses a predefined argument list rather than arbitrary model-generated shell commands.

**Timeout:** Test execution has a 30-second timeout.

**Read-only behavior:** The agent does not provide tools for creating, editing, or deleting project files.

**Step limit:** The agent loop is limited to 20 iterations to prevent unlimited execution.

These checks are implemented in the Python program rather than relying only on instructions given to the language model.

## 5. Project Context and Stopping Condition

Before starting the agent loop, the program collects the project file structure using `list_files`.

This information is included in the system message so the model has an initial understanding of the workspace.

The system message also instructs the model to use the available tools, avoid inventing file contents or test results, and recognize that file modification is not supported.

The agent uses a maximum of 20 loop iterations. If the model does not finish within this limit, the program stops and displays a message explaining that the maximum number of steps has been reached.

## 6. Testing and Results

I tested the agent using Ollama and the `llama3.1:8b` language model.

### Manual Agent Testing

**File inspection test:** The agent successfully listed project files, read `README.md`, and summarized the project.

**Permission-denied test:** When I denied permission to run tests, the program did not execute the test command.

**Initial test execution:** Before adding unit tests, the agent correctly reported that no tests were found.

**Agent-executed tests:** After I approved test execution, the agent ran the initial four unit tests and reported that all four passed.

### Automated Unit Testing

I later expanded the automated test suite to include 11 tests covering:

1. Listing project files.
2. Reading project files.
3. Blocking access outside the project directory.
4. Requiring approval before running tests.
5. Rejecting unknown tools.
6. Rejecting invalid argument types.
7. Rejecting missing required arguments.
8. Rejecting unexpected tool arguments.
9. Rejecting unexpected arguments for `run_tests`.
10. Blocking unsafe file paths through the tool dispatcher.
11. Verifying that the configured maximum step count is 20.

I ran the following command:

`python -m unittest discover -v`

The final result was:

```
Ran 11 tests in 0.010s

OK
```

All 11 automated tests passed successfully.

The step-limit test checks the configured value of 20. It does not independently simulate a complete 20-step model conversation.

## 7. Challenges and Observations

During the permission-denied test, the language model incorrectly stated that the `run_tests` tool was unavailable, even though the tool had correctly refused execution.

This demonstrated that tool execution can behave correctly while the language model still misinterprets the result.

I also encountered a testing issue because an older downloaded project folder contained only four tests. After downloading the updated project files and running the tests from the correct directory, all 11 tests were discovered and passed.

These experiences helped me understand the importance of separating tool execution from model-generated explanations and verifying that tests run against the latest version of the code.

## 8. Comparison with rasbt/mini-coding-agent

I compared my implementation with the reference project [rasbt/mini-coding-agent](https://github.com/rasbt/mini-coding-agent).

### Similarities

Both projects use Python and Ollama to implement a local coding agent.

Both use an iterative agent loop in which the language model requests tools and receives their results.

Both include workspace context, structured tool handling, input validation, permission controls, and limits on agent execution.

### Differences

My implementation is intentionally smaller and focuses on three tools: `list_files`, `read_file`, and `run_tests`.

It uses the `llama3.1:8b` model, Ollama's structured tool-calling interface, and a fixed maximum of 20 iterations.

The reference project provides a more comprehensive coding-agent environment. According to its documentation, it supports additional workspace information, context management, persistent transcripts, session memory, session recovery, and bounded delegation to subagents.

The reference implementation also supports file modifications and shell operations with configurable approval modes. My agent does not modify files and requires explicit user approval before running tests.

Another difference is the model interaction format. My implementation uses structured tool calls from the Ollama Python library, while the reference project documents a prompt-based format using `<tool>` and `<final>` tags.

### What I Learned from the Comparison

This comparison showed me the difference between a minimal educational coding agent and a more feature-rich coding-agent harness.

My implementation demonstrates the main concepts required for this lab while keeping the code relatively simple and easy to understand.

The reference project demonstrates possible future improvements, including persistent memory, session recovery, context reduction, configurable permissions, and delegation.

These additional features are useful for more advanced coding agents but are outside the scope of my current implementation.

## 9. Conclusion

In this lab, I learned how a language model can interact with programming tools through an iterative agent loop.

I implemented file inspection, controlled test execution, argument validation, project-directory restrictions, user approval, workspace context, and a maximum step limit.

The agent was tested manually with Ollama, and all 11 automated unit tests passed.

Comparing my project with `rasbt/mini-coding-agent` also helped me understand how a simple agent can be extended into a more advanced system.

Overall, this lab improved my understanding of tool calling, agent architecture, safety checks, testing, and the practical limitations of language-model-based coding agents.
