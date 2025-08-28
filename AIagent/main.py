from google.genai import types
import os
from dotenv import load_dotenv
from google import genai
import sys
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python import schema_run_python_file, run_python_file

def main():
    print("Hello from aiagent!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("Missing Argument")
        sys.exit(1)


    user_prompt = sys.argv[1]
    system_prompt = '''You are a helpful AI coding agent. When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
            - List files and directories
            - Read file contents
            - Execute Python files with optional arguments
            - Write or overwrite files

            All paths you provide should be relative to the working directory. 
            You do not need to specify the working directory in your function calls as it is
            automatically injected for security reasons.
        '''
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(
                                                        tools=[available_functions], system_instruction=system_prompt)
    )

    if len(sys.argv)>=3 and sys.argv[2] == '--verbose':
        verbose=True
        '''print(f'User prompt: {user_prompt}')
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')'''
    else:
        verbose=False

    if response.function_calls:
        for fc in response.function_calls:
            result = call_function(fc, verbose)
            try:
                result_response = result.parts[0].function_response.response
                if verbose:
                    print(f"-> {result_response}")
            except Exception as e: 
                raise Exception(f'Error calling functions: {e}')
    else:
        print(response.text)


    

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}") 

    args=function_call_part.args
    args["working_directory"] = "./calculator"
    match function_call_part.name:
        case "get_files_info": function_result = get_files_info(**args)
        case "get_file_content": function_result = get_file_content(**args)
        case "run_python_file": function_result = run_python_file(**args)
        case "write_file": function_result = write_file(**args)
        case _: return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_name,
                            response={"error": f"Unknown function: {function_name}"},
                        )
                    ],
                )

    return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
                )
            ],
        )
    

if __name__ == "__main__":
    main()





