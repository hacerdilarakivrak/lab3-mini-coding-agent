
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


if __name__ == "__main__":
    unittest.main()
