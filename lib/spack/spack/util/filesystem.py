import os
import re
import shutil
import errno
from contextlib import contextmanager, closing

import spack.tty as tty
from spack.util.compression import ALLOWED_ARCHIVE_TYPES

def install(src, dest):
    """Manually install a file to a particular location."""
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


def new_path(prefix, *args):
    path=str(prefix)
    for elt in args:
        path = os.path.join(path, str(elt))

    if re.search(r'\s', path):
        tty.die("Invalid path: '%s'.  Use a path without whitespace." % path)

    return path


def ancestor(dir, n=1):
    """Get the nth ancestor of a directory."""
    parent = os.path.abspath(dir)
    for i in range(n):
        parent = os.path.dirname(parent)
    return parent


def stem(path):
    """Get the part of a path that does not include its compressed
       type extension."""
    for type in ALLOWED_ARCHIVE_TYPES:
        suffix = r'\.%s$' % type
        if re.search(suffix, path):
            return re.sub(suffix, "", path)
    return path


def md5(filename, block_size=2**20):
    """Computes the md5 hash of a file."""
    import hashlib
    md5 = hashlib.md5()
    with closing(open(filename)) as file:
        while True:
            data = file.read(block_size)
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()
