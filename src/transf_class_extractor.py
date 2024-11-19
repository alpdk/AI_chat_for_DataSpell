import ast


def extract_doc_string(node_body, ) -> str:
    if node_body and isinstance(node_body[0], ast.Expr) and isinstance(node_body[0].value, ast.Str):
        method_docstring = node_body[0].value.s
        return f'    """{method_docstring}"""'
    return ""

def extract_class_core(code: str) -> str:
    """
    Extracts class and method definitions along with their docstrings from the provided Python code.

    Args:
        code (str): Python code as a string.

    Returns:
        str: Extracted class and method signatures along with docstrings.
    """
    # Parse the code into an Abstract Syntax Tree (AST)
    tree = ast.parse(code)
    extracted_definitions = []

    # Traverse the AST to find classes and their methods
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            # Extract class name
            class_name = f"class {node.name}:"
            extracted_definitions.append(class_name)

            class_docstring = extract_doc_string(node.body)

            if class_docstring != "":
                extracted_definitions.append(class_docstring)

            # Extract methods within the class
            for class_node in node.body:
                if isinstance(class_node, ast.FunctionDef):
                    method_name = f"    def {class_node.name}({', '.join(arg.arg for arg in class_node.args.args)}):"
                    extracted_definitions.append(method_name)

                    method_docstring = extract_doc_string(class_node.body)

                    if method_docstring != "":
                        extracted_definitions.append('    ' + method_docstring)

    # Combine the extracted lines
    return "\n".join(extracted_definitions)