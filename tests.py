from functions.run_python_file import run_python_file


if __name__ == "__main__":
    result1 = print(run_python_file("calculator", "main.py"))
    result2 = print(run_python_file("calculator", "tests.py"))
    result3 = print(run_python_file("calculator", "../main.py"))
    result4 = print(run_python_file("calculator", "nonexistent.py"))
