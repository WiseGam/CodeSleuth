import unittest
import os
from codesleuth.analysis import detect_large_files, analyze_project

class TestAnalysis(unittest.TestCase):
    def test_detect_large_files(self):
        # Create a large file for testing
        os.makedirs("temp_test_dir", exist_ok=True)
        with open("temp_test_dir/large_file.py", "w") as f:
            f.write("\n".join(["line"] * 600))
        
        large_files = detect_large_files("temp_test_dir", max_lines=500)
        self.assertIn("temp_test_dir/large_file.py", large_files)

    def test_analyze_project(self):
        # Test the overall analysis (mock for simplicity)
        os.makedirs("temp_test_dir", exist_ok=True)
        with open("temp_test_dir/simple_file.py", "w") as f:
            f.write("def test():\n    pass\n")

        try:
            analyze_project("temp_test_dir")
        except Exception as e:
            self.fail(f"analyze_project raised an exception: {e}")
