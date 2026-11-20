from __future__ import annotations

import unittest

from classtimer.timer import TimerError, parse_presets, render_page


class ParsePresetsTest(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(parse_presets("1,3,5,10"), (1, 3, 5, 10))

    def test_chinese_separators(self) -> None:
        self.assertEqual(parse_presets("1，3、5; 10"), (1, 3, 5, 10))

    def test_deduplicate(self) -> None:
        self.assertEqual(parse_presets("5,1,5,3"), (5, 1, 3))

    def test_empty(self) -> None:
        with self.assertRaises(TimerError):
            parse_presets(" ")

    def test_non_integer(self) -> None:
        with self.assertRaises(TimerError):
            parse_presets("1,abc")

    def test_zero_and_negative(self) -> None:
        with self.assertRaises(TimerError):
            parse_presets("0,5")
        with self.assertRaises(TimerError):
            parse_presets("-1")

    def test_too_long(self) -> None:
        with self.assertRaises(TimerError):
            parse_presets("181")

    def test_too_many(self) -> None:
        with self.assertRaises(TimerError):
            parse_presets("1,2,3,4,5,6,7,8,9,10")


class RenderTest(unittest.TestCase):
    def test_content(self) -> None:
        page = render_page("数学课", (1, 3))
        self.assertIn("数学课", page)
        self.assertIn("05:00", page)
        self.assertIn('data-seconds="60"', page)
        self.assertIn('data-seconds="180"', page)
        self.assertIn("时间到", page)
        self.assertIn("AudioContext", page)
        self.assertIn("setInterval", page)

    def test_self_contained(self) -> None:
        page = render_page()
        self.assertTrue(page.startswith("<!doctype html>"))
        self.assertIn("<style>", page)
        self.assertNotIn("<link", page)
        self.assertNotIn("<script src", page)

    def test_title_escaped(self) -> None:
        page = render_page("<b>计时</b>", (1,))
        self.assertNotIn("<b>计时</b>", page)
        self.assertIn("&lt;b&gt;", page)

    def test_invalid_input(self) -> None:
        with self.assertRaises(TimerError):
            render_page("   ")
        with self.assertRaises(TimerError):
            render_page("计时", ())


if __name__ == "__main__":
    unittest.main()
