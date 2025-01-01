import unittest
from codesleuth.complexity import analyze_complexity, generate_complexity_report

class TestComplexity(unittest.TestCase):
    def test_analyze_complexity(self):
        # Test complexity analysis for a simple function
        file_content = "def simple_function():\n    return 42\n"
        with open("temp_test_file.py", "w") as f:
            f.write(file_content)
        
        results = analyze_complexity("temp_test_file.py")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['function'], "simple_function")
        self.assertEqual(results[0]['complexity'], 1)

    def test_generate_complexity_report(self):
        # Test generating a report for a single function
        file_path = "temp_test_file.py"
        complexity_results = [{'function': 'simple_function', 'complexity': 1}]
        thresholds = {'low': 5, 'medium': 10}

        # No exceptions should be raised
        try:
            generate_complexity_report(file_path, complexity_results, thresholds)
        except Exception as e:
            self.fail(f"generate_complexity_report raised an exception: {e}")
