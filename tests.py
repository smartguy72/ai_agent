from functions.get_files_info import get_files_info


if __name__ == "__main__":
    result1 = print(get_files_info("calculator", "."))
    result2 = print(get_files_info("calculator", "pkg"))
    result3 = print(get_files_info("calculator", "/bin"))
    result4 = print(get_files_info("calculator", "../"))
    