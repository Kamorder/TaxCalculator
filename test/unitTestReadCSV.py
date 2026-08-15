import unittest
import csv
import tempfile
from pathlib import Path

from csvReader.readCSV import (
    parseDescription, parseStarDescription,
    getCSVType, getCSVTypeDebit,
    collateDocuments,
)
from csvReader.csvClass import csvRow, csvDebitRow


class TestParseDescription(unittest.TestCase):
    def test_strips_non_alpha(self):
        self.assertEqual(parseDescription("Amazon.com 123!"), "AMAZONCOM")

    def test_uppercases_result(self):
        self.assertEqual(parseDescription("gas station"), "GASSTATION")

    def test_empty_string(self):
        self.assertEqual(parseDescription(""), "")

    def test_numbers_only(self):
        self.assertEqual(parseDescription("12345"), "")

    def test_special_chars_only(self):
        self.assertEqual(parseDescription("*** --- !!!"), "")

    def test_mixed_case_preserved_as_upper(self):
        self.assertEqual(parseDescription("WalMart"), "WALMART")


class TestParseStarDescription(unittest.TestCase):
    def test_strips_everything_after_star(self):
        self.assertEqual(parseStarDescription("VENDOR*EXTRA INFO 123"), "VENDOR")

    def test_no_star_strips_non_alpha(self):
        self.assertEqual(parseStarDescription("AMAZON.COM"), "AMAZONCOM")

    def test_empty_string(self):
        self.assertEqual(parseStarDescription(""), "")

    def test_star_at_start(self):
        self.assertEqual(parseStarDescription("*EVERYTHING"), "")


class TestGetCSVType(unittest.TestCase):
    # Credit card row: [date, post_date, description, category, type, amount, ...]
    def _row(self, date="01/01/2023", desc="AMAZON.COM 123", amount="-45.99"):
        return [date, "01/02/2023", desc, "Shopping", "Sale", amount]

    def test_card_from_filename(self):
        row = getCSVType(self._row(), "VISA_statement.csv")
        self.assertEqual(row.card, "VISA")

    def test_date_parsed(self):
        row = getCSVType(self._row(date="03/15/2023"), "VISA_statement.csv")
        self.assertEqual(row.date, "03/15/2023")

    def test_description_preserved(self):
        row = getCSVType(self._row(desc="WHOLE FOODS #123"), "VISA_statement.csv")
        self.assertEqual(row.description, "WHOLE FOODS #123")

    def test_parsed_is_alpha_upper(self):
        row = getCSVType(self._row(desc="Amazon.com 123"), "VISA_statement.csv")
        self.assertEqual(row.parsed, "AMAZONCOM")

    def test_cost_is_absolute_value(self):
        row = getCSVType(self._row(amount="-45.99"), "VISA_statement.csv")
        self.assertAlmostEqual(row.cost, 45.99)

    def test_cost_positive_stays_positive(self):
        row = getCSVType(self._row(amount="30.00"), "VISA_statement.csv")
        self.assertAlmostEqual(row.cost, 30.00)

    def test_returns_csvRow_instance(self):
        row = getCSVType(self._row(), "VISA_statement.csv")
        self.assertIsInstance(row, csvRow)


class TestGetCSVTypeDebit(unittest.TestCase):
    # Debit row: [details, date, description, amount, type, balance, ...]
    def _row(self, date="01/15/2023", desc="WALMART SUPERCENTER", amount="55.43"):
        return ["DEBIT", date, desc, amount, "ACH_DEBIT", "1000.00"]

    def test_line_from_filename(self):
        row = getCSVTypeDebit(self._row(), "CHASE_checking.csv")
        self.assertEqual(row.line, "CHASE")

    def test_date_parsed(self):
        row = getCSVTypeDebit(self._row(date="06/20/2023"), "CHASE_checking.csv")
        self.assertEqual(row.date, "06/20/2023")

    def test_description_preserved(self):
        row = getCSVTypeDebit(self._row(desc="COSTCO WHSE #1234"), "CHASE_checking.csv")
        self.assertEqual(row.description, "COSTCO WHSE #1234")

    def test_parsed_is_alpha_upper(self):
        row = getCSVTypeDebit(self._row(desc="Walmart Supercenter"), "CHASE_checking.csv")
        self.assertEqual(row.parsed, "WALMARTSUPERCENTER")

    def test_cost_is_absolute_value(self):
        row = getCSVTypeDebit(self._row(amount="-55.43"), "CHASE_checking.csv")
        self.assertAlmostEqual(row.cost, 55.43)

    def test_returns_csvDebitRow_instance(self):
        row = getCSVTypeDebit(self._row(), "CHASE_checking.csv")
        self.assertIsInstance(row, csvDebitRow)


