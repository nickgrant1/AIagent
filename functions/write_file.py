import os
from google.genai import types

def write_file(working_directory, file_path, content):
    dirPath = os.path.join(working_directory, file_path)
    dirAbs = os.path.abspath(dirPath)
    cwdAbs = os.path.abspath(working_directory)
        
    if os.path.commonpath([cwdAbs]) != os.path.commonpath([cwdAbs, dirAbs]):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        

    try:
        with open(dirAbs, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error writing file '{dirPath}': {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to file in specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to overwrite, relative to the working directory.\
                If file doesn't exist, one is created."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text to be written to file_path."
            )
        }
    )
)