# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys
from itertools import product

from six import string_types

from spack.util.executable import CommandNotFoundError, which

# Supported archive extensions.
PRE_EXTS   = ["tar", "TAR"]
EXTS       = ["gz", "bz2", "xz", "Z"]
NOTAR_EXTS = ["zip", "tgz", "tbz", "tbz2", "txz"]

# Add PRE_EXTS and EXTS last so that .tar.gz is matched *before* .tar or .gz
ALLOWED_ARCHIVE_TYPES = [".".join(ext) for ext in product(
    PRE_EXTS, EXTS)] + PRE_EXTS + EXTS + NOTAR_EXTS

is_windows = sys.platform == 'win32'


def allowed_archive(path):
    return any(path.endswith(t) for t in ALLOWED_ARCHIVE_TYPES)


def try_exec(exec):
    try:
        return which(exec, required=True)
    except CommandNotFoundError:
        pass
    return None


def derive_fallback_executable(fallback):
    for strategy in fallback:
        test_exec = strategy
        islist = False
        if not isinstance(strategy, string_types):
            test_exec = strategy[0]
            islist = True
        executor = try_exec(test_exec)
        if executor:
            args = ''
            if islist:
                args = strategy[1:]
            return executor, args
    return None, None


def _system_fallback(archive_file):
    import spack.config as sconf
    outfile = os.path.basename(archive_file)
    fallback = sconf.config.get('config:fallback_decompression_strategy')
    if isinstance(fallback, string_types):
        fallback = [fallback]
    extractor, args = derive_fallback_executable(fallback)
    if not extractor:
        raise CommandNotFoundError("Unable to find system fallback unpacking utility")
    if args:
        [extractor.add_default_arg(arg) for arg in args[1:]]
    extractor(archive_file)
    return outfile


def _untar(archive_file):
    """ Untar archive. Prefer native Python `tarfile`
    but fall back to system utility failing
    to find the native Python module (tar on Unix).
    Filters archives through native support gzip and xz
    compression formats.

    Args:
        archive_file (str): absolute path to the archive to be extracted.
        Can be one of .tar.(gz|bz2|xz|Z) or .(tgz|tbz|tbz2|txz).
    """
    outfile = os.path.basename(archive_file)
    remnant = os.path.join(os.getcwd(), outfile)
    try:
        import tarfile
        if ext in [".xz", ".txz"]:
            # Sucessful import of lzma module indicates
            # support for xz compression type
            import lzma  # noqa # novermin
        tar = tarfile.open(archive_file)
        tar.extractall()
        tar.close()
        if sys.platform == "win32":
            if os.path.exists(remnant):
                os.remove(remnant)
    except ImportError:
        tar = which('tar', required=True)
        tar.add_default_arg('-oxf')
        tar(archive_file)
    return outfile


def _bunzip2(archive_file):
    """ Use Python's bz2 module to decompress bz2 compressed archives
    Fall back to system utility failing to find Python module `bz2`

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
    """ Decompress `.gz` extensions. Prefer native Python `gzip` module.
    Failing back to system utility gunzip.
    Like gunzip, but extracts in the current working directory
    instead of in-place.

    Args:
        archive_file (str): absolute path of the file to be decompressed
    """
    decompressed_file = os.path.basename(archive_file.strip('.gz'))
    working_dir = os.getcwd()
    destination_abspath = os.path.join(working_dir, decompressed_file)
    try:
        import gzip
        f_in =  gzip.open(archive_file, "rb")
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

    If unavailable, search for 'unzip' executable on system and use instead

    Args:
        archive_file (str): absolute path of the file to be decompressed
    """

    destination_abspath = os.getcwd()
    try:
        from zipfile import ZipFile
        zf = ZipFile(archive_file, 'r')
        zf.extractall(destination_abspath)
        zf.close()
    except ImportError:
        exe = 'unzip'
        arg = '-q'
        if is_windows:
            exe = 'tar'
            arg = '-xf'
        unzip = which(exe, required=True)
        unzip.add_default_arg(arg)
        unzip(archive_file)
    return destination_abspath


def composer(funcA):
    """Utility method currying function pointers
    returns a function pointer to be called with
    a function to be curried with the current function
    argument.

    Args:
        funcA (function): Function to be curried.
    """
    def b(funcB):
        def c(*args, **kwargs):
            return funcA(funcB(*args, **kwargs))
        return c
    return b


def decompressor_for(path, ext=None):
    """Wrapper for select_decompressor_for, returns
    a function pointer to appropriate decompression
    algorithm.

    On Unix - simply invokes select_decompressor_for

    On Windows - archives with one extension are
    passed through to select_decompressor_for. Multiple
    extension archives are decomposed into their component
    extensions and the requsite decompression algorithms are
    curried and returned as a single callable function pointer.

    Args:
        path (str): path of the archive file requiring decompression
        ext (str): Extension of archive file
    """
    if ext:
        assert allowed_archive(ext)
    if sys.platform == 'win32':
        if ext is None:
            ext = extension(path)
        ext_l = ext.split(".")
        # special case as there is no consistently
        # available native python tool for .Z files
        if not ext_l[1:] or re.search(r'.Z|xz',ext):
            return select_decompressor_for(path, ext)
        else:
            return composer(
                decompressor_for(path, ext_l[0])
            )(
                decompressor_for(
                    path, ext=".".join(ext_l[1:]))
            )
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
    # Catch unexpected extensions and .Z files
    # here. Python does not have native support
    # of any kind for .Z files. In these cases, fall back
    # to system defined strategy.
    # Additionally, use python (or system) tarfile for
    # files with .xz style extensions due to inconsistent
    # availability of the lzma module needed to decompress
    # .xz files
    if extension and not re.search(r'Z$', extension):
        return _untar
    return _system_fallback

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
