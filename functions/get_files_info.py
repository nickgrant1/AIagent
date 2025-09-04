import os, sys
from google.genai import types

def get_files_info(working_directory, directory="."):
    dirPath = os.path.join(working_directory, directory)
    dirAbs = os.path.abspath(dirPath)
    cwdAbs = os.path.abspath(working_directory)

    if not os.path.isdir(dirAbs):
        print(f'Error: "{directory}" is not a directory')
        return
        
    if os.path.commonpath([cwdAbs]) != os.path.commonpath([cwdAbs, dirAbs]):
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return

    result=[]
    for entry in os.scandir(dirAbs):
        if not entry.name[0].isalpha():
            continue
        
        size = entry.stat().st_size
        result.append(f' - {entry.name}: file_size={size} bytes, is_dir={entry.is_dir()}')
    return "\n".join(result)
        
    

def get_dir_size(path):
    total=0

    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp):
                total += os.path.getsize(fp)

    return total

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory.\
                If not provided, lists files in the working directory itself."
            )
        }
    )
)
    




