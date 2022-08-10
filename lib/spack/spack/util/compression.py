# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import shutil
import sys
from itertools import product

from spack.util.executable import CommandNotFoundError, which

# Supported archive extensions.
PRE_EXTS = ["tar", "TAR"]
EXTS = ["gz", "bz2", "xz", "Z"]
NOTAR_EXTS = ["zip", "tgz", "tbz", "tbz2", "txz"]

# Add PRE_EXTS and EXTS last so that .tar.gz is matched *before* .tar or .gz
ALLOWED_ARCHIVE_TYPES = (
    [".".join(ext) for ext in product(PRE_EXTS, EXTS)] + PRE_EXTS + EXTS + NOTAR_EXTS
)

is_windows = sys.platform == "win32"


def bz2_support():
    try:
        import bz2  # noqa: F401

        return True
    except ImportError:
        return False


def gzip_support():
    try:
        import gzip  # noqa: F401

        return True
    except ImportError:
        return False


def lzma_support():
    try:
        import lzma  # noqa: F401 # novm

        return True
    except ImportError:
        return False


def tar_support():
    try:
        import tarfile  # noqa: F401

        return True
    except ImportError:
        return False


def allowed_archive(path):
    return False if not path else any(path.endswith(t) for t in ALLOWED_ARCHIVE_TYPES)


def _untar(archive_file):
    """Untar archive. Prefer native Python `tarfile`
    but fall back to system utility if there is a failure
    to find the native Python module (tar on Unix).
    Filters archives through native support gzip and xz
    compression formats.

    Args:
        archive_file (str): absolute path to the archive to be extracted.
        Can be one of .tar(.[gz|bz2|xz|Z]) or .(tgz|tbz|tbz2|txz).
    """
    _, ext = os.path.splitext(archive_file)
    outfile = os.path.basename(archive_file.strip(ext))

    tar = which("tar", required=True)
    tar.add_default_arg("-oxf")
    tar(archive_file)
    return outfile


def _bunzip2(archive_file):
    """Use Python's bz2 module to decompress bz2 compressed archives
    Fall back to system utility failing to find Python module `bz2`

    Args:
        archive_file (str): absolute path to the bz2 archive to be decompressed
    """
    _, ext = os.path.splitext(archive_file)
    compressed_file_name = os.path.basename(archive_file)
    decompressed_file = os.path.basename(archive_file.strip(ext))
    working_dir = os.getcwd()
    archive_out = os.path.join(working_dir, decompressed_file)
    copy_path = os.path.join(working_dir, compressed_file_name)
    if bz2_support():
        import bz2

        f_bz = bz2.BZ2File(archive_file, mode="rb")
        with open(archive_out, "wb") as ar:
            shutil.copyfileobj(f_bz, ar)
        f_bz.close()
    else:
        shutil.copy(archive_file, copy_path)
        bunzip2 = which("bunzip2", required=True)
        bunzip2.add_default_arg("-q")
        return bunzip2(copy_path)
    return archive_out


