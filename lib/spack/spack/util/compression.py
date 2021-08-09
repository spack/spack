# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys
from itertools import product
import shutil

from spack.util.executable import which

# Supported archive extensions.
PRE_EXTS   = ["tar", "TAR"]
EXTS       = ["gz", "bz2", "xz", "Z"]
NOTAR_EXTS = ["zip", "tgz", "tbz", "tbz2", "txz"]

# Add PRE_EXTS and EXTS last so that .tar.gz is matched *before* .tar or .gz
ALLOWED_ARCHIVE_TYPES = [".".join(ext) for ext in product(
    PRE_EXTS, EXTS)] + PRE_EXTS + EXTS + NOTAR_EXTS


def allowed_archive(path):
    return any(path.endswith(t) for t in ALLOWED_ARCHIVE_TYPES)

def _tar(archive_file):
    outfile = os.path.basename(archive_file)
    remnant = os.path.join(os.getcwd(), outfile)
    try:
        import tarfile
        tar = tarfile.open(archive_file)
        tar.extractall()
        tar.close()
        if sys.platform == "win32":
            os.remove(remnant)
    except ImportError:
        tar = which('tar', required=True)
        tar.add_default_arg('-oxf')
        tar(archive_file)
    return outfile

def _bunzip2(archive_file):
    """ Use Python's bz2 module to decompress bz2 compressed archives

    Args:
        archive_file (str): absolute path to the bz2 archive to be decompressed
    """
    decompressed_file = os.path.basename(archive_file.strip(".bz2"))
    archive_out = os.path.join(os.getcwd(), decompressed_file)
    try:
        import bz2
        f_bz = bz2.BZ2File(archive_file, mode='rb')
        with open(archive_out, 'wb') as ar:
            ar.write(f_bz.read())
        f_bz.close()
    except ImportError:
        bunzip2 = which('bunzip2', required=True)
        bunzip2.add_default_arg('-q')
        return bunzip2(archive_file)
    return archive_out

def _gunzip(archive_file):
    """Like gunzip, but extracts in the current working directory
    instead of in-place.

    Args:
        archive_file (str): absolute path of the file to be decompressed
    """
    decompressed_file = os.path.basename(archive_file.strip('.gz'))
    working_dir = os.getcwd()
    destination_abspath = os.path.join(working_dir, decompressed_file)
    try:
        import gzip
        with gzip.open(archive_file, "rb") as f_in:
            with open(destination_abspath, "wb") as f_out:
                f_out.write(f_in.read())
    except ImportError:
        gzip = which("gzip")
        gzip.add_default_arg("-d")
        gzip(archive_file)
    return destination_abspath


def _unzip(archive_file):
    """Try to use Python's zipfile, but extract in the current working
    directory instead of in-place.

    If unavailable, try unzip

    Args:
        archive_file (str): absolute path of the file to be decompressed
    """
    destination_abspath = os.getcwd()
    try:
        from zipfile import ZipFile
        with ZipFile(archive_file, 'r') as zf:
            zf.extractall(destination_abspath)
    except ImportError:
        unzip = which('unzip', required=True)
        unzip.add_default_arg('-q')
        unzip(archive_file)
    return destination_abspath


def composer(funcA):
    def b(funcB):
        def c(*args,**kwargs):
            return funcA(funcB(*args,**kwargs))
        return c
    return b


def decompressor_for(path, ext=None):
    if sys.platform == 'win32':
        if ext is None:
            ext = extension(path)
        ext_l = ext.split(".")
        if not ext_l[1:]:
            return select_decompressor_for(path, ext_l[0])
        else:
            return composer(decompressor_for(path,ext_l[0]))(decompressor_for(path, ext = ".".join(ext_l[1:])))
    else:
        return select_decompressor_for(path, ext)


def select_decompressor_for(path, extension=None):
    """Get the appropriate decompressor for a path."""
    if ((extension and re.match(r'\.?zip$', extension)) or
            path.endswith('.zip')):
        return _unzip
    if extension and re.match(r'gz', extension):
        return _gunzip
    if extension and re.match(r'bz2', extension):
        return _bunzip2
    return _tar


def strip_extension(path):
    """Get the part of a path that does not include its compressed
       type extension."""
    for type in ALLOWED_ARCHIVE_TYPES:
        suffix = r'\.%s$' % type
        if re.search(suffix, path):
            return re.sub(suffix, "", path)
    return path


def extension(path):
    """Get the archive extension for a path."""
    if path is None:
        raise ValueError("Can't call extension() on None")

    # Strip sourceforge suffix.
    if re.search(r'((?:sourceforge.net|sf.net)/.*)/download$', path):
        path = os.path.dirname(path)

    for t in ALLOWED_ARCHIVE_TYPES:
        suffix = r'\.%s$' % t
        if re.search(suffix, path):
            return t
    return None
