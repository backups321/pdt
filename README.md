# PRINT DIRECTORY TREE

Print out the directory structure of the input path in a tree format.

## Usage - 1

```python
Create a 'dictionary.json' file and provide descriptions for files/folders you want to annotate with arrows as follows:
{
    "README.md":"The top-level README for developers using this project.",
    "files/folder name":"description",
    "files/folder name":"description",
    "files/folder name":"description",
}
```

```bash
cd /directory/where/print_directory_tree.py/is/located
```
```bash
python print_directory_tree.py /The/path/of/the/project/whose/directory/structure/you/want/to/print --max_file_num 3 --arrow --tabs_num 8 --description_dict_file dictionary.json
```


## Usage - 2

```python
# Import libraries
import os
import pathlib
import glob
import unicodedata

def print_directory_tree(path, layer_num=0, last_dir=False, indent_current='    ', count=0, max_file_num=3, dictionary = {}, arrow = False, tabs_num = 10):
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
        indent = ' '*((tabs_num - layer_num) * 6 - sum(2 if unicodedata.east_asian_width(c) in 'FWA' else 1 for c in current_dir)) if arrow == True else ''
        branch_format = ('<- ' if layer_num == 1 else ' <- ') if arrow == True else ''
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
                path = p, 
                layer_num = layer_num + 1, 
                last_dir = i == len(paths) - 1, 
                indent_current = indent_lower, 
                max_file_num = max_file_num, 
                dictionary = dictionary, 
                arrow = arrow, 
                tabs_num = tabs_num
                )

# A dictionary containing descriptions for directory names
description_dictionary = {
    'README.md':'The top-level README for developers using this project.',
    'raw':'The original, immutable data dump.',
    'processed':'The final, canonical data sets for modeling.',
    'label':'label data',
    'docs':'A default Sphinx project.',
    'models':'Trained and serialized models, model predictions, or model summaries.',
    'reports':'Generated analysis as HTML, PDF, LaTeX, etc.',
    'figures':'Generated graphics and figures to be used in reporting.',
    'requirements.txt':'The requirements file for reproducing the analysis environment, e.g. generated with `pip freeze > requirements.txt`.',
    'setup.py':'makes project pip installable (pip install -e .) so src can be imported.',
    'src':'Source code for use in this project.',
    '__init__.py':'Makes src a Python module.',
    'dataset':'Scripts to download or generate dataset.',
    'model':'Scripts to train models and then use trained models to make predictions.',
    'visualization':'Scripts to create exploratory and results oriented visualizations.',
    'main.py':'run this python file',
    'main.ipynb':'jupyter notebook version of main.py',
}

# Print out the directory structure of the input path in a tree
print_directory_tree(
    path='/Users/user/Desktop/project_name', 
    max_file_num = 3,
    dictionary=description_dictionary, 
    arrow=True, 
    tabs_num = 10)
```