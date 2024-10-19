
# Tree File to Directory Structure

This Python script generates directories and files based on a tree structure provided in a text file. It's particularly useful for recreating directory structures from the output of the `tree` command or similar tools.

It can also parse other tree styles, usually given as examples for larger projects in different languages.

Important: files must have extensions, otherwise they will be treated as directories (there is some attempt to deal with that in other tree formating styles, in which directories end with slahes, but currently this is how it works.)

## Usage

1.  **Save your tree structure in a text file.** Ensure the file uses consistent indentation (either tabs or spaces, but not both) to represent the hierarchy.

For example, you can generate a treefile for a given directory by running
    
```bash
tree -a -L 3 > tree_as_text_file.txt
```

2.  **Run the script:**

```bash
python tree_to_dirs.py <tree_as_text_file_path> [--root <root_folder>] [--identchar <indentation_character>] [--identsize <indentation_size>]
```

- `<tree_as_text_file_path>`: Path to the text file containing the tree structure.
- `--root`: (Optional) The root folder where the structure will be created. Defaults to "project".
- `--identchar`: (Optional) The indentation character used in the file. Defaults to " " (space).
- `--identsize`: (Optional) The number of indentation characters per level. Defaults to 1.

## Example

The content of `other_tree_format.txt` is not in standard tree format:

```
libA/
- include/
    - libA/
        - sourceA.h
- privateHeaderA1.h
- privateHeaderA2.h
- sourceA.cpp
libB/
    - include/
        - libB/
            - sourceB.h
    - submodule/
        - submodule.h
        - submodule.cpp
    - privateHeaderB1.h
    - privateHeaderB2.h
    - sourceB.cpp
    - sourceB_impl.h
    - sourceB_impl.cpp
libC/
    - include/
        - libC/
            - sourceC.h
    - privateHeaderC1.h
    - privateHeaderC2.h
    - sourceC.cpp
main.cpp
```

By running:

```bash
./generate_files_from_simpletree.py other_tree_format.txt --root project
```

... you will generate the respective folder/files structure.

You can generate a standard `tree` of this folder running `tree -a ./project > project_tree.txt`

And create everything again in another root folder:

```bash
./generate_files_from_simpletree.py other_tree_format.txt --root project2
```

Important Notes

Indentation: The script relies on consistent indentation to determine the hierarchy. Use either tabs or spaces, but not both, in your tree file.

## License
This script is released under the MIT License.
