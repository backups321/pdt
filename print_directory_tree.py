import os
import pathlib
import glob
import unicodedata
import argparse
import json

def print_directory_tree(path, layer_num=0, last_dir=False, indent_current='    ', count=0, max_file_num=3, dictionary={}, arrow=False, tabs_num=10):
    """Print out the directory structure of the input path in a tree format.

    Parameters:
    -----------
    path : str
        The path of the project whose directory structure you want to print.

    layer_num : int, optional
        The current layer number (default is 0).

    last_dir : bool, optional
        Specifies whether the current directory is the last one in the parent directory.

    indent_current : str, optional
        The string used for indentation at the current layer (default is four spaces '    ').

    count : int, optional
        A counter used for tracking the number of files within a specific folder.

    max_file_num : int, optional
        The maximum number of files to print within a single folder.

    dictionary : dict, optional
        A dictionary containing descriptions for directory names.

    arrow : bool, optional
        Specifies whether to include arrow symbols to indicate the hierarchy (default is False).

    tabs_num : int, optional
        The number of tabs used for indentation in the tree structure (default is 10).
    """

    # Ensure the path is absolute
    if not pathlib.Path(path).is_absolute():
        path = str(pathlib.Path(path).resolve())

    # Get the current directory name
    current_dir = os.path.basename(path)

    # Print the current directory (folders)
    if layer_num == 0:
        print(current_dir)
    else:
        branch = '└─ ' if last_dir else '├─ '
        description = dictionary.get(current_dir, '')
        output_format = '{indent}{branch}{dirname}{description}'
        indent = ' '*((tabs_num - layer_num) * 6 - sum(2 if unicodedata.east_asian_width(c) in 'FWA' else 1 for c in current_dir)) if arrow else ''
        branch_format = ('<- ' if layer_num == 1 else ' <- ') if arrow else ''
        print(output_format.format(indent=indent_current, branch=branch, dirname=current_dir, description=(indent + branch_format + description) if description else ''))

    # Get paths in the current directory
    paths = [p for p in glob.glob(os.path.join(path, '*')) if os.path.isdir(p) or os.path.isfile(p)]
    paths.sort()
    
    # Print the current directory (files)
    for i, p in enumerate(paths):
        indent_lower = indent_current

        if layer_num != 0:
            indent_lower += '     ' if last_dir else '│    '

        if os.path.isfile(p):
            count += 1
            branch = '└─ ' if i == len(paths) - 1 else '├─ '

            if count > max_file_num:
                print('{indent}{branch}...'.format(indent=indent_lower, branch='└─ '))
            else:
                filename = os.path.basename(p)
                description = dictionary.get(filename, '')
                indent = ' '*((tabs_num - layer_num - 1) * 6 - sum(2 if unicodedata.east_asian_width(c) in 'FWA' else 1 for c in filename))
                branch_format = '<- ' if layer_num == 0 else ' <- '
                output_format = '{indent}{branch}{filename}{description}'
                print(output_format.format(indent=indent_lower, branch=branch, filename=filename, description=(indent + branch_format + description) if description else ''))

        # Recursive
        if os.path.isdir(p):
            count = 0
            print_directory_tree(
                path=p, 
                layer_num=layer_num + 1, 
                last_dir=i == len(paths) - 1, 
                indent_current=indent_lower, 
                max_file_num=max_file_num, 
                dictionary=dictionary, 
                arrow=arrow, 
                tabs_num=tabs_num
            )

if __name__ == "__main__":
    # Command-line arguments processing
    parser = argparse.ArgumentParser(description='Print the directory structure in a tree format.')
    parser.add_argument('path', type=str, help='The path of the project whose directory structure you want to print.')
    parser.add_argument('--max_file_num', type=int, default=3, help='The maximum number of files to print within a single folder.')
    parser.add_argument('--arrow', action='store_true', help='Include arrow symbols to indicate the hierarchy.')
    parser.add_argument('--tabs_num', type=int, default=10, help='The number of tabs used for indentation in the tree structure.')
    parser.add_argument('--description_dict_file', type=str, help='Path to the JSON file containing the description dictionary.')
    args = parser.parse_args()

    # Loading the description dictionary
    if args.description_dict_file:
        with open(args.description_dict_file, 'r') as json_file:
            description_dictionary = json.load(json_file)
    else:
        description_dictionary = {}

    print_directory_tree(
        path=args.path,
        max_file_num=args.max_file_num,
        dictionary=description_dictionary,
        arrow=args.arrow,
        tabs_num=args.tabs_num
    )





