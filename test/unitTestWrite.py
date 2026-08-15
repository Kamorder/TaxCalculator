import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from write.writeToFile import addPrev, save, load, loadOrDefault, writeAllData, startTaxProcess, collatedataintosheet
from csvReader.csvClass import csvRow


class TestAddPrev(unittest.TestCase):
    def test_inserts_at_front(self):
        lst = []
        addPrev(lst, "first")
        self.assertEqual(lst[0], "first")

    def test_newest_item_is_always_first(self):
        lst = []
        addPrev(lst, "old")
        addPrev(lst, "new")
        self.assertEqual(lst[0], "new")

    def test_caps_list_at_five(self):
        lst = []
        for i in range(6):
            addPrev(lst, f"item{i}")
        self.assertEqual(len(lst), 5)

    def test_oldest_item_dropped_when_over_five(self):
        lst = []
        for i in range(6):
            addPrev(lst, f"item{i}")
        self.assertNotIn("item0", lst)

    def test_does_not_exceed_five_after_many_inserts(self):
        lst = []
        for i in range(20):
            addPrev(lst, i)
        self.assertEqual(len(lst), 5)


class TestSaveLoad(unittest.TestCase):
    def test_dict_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data"
            data = {"AMAZON": "amazon", "GAS": "gas"}
            save(data, path)
            result = load(path)
        self.assertEqual(result, data)

    def test_list_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "prev5"
            items = ["item1", "item2"]
            save(items, path)
            result = load(path)
        self.assertEqual(result, items)

    def test_saves_with_pkl_extension(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data"
            save({"key": "val"}, path)
            self.assertTrue((path.with_suffix(".pkl")).exists())

    def test_csvrow_object_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "row"
            row = csvRow("VISA", "01/01/2023", "AMAZON", "AMAZON", 45.99)
            save(row, path)
            result = load(path)
        self.assertEqual(result.card, "VISA")
        self.assertAlmostEqual(result.cost, 45.99)

    def test_save_is_atomic_no_tmp_leftover(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data"
            save({"key": "val"}, path)
            self.assertFalse(path.with_suffix(".pkl.tmp").exists())

    def test_save_overwrites_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data"
            save({"v": 1}, path)
            save({"v": 2}, path)
            self.assertEqual(load(path), {"v": 2})


class TestLoadOrDefault(unittest.TestCase):
    def test_returns_default_when_file_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = loadOrDefault(Path(tmp), "nonexistent", {"default": True})
        self.assertEqual(result, {"default": True})

    def test_returns_default_for_empty_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = loadOrDefault(Path(tmp), "missing", [])
        self.assertEqual(result, [])

    def test_loads_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            save({"saved": True}, path / "myfile")
            result = loadOrDefault(path, "myfile", {})
        self.assertEqual(result, {"saved": True})

    def test_does_not_use_default_when_file_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            save({"real": "data"}, path / "myfile")
            result = loadOrDefault(path, "myfile", {"default": "data"})
        self.assertNotEqual(result, {"default": "data"})

    def test_corrupt_pickle_returns_default_and_quarantines(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            bad = path / "bad.pkl"
            bad.write_bytes(b"not a pickle")
            result = loadOrDefault(path, "bad", {"fallback": True})
            self.assertEqual(result, {"fallback": True})
            self.assertFalse(bad.exists())
            quarantined = list(path.glob("bad.pkl.corrupt-*"))
            self.assertEqual(len(quarantined), 1)

    def test_truncated_pickle_returns_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            (path / "truncated.pkl").write_bytes(b"")
            result = loadOrDefault(path, "truncated", [])
            self.assertEqual(result, [])


class TestWriteAllData(unittest.TestCase):
    def _run(self, write_dict):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.txt"
            with open(path, "w") as f:
                writeAllData(f, write_dict)
            return path.read_text()

    def test_headers_are_uppercased(self):
        content = self._run({"gas": [30.0]})
        self.assertIn("GAS", content)

    def test_costs_written_per_line(self):
        content = self._run({"gas": [30.0, 45.0]})
        self.assertIn("30.0", content)
        self.assertIn("45.0", content)

    def test_multiple_categories_written(self):
        content = self._run({"gas": [30.0], "food": [12.5]})
        self.assertIn("GAS", content)
        self.assertIn("FOOD", content)

    def test_empty_category_writes_header(self):
        content = self._run({"gas": []})
        self.assertIn("GAS", content)

    def test_empty_dict_writes_nothing(self):
        content = self._run({})
        self.assertEqual(content.strip(), "")


class TestStartTaxProcess(unittest.TestCase):
    def _run(self, rows, input_values, initial_parsedMap=None):
        """Run startTaxProcess with mocked csvGenerator, input, save, and loadOrDefault."""
        saved = {}

        def fake_save(obj, path):
            saved[path.stem] = obj

        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "packaged").mkdir()
            (directory / "raw").mkdir()

            with patch("write.writeToFile.csvGenerator", return_value=iter(rows)), \
                 patch("write.writeToFile.loadOrDefault", side_effect=[initial_parsedMap or {}, {}, []]), \
                 patch("write.writeToFile.save", side_effect=fake_save), \
                 patch("write.writeToFile.collatedataintosheet", return_value={}), \
                 patch("builtins.input", side_effect=input_values):
                startTaxProcess(directory, "raw/out.txt")

        return saved

    def test_new_item_gets_categorized(self):
        row = csvRow("VISA", "01/01/2023", "AMAZON.COM", "AMAZONCOM", 45.99)
        saved = self._run([row], ["amazon"])
        self.assertEqual(saved["parsedMap"]["AMAZONCOM"], "amazon")

    def test_known_item_skipped_without_prompting_input(self):
        row = csvRow("VISA", "01/01/2023", "AMAZON.COM", "AMAZONCOM", 45.99)
        with patch("builtins.input") as mock_input:
            self._run([row], [], initial_parsedMap={"AMAZONCOM": "amazon"})
            mock_input.assert_not_called()

    def test_skip_category_saved_as_skip(self):
        row = csvRow("VISA", "01/01/2023", "PERSONAL", "PERSONAL", 10.00)
        saved = self._run([row], ["skip"])
        self.assertEqual(saved["parsedMap"]["PERSONAL"], "skip")

    def test_state_always_saved_even_on_exception(self):
        row = csvRow("VISA", "01/01/2023", "AMAZON", "AMAZON", 45.99)
        saved = self._run([row], ["amazon"])
        self.assertIn("parsedMap", saved)
        self.assertIn("prev5", saved)

    def test_prev5_updated_after_categorization(self):
        row = csvRow("VISA", "01/01/2023", "AMAZON.COM", "AMAZONCOM", 45.99)
        saved = self._run([row], ["amazon"])
        self.assertIn(row, saved["prev5"])

    def test_multiple_items_all_categorized(self):
        rows = [
            csvRow("VISA", "01/01/2023", "AMAZON", "AMAZON", 45.99),
            csvRow("VISA", "01/02/2023", "GAS", "GAS", 30.00),
        ]
        saved = self._run(rows, ["amazon", "gas"])
        self.assertEqual(saved["parsedMap"]["AMAZON"], "amazon")
        self.assertEqual(saved["parsedMap"]["GAS"], "gas")

    def test_already_known_items_not_re_added_to_parsedmap(self):
        row = csvRow("VISA", "01/01/2023", "AMAZON", "AMAZON", 45.99)
        saved = self._run([row], [], initial_parsedMap={"AMAZON": "amazon"})
        self.assertEqual(saved["parsedMap"]["AMAZON"], "amazon")


class TestCollatedataintosheet(unittest.TestCase):
    def _run(self, rows, parsedMap, allCategories):
        with patch("write.writeToFile.csvGenerator", return_value=iter(rows)):
            return collatedataintosheet(parsedMap, allCategories)

    def test_costs_grouped_by_category(self):
        rows = [
            csvRow("VISA", "01/01/2023", "AMAZON", "AMAZON", 45.99),
            csvRow("VISA", "01/02/2023", "GAS", "GAS", 30.00),
        ]
        result = self._run(rows, {"AMAZON": "amazon", "GAS": "gas"}, {0: "amazon", 1: "gas"})
        self.assertAlmostEqual(sum(result["amazon"]), 45.99)
        self.assertAlmostEqual(sum(result["gas"]), 30.00)

    def test_skip_items_excluded_from_costs(self):
        rows = [csvRow("VISA", "01/01/2023", "PERSONAL", "PERSONAL", 100.00)]
        result = self._run(rows, {"PERSONAL": "skip"}, {0: "skip"})
        self.assertEqual(result.get("skip", []), [])

    def test_all_categories_present_as_keys(self):
        result = self._run([], {}, {0: "gas", 1: "food"})
        self.assertIn("gas", result)
        self.assertIn("food", result)

    def test_category_missing_from_allCategories_still_reported(self):
        """Resuming a company whose allCategories.pkl is absent or stale must not
        KeyError - parsedMap is the source of truth for what a vendor maps to."""
        rows = [
            csvRow("VISA", "01/01/2023", "SHELL OIL", "SHELLOIL", 40.00),
            csvRow("VISA", "01/02/2023", "SHELL OIL 2", "SHELLOIL", 25.25),
            csvRow("VISA", "01/03/2023", "ACME", "ACME", 12.50),
        ]
        result = self._run(rows, {"SHELLOIL": "gas", "ACME": "widgets"}, {})
        self.assertAlmostEqual(sum(result["gas"]), 65.25)
        self.assertAlmostEqual(sum(result["widgets"]), 12.50)

    def test_skip_still_excluded_when_allCategories_empty(self):
        rows = [csvRow("VISA", "01/01/2023", "PERSONAL", "PERSONAL", 100.00)]
        result = self._run(rows, {"PERSONAL": "skip"}, {})
        self.assertNotIn("skip", result)

    def test_multiple_costs_same_category(self):
        rows = [
            csvRow("VISA", "01/01/2023", "SHELL", "SHELL", 30.00),
            csvRow("VISA", "01/02/2023", "BP", "BP", 40.00),
        ]
        parsedMap = {"SHELL": "gas", "BP": "gas"}
        result = self._run(rows, parsedMap, {0: "gas"})
        self.assertEqual(len(result["gas"]), 2)
        self.assertAlmostEqual(sum(result["gas"]), 70.00)

    def test_empty_rows_returns_empty_cost_lists(self):
        result = self._run([], {}, {0: "gas"})
        self.assertEqual(result["gas"], [])


if __name__ == "__main__":
    unittest.main()
