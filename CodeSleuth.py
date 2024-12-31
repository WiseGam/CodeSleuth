import os
import ast
from radon.complexity import cc_visit
from radon.visitors import ComplexityVisitor
import networkx as nx
import argparse

# Function to analyze cyclomatic complexity per function
def analyze_complexity(file_path):
    """_summary_

    Args:
        file_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open(file_path, 'r') as file:
        code = file.read()
    complexity = cc_visit(code)
    complexity_results = []

    for func in complexity:
        complexity_results.append({
            'function': func.name,
            'complexity': func.complexity
        })

    return complexity_results

# Function to detect large files
def detect_large_files(directory, max_lines=500):
    """_summary_

    Args:
        directory (_type_): _description_
        max_lines (int, optional): _description_. Defaults to 500.

    Returns:
        _type_: _description_
    """
    large_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    if len(lines) > max_lines:
                        large_files.append(file_path)
    return large_files

# Function to analyze dependencies between files
def analyze_dependencies(directory):
    """_summary_

    Args:
        directory (_type_): _description_

    Returns:
        _type_: _description_
    """
    graph = nx.DiGraph()  # Directed graph for dependencies
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    code = f.read()
                    # Parse the code to find imports
                    tree = ast.parse(code)
                    imports = [node.name for node in ast.walk(tree) if isinstance(node, ast.Import)]
                    for imp in imports:
                        graph.add_edge(file_path, imp)  # Add edge representing a dependency
    return graph

# Function to detect circular dependencies
def detect_circular_dependencies(graph):
    """_summary_

    Args:
        graph (_type_): _description_

    Returns:
        _type_: _description_
    """
    return list(nx.simple_cycles(graph))  # Find all cycles in the directed graph

# Function to generate complexity report with thresholds
def generate_complexity_report(file_path, complexity_results, complexity_thresholds):
    """_summary_

    Args:
        file_path (_type_): _description_
        complexity_results (_type_): _description_
        complexity_thresholds (_type_): _description_
    """
    print(f"\nComplexity report for {file_path}:")

    for result in complexity_results:
        func_name = result['function']
        complexity = result['complexity']

        # Apply complexity thresholds
        if complexity <= complexity_thresholds['low']:
            status = "Low Complexity - OK"
        elif complexity <= complexity_thresholds['medium']:
            status = f"Medium Complexity - Consider refactoring"
        else:
            status = f"High Complexity - Needs refactoring"

        print(f"  - {func_name}: Complexity = {complexity} ({status})")

# Main function to analyze a project
def analyze_project(directory, max_lines=500, complexity_thresholds=None):
    """_summary_

    Args:
        directory (_type_): _description_
        max_lines (int, optional): _description_. Defaults to 500.
        complexity_thresholds (_type_, optional): _description_. Defaults to None.
    """
    if complexity_thresholds is None:
        complexity_thresholds = {'low': 5, 'medium': 10}

    print("Analyzing complexity and dependencies...\n")

    # Detect large files
    large_files = detect_large_files(directory, max_lines)
    print("Large files (over 500 lines):")
    for file in large_files:
        print(file)

    # Analyze cyclomatic complexity
    print("\nCyclomatic complexity of functions:")
    total_complexity = 0
    num_functions = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                complexity_results = analyze_complexity(file_path)

                # Generate complexity report for each file
                generate_complexity_report(file_path, complexity_results, complexity_thresholds)

                # Collect overall complexity data for the project
                total_complexity += sum(result['complexity'] for result in complexity_results)
                num_functions += len(complexity_results)

    if num_functions > 0:
        average_complexity = total_complexity / num_functions
        print(f"\nAverage cyclomatic complexity for the project: {average_complexity:.2f}")
    else:
        print("\nNo functions found to analyze.")

    # Analyze dependencies and cycles
    print("\nAnalyzing dependencies...")
    graph = analyze_dependencies(directory)
    cycles = detect_circular_dependencies(graph)
    if cycles:
        print("\nCircular dependencies detected:")
        for cycle in cycles:
            print(cycle)
    else:
        print("\nNo circular dependencies detected.")

# Main entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Python project for complexity, dependencies, and file size.")
    parser.add_argument('directory', help="Path to the Python project directory.")
    parser.add_argument('--max_lines', type=int, default=500, help="Maximum number of lines in a file to consider it large.")
    parser.add_argument('--complexity_low', type=int, default=5, help="Threshold for low cyclomatic complexity.")
    parser.add_argument('--complexity_medium', type=int, default=10, help="Threshold for medium cyclomatic complexity.")
    args = parser.parse_args()

    complexity_thresholds = {
        'low': args.complexity_low,
        'medium': args.complexity_medium
    }

    analyze_project(args.directory, args.max_lines, complexity_thresholds)
