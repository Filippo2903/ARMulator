import os
import importlib.util

def load_python_file(file_path):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, 'dict', None)

def create_main_dict(directory="translation\\dictionaries"):
    main_dict = {}

    dir_path = os.path.join(os.getcwd(), directory)

    for file_name in os.listdir(dir_path):
        if file_name.endswith(".py"):
            file_path = os.path.join(dir_path, file_name)
            dict_content = load_python_file(file_path)
            
            if dict_content is not None:
                main_dict[os.path.splitext(file_name)[0]] = dict_content

    return main_dict
