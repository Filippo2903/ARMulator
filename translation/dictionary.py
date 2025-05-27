import os
import importlib.util

def load_python_file(file_path):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, 'dict', None)

def create_main_dict(directory=os.path.join("translation", "dictionaries")):
    """
        Loads the language dictionary by aggregating data from multiple Python files in a directory.

        This function scans the specified directory for Python files (*.py), loads their contents
        using the `load_python_file` function, and combines them into a single dictionary.
        Each entry in the resulting dictionary is keyed by the filename (without extension),
        and its value is the corresponding loaded content.

        Args:
            directory (str): Path to the directory containing language dictionary files.

        Returns:
            dict: A dictionary aggregating all loaded language data from the directory.
    """
    main_dict = {}

    dir_path = os.path.join(os.getcwd(), directory)

    for file_name in os.listdir(dir_path):
        if file_name.endswith(".py"):
            file_path = os.path.join(dir_path, file_name)
            dict_content = load_python_file(file_path)
            
            if dict_content is not None:
                main_dict[os.path.splitext(file_name)[0]] = dict_content

    return main_dict
