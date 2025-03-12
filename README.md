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

```bash
python src/main.py
```