
import json
import os
import subprocess
from pathlib import Path
from ollama import chat

MODEL = "llama3.1:8b"
PROJECT_ROOT = Path(__file__).resolve().parent
MAX_STEPS = 20


def safe_path(filename):
    path = (PROJECT_ROOT / filename).resolve()
    if not path.is_relative_to(PROJECT_ROOT):
        raise ValueError("Access outside the project is forbidden.")
    return path


def list_files():
    files = []
    for root, dirs, names in os.walk(PROJECT_ROOT):
        dirs[:] = [
            d for d in dirs
            if d not in {".git", "__pycache__", ".venv", "venv"}
            and not (Path(root) / d).is_symlink()
        ]
        for name in names:
            path = Path(root) / name
            if path.is_file() and not path.is_symlink():
                files.append(str(path.relative_to(PROJECT_ROOT)))
    return json.dumps(files[:100])


def read_file(filename):
    path = safe_path(filename)
    if not path.is_file():
        return "File not found."
    if path.stat().st_size > 100_000:
        return "File too large."
    return path.read_text(encoding="utf-8")


def run_tests():
    approval = input("Allow running tests? (yes/no): ")
    if approval.strip().lower() != "yes":
        return "Test execution denied by user."

    try:
        result = subprocess.run(
            ["python", "-m", "unittest", "discover"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            shell=False,
        )
        return (
            f"Exit code: {result.returncode}\n"
            + (result.stdout + result.stderr)[-5000:]
        )
    except subprocess.TimeoutExpired:
        return "Tests timed out."


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files inside the project directory.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a text file inside the project directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Relative path of the file to read.",
                    }
                },
                "required": ["filename"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_tests",
            "description": "Run project unit tests after user approval.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]


def execute_tool(name, arguments):
    if not isinstance(arguments, dict):
        return "Invalid tool arguments."

    try:
        if name == "list_files":
            if arguments:
                return "Unexpected arguments."
            return list_files()

        if name == "read_file":
            if set(arguments) != {"filename"}:
                return "Invalid read_file arguments."
            filename = arguments["filename"]
            if not isinstance(filename, str):
                return "Filename must be a string."
            return read_file(filename)

        if name == "run_tests":
            if arguments:
                return "Unexpected arguments."
            return run_tests()

        return "Unknown tool. Execution denied."

    except (ValueError, OSError, UnicodeError) as error:
        return f"Tool error: {error}"


def main():
    print("Mini Coding Agent")
    print("Project:", PROJECT_ROOT)

    question = input("What should the agent do? ")

    structure = list_files()

    messages = [
        {
            "role": "system",
            "content": (
                "You are a mini coding agent. "
                "Use tools to inspect the project and run tests. "
                "Never invent file contents or test results. "
                "Use only the three provided tools. "
                "You cannot modify files. "
                "Project structure:\n" + structure
            ),
        },
        {"role": "user", "content": question},
    ]

    for step in range(MAX_STEPS):
        print(f"\nStep {step + 1}/{MAX_STEPS}")

        response = chat(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            options={"temperature": 0.0},
        )

        messages.append(response.message)

        calls = response.message.tool_calls or []

        if not calls:
            print("\nAgent:", response.message.content)
            return

        for call in calls:
            name = call.function.name
            arguments = call.function.arguments
            print("Tool:", name)

            result = execute_tool(name, arguments)

            messages.append({
                "role": "tool",
                "tool_name": name,
                "content": result,
            })

            print("Result:", result[:500])

    print("Stopped: maximum 20 steps reached.")


if __name__ == "__main__":
    main()
