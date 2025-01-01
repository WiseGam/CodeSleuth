# Complexity Analysis Module

"""
complexity.py: Functions for analyzing the cyclomatic complexity of Python functions.
"""

import logging
from radon.complexity import cc_visit

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def analyze_complexity(file_path):
    """
    Analyze the cyclomatic complexity of each function in a given Python file.

    Args:
        file_path (str): The path to the Python file to analyze.

    Returns:
        list: A list of dictionaries containing function names and their complexity scores.
    """
    logger.info("Analyzing complexity for file: %s", file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
    complexity = cc_visit(code)
    complexity_results = []

    for func in complexity:
        complexity_results.append({
            'function': func.name,
            'complexity': func.complexity
        })

    logger.debug("Complexity results: %s", complexity_results)
    return complexity_results

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
    logger.info("Generating complexity report for file: %s", file_path)
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
        logger.info("Function %s has complexity %d: %s", func_name, complexity, status)
