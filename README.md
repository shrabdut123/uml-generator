# UML Generator

A Python tool to extract dependencies from JavaScript/TypeScript code and generate UML diagrams.

## Features
✅ Extracts function and class dependencies  
✅ Uses OpenAI API for AST analysis  
✅ Generates UML diagrams using PlantUML  

## Files
- `src/dependency_extractor.py`: Main script to extract function dependencies from JavaScript and TypeScript files.
- `src/ast_analyzer.py`: Analyzes the AST to extract structural components and relationships.
- `src/uml_generator.py`: Generates UML diagrams from extracted data using PlantUML.
- `src/main.py`: Main entry point to process code and generate UML diagrams.
- `uml_generator_cli.py`: Command-line interface for generating UML diagrams.

## Installation

1. Clone the repository:

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Ensure you have Babel and its plugins installed for JavaScript/TypeScript parsing:

```bash
npm install @babel/core @babel/parser @babel/traverse
```

## Usage

### Using the CLI Tool

You can use the CLI tool to generate UML diagrams from your source code files.

```bash
python uml_generator_cli.py <file_path> [--output <output_file>]
```

- `<file_path>`: Path to the source code file for UML generation (e.g., `source-code/sample.js`).
- `--output`, `-o`: (Optional) Output file name for the UML diagram (default: `uml_diagram.png`).

Example:

```bash
python uml_generator_cli.py source-code/sample.js -o my_diagram.png
```

### Using the Main Script

```bash
python src/main.py
```