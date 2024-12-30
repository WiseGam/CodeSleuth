# CodeSleuth

![Logo](assets/logo.png)

**CodeSleuth.py** is an open-source tool for analyzing the architecture of a Python project, measuring the cyclomatic complexity of its code, detecting circular dependencies, and identifying overly large files. This script helps you maintain a clean codebase and improve your project's quality by providing useful metrics and recommendations.

---

## Features

- **Project structure analysis**: Scans the Python files in a project and analyzes dependencies between them.
- **Circular dependency detection**: Identifies cycles in the dependencies between files to avoid architectural issues.
- **Cyclomatic complexity analysis**: Measures the complexity of each function and method to assess code maintainability.
- **Identification of large files**: Detects files that exceed 500 lines and suggests splitting them.
- **Detailed report generation**: Generates a report that includes large files, function complexity, and dependency cycles.

---

## Installation

### Prerequisites

- Python 3.x
- Required Python libraries: `ast`, `radon`, `networkx`, `argparse`, and `graphviz` (for generating graphs if needed).

### Install dependencies

Clone this repository and install the required dependencies using pip.

```bash
git clone https://github.com/your-username/CodeSleuth.git
cd CodeSleuth
pip install -r requirements.txt
```

The requirements.txt file includes:

```bash
radon
networkx
graphviz
argparse
```

If you don’t have graphviz installed, you might need to install it separately via your package manager or from Graphviz Downloads.

---

## Usage

### Running the script

To analyze a Python project, simply run the script from the terminal, specifying the path to the project you want to analyze.

```bash
python CodeSleuth.py /path/to/your/project
```

You can also customize the analysis with the following options:

```bash
python CodeSleuth.py /path/to/your/project --max_lines 400 --complexity_threshold 12
```

### Options:

- `--max_lines` : Sets the threshold for the number of lines a file can have before it is considered "too large" (default is 500).
- `--complexity_threshold` : Sets the cyclomatic complexity threshold to flag complex functions (default is 10).

### Example run:

```bash
python CodeSleuth.py /path/to/your/project --max_lines 400 --complexity_threshold 12
```

This will generate a report that includes:

- The size of each analyzed file.
- Cyclomatic complexity of each function.
- Detected dependency cycles.
- Any overly large files.

---

## Contributing

Contributions are welcome! If you have ideas for improvements or fixes, feel free to open an issue or submit a pull request.
Steps to contribute:

- Fork this repository.
- Clone your fork locally.
- Create a branch for your feature (git checkout -b my-feature).
- Make your changes.
- Test your changes.
- Submit a pull request.

---

## License

This project is licensed under the MIT License.