def _gunzip(archive_file):
    """Decompress `.gz` extensions. Prefer native Python `gzip` module.
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
    if gzip_support():
        import gzip

        f_in = gzip.open(archive_file, "rb")
        with open(destination_abspath, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        f_in.close()
    else:
        _system_gunzip(archive_file)
    return destination_abspath


def _system_gunzip(archive_file):
    _, ext = os.path.splitext(archive_file)
    decompressed_file = os.path.basename(archive_file.strip(ext))
    working_dir = os.getcwd()
    destination_abspath = os.path.join(working_dir, decompressed_file)
    compressed_file = os.path.basename(archive_file)
    copy_path = os.path.join(working_dir, compressed_file)
    shutil.copy(archive_file, copy_path)
    gzip = which("gzip")
    gzip.add_default_arg("-d")
    gzip(copy_path)
    return destination_abspath


def _unzip(archive_file):
    """
    Extract Zipfile, searching for unzip system executable
    If unavailable, search for 'tar' executable on system and use instead

    Args:
        archive_file (str): absolute path of the file to be decompressed
    """

    destination_abspath = os.getcwd()
    exe = "unzip"
    arg = "-q"
    if is_windows:
        exe = "tar"
        arg = "-xf"
    unzip = which(exe, required=True)
    unzip.add_default_arg(arg)
    unzip(archive_file)
    return destination_abspath


def _unZ(archive_file):
    if is_windows:
        result = _7zip(archive_file)
    else:
        result = _system_gunzip(archive_file)
    return result


def _lzma_decomp(archive_file):
    """Decompress lzma compressed files. Prefer Python native
    lzma module, but fall back on command line xz tooling
    to find available Python support. This is the xz command
    on Unix and 7z on Windows"""
    if lzma_support():
        import lzma  # novermin

        _, ext = os.path.splitext(archive_file)
        decompressed_file = os.path.basename(archive_file.strip(ext))
        archive_out = os.path.join(os.getcwd(), decompressed_file)
        with open(archive_out, "wb") as ar:
            with lzma.open(archive_file) as lar:
                shutil.copyfileobj(lar, ar)
    else:
        if is_windows:
            return _7zip(archive_file)
        else:
            return _xz(archive_file)


def _xz(archive_file):
    """Decompress lzma compressed .xz files via xz command line
    tool. Available only on Unix
    """
    if is_windows:
        raise RuntimeError("XZ tool unavailable on Windows")
    _, ext = os.path.splitext(archive_file)
    decompressed_file = os.path.basename(archive_file.strip(ext))
    working_dir = os.getcwd()
    destination_abspath = os.path.join(working_dir, decompressed_file)
    compressed_file = os.path.basename(archive_file)
    copy_path = os.path.join(working_dir, compressed_file)
    shutil.copy(archive_file, copy_path)
    xz = which("xz", required=True)
    xz.add_default_arg("-d")
    xz(copy_path)
    return destination_abspath


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
    _7z = which("7z")
    if not _7z:
        raise CommandNotFoundError(
            "7z unavailable,\
unable to extract %s files. 7z can be installed via Spack"
            % ext
        )
    _7z.add_default_arg("e")
    _7z(archive_file)
    return outfile


def decompressor_for(path, ext):
    """Returns a function pointer to appropriate decompression
    algorithm based on extension type.

    Args:
        path (str): path of the archive file requiring decompression
        ext (str): Extension of archive file
    """
    if not allowed_archive(ext):
        raise CommandNotFoundError(
            "Cannot extract archive, \
unrecognized file extension: '%s'"
            % ext
        )

    if re.match(r"\.?zip$", ext) or path.endswith(".zip"):
        return _unzip

    if re.match(r"gz", ext):
        return _gunzip

    if re.match(r"bz2", ext):
        return _bunzip2

    # Python does not have native support
    # of any kind for .Z files. In these cases,
    # we rely on external tools such as tar,
    # 7z, or uncompressZ
    if re.match(r"Z$", ext):
        return _unZ

    # Python and platform may not have support for lzma
    # compression. If no lzma support, use tools available on systems
    # 7zip on Windows and the xz tool on Unix systems.
    if re.match(r"xz", ext):
        return _lzma_decomp

    if ("xz" in ext or "Z" in ext) and is_windows:
        return _7zip

    return _untar


def strip_extension(path):
    """Get the part of a path that does not include its compressed
    type extension."""
    for type in ALLOWED_ARCHIVE_TYPES:
        suffix = r"\.%s$" % type
        if re.search(suffix, path):
            return re.sub(suffix, "", path)
    return path


def extension(path):
    """Get the archive extension for a path."""
    if path is None:
        raise ValueError("Can't call extension() on None")

    # Strip sourceforge suffix.
    if re.search(r"((?:sourceforge.net|sf.net)/.*)/download$", path):
        path = os.path.dirname(path)

    for t in ALLOWED_ARCHIVE_TYPES:
        suffix = r"\.%s$" % t
        if re.search(suffix, path):
            return t
    return None
