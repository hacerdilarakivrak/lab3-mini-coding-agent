# Lab 3 Writeup: A Mini Coding Agent

## 1. Project Overview

In this lab, I developed a mini coding agent using Python, the OpenAI Python client, Ollama, and the `llama3.1:8b` language model.

The main objective was to build a simple coding agent that can inspect project files, read file contents, and run Python unit tests through tool calling while following basic safety restrictions.

To meet the lab requirements, I used Ollama's OpenAI-compatible API to communicate with the local language model. This approach allows the agent to use the OpenAI API format without requiring a paid OpenAI API service.

The project focuses on the essential components of a coding agent: an iterative agent loop, structured tool calling, input validation, user approval, workspace context, and a maximum iteration limit.

## 2. Agent Loop

I implemented the agent loop using the OpenAI-compatible Chat Completions API.

The program connects to a locally running Ollama server through the endpoint `http://localhost:11434/v1` and uses the `llama3.1:8b` model.

When the agent starts, it receives a user request and sends it to the model together with a system message and the definitions of the available tools.

If the model requests a tool, the agent parses the tool arguments from JSON, validates the request, and executes the appropriate Python function.

The result is added to the conversation history using the corresponding tool call ID. The updated conversation is then sent back to the model.

This process continues until the model generates a final response or the maximum limit of 20 iterations is reached.

I set the model temperature to 0.0 to encourage more consistent responses.

## 3. Implemented Coding Tools

I implemented three tools:

- **list_files:** Lists files inside the project directory while excluding selected temporary and environment directories.
- **read_file:** Reads the contents of a specified text file located inside the project directory.
- **run_tests:** Executes Python unit tests using `unittest` after receiving explicit user approval.

Each tool includes a name, description, and parameter schema. These definitions help the language model select the correct tool and provide the required arguments.

The tools are registered using the function-calling format supported by the OpenAI-compatible API.

## 4. Harness Checks and Safety Measures

I implemented several safety checks to prevent invalid or unauthorized tool execution.

**Tool validation:** Only the three predefined tools are accepted. Unknown tool names are rejected.

**Argument validation:** Tool arguments are checked before execution. Missing, invalid, or unexpected arguments are rejected.

**Project-directory restrictions:** File paths are resolved and validated to prevent access outside the project directory.

**User approval:** Before running tests, the agent asks for explicit user permission. If permission is denied, the test command is not executed.

**Execution restrictions:** The agent uses a predefined Python test command instead of allowing arbitrary model-generated shell commands.

**Timeout:** Test execution is limited to 30 seconds.

**Read-only agent tools:** The agent does not provide direct tools for creating, modifying, or deleting project files.

**Maximum iteration limit:** The agent loop is limited to 20 iterations to prevent unlimited execution.

These safety checks are enforced by the Python program rather than relying only on the language model's instructions.

Although the agent does not provide direct file modification tools, running Python tests can execute code with side effects. Therefore, explicit user approval is required before test execution.

## 5. Project Context and Stopping Condition

Before starting the agent loop, the program collects the project file structure using the `list_files` tool.

This information is included in the system message to provide the model with an initial understanding of the workspace.

The system message also instructs the model to use the available tools, avoid inventing file contents or test results, and recognize that direct file modification is not supported.

I configured the agent to stop after a maximum of 20 iterations.

If the model does not finish within this limit, the program stops and displays an appropriate message.

I also implemented an automated test to verify that the agent stops after exactly 20 model calls when the model continues requesting tools.

## 6. Testing and Results

I tested the project using automated unit tests and manual agent execution.

### Automated Unit Testing

I implemented 12 automated unit tests covering the following functionality:

1. Listing project files.
2. Reading project files.
3. Preventing access outside the project directory.
4. Requiring user approval before running tests.
5. Rejecting unknown tools.
6. Rejecting invalid argument types.
7. Rejecting missing required arguments.
8. Rejecting unexpected tool arguments.
9. Rejecting unexpected arguments for `run_tests`.
10. Blocking unsafe file paths through the tool dispatcher.
11. Verifying that the maximum iteration count is 20.
12. Verifying that the agent stops after 20 iterations when the model continues requesting tools.

After updating the project to use the OpenAI-compatible API, I ran the following command:

`python -m unittest discover -v`

The test results were:

```text
Ran 12 tests in 0.020s

OK
```

All 12 automated tests passed successfully.

