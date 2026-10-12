# Lab 3 Writeup: A Mini Coding Agent

## 1. Project Overview

In this lab, I developed a mini coding agent using Python, Ollama, the OpenAI-compatible API, and the `llama3.1:8b` language model.

The goal was to build a simple agent that can inspect project files, read their contents, and run Python unit tests through tool calling while following basic safety restrictions.

The implementation focuses on the essential components of a coding agent: an agent loop, structured tool calling, input validation, user approval, project context, and a maximum step limit.

I used the OpenAI Python client to communicate with the locally running Ollama server through its OpenAI-compatible API. This allows the agent to use a local language model without requiring a paid OpenAI API service.

## 2. Agent Loop

The agent receives a user request and sends it to the language model together with a system message containing project information and tool instructions.

I implemented the agent loop using the OpenAI-compatible Chat Completions API. The program connects to the local Ollama server using the endpoint `http://localhost:11434/v1` and the `llama3.1:8b` model.

The model receives the conversation history and the definitions of the available tools.

When the model requests a tool, the agent identifies the tool, parses its JSON arguments, validates the request, and executes the appropriate operation.

The tool result is then added to the conversation history using the corresponding tool call ID. The updated conversation is sent back to the model so it can continue processing the user's request.

This process repeats until the model produces a final response or the maximum limit of 20 iterations is reached.

I set the model temperature to 0.0 to encourage more consistent responses.

## 3. Implemented Coding Tools

I implemented three tools:

- **list_files:** Lists files within the project directory, excluding selected temporary and environment directories.
- **read_file:** Reads the contents of a specified text file inside the project directory.
- **run_tests:** Runs Python unit tests using `unittest` after receiving explicit user approval.

Each tool has a name, description, and parameter schema so the language model can select the appropriate operation.

The tools are provided to the model using the function-calling format supported by the OpenAI-compatible API.

## 4. Harness Checks and Safety Measures

I implemented several safety controls to prevent invalid or unauthorized tool execution.

**Tool validation:** Only the three defined tools are accepted. Unknown tool names are rejected.

**Argument validation:** Tool arguments must have the expected structure and types. Missing, invalid, or unexpected arguments are rejected.

**Project-directory restrictions:** File paths are resolved and checked to ensure that the agent cannot read files outside the project directory.

**Test execution approval:** Before running tests, the agent asks for explicit user permission. If permission is denied, the test command is not executed.

**Execution restrictions:** The test command uses a predefined argument list rather than arbitrary model-generated shell commands.

**Timeout:** Test execution has a 30-second timeout.

**Read-only agent tools:** The agent does not provide direct tools for creating, editing, or deleting project files.

**Step limit:** The
