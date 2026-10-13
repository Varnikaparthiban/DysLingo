import unittest
from utils.text_processing import analyze_reading

class TextProcessingTests(unittest.TestCase):
    def test_identical_text_has_full_match(self):
        result = analyze_reading("The cat sat", "The cat sat")
        self.assertEqual(result["accuracy"], 100.0)
        self.assertEqual(result["errors"], 0)

    def test_empty_target_is_handled(self):
        result = analyze_reading("", "hello")
        self.assertEqual(result["accuracy"], 0)
        self.assertIn("feedback", result)

if __name__ == "__main__":
    unittest.main()
