
import os

def get_files_info(working_directory, directory=None):
    if directory is None:
        return f'Error: No directory provided'
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_directory.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_directory):
        return f'Error: "{directory}" is not a directory'
    try:
        dir_contents = os.listdir(abs_directory)
        dir_list = []
        for entry in dir_contents:
            full_path = os.path.join(abs_directory, entry) 
            size = os.path.getsize(full_path)
            dir_status = os.path.isdir(full_path)
            dir_list.append(f'- {entry}: file_size={size} bytes, is_dir={dir_status}')
        final_output = "\n".join(dir_list)
        return final_output
    except Exception as e:
        return f'Error: {str(e)}'
    
