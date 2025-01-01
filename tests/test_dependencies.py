import unittest
import os
import networkx as nx
from codesleuth.dependencies import analyze_dependencies, detect_circular_dependencies

class TestDependencies(unittest.TestCase):
    def test_analyze_dependencies(self):
        # Create a temporary directory structure
        os.makedirs("temp_test_dir", exist_ok=True)
        with open("temp_test_dir/module_a.py", "w") as f:
            f.write("import module_b\n")
        with open("temp_test_dir/module_b.py", "w") as f:
            f.write("import module_a\n")
        
        graph = analyze_dependencies("temp_test_dir")
        self.assertIn("temp_test_dir/module_a.py", graph.nodes())
        self.assertIn("temp_test_dir/module_b.py", graph.nodes())

    def test_detect_circular_dependencies(self):
        # Create a simple circular dependency graph
        graph = nx.DiGraph()
        graph.add_edge("module_a.py", "module_b.py")
        graph.add_edge("module_b.py", "module_a.py")
        
        cycles = detect_circular_dependencies(graph)
        self.assertEqual(len(cycles), 1)
        self.assertCountEqual(cycles[0], ["module_a.py", "module_b.py"])

