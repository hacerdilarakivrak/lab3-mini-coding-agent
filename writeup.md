# Lab 3 Writeup: A Mini Coding Agent

## 1. Project Overview

In this lab, I developed a mini coding agent using Python, Ollama, and the `llama3.1:8b` language model.

The goal was to create an agent that can inspect project files, read their contents, and run unit tests through tool calling.

## 2. Agent Loop

The agent receives a user request and sends it to the language model. When the model requests a tool, the agent executes the tool and returns the result to the model.

This process continues until the model produces a final response or the maximum limit of 20 steps is reached.

## 3. Implemented Tools

- **list_files:** Lists files within the project directory.
- **read_file:** Reads the contents of a specified file.
- **run_tests:** Runs Python unit tests after receiving user approval.

## 4. Safety Measures

I implemented several safety controls:

- File access is restricted to the project directory.
- Running unit tests requires explicit user permission.
- The agent loop has a maximum of 20 steps.
- Unknown tool calls are rejected.
- The agent cannot modify project files.

## 5. Testing and Results

I tested the agent using Ollama and the `llama3.1:8b` model.

**File inspection test:** The agent successfully listed project files, read `README.md`, and summarized the project.

**Permission test:** When I denied permission, the agent did not run the tests.

**Initial test execution:** Before adding unit tests, the agent correctly reported that no tests were found.

**Automated unit tests:** I created four tests covering file listing, file reading, project-directory restrictions, and permission handling. All four tests passed.

**Agent-executed tests:** The agent successfully ran the tests with my approval and reported that all four tests passed.

Final result:

```text
Ran 4 tests

OK
```

## 6. Challenges and Observations

During the permission-denied test, the language model incorrectly stated that the `run_tests` tool was unavailable, even though the tool had correctly refused execution.

This showed that tool execution can behave correctly while the language model still misinterprets the result.

I also learned the importance of using the correct project directory when running tests.

## 7. Conclusion

This lab helped me understand how an agent loop works, how language models interact with tools, and why safety controls and testing are important in coding agents.

The final implementation successfully demonstrated tool calling, file inspection, permission-based test execution, and automated unit testing.
