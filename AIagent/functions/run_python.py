import os, subprocess, sys
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    dirPath = os.path.join(working_directory, file_path)
    dirAbs = os.path.abspath(dirPath)
    cwdAbs = os.path.abspath(working_directory)

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    if os.path.commonpath([cwdAbs]) != os.path.commonpath([cwdAbs, dirAbs]):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(dirAbs):
        return f'Error: File "{file_path}" not found.'
        
    command = [sys.executable, dirAbs] + args
    try:
        result = subprocess.run(command, cwd=working_directory, text=True, capture_output=True, timeout=30)
        msg = f'STDOUT: {result.stdout} STDERR: {result.stderr}'
        if result.returncode != 0:
            msg += f'\nProcess exited with code {result.returncode}'
        if not result.stdout and not result.stderr:
            msg = f'No output produced.'
        return msg
    except Exception as e:
        return f"Error: executing Python file: {e}"
        

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes python file with arguments if they are given, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file path to executre, relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Addtional and optional arguments to use when executing python file.\
                            If no arguments are given, execute without any."
            )
        }
    )
)

    