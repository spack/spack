# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys
from itertools import product

from llnl.util.filesystem import exploding_archive_catch

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


def _untar(archive_file):
    """ Untar archive. Prefer native Python `tarfile`
    but fall back to system utility failing
    to find the native Python module (tar on Unix).
    Filters archives through native support gzip and xz
    compression formats.

    Args:
        archive_file (str): absolute path to the archive to be extracted.
        Can be one of .tar(.[gz|bz2|xz|Z]) or .(tgz|tbz|tbz2|txz).
    """
    _, ext = os.path.splitext(archive_file)
    outfile = os.path.basename(archive_file.strip(ext))
    remnant = os.path.join(os.getcwd(), archive_file)
    lzma = [".xz", ".txz"]
    tmp_src = os.path.join(os.getcwd(), 'tmp-src')
    with exploding_archive_catch(os.getcwd(), tmp_src):
        try:
            import tarfile
            if ext in lzma:
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
            if is_windows and ext in lzma:
                return _7zip(archive_file)
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
    _, ext = os.path.splitext(archive_file)
    decompressed_file = os.path.basename(archive_file.strip(ext))
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
    _, ext = os.path.splitext(archive_file)
    decompressed_file = os.path.basename(archive_file.strip(ext))
    working_dir = os.getcwd()
    destination_abspath = os.path.join(working_dir, decompressed_file)
    try:
        import gzip
        f_in = gzip.open(archive_file, "rb")
        with open(destination_abspath, "wb") as f_out:
            f_out.write(f_in.read())
    except ImportError:
        gzip = which("gzip")
        gzip.add_default_arg("-d")
        gzip(archive_file)
    return destination_abspath


def _unzip(archive_file):
    """
    Extract Zipfile, searching for unzip system executable
    If unavailable, search for 'tar' executable on system and use instead

    Args:
        archive_file (str): absolute path of the file to be decompressed
    """

    destination_abspath = os.getcwd()
    exe = 'unzip'
    arg = '-q'
    if is_windows:
        exe = 'tar'
        arg = '-xf'
    unzip = which(exe, required=True)
    unzip.add_default_arg(arg)
    unzip(archive_file)
    return destination_abspath


def _unZ(archive_file):
    if is_windows:
        result = _7zip(archive_file)
    else:
        result = _untar(archive_file)
    return result


def _7zip(archive_file):
    """Unpack/decompress with 7z executable
    7z is able to handle a number file extensions however
    it may not be available on system.

    Without 7z, Windows users with certain versions of Python may
    be unable to extract .xz files, and all Windows users will be unable
    to extract .Z files. If we cannot find 7z either externally or a
    Spack installed copy, we fail, but inform the user that 7z can
    be installed via `spack install 7zip`

    Args:
        archive_file (str): absolute path of file to be unarchived
    """
    _, ext = os.path.splitext(archive_file)
    outfile = os.path.basename(archive_file.strip(ext))
    with exploding_archive_catch(os.getcwd(), os.getcwd()):
        _7z = which('7z')
        if not _7z:
            raise CommandNotFoundError("7z unavailable on Windows,\
unable to extract %s files. 7z can be installed via Spack" % ext)
        _7z.add_default_arg('e')
        _7z(archive_file)
    return outfile


def decomp_composer(funcA, funcB):
    """Utility to compose two callables
    into one, where funcA is invoked on the
    return of funcB, and funcB is called on
    the arguments supplied to the returned
    callable

    Args:
        funcA: callable to be invoked on funcB
        funcB: callable to be passed into funcA,
            called on arguments passed to returned
            callable

    Returns:
        A callable whose arguments will be passed to funcB,
        and will then invoke funA on the return from funcB
    """

    def b(*args, **kwargs):
        funcA(funcB(*args, **kwargs))
    return b


def decompressor_for(path, ext=None):
    """Wrapper for select_decompressor_for, returns
    a function pointer to appropriate decompression
    algorithm.

    On Unix - simply invokes select_decompressor_for

    On Windows - archives with one extension are
    passed through to select_decompressor_for. Files
    with two extensions (i.e. .tar.gz) are decomposed
    into their components (.tar and .gz) and the results
    of handling each extension are fed into the handler of
    the next.

    Args:
        path (str): path of the archive file requiring decompression
        ext (str): Extension of archive file
    """
    if ext:
        if not allowed_archive(ext):
            raise CommandNotFoundError("Unrecognized file extension")
    if sys.platform == 'win32':
        if ext is None:
            ext = extension(path)
        ext_l = [] if not ext else ext.split(".")
        # special case as there is no consistently
        # available native python tool for .Z files
        if not ext_l[1:] or re.search(r'.Z|xz', ext):
            return select_decompressor_for(path, ext)
        else:
            return decomp_composer(
                decompressor_for(path, ext_l[0]),
                decompressor_for(
                    path, ext=".".join(ext_l[1:]))
            )
    else:
        return select_decompressor_for(path, ext)


def select_decompressor_for(path, extension=None):
    """Get the appropriate decompressor for a path.
    """
    if ((extension and re.match(r'\.?zip$', extension)) or
            path.endswith('.zip')):
        return _unzip
    if extension and re.match(r'gz', extension):
        return _gunzip
    if extension and re.match(r'bz2', extension):
        return _bunzip2
    # Catch .Z files here. Python does not have native support
    # of any kind for .Z files. In these cases, we rely on external
    # tools such as tar, 7z, or uncompressZ
    if extension and re.match(r'Z$', extension):
        return _unZ

    # Use python (or system) tarfile for
    # files with .xz style extensions due to inconsistent
    # availability of the lzma module needed to decompress
    # .xz files
    if extension:
        return _untar

    raise CommandNotFoundError("Cannot unpack archive with extension: %s" % extension)


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
