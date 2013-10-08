
def env_flag(name):
    if name in os.environ:
        return os.environ[name].lower() == "true"
    return False


def path_set(var_name, directories):
    path_str = ":".join(str(dir) for dir in directories)
    os.environ[var_name] = path_str


def path_put_first(var_name, directories):
    """Puts the provided directories first in the path, adding them
       if they're not already there.
    """
    path = os.environ.get(var_name, "").split(':')

    for dir in directories:
        if dir in path:
            path.remove(dir)

    new_path = tuple(directories) + tuple(path)
    path_set(var_name, new_path)


def pop_keys(dictionary, *keys):
    for key in keys:
        if key in dictionary:
            dictionary.pop(key)
