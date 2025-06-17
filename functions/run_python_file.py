import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run(["python3", os.path.basename(abs_file_path)], timeout=30, capture_output=True, cwd=abs_working_directory)
        if result.stdout == b'' and result.stderr == b'':
            output1 = "No output produced"
            if result.returncode != 0:
                output2 = f"Process exited with code {result.returncode}"
                return f"{output1}\n{output2}"
            return output1
        else:
            output1 = f"STDOUT: {result.stdout.decode()}\nSTDERR: {result.stderr.decode()}"
            if result.returncode != 0:
                output2 = f"Process exited with code {result.returncode}"
                return f"{output1}\n{output2}"
            return output1
    except Exception as e:
        return f'Error: executing Python file: {e}'
    
    