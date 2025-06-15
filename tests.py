from functions.write_file import write_file


if __name__ == "__main__":
    result1 = print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    result2 = print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    result3 = print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

    