from importlib import import_module

def find_class(class_path):
    (module_name, class_name) = class_path.rsplit('.', 1)
    module = import_module(module_name)

    if hasattr(module, class_name):
        return getattr(module, class_name)
    else:
        raise ImportError, "Cannot find class {} in module {}".format(class_name, module_name)
