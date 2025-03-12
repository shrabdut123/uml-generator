import argparse
import asyncio
from src.dependency_extractor import extract_function_dependencies
from src.ast_analyzer import extract_structural_components
from src.uml_generator import generate_uml

async def generate_uml_diagram(file_path, output_file):
    """Asynchronously extract dependencies, analyze structure, and generate UML."""
    # Run synchronous functions in separate threads using asyncio.to_thread
    dependencies, _ = await asyncio.to_thread(extract_function_dependencies, file_path)
    
    # Await the coroutine result from extract_structural_components
    extracted_data = await asyncio.to_thread(extract_structural_components, dependencies)
    
    # Pass the extracted data to generate_uml
    await asyncio.to_thread(generate_uml, extracted_data, output_file)

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Generate UML diagrams from source code.")
    parser.add_argument(
        "file_path", 
        help="Path to the source code file for UML generation (e.g., source-code/sample.js)"
    )
    parser.add_argument(
        "--output", "-o", 
        default="uml_diagram.png", 
        help="Output file name for the UML diagram (default: uml_diagram.png)"
    )
    
    args = parser.parse_args()
    
    # Run the UML diagram generation asynchronously
    asyncio.run(generate_uml_diagram(args.file_path, args.output))

if __name__ == "__main__":
    main()