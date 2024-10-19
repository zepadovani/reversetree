#!/usr/bin/env python3

# Script to create directories and files based on a file tree structure. Take care with identation characters in the file tree file (you can use tabs or spaces, but not both).

import os
import argparse
import re

  # Matches any characters followed by a dot and 1 to 4 letters at the end


def parse_tree(file_name, identchar="tab", identsize=1, dirs_end_with_slashes=False):
    """
    Parses a file containing a tree structure and generates lists of directories and files to create.
    Args:
        file_name (str): The path to the file containing the tree structure.
        identchar (str, optional): The character used for indentation. Defaults to "tab".
        identsize (int, optional): The number of indentation characters per level. Defaults to 1.
        dirs_end_with_slashes (bool, optional): Whether directories are indicated by trailing slashes. Defaults to True.
    Returns:
        tuple: A tuple containing two lists:
            - list_dirs_to_create (list): A list of directory paths to create.
            - list_files_to_create (list): A list of file paths to create.
    """

    directory_stack = []
    list_files_to_create = []
    list_dirs_to_create = []
    file_with_extension_pattern = r".*\.[a-zA-Z]{1,4}$"
    line_count = 0

    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()

            if not line:
                print(f'Empty line at line {line_count + 1}. So, ignoring...')
                continue
            if "," in line:
                print(f'Comma in line {line_count + 1}. So, ignoring...')
                continue

            # If the first line is the root and starts with "./", remove the "./"
            if line_count == 0 and line.startswith("./"):
                line = line[2:]

            # Count the number of indentation characters
            if identchar == "tab":
                identation = line.count("\t")
            else:
                identation = line.count(identchar)

            identlevel = identation // identsize
            item = line.strip(" -└─├│  ")
            isdirectory = None

            # Check if directories are indicated by trailing slashes
            if dirs_end_with_slashes:
                if item[-1] == "/":
                    isdirectory = True
            else:
                # Determine if the item is a directory based on the absence of a file extension
                isdirectory = not(bool(re.match(file_with_extension_pattern, item)))
                if isdirectory:
                    item += "/"
            
            if identlevel == 0:
                if isdirectory:
                    directory_stack = [item]
                    list_dirs_to_create.append("".join(directory_stack))
                else:
                    list_files_to_create.append(item)

            else:
                if isdirectory:
                    if identlevel == len(directory_stack):
                        directory_stack.append(item)
                    else:
                        directory_stack = directory_stack[:identlevel] + [item]
                    list_dirs_to_create.append("".join(directory_stack))
                else:
                    directory_stack = directory_stack[:identlevel]
                    path = "".join(directory_stack + [item])
                    list_files_to_create.append(path)   
            line_count += 1       
    return list_dirs_to_create, list_files_to_create

def create_dirs_and_files(filetree, root_folder="project", identchar=" ", identsize=1, dirs_end_with_slashes=False):
    """
    Creates directories and files based on a simple tree structure. It works with file texts generated from the tree command.

    Args:
        filetree (str): A string representation of the directory and file structure.
        root_folder (str, optional): The root folder where the structure will be created. Defaults to "project".
        identchar (str, optional): The character used for indentation in the filetree. Defaults to " ".
        identsize (int, optional): The number of identchar characters that represent one level of indentation. Defaults to 1.
        dirs_end_with_slashes (bool, optional): If True, directories in the filetree should end with slashes. Defaults to True.

    Example:
        filetree = '''
        dir1/
         file1.txt
         file2.txt
        dir2/
         subdir1/
          file3.txt
        '''
        create_dirs_and_files(filetree)
    """

    diretorios, files = parse_tree(filetree, identchar=identchar, identsize=identsize, dirs_end_with_slashes=dirs_end_with_slashes)

    rootpath = os.path.join(os.getcwd(), root_folder)
    os.makedirs(rootpath, exist_ok=True)

    for diretorio in diretorios:
        dir_path = os.path.join(rootpath, diretorio)
        os.makedirs(dir_path, exist_ok=True)

    for file in files:
        dir_path, file_name = os.path.split(file)
        path_file = os.path.join(rootpath, dir_path, file_name)


        with open(path_file, 'w') as f:
            pass                   

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate directories and files based on a file tree structure (given as a text file).")
    parser.add_argument("file", help="The path to the file containing the directory tree structure.")
    parser.add_argument("--root", default="project", help="The root folder where the directories and files will be created. Defaults to 'project'.")
    parser.add_argument("--identchar", default=" ", help="The character used for indentation in the file tree. Defaults to ' '. (Warning: Some editors place spaces in text files when you press tab!)")
    parser.add_argument("--identsize", default=1, type=int, help="The number of identchar characters that represent one level of indentation. Defaults to 1.")
    args = parser.parse_args()

    create_dirs_and_files(args.file, args.root, args.identchar, args.identsize)
