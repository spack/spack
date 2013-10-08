import os
import re
import functools
from spack.util.filesystem import new_path

def memoized(obj):
    """Decorator that caches the results of a function, storing them
       in an attribute of that function."""
    cache = obj.cache = {}
    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer


def list_modules(directory):
    """Lists all of the modules, excluding __init__.py, in
       a particular directory."""
    for name in os.listdir(directory):
        if name == '__init__.py':
            continue

        path = new_path(directory, name)
        if os.path.isdir(path):
            init_py = new_path(path, '__init__.py')
            if os.path.isfile(init_py):
                yield name

        elif name.endswith('.py'):
            yield re.sub('.py$', '', name)
