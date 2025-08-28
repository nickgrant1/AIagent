import os
from google.genai import types
def get_file_content(working_directory, file_path):
    dirPath = os.path.join(working_directory, file_path)
    dirAbs = os.path.abspath(dirPath)
    cwdAbs = os.path.abspath(working_directory)

    if not os.path.isfile(dirAbs):
        print(f'Error: File not found or is not a regular file: "{file_path}"')
        return
        
    if os.path.commonpath([cwdAbs]) != os.path.commonpath([cwdAbs, dirAbs]):
        print(f'Error: Cannot list "{file_path}" as it is outside the permitted working directory')
        return

    MAX_CHARS = 10000
    try:
        with open(dirAbs, "r") as f:
            content = f.read()
            message = ""
            if len(content) > MAX_CHARS:
                f.seek(0)
                content = f.read(MAX_CHARS)
                content += f' [...File "{file_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return f"Error reading file '{dirPath}': {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads at most 10,000 characters of file in specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read from, relative to the working directory."
            )
        }
    )
)