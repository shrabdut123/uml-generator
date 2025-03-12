import openai
import json
import time
from concurrent.futures import ThreadPoolExecutor
from config.settings import DEPLOYMENT_NAME, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY

# OpenAI API Configuration
openai.api_base, openai.api_key, openai.api_type, openai.api_version = (
    AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, "azure", "2024-05-01-preview"
)

def extract_json(content):
    """Safely extract JSON from OpenAI response."""
    start_idx = content.find('{')
    if start_idx == -1:
        print("⚠️ No JSON found in the content.")
        return None

    stack = []
    for i, char in enumerate(content[start_idx:], start=start_idx):
        if char == '{':
            stack.append(char)
        elif char == '}':
            stack.pop()
            if not stack:
                end_idx = i + 1
                break
    else:
        print("⚠️ No matching closing brace found.")
        return None

    try:
        return json.loads(content[start_idx:end_idx])
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parsing Error: {e}")
        return None

def analyze_functions_and_classes(ast_data):
    """Extract function dependencies and class structures from AST."""
    prompt = (
        "Analyze the following JavaScript/TypeScript AST and extract:\n"
        "- **Functions & Dependencies**: Identify functions and the functions they call.\n"
        "- **Classes & Methods**: Extract all class definitions and their methods.\n\n"
        f"AST Data:\n{ast_data}\n\n"
        "Output JSON:\n"
        "```\n"
        "{\n"
        "    \"functions\": {\"FunctionA\": [\"FunctionB\", \"FunctionC\"]},\n"
        "    \"classes\": {\"ClassA\": {\"methods\": [\"method1\", \"method2\"]}}\n"
        "}\n"
        "```"
    )

    response = openai.ChatCompletion.create(
        engine=DEPLOYMENT_NAME,
        messages=[{"role": "system", "content": "You are an expert in analyzing JavaScript/TypeScript ASTs."},
                  {"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1500,
        stream=True  # Enable streaming
    )

    # Handle streaming response safely
    content = ""
    for chunk in response:
        choices = chunk.get("choices", [])
        if choices and "delta" in choices[0] and "content" in choices[0]["delta"]:
            content += choices[0]["delta"]["content"]

    return extract_json(content)

def analyze_relationships(ast_data):
    """Extract function relationships, arguments, return types, and error cases."""
    prompt = (
        "Analyze the following JavaScript/TypeScript AST and extract relationships:\n"
        "- **Explicit relationships**: Represent function calls as directed relationships (`FunctionA -> FunctionB`).\n"
        "- **Function arguments**: Capture parameters and types.\n"
        "- **Output returned**: Identify return types.\n"
        "- **Error cases**: Detect possible errors (throw, try-catch, rejections).\n\n"
        f"AST Data:\n{ast_data}\n\n"
        "Output JSON:\n"
        "```\n"
        "{\n"
        "    \"relationships\": [\n"
        "        {\"from\": \"FunctionA\", \"to\": \"FunctionB\", \"arguments\": [{\"name\": \"param1\", \"type\": \"string\"}], \"returns\": \"boolean\", \"errors\": [\"TypeError\"]}\n"
        "    ]\n"
        "}\n"
        "```"
    )

    response = openai.ChatCompletion.create(
        engine=DEPLOYMENT_NAME,
        messages=[{"role": "system", "content": "You are an expert in analyzing JavaScript/TypeScript ASTs."},
                  {"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=3000,
        stream=True  # Enable streaming
    )

    # Handle streaming response safely
    content = ""
    for chunk in response:
        choices = chunk.get("choices", [])
        if choices and "delta" in choices[0] and "content" in choices[0]["delta"]:
            content += choices[0]["delta"]["content"]

    return extract_json(content)

def extract_structural_components(ast_data):
    """Extract functions, classes, dependencies, and relationships using parallel execution."""
    start_time = time.time()

    with ThreadPoolExecutor() as executor:
        future_functions = executor.submit(analyze_functions_and_classes, ast_data)
        future_relationships = executor.submit(analyze_relationships, ast_data)

        extracted_data1 = future_functions.result()
        extracted_data2 = future_relationships.result()

    if not extracted_data1 or not extracted_data2:
        print("⚠️ Failed to extract structural components or relationships.")
        return None

    extracted_data = {**extracted_data1, "relationships": extracted_data2["relationships"]}
    end_time = time.time()

    print(f"✨ Extracted components successfully. ⏱️ Total time: {end_time - start_time:.2f} seconds")
    return extracted_data