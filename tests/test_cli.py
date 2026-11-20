from __future__ import annotations

import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

from classtimer.cli import main


class CliTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.output = os.path.join(self._tmp.name, "timer.html")

    def run_cli(self, args):
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(args)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_generate(self) -> None:
        code, output, _ = self.run_cli(["-o", self.output])
        self.assertEqual(code, 0)
        self.assertTrue(os.path.exists(self.output))
        self.assertIn("1、3、5、10", output)
        with open(self.output, encoding="utf-8") as handle:
            content = handle.read()
        self.assertIn('data-seconds="300"', content)

    def test_custom_presets(self) -> None:
        code, output, _ = self.run_cli(
            ["-o", self.output, "--presets", "2,4", "--title", "英语课"]
        )
        self.assertEqual(code, 0)
        self.assertIn("2、4", output)
        with open(self.output, encoding="utf-8") as handle:
            content = handle.read()
        self.assertIn("英语课", content)
        self.assertIn('data-seconds="240"', content)

    def test_invalid_presets(self) -> None:
        code, _, stderr = self.run_cli(["-o", self.output, "--presets", "0"])
        self.assertEqual(code, 2)
        self.assertIn("大于 0", stderr)

    def test_empty_title(self) -> None:
        code, _, stderr = self.run_cli(["-o", self.output, "--title", " "])
        self.assertEqual(code, 2)
        self.assertIn("标题", stderr)

    def test_write_failure(self) -> None:
        bad = os.path.join(self._tmp.name, "missing", "timer.html")
        code, _, stderr = self.run_cli(["-o", bad])
        self.assertEqual(code, 1)
        self.assertIn("写入文件失败", stderr)


if __name__ == "__main__":
    unittest.main()
