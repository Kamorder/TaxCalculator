import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from tax.tax import taxFormat, duplicateLabel


def make_tax(lines):
    return taxFormat(iter(lines))


class TestTaxFormatGen(unittest.TestCase):
    def test_single_category_sums_costs(self):
        tf = make_tax(["Gas\n", "30.00 45.00\n"])
        tf.formatGen()
        self.assertAlmostEqual(tf.taxHeader["Gas"], 75.00)

    def test_multiple_categories(self):
        tf = make_tax(["Gas\n", "30.00\n", "\n", "Food\n", "12.50\n"])
        tf.formatGen()
        self.assertAlmostEqual(tf.taxHeader["Gas"], 30.00)
        self.assertAlmostEqual(tf.taxHeader["Food"], 12.50)

    def test_blank_lines_ignored(self):
        tf = make_tax(["\n", "\n", "Gas\n", "30.00\n"])
        tf.formatGen()
        self.assertIn("Gas", tf.taxHeader)
        self.assertEqual(len(tf.taxHeader), 1)

    def test_costs_with_commas(self):
        tf = make_tax(["Gas\n", "1,234.56\n"])
        tf.formatGen()
        self.assertAlmostEqual(tf.taxHeader["Gas"], 1234.56)

    def test_multiple_costs_on_one_line(self):
        tf = make_tax(["Gas\n", "10.00 20.00 30.00\n"])
        tf.formatGen()
        self.assertAlmostEqual(tf.taxHeader["Gas"], 60.00)

    def test_costs_accumulate_across_lines(self):
        tf = make_tax(["Gas\n", "10.00\n", "20.00\n"])
        tf.formatGen()
        self.assertAlmostEqual(tf.taxHeader["Gas"], 30.00)

    def test_duplicate_header_stops_and_keeps_first(self):
        tf = make_tax(["Gas\n", "30.00\n", "Food\n", "12.00\n", "Gas\n", "99.00\n"])
        tf.formatGen()
        self.assertAlmostEqual(tf.taxHeader["Gas"], 30.00)
        self.assertAlmostEqual(tf.taxHeader["Food"], 12.00)

    def test_empty_input(self):
        tf = make_tax([])
        tf.formatGen()
        self.assertEqual(tf.taxHeader, {})

    def test_header_whitespace_stripped(self):
        tf = make_tax(["  Gas  \n", "30.00\n"])
        tf.formatGen()
        self.assertIn("Gas", tf.taxHeader)

    def test_cost_line_before_any_header_ignored(self):
        tf = make_tax(["30.00\n", "Gas\n", "10.00\n"])
        tf.formatGen()
        self.assertAlmostEqual(tf.taxHeader["Gas"], 10.00)


class TestTaxFormatWriteInFile(unittest.TestCase):
    def test_writes_formatted_lines(self):
        tf = make_tax(["Gas\n", "30.00\n", "\n", "Food\n", "12.50\n"])
        tf.formatGen()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "output.txt"
            tf.writeInFile(path)
            content = path.read_text()
        self.assertIn("Gas: $30.00", content)
        self.assertIn("Food: $12.50", content)

    def test_creates_file_at_path(self):
        tf = make_tax(["Gas\n", "30.00\n"])
        tf.formatGen()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "output.txt"
            tf.writeInFile(path)
            self.assertTrue(path.exists())

    def test_large_numbers_formatted_with_commas(self):
        tf = make_tax(["Gas\n", "1234567.89\n"])
        tf.formatGen()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "output.txt"
            tf.writeInFile(path)
            content = path.read_text()
        self.assertIn("1,234,567.89", content)


class TestTaxFormatPrintResults(unittest.TestCase):
    def test_prints_each_category(self):
        tf = make_tax(["Gas\n", "30.00\n", "\n", "Food\n", "12.50\n"])
        tf.formatGen()
        with patch("builtins.print") as mock_print:
            tf.printResults()
        printed = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("Gas", printed)
        self.assertIn("Food", printed)


class TestDuplicateLabel(unittest.TestCase):
    def test_str_includes_label_name(self):
        exc = duplicateLabel("Gas")
        self.assertIn("Gas", str(exc))

    def test_is_exception(self):
        self.assertIsInstance(duplicateLabel("Gas"), Exception)


if __name__ == "__main__":
    unittest.main()
