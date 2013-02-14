import os
import subprocess
import re
from itertools import product
from contextlib import closing

import tty

# Supported archvie extensions.
PRE_EXTS = ["tar"]
EXTS     = ["gz", "bz2", "xz", "Z", "zip", "tgz"]

# Add EXTS last so that .tar.gz is matched *before* tar.gz
ALLOWED_ARCHIVE_TYPES = [".".join(l) for l in product(PRE_EXTS, EXTS)] + EXTS


def has_whitespace(string):
    return re.search(r'\s', string)


def new_path(prefix, *args):
    path=prefix
    for elt in args:
        path = os.path.join(path, elt)

    if has_whitespace(path):
        tty.die("Invalid path: '%s'.  Use a path without whitespace.")

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
        else:
            return subprocess.check_call(cmd)

    def __repr__(self):
        return "<exe: %s>" % self.exe


def which(name, path=None):
    """Finds an executable in the path like command-line which."""
    if not path:
        path = os.environ.get('PATH', '').split(os.pathsep)
    if not path:
        return None

    for dir in path:
        exe = os.path.join(dir, name)
        if os.access(exe, os.X_OK):
            return Executable(exe)
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
    if which("tar"):
        return Executable("tar -xf")
    else:
        tty.die("spack requires tar.  Make sure it's on your path.")


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
