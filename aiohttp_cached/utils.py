from importlib import import_module

__all__ = (
    'import_string',
)


def import_string(path):
    try:
        module_path, class_name = path.rsplit('.', 1)
    except ValueError:
        raise ImportError("%s doesn't look like a module path" % path)

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name))
