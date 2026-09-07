import ast


ALLOWED_NAMES = {
    "df",
    "pd",
    "result"
}


BLOCKED_NAMES = {
    "os",
    "sys",
    "subprocess",
    "shutil",
    "socket",
    "requests",
    "open",
    "eval",
    "exec",
    "compile",
    "__import__",
    "input"
}


def validate_code(code):
    """
    Basic safety validation for AI-generated analysis code.
    """

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False, "Generated code contains invalid Python syntax."

    for node in ast.walk(tree):

        # Block imports
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            return False, "Imports are not allowed."

        # Block dangerous names
        if isinstance(node, ast.Name):

            if node.id in BLOCKED_NAMES:
                return False, (
                    f"Use of '{node.id}' is not allowed."
                )

        # Block dangerous attribute access
        if isinstance(node, ast.Attribute):

            if node.attr in BLOCKED_NAMES:
                return False, (
                    f"Use of '{node.attr}' is not allowed."
                )

    return True, "Code passed safety validation."


def execute_analysis(code, df):
    """
    Validate and execute AI-generated Pandas analysis.
    """

    is_valid, message = validate_code(code)

    if not is_valid:
        return None, message

    safe_globals = {
        "__builtins__": {},
        "pd": __import__("pandas")
    }

    safe_locals = {
        "df": df
    }

    try:

        exec(
            code,
            safe_globals,
            safe_locals
        )

        if "result" not in safe_locals:

            return None, (
                "The generated analysis did not "
                "produce a result."
            )

        return (
            safe_locals["result"],
            "Analysis executed successfully."
        )

    except Exception as e:

        return None, (
            f"Analysis execution failed: {str(e)}"
        )