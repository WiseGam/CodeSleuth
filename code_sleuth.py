import os
import ast
from radon.complexity import cc_visit
import networkx as nx
import argparse

def analyze_complexity(file_path):
    """
    Analyze the cyclomatic complexity of each function in a given Python file.

    Args:
        file_path (str): The path to the Python file to analyze.

    Returns:
        list: A list of dictionaries containing function names and their complexity scores.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
    complexity = cc_visit(code)
    complexity_results = []

    for func in complexity:
        complexity_results.append({
            'function': func.name,
            'complexity': func.complexity
        })

    return complexity_results

def detect_large_files(directory, max_lines=500):
    """
    Detect Python files in a directory that exceed a specified number of lines.

    Args:
        directory (str): The root directory to analyze.
        max_lines (int): The maximum number of lines to consider a file as large. Default is 500.

    Returns:
        list: A list of file paths for files that exceed the specified number of lines.
    """
    large_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as file_handle:
                    lines = file_handle.readlines()
                    if len(lines) > max_lines:
                        large_files.append(file_path)
    return large_files

def analyze_dependencies(directory):
    """
    Analyze dependencies between Python files in a directory.

    Args:
        directory (str): The root directory to analyze.

    Returns:
        networkx.DiGraph: A directed graph representing file dependencies.
    """
    graph = nx.DiGraph()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as file_handle:
                    code = file_handle.read()
                    tree = ast.parse(code)
                    imports = [node.name for node in ast.walk(tree) if isinstance(node, ast.Import)]
                    for imp in imports:
                        graph.add_edge(file_path, imp)
    return graph

def detect_circular_dependencies(graph):
    """
    Detect circular dependencies in a dependency graph.

    Args:
        graph (networkx.DiGraph): A directed graph representing file dependencies.

    Returns:
        list: A list of cycles detected in the graph, each cycle represented as a list of nodes.
    """
    return list(nx.simple_cycles(graph))

def generate_complexity_report(file_path, complexity_results, complexity_thresholds):
    """
    Generate a complexity report for a given Python file based on threshold values.

    Args:
        file_path (str): The path to the Python file being analyzed.
        complexity_results (list): A list of dictionaries containing function names and complexity scores.
        complexity_thresholds (dict): A dictionary containing thresholds for low, medium, and high complexity levels.

    Returns:
        None
    """
    print(f"\nComplexity report for {file_path}:")

    for result in complexity_results:
        func_name = result['function']
        complexity = result['complexity']

        if complexity <= complexity_thresholds['low']:
            status = "Low Complexity - OK"
        elif complexity <= complexity_thresholds['medium']:
            status = "Medium Complexity - Consider refactoring"
        else:
            status = "High Complexity - Needs refactoring"

        print(f"  - {func_name}: Complexity = {complexity} ({status})")

def analyze_project(directory, max_lines=500, complexity_thresholds=None):
    """
    Analyze a Python project for file size, cyclomatic complexity, and file dependencies.

    Args:
        directory (str): The root directory of the Python project to analyze.
        max_lines (int): The maximum number of lines in a file to consider it large. Default is 500.
        complexity_thresholds (dict, optional): A dictionary containing thresholds for low, medium, and high complexity levels. Default thresholds are {'low': 5, 'medium': 10}.

    Returns:
        None
    """
    if complexity_thresholds is None:
        complexity_thresholds = {'low': 5, 'medium': 10}

    print("Analyzing complexity and dependencies...\n")

    large_files = detect_large_files(directory, max_lines)
    print("Large files (over 500 lines):")
    for file in large_files:
        print(file)

    print("\nCyclomatic complexity of functions:")
    total_complexity = 0
    num_functions = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                complexity_results = analyze_complexity(file_path)

                generate_complexity_report(file_path, complexity_results, complexity_thresholds)

                total_complexity += sum(result['complexity'] for result in complexity_results)
                num_functions += len(complexity_results)

    if num_functions > 0:
        average_complexity = total_complexity / num_functions
        print(f"\nAverage cyclomatic complexity for the project: {average_complexity:.2f}")
    else:
        print("\nNo functions found to analyze.")

    print("\nAnalyzing dependencies...")
    graph = analyze_dependencies(directory)
    cycles = detect_circular_dependencies(graph)
    if cycles:
        print("\nCircular dependencies detected:")
        for cycle in cycles:
            print(cycle)
    else:
        print("\nNo circular dependencies detected.")

if __name__ == "__main__":
    """
    Entry point for the script. Parses command-line arguments and triggers the project analysis.

    Command-Line Arguments:
        directory (str): Path to the Python project directory to analyze.
        --max_lines (int): Maximum number of lines in a file to consider it large. Default is 500.
        --complexity_low (int): Threshold for low cyclomatic complexity. Default is 5.
        --complexity_medium (int): Threshold for medium cyclomatic complexity. Default is 10.

    Example:
        python codesleuth.py /path/to/project --max_lines 600 --complexity_low 7 --complexity_medium 15
    """
    parser = argparse.ArgumentParser(
        description="Analyze Python project for complexity, dependencies, and file size."
    )
    parser.add_argument('directory', help="Path to the Python project directory.")
    parser.add_argument(
        '--max_lines', type=int, default=500,
        help="Maximum number of lines in a file to consider it large."
    )
    parser.add_argument(
        '--complexity_low', type=int, default=5,
        help="Threshold for low cyclomatic complexity."
    )
    parser.add_argument(
        '--complexity_medium', type=int, default=10,
        help="Threshold for medium cyclomatic complexity."
    )
    args = parser.parse_args()

    complexity_thresholds = {
        'low': args.complexity_low,
        'medium': args.complexity_medium
    }

    analyze_project(args.directory, args.max_lines, complexity_thresholds)
