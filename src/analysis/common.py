import os    
    
def delete_if_exists(input_path):
    """
    Delete folder on a given path if the folder exists.
    """

    if os.path.exists(input_path):
        os.remove(input_path)
    if os.path.exists(input_path):
        os.remove(input_path)


def file_to_list(input_file):
    """
    Creates a list from input file by reading .txt file by row.

    Args:
        input_file (file): .txt file with '\n' delimiter.

    Returns:
        list: A list of elements from .txt.
    """
    list = []
    file = open(input_file, 'r', encoding='utf-8')
    
    for row in file:
        row = row.rstrip()      # Remove \n at the end of row
        list.append(row)
    
    return list