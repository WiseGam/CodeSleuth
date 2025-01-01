# Dependencies Analysis Module

"""
dependencies.py: Functions for analyzing dependencies and detecting circular dependencies.
"""

import os
import logging
import ast
import networkx as nx

# Configure logging
logger = logging.getLogger(__name__)

def analyze_dependencies(directory):
    """
    Analyze dependencies between Python files in a directory.

    Args:
        directory (str): The root directory to analyze.

    Returns:
        networkx.DiGraph: A directed graph representing file dependencies.
    """
    logger.info("Analyzing dependencies in directory: %s", directory)
    graph = nx.DiGraph()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as file_handle:
                    code = file_handle.read()
                    tree = ast.parse(code)
                    imports = [
                        alias.name
                        for node in ast.walk(tree)
                        if isinstance(node, (ast.Import, ast.ImportFrom))
                        for alias in node.names
                    ]
                    for imp in imports:
                        graph.add_edge(file_path, imp)
    logger.debug("Dependency graph nodes: %s", graph.nodes())
    return graph

def detect_circular_dependencies(graph):
    """
    Detect circular dependencies in a dependency graph.

    Args:
        graph (networkx.DiGraph): A directed graph representing file dependencies.

    Returns:
        list: A list of cycles detected in the graph, each cycle represented as a list of nodes.
    """
    logger.info("Detecting circular dependencies...")
    cycles = list(nx.simple_cycles(graph))
    if cycles:
        logger.warning("Circular dependencies found: %s", cycles)
    else:
        logger.info("No circular dependencies detected.")
    return cycles
