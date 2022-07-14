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

from llnl.util.lang import memoized

# Supported archive extensions.
PRE_EXTS = ["tar", "TAR"]
EXTS = ["gz", "bz2", "xz", "Z"]
NOTAR_EXTS = ["zip", "tgz", "tbz", "tbz2", "txz"]

# Add PRE_EXTS and EXTS last so that .tar.gz is matched *before* .tar or .gz
ALLOWED_ARCHIVE_TYPES = (
    [".".join(ext) for ext in product(PRE_EXTS, EXTS)] + PRE_EXTS + EXTS + NOTAR_EXTS
)

is_windows = sys.platform == "win32"

try:
    import bz2 # noqa
    _bz2_support = True
except ImportError:
    _bz2_support = False


try:
    import gzip # noqa
    _gzip_support = True
except ImportError:
    _gzip_support = False


try:
    import lzma  # noqa # novermin
    _lzma_support = True
except ImportError:
    _lzma_support = False


def is_lzma_supported():
    return _lzma_support


def is_gzip_supported():
    return _gzip_support


def is_bz2_supported():
    return _bz2_support


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
    if is_bz2_supported():
        f_bz = bz2.BZ2File(archive_file, mode='rb')
        with open(archive_out, 'wb') as ar:
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
    if is_gzip_supported():
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
    if lzma_support:
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


def decompressor_for(path):
    """Returns a function pointer to appropriate decompression
    algorithm based on extension type.

    Args:
        path (str): path of the archive file requiring decompression
    """
    ext = extension(path)
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


class FileType:
    _OFFSET = 0
    _MAGIC_NUMBER = b'\x00'
    _ext = ''
    _compressed = False

    @classmethod
    @property
    def is_compression_type(cls):
        return cls._compressed

    @classmethod
    @property
    def offset(cls):
        return cls._OFFSET

    @classmethod
    @property
    def magic_number(cls):
        return cls._MAGIC_NUMBER

    @classmethod
    @property
    def extension(cls):
        return cls._ext

    @classmethod
    @property
    def header_size(cls):
        return len(cls.magic_number)

    @classmethod
    @property
    def _bytes_check(cls, magic_bytes):
        return cls._MAGIC_NUMBER == magic_bytes

    @classmethod
    def is_file_of_type(cls, iostream):
        iostream.seek(cls.offset)
        magic_bytes = iostream.read(cls.header_size)
        if cls._bytes_check(magic_bytes):
            return True
        return False

class CompressedFileType(FileType):
    _compressed = True

    @classmethod
    def decomp_in_memory(cls, filepath):
        raise RuntimeError("Implementation by subclass required")


class BZipFileType(CompressedFileType):
    _MAGIC_NUMBER = b'\x42\x5a\x68'
    _ext = 'bz2'

    @classmethod
    def decomp_in_memory(cls, filepath):
        pass


class ZCompressedFileType(CompressedFileType):
    _MAGIC_NUMBER_LZW = b'\x1f\x9d'
    _MAGIC_NUMBER_LZH = b'\x1f\xa0'
    _ext = 'Z'

    @classmethod
    @property
    def magic_number(cls):
        [cls._MAGIC_NUMBER_LZH, cls._MAGIC_NUMBER_LZW]

    @classmethod
    @property
    def header_size(cls):
        return max(len(cls._MAGIC_NUMBER_LZW), len(cls._MAGIC_NUMBER_LZH))

    @classmethod
    def decomp_in_memory(cls, filepath):
        pass


class GZipFileType(CompressedFileType):
    _MAGIC_NUMBER = b'\x1f\x8b\x08'
    _ext = 'gz'

    @classmethod
    def decomp_in_memory(cls, filepath):
        pass


class LzmaFileType(CompressedFileType):
    _MAGIC_NUMBER = b'\xfd7zXZ'
    _ext = 'xz'

    @classmethod
    def decomp_in_memory(cls, filepath):
        pass

class TarFileType(FileType):
    _OFFSET = 257
    _GNU_MAGIC = b'ustar  \0'
    _POSIX_MAGIC = b'ustar\x0000'
    _ext = 'tar'

    @classmethod
    @property
    def magic_number(cls):
        [cls._GNU_MAGIC, cls._POSIX_MAGIC]

    @classmethod
    @property
    def header_size(cls):
        return max(len(cls._GNU_MAGIC), len(cls._POSIX_MAGIC))


class ZipFleType(FileType):
    _MAGIC_NUMBER = b'PK\003\004'
    _ext = 'zip'


VALID_FILETYPES = [BZipFileType, ZCompressedFileType,
                   GZipFileType, LzmaFileType, TarFileType,
                   ZipFleType]


def extension_from_stream(stream, decompress=False):
    """Return extension represented by stream corresponding to archive file
    If stream does not represent an archive type recongized by Spack
    (see `spack.util.compression.ALLOWED_ARCHIVE_TYPES`) method will return None

    Extension type is derived by searching for identifying bytes
    in file stream.

    Args:
        stream (IOBase): stream representing a file on system
        decompress (bool) : if True, compressed files are checked
                            for archive types beneath compression i.e. tar.gz
                            default is False

    Return:
        extension (str|None): A string represting corresponding archive extension
            or None as relevant.

    """
    for arc_type in VALID_FILETYPES:
        if arc_type.is_file_of_type(stream):
            suffix_ext = arc_type.extension
            prefix_ext = ''
            if arc_type.is_compression_type() and decompress:
                # stream represents compressed file
                prefix_ext = extension_from_stream(arc_type.decomp_in_memory(stream))
            return suffix_ext if not prefix_ext else '.'.join([prefix_ext, suffix_ext])
    return None


def extension_from_file(file, decompress=False):
    """Takes filepath representing file on system.
    Opens file into memory and checks for spack supported archive types.

    Args:
        file (os.PathLike)
    """
    with open(file, 'rb') as f:
        ext = extension_from_stream(f, decompress)
        # based on magic number, file is compressed
        # tar archive. Check to see if file is abbreviated as
        # t[xz|gz|bz2|bz]
        if ext.startswith('tar.'):
            suf = ext.split('.')[1]
            abbr = 't' + suf
            if check_extension(file, abbr):
                return abbr
        return ext


def strip_extension(path):
    """Get the part of a path that does not include its compressed
    type extension."""
    for type in ALLOWED_ARCHIVE_TYPES:
        suffix = r"\.%s$" % type
        if re.search(suffix, path):
            return re.sub(suffix, "", path)
    return path


def check_extension(path, ext):
    """Check if extension is present in path"""
    # Strip sourceforge suffix.
    suffix = r'%s$' % ext
    if re.search(suffix, path):
        return True
    return False


def strip_sourceforge_suffix(path):
    """remove sourceforge suffix from path if present
    return stripped path"""
    # Strip sourceforge suffix.
    if re.search(r'((?:sourceforge.net|sf.net)/.*)/download$', path):
        return os.path.dirname(path)
    return path


def extension(path):
    """Get the allowed archive extension for a path.
    If path does not include a valid archive extension
    (see`spack.util.compression.ALLOWED_ARCHIVE_TYPES`) return None
    """
    if path is None:
        raise ValueError("Can't call extension() on None")

    # Strip sourceforge suffix.
    path = strip_sourceforge_suffix(path)

    for t in ALLOWED_ARCHIVE_TYPES:
        if check_extension(path, '\.'+t):
            return t
    return None