These tests verified the main safety controls, tool validation, project-directory restrictions, user approval requirements, and maximum iteration limit.

The 20-iteration test used a mocked model response to simulate repeated tool requests. This allowed me to verify the stopping condition without requiring a running Ollama server.

### Manual Agent Testing

After completing the API migration, I performed a manual test using the `llama3.1:8b` model.

I started the agent using:

`python mini_coding_agent.py`

I then entered the following request:

`List the project files, read README.md, and briefly summarize the project.`

The agent successfully connected to the local Ollama model through the OpenAI-compatible API.

During execution, the agent called the `list_files` tool to identify the project files and used the `read_file` tool to inspect the project documentation.

The agent generated a summary describing the project's purpose, implemented tools, and safety controls.

The task was completed in two iterations without errors.

This confirmed that the OpenAI-compatible API connection, tool calling, conversation history, and final response generation worked during actual model execution.

The `run_tests` tool's permission checks were verified through automated tests. A separate live-model test of this tool was not performed after the API migration.

## 7. Challenges and Observations

One challenge was ensuring that the implementation explicitly satisfied the OpenAI-compatible API requirement.

The original version used the native Ollama Python library. I later updated the implementation to use the OpenAI Python client with Ollama's OpenAI-compatible endpoint.

This required changes to model response handling, JSON argument parsing, and the format used to return tool results.

I also updated the automated tests to match the new API structure.

Another challenge was ensuring that the agent could not execute unauthorized tools or access files outside the project directory.

I addressed these issues by implementing tool-name validation, argument validation, and project-directory restrictions.

During earlier testing, I also observed that the language model could sometimes misinterpret a tool result, even when the tool itself behaved correctly. This demonstrated the importance of separating actual tool execution from model-generated explanations.

Finally, I learned that testing should verify not only configuration values but also actual program behavior. For this reason, I included a behavioral test confirming that the agent stops after 20 iterations.

These experiences improved my understanding of API compatibility, tool calling, error handling, safety controls, and software testing.

## 8. Comparison with rasbt/mini-coding-agent

I compared my implementation with the reference project [rasbt/mini-coding-agent](https://github.com/rasbt/mini-coding-agent).

### Similarities

Both projects use Python and language models to implement coding agents.

Both follow an iterative agent loop in which the model requests tools and receives their results.

Both include workspace context, tool handling, safety checks, and execution limits.

### Differences

My implementation is intentionally smaller and focuses on three tools: `list_files`, `read_file`, and `run_tests`.

It uses the `llama3.1:8b` model through Ollama's OpenAI-compatible API and has a fixed maximum of 20 iterations.

The reference project provides a more advanced coding-agent environment with additional capabilities such as context management, persistent transcripts, session memory, session recovery, and delegation to subagents.

The reference implementation also supports file modification and shell operations with configurable approval modes.

In contrast, my agent does not provide direct file modification tools and requires explicit approval before executing Python unit tests.

Another difference is the model interaction format. My implementation uses structured function calls through the OpenAI-compatible Chat Completions API, while the reference project documents a prompt-based format using `<tool>` and `<final>` tags.

### What I Learned from the Comparison

This comparison helped me understand the difference between a minimal educational coding agent and a more advanced coding-agent harness.

My implementation demonstrates the fundamental concepts required for this lab while keeping the code relatively simple and easy to understand.

The reference project demonstrates possible future improvements, including persistent memory, session recovery, context reduction, configurable permissions, and delegation.

These additional capabilities could make the agent more useful for larger projects, but they are outside the scope of my current implementation.

## 9. Conclusion

In this lab, I developed a mini coding agent using Python, Ollama, the OpenAI Python client, and the `llama3.1:8b` language model.

I implemented an iterative agent loop, three coding tools, argument validation, project-directory restrictions, user approval, workspace context, and a maximum limit of 20 iterations.

I also learned how to use an OpenAI-compatible API to communicate with a locally running language model.

After updating the implementation, I ran 12 automated unit tests, and all of them passed successfully.

I also tested the agent manually. It successfully listed project files, read project documentation, and generated a summary in two iterations.

Comparing my implementation with `rasbt/mini-coding-agent` helped me understand how a simple coding agent can be extended with more advanced features.

Overall, this lab improved my understanding of agent architecture, tool calling, API compatibility, safety checks, testing, and the practical limitations of language-model-based coding agents.
