# Project Analysis Orchestrator

"""
analysis.py: Orchestrates the analysis of a Python project for complexity, dependencies, and file size.
"""

import os
import logging
from .complexity import analyze_complexity, generate_complexity_report
from .dependencies import analyze_dependencies, detect_circular_dependencies

# Configure logging
logger = logging.getLogger(__name__)

def detect_large_files(directory, max_lines=500):
    """
    Detect Python files in a directory that exceed a specified number of lines.

    Args:
        directory (str): The root directory to analyze.
        max_lines (int): The maximum number of lines to consider a file as large. Default is 500.

    Returns:
        list: A list of file paths for files that exceed the specified number of lines.
    """
    logger.info("Detecting large files in directory: %s", directory)
    large_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as file_handle:
                    lines = file_handle.readlines()
                    if len(lines) > max_lines:
                        large_files.append(file_path)
                        logger.warning("Large file detected: %s (%d lines)", file_path, len(lines))
    return large_files

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

    logger.info("Starting project analysis for directory: %s", directory)

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
        logger.info("Average cyclomatic complexity: %.2f", average_complexity)
    else:
        print("\nNo functions found to analyze.")
        logger.warning("No functions found in the project for complexity analysis.")

    print("\nAnalyzing dependencies...")
    graph = analyze_dependencies(directory)
    cycles = detect_circular_dependencies(graph)
    if cycles:
        print("\nCircular dependencies detected:")
        for cycle in cycles:
            print(cycle)
    else:
        print("\nNo circular dependencies detected.")
