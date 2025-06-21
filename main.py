import os
import subprocess
from dotenv import load_dotenv
import inspect
import sys
from google import genai
from google.genai import types
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

user_prompt = " ".join(sys.argv[1:])

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

system_prompt = system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads file content from the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            )
        }
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to be executed, relative to the working directory"
            )
        }
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be written, relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the specified file."
            )
        }
    )
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
    ]
)
functions_dict = {"get_files_info": get_files_info, "get_file_content": get_file_content, "run_python_file": run_python_file, "write_file": write_file}

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name} ({function_call_part.args})")
    else: 
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name in functions_dict:
        function_to_call = functions_dict[function_call_part.name]
        args = dict(function_call_part.args)  # Copy to modify if needed

        # Check if working_directory is needed, and insert default if not supplied
        sig = inspect.signature(function_to_call)
        if 'working_directory' in sig.parameters and 'working_directory' not in args:
            args['working_directory'] = "."

        result = function_to_call(**args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    
if len(sys.argv) > 1:
    iteration = 0
    while iteration < 20:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt),
            )
        candidate = response.candidates[0]
        for part in candidate.content.parts:
            if part.text:
                print("Agent text:", part.text)
                messages.append(part)
            if part.function_call:
                print("Agent function call:", part.function_call)
                is_verbose = "--verbose" in sys.argv
                func_return = call_function(part.function_call)
                messages.append(func_return)
                if part.function_call.name == "get_file_content":
                    message = [
                        types.Content(role="user", parts=[types.Part(text=user_prompt)]), func_return,
                    ]
                    
                try:
                    final_response = func_return.parts[0].function_response.response
                    if is_verbose:
                        print(f"-> {final_response}")
                except (AttributeError, IndexError) as e:
                    raise RuntimeError(f"Function callr esult had an unexpected structure: {e}")
        calc_output = subprocess.run(['python3', 'calculator/main.py', "3 + 7 * 2"], capture_output=True)
        calc_output_decoded = calc_output.stdout.decode('utf-8')
        if calc_output_decoded != "20\n":
            print(response.text)
            break
        iteration += 1
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        if "--verbose" in sys.argv:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
else:
    print("Error: No response received")
    sys.exit(1)



