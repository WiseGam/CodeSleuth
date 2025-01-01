# API Documentation

## Modules Overview

This project consists of three main modules for Python project analysis:
1. **`complexity.py`**: Cyclomatic complexity analysis of functions.
2. **`dependencies.py`**: File dependency analysis and detection of circular dependencies.
3. **`analysis.py`**: Orchestrates the entire project analysis, including file size, complexity, and dependencies.

---

## `complexity.py`

### `analyze_complexity(file_path)`
- **Description**: Analyzes the cyclomatic complexity of functions in a Python file.
- **Parameters**:
  - `file_path` *(str)*: Path to the Python file to analyze.
- **Returns**:
  - `list[dict]`: List of dictionaries with `function` (name) and `complexity` (score).

### `generate_complexity_report(file_path, complexity_results, complexity_thresholds)`
- **Description**: Generates a complexity report for a Python file based on specified thresholds.
- **Parameters**:
  - `file_path` *(str)*: Path to the analyzed Python file.
  - `complexity_results` *(list)*: Results from `analyze_complexity`.
  - `complexity_thresholds` *(dict)*: Threshold levels (`low`, `medium`, `high`).
- **Returns**: None.

---

## `dependencies.py`

### `analyze_dependencies(directory)`
- **Description**: Analyzes inter-file dependencies within a directory.
- **Parameters**:
  - `directory` *(str)*: Root directory for analysis.
- **Returns**:
  - `networkx.DiGraph`: Directed graph of file dependencies.

### `detect_circular_dependencies(graph)`
- **Description**: Detects circular dependencies in a dependency graph.
- **Parameters**:
  - `graph` *(networkx.DiGraph)*: Dependency graph.
- **Returns**:
  - `list[list[str]]`: Cycles in the graph, each represented as a list of nodes.

---

## `analysis.py`

### `detect_large_files(directory, max_lines=500)`
- **Description**: Identifies Python files exceeding a specified line count.
- **Parameters**:
  - `directory` *(str)*: Directory to scan.
  - `max_lines` *(int)*: Maximum allowable lines per file (default: 500).
- **Returns**:
  - `list[str]`: List of large file paths.

### `analyze_project(directory, max_lines=500, complexity_thresholds=None)`
- **Description**: Comprehensive analysis of a Python project, including file size, complexity, and dependencies.
- **Parameters**:
  - `directory` *(str)*: Root directory of the project.
  - `max_lines` *(int)*: Line threshold for large files.
  - `complexity_thresholds` *(dict, optional)*: Complexity thresholds (default: `{low: 5, medium: 10}`).
- **Returns**: None.
