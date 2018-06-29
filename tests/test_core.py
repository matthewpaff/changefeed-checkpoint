import unittest
from copy import deepcopy
from pathlib import Path
from checkpoint_tool.core import evaluate
from checkpoint_tool.fixture_check import check
from checkpoint_tool.generate_fixtures import make_case


class CoreTests(unittest.TestCase):
    def test_explicit_expected_results_for_the_complete_corpus(self):
        self.assertGreater(check(Path(__file__).resolve().parents[1] / "fixtures/cases.jsonl", evaluate), 0)

    def test_supplied_input_is_not_modified(self):
        case = make_case(0)
        original = deepcopy(case["input"])
        self.assertEqual(evaluate(case["input"]), case["expected"])
        self.assertEqual(case["input"], original)

    def test_missing_required_fields_are_rejected(self):
        with self.assertRaises(ValueError):
            evaluate({})

if __name__ == "__main__":
    unittest.main()