class TestCsvRowStr(unittest.TestCase):
    def test_str_contains_fields(self):
        row = csvRow("VISA", "01/01/2023", "AMAZON", "AMAZON", 45.99)
        s = str(row)
        self.assertIn("VISA", s)
        self.assertIn("01/01/2023", s)
        self.assertIn("45.99", s)


class TestCsvDebitRowStr(unittest.TestCase):
    def test_str_contains_fields(self):
        row = csvDebitRow("CHASE", "01/15/2023", "WALMART", "WALMART", 55.43)
        s = str(row)
        self.assertIn("CHASE", s)
        self.assertIn("01/15/2023", s)
        self.assertIn("55.43", s)


class TestCollateDocuments(unittest.TestCase):
    def _write_credit_csv(self, path, filename):
        filepath = path / filename
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Transaction Date", "Post Date", "Description", "Category", "Type", "Amount"])
            writer.writerow(["01/01/2023", "01/02/2023", "AMAZON.COM", "Shopping", "Sale", "-45.99"])
            writer.writerow(["01/05/2023", "01/06/2023", "GAS STATION", "Gas", "Sale", "-30.00"])

    def _write_debit_csv(self, path, filename):
        filepath = path / filename
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Details", "Posting Date", "Description", "Amount", "Type", "Balance"])
            writer.writerow(["DEBIT", "01/15/2023", "WALMART", "55.43", "ACH_DEBIT", "1000.00"])

    def test_reads_credit_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._write_credit_csv(Path(tmp), "VISA_statement.csv")
            results = collateDocuments(resource=Path(tmp))
        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], csvRow)

    def test_reads_debit_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._write_debit_csv(Path(tmp), "CHASE_checking.csv")
            results = collateDocuments(resource=Path(tmp))
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], csvDebitRow)

    def test_reads_multiple_csv_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._write_credit_csv(Path(tmp), "VISA_statement.csv")
            self._write_debit_csv(Path(tmp), "CHASE_checking.csv")
            results = collateDocuments(resource=Path(tmp))
        self.assertEqual(len(results), 3)

    def test_ignores_non_csv_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "notes.txt").write_text("ignore me")
            results = collateDocuments(resource=Path(tmp))
        self.assertEqual(results, [])

    def test_empty_directory_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            results = collateDocuments(resource=Path(tmp))
        self.assertEqual(results, [])

    def _write_debit_csv_with_bom(self, path, filename):
        '''Chase exports a checking statement with a UTF-8 BOM on the header.'''
        filepath = path / filename
        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["Details", "Posting Date", "Description", "Amount", "Type", "Balance"])
            writer.writerow(["DEBIT", "12/30/2025", "T-MOBILE", "-85.00", "ACH_DEBIT", "26881.21"])

    def test_bom_header_still_detected_as_debit(self):
        """A BOM must not push a checking statement into the credit parser, which
        would read column 5 (Balance) as the cost instead of column 3 (Amount)."""
        with tempfile.TemporaryDirectory() as tmp:
            self._write_debit_csv_with_bom(Path(tmp), "Chase3890_checking.csv")
            results = collateDocuments(resource=Path(tmp))
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], csvDebitRow)
        self.assertAlmostEqual(results[0].cost, 85.00)
        self.assertEqual(results[0].date, "12/30/2025")

    def test_cost_values_are_correct(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._write_credit_csv(Path(tmp), "VISA_statement.csv")
            results = collateDocuments(resource=Path(tmp))
        costs = {r.description: r.cost for r in results}
        self.assertAlmostEqual(costs["AMAZON.COM"], 45.99)
        self.assertAlmostEqual(costs["GAS STATION"], 30.00)


if __name__ == "__main__":
    unittest.main()
