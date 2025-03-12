import subprocess
import os

PLANTUML_PATH = "/opt/homebrew/opt/plantuml/bin/plantuml"

def generate_uml(extracted_data, output_file="uml_diagram.png"):
    """Generate UML diagrams from extracted data using PlantUML."""
    
    if not extracted_data:
        raise ValueError("No extracted data to generate UML.")

    plantuml_code = "@startuml\nleft to right direction\n"
    
    for class_name, class_info in extracted_data.get('classes', {}).items():
        plantuml_code += f"class {class_name} {{\n"
        for method in class_info.get("methods", []):
            plantuml_code += f"    + {method}()\n"
        plantuml_code += "}\n"

    for relationship in extracted_data.get("relationships", []):
        from_function = relationship["from"]
        to_function = relationship["to"]
        
        # Extract arguments
        args_list = relationship.get("arguments", [])
        formatted_args = ", ".join(f"{arg.get('name', 'unknown')}: {arg.get('type', 'unknown')}" for arg in args_list)

        # Extract return type
        return_type = relationship.get("returns", "unknown")

        # Extract errors
        errors = relationship.get("errors", [])
        error_text = "\\n".join(errors) if errors else ""

        # Build UML relationship line with arguments and return type
        if formatted_args:
            plantuml_code += f"{from_function} --> {to_function} : ({formatted_args}) : {return_type}\n"
        else:
            plantuml_code += f"{from_function} --> {to_function} : {return_type}\n"

        # Add error notes if applicable
        if error_text:
            plantuml_code += f"note right of {from_function}: Throws {error_text}\n"
    
    plantuml_code += "@enduml\n"

    with open("temp_uml.puml", "w") as f:
        f.write(plantuml_code)

    base_name, ext = os.path.splitext(output_file)
    counter = 1
    unique_output_file = output_file

    while os.path.exists(unique_output_file):
        unique_output_file = f"{base_name}_{counter}{ext}"
        counter += 1

    subprocess.run([PLANTUML_PATH, "-tpng", "temp_uml.puml"])
    subprocess.run(["mv", "temp_uml.png", unique_output_file])

    print(f"✅ UML diagram saved as {unique_output_file}")