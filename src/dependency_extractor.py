import os
import json
import execjs
import time

def extract_function_dependencies(file_path):
    start_time = time.time()  # Start time
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    # JavaScript function to parse the AST with Babel
    js_code = """
    const parser = require('@babel/parser');
    const traverse = require('@babel/traverse').default;

    function parseCode(code) {
        try {
            // Parse JS/TS with Babel, supporting modern syntax
            const ast = parser.parse(code, {
                sourceType: "module",
                plugins: ["jsx", "typescript"]
            });

            const functionDetails = {};

            traverse(ast, {
                FunctionDeclaration(path) {
                    const funcName = path.node.id ? path.node.id.name : "anonymous";
                    functionDetails[funcName] = {
                        calls: [],
                        arguments: path.node.params.map(param => ({
                            name: param.name || "unknown",
                            type: param.typeAnnotation
                                ? param.typeAnnotation.typeAnnotation.type
                                : "unknown"
                        })),
                        returns: "unknown",
                        errors: []
                    };

                    path.traverse({
                        CallExpression(innerPath) {
                            if (innerPath.node.callee.type === "Identifier") {
                                functionDetails[funcName].calls.push(innerPath.node.callee.name);
                            }
                        },
                        ReturnStatement(innerPath) {
                            functionDetails[funcName].returns = innerPath.node.argument
                                ? innerPath.node.argument.type
                                : "void";
                        },
                        ThrowStatement(innerPath) {
                            functionDetails[funcName].errors.push(
                                innerPath.node.argument.type === "NewExpression" &&
                                innerPath.node.argument.callee.type === "Identifier"
                                    ? innerPath.node.argument.callee.name
                                    : "Error"
                            );
                        }
                    });
                },

                VariableDeclarator(path) {
                    // Capture arrow functions and function expressions
                    if (
                        path.node.init &&
                        (path.node.init.type === "ArrowFunctionExpression" || path.node.init.type === "FunctionExpression")
                    ) {
                        const funcName = path.node.id.name;
                        functionDetails[funcName] = {
                            calls: [],
                            arguments: path.node.init.params.map(param => ({
                                name: param.name || "unknown",
                                type: param.typeAnnotation
                                    ? param.typeAnnotation.typeAnnotation.type
                                    : "unknown"
                            })),
                            returns: "unknown",
                            errors: []
                        };

                        path.traverse({
                            CallExpression(innerPath) {
                                if (innerPath.node.callee.type === "Identifier") {
                                    functionDetails[funcName].calls.push(innerPath.node.callee.name);
                                }
                            },
                            ReturnStatement(innerPath) {
                                functionDetails[funcName].returns = innerPath.node.argument
                                    ? innerPath.node.argument.type
                                    : "void";
                            },
                            ThrowStatement(innerPath) {
                                functionDetails[funcName].errors.push(
                                    innerPath.node.argument.type === "NewExpression" &&
                                    innerPath.node.argument.callee.type === "Identifier"
                                        ? innerPath.node.argument.callee.name
                                        : "Error"
                                );
                            }
                        });
                    }
                }
            });

            return JSON.stringify(functionDetails, null, 2);
        } catch (error) {
            return JSON.stringify({ "error": error.message });
        }
    }
    """

    try:
        ctx = execjs.compile(js_code)
        ast_json = ctx.call("parseCode", code)

        dependencies = json.loads(ast_json)
        if "error" in dependencies:
            print(f"⚠️ Error parsing JS/TS file: {dependencies['error']}")
            return {}, code
        end_time = time.time()  # End time
        print(f"⏱️ Response time: {end_time - start_time:.2f} seconds")

        return dependencies, code

    except execjs.ProgramError as e:
        return {}, code

    except json.JSONDecodeError as e:
        return {}, code