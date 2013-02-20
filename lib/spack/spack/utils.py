import os
import re
import errno
import shutil
import subprocess
import multiprocessing
from itertools import product
import functools
from contextlib import closing, contextmanager

import tty

# Supported archvie extensions.
PRE_EXTS = ["tar"]
EXTS     = ["gz", "bz2", "xz", "Z", "zip", "tgz"]

# Add EXTS last so that .tar.gz is matched *before* tar.gz
ALLOWED_ARCHIVE_TYPES = [".".join(l) for l in product(PRE_EXTS, EXTS)] + EXTS


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


def install(src, dest):
    tty.info("Installing %s to %s" % (src, dest))
    shutil.copy(src, dest)


@contextmanager
def working_dir(dirname):
    orig_dir = os.getcwd()
    os.chdir(dirname)
    yield
    os.chdir(orig_dir)


def mkdirp(*paths):
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)
        elif not os.path.isdir(path):
            raise OSError(errno.EEXIST, "File alredy exists", path)


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


def remove_items(item_list, *items):
    for item in items:
        if item in item_list:
            item_list.remove(item)


def has_whitespace(string):
    return re.search(r'\s', string)


def new_path(prefix, *args):
    path=str(prefix)
    for elt in args:
        path = os.path.join(path, str(elt))

    if has_whitespace(path):
        tty.die("Invalid path: '%s'.  Use a path without whitespace." % path)

    return path


def ancestor(dir, n=1):
    """Get the nth ancestor of a directory."""
    parent = os.path.abspath(dir)
    for i in range(n):
        parent = os.path.dirname(parent)
    return parent


class Executable(object):
    """Class representing a program that can be run on the command line."""
    def __init__(self, name):
        self.exe = name.split(' ')

    def add_default_arg(self, arg):
        self.exe.append(arg)

    def __call__(self, *args, **kwargs):
        """Run the executable with subprocess.check_output, return output."""
        return_output = kwargs.get("return_output", False)
        fail_on_error = kwargs.get("fail_on_error", True)

        quoted_args = [arg for arg in args if re.search(r'^"|^\'|"$|\'$', arg)]
        if quoted_args:
            tty.warn("Quotes in package command arguments can confuse shell scripts like configure.",
                     "The following arguments may cause problems when executed:",
                     str("\n".join(["    "+arg for arg in quoted_args])),
                     "Quotes aren't needed because spack doesn't use a shell.  Consider removing them")

        cmd = self.exe + list(args)
        tty.verbose(cmd)

        if return_output:
            return subprocess.check_output(cmd)
        elif fail_on_error:
            return subprocess.check_call(cmd)
        else:
            return subprocess.call(cmd)

    def __repr__(self):
        return "<exe: %s>" % self.exe


def which(name, **kwargs):
    """Finds an executable in the path like command-line which."""
    path     = kwargs.get('path', os.environ.get('PATH', '').split(os.pathsep))
    required = kwargs.get('required', False)

    if not path:
        path = []

    for dir in path:
        exe = os.path.join(dir, name)
        if os.access(exe, os.X_OK):
            return Executable(exe)

    if required:
        tty.die("spack requires %s.  Make sure it is in your path." % name)
    return None


def stem(path):
    """Get the part of a path that does not include its compressed
       type extension."""
    for type in ALLOWED_ARCHIVE_TYPES:
        suffix = r'\.%s$' % type
        if re.search(suffix, path):
            return re.sub(suffix, "", path)
    return path


def decompressor_for(path):
    """Get the appropriate decompressor for a path."""
    tar = which('tar', required=True)
    tar.add_default_arg('-xf')
    return tar


def md5(filename, block_size=2**20):
    import hashlib
    md5 = hashlib.md5()
    with closing(open(filename)) as file:
        while True:
            data = file.read(block_size)
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()
