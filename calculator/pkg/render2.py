# render2.py

def render(expression, result):
    if isinstance(result, float) and result.is_integer():
        result_str = str(int(result))
    else:
        result_str = str(result)

    # Calculate the maximum length for the base of the triangle
    max_len = max(len(expression), len(result_str)) + 4

    triangle = []

    # Top of the triangle
    triangle.append(" " * ((max_len - 1) // 2) + "▲" + " " * ((max_len - 1) // 2))

    # Expression line
    padding = (max_len - len(expression)) // 2
    triangle.append(" " * padding + expression + " " * padding)

    # Separator line
    triangle.append(" " * ((max_len - 1) // 2) + "|" + " " * ((max_len - 1) // 2))

    # Result line
    padding = (max_len - len(result_str)) // 2
    triangle.append(" " * padding + result_str + " " * padding)

    # Base of the triangle
    triangle.append("-" * max_len)

    return "\n".join(triangle)
