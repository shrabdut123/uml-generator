from dependency_extractor import extract_function_dependencies
from ast_analyzer import extract_structural_components
from uml_generator import generate_uml

def process_code_and_generate_uml(file_path):
    """Extract dependencies, analyze structure, and generate UML."""
    
    dependencies, _ = extract_function_dependencies(file_path)
    extracted_data = extract_structural_components(dependencies)
    generate_uml(extracted_data, output_file="uml_diagram.png")


# Example execution
if __name__ == "__main__":
    process_code_and_generate_uml("source-code/sample.js")
