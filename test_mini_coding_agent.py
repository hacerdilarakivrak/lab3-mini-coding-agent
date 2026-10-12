
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import mini_coding_agent as agent


class TestMiniCodingAgent(unittest.TestCase):

    def test_list_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "example.txt").write_text("Hello", encoding="utf-8")

            with patch.object(agent, "PROJECT_ROOT", root):
                result = agent.list_files()

            self.assertIn("example.txt", result)

    def test_read_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "example.txt").write_text("Hello", encoding="utf-8")

            with patch.object(agent, "PROJECT_ROOT", root):
                result = agent.read_file("example.txt")

            self.assertEqual(result, "Hello")

    def test_block_access_outside_project(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(agent, "PROJECT_ROOT", Path(directory)):
                with self.assertRaises(ValueError):
                    agent.safe_path("../outside.txt")

    def test_run_tests_requires_approval(self):
        with patch("builtins.input", return_value="no"):
            with patch.object(agent.subprocess, "run") as mock_run:
                result = agent.run_tests()

        self.assertEqual(result, "Test execution denied by user.")
        mock_run.assert_not_called()


    def test_unknown_tool_is_rejected(self):
        result = agent.execute_tool("delete_file", {})
        self.assertEqual(result, "Unknown tool. Execution denied.")

    def test_invalid_tool_arguments_are_rejected(self):
        result = agent.execute_tool("read_file", {"filename": 123})
        self.assertEqual(result, "Filename must be a string.")

    def test_missing_filename_is_rejected(self):
        result = agent.execute_tool("read_file", {})
        self.assertEqual(result, "Invalid read_file arguments.")

    def test_unexpected_arguments_are_rejected(self):
        result = agent.execute_tool("list_files", {"extra": "value"})
        self.assertEqual(result, "Unexpected arguments.")

    def test_run_tests_rejects_unexpected_arguments(self):
        with patch.object(agent, "run_tests") as mock_run:
            result = agent.execute_tool("run_tests", {"command": "anything"})
        self.assertEqual(result, "Unexpected arguments.")
        mock_run.assert_not_called()

    def test_execute_tool_blocks_outside_path(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(agent, "PROJECT_ROOT", Path(directory)):
                result = agent.execute_tool(
                    "read_file", {"filename": "../outside.txt"}
                )
        self.assertIn("Access outside the project is forbidden", result)

    def test_maximum_steps_is_twenty(self):
        self.assertEqual(agent.MAX_STEPS, 20)


if __name__ == "__main__":
    unittest.main()
