# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect
import io
import os
import re
import shutil
import sys
from itertools import product

from llnl.util import tty

import spack.util.path as spath
from spack.util.executable import CommandNotFoundError, which

# Supported archive extensions.
PRE_EXTS = ["tar", "TAR"]
EXTS = ["gz", "bz2", "xz", "Z"]
NOTAR_EXTS = ["zip", "tgz", "tbz2", "tbz", "txz"]

# Add PRE_EXTS and EXTS last so that .tar.gz is matched *before* .tar or .gz
ALLOWED_ARCHIVE_TYPES = (
    [".".join(ext) for ext in product(PRE_EXTS, EXTS)] + PRE_EXTS + EXTS + NOTAR_EXTS
)

ALLOWED_SINGLE_EXT_ARCHIVE_TYPES = PRE_EXTS + EXTS + NOTAR_EXTS

try:
    import bz2  # noqa

    _bz2_support = True
except ImportError:
    _bz2_support = False


try:
    import gzip  # noqa

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
    outfile = os.path.basename(strip_extension(archive_file, "tar"))

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
    compressed_file_name = os.path.basename(archive_file)
    decompressed_file = os.path.basename(strip_extension(archive_file, "bz2"))
    working_dir = os.getcwd()
    archive_out = os.path.join(working_dir, decompressed_file)
    copy_path = os.path.join(working_dir, compressed_file_name)
    if is_bz2_supported():
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
    decompressed_file = os.path.basename(strip_extension(archive_file, "gz"))
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
    decompressed_file = os.path.basename(strip_extension(archive_file, "gz"))
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
    extracted_file = os.path.basename(strip_extension(archive_file, "zip"))
    if sys.platform == "win32":
        return _untar(archive_file)
    else:
        exe = "unzip"
        arg = "-q"
        unzip = which(exe, required=True)
        unzip.add_default_arg(arg)
        unzip(archive_file)
    return extracted_file


def _unZ(archive_file):
    if sys.platform == "win32":
        result = _7zip(archive_file)
    else:
        result = _system_gunzip(archive_file)
    return result


def _lzma_decomp(archive_file):
    """Decompress lzma compressed files. Prefer Python native
    lzma module, but fall back on command line xz tooling
    to find available Python support. This is the xz command
    on Unix and 7z on Windows"""
    if is_lzma_supported():
        decompressed_file = os.path.basename(strip_extension(archive_file, "xz"))
        archive_out = os.path.join(os.getcwd(), decompressed_file)
        with open(archive_out, "wb") as ar:
            with lzma.open(archive_file) as lar:
                shutil.copyfileobj(lar, ar)
    else:
        if sys.platform == "win32":
            return _7zip(archive_file)
        else:
            return _xz(archive_file)


def _win_compressed_tarball_handler(archive_file):
    """Decompress and extract compressed tarballs on Windows.
    This method uses 7zip in conjunction with the tar utility
    to perform decompression and extraction in a two step process
    first using 7zip to decompress, and tar to extract.

    The motivation for this method is the inability of 7zip
    to directly decompress and extract compressed archives
    in a single shot without undocumented workarounds, and
    the Windows tar utility's lack of access to the xz tool (unsupported on Windows)
    """
    # perform intermediate extraction step
    # record name of new archive so we can extract
    # and later clean up
    decomped_tarball = _7zip(archive_file)
    # 7zip is able to one shot extract compressed archives
    # that have been named .txz. If that is the case, there will
    # be no intermediate archvie to extract.
    if check_extension(decomped_tarball, "tar"):
        # run tar on newly decomped archive
        outfile = _untar(decomped_tarball)
        # clean intermediate archive to mimic end result
        # produced by one shot decomp/extraction
        os.remove(decomped_tarball)
        return outfile
    return decomped_tarball


def _xz(archive_file):
    """Decompress lzma compressed .xz files via xz command line
    tool. Available only on Unix
    """
    if sys.platform == "win32":
        raise RuntimeError("XZ tool unavailable on Windows")
    decompressed_file = os.path.basename(strip_extension(archive_file, "xz"))
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
    outfile = os.path.basename(strip_last_extension(archive_file))
    _7z = which("7z")
    if not _7z:
        raise CommandNotFoundError(
            "7z unavailable,\
unable to extract %s files. 7z can be installed via Spack"
            % extension_from_path(archive_file)
        )
    _7z.add_default_arg("e")
    _7z(archive_file)
    return outfile


def decompressor_for(path, extension=None):
    """Returns a function pointer to appropriate decompression
    algorithm based on extension type.

    Args:
        path (str): path of the archive file requiring decompression
    """
    if not extension:
        extension = extension_from_file(path, decompress=True)

    if not allowed_archive(extension):
        raise CommandNotFoundError(
            "Cannot extract archive, \
unrecognized file extension: '%s'"
            % extension
        )

    if re.match(r"\.?zip$", extension) or path.endswith(".zip"):
        return _unzip

    if re.match(r"gz", extension):
        return _gunzip

    if re.match(r"bz2", extension):
        return _bunzip2

    # Python does not have native support
    # of any kind for .Z files. In these cases,
    # we rely on external tools such as tar,
    # 7z, or uncompressZ
    if re.match(r"Z$", extension):
        return _unZ

    # Python and platform may not have support for lzma
    # compression. If no lzma support, use tools available on systems
    # 7zip on Windows and the xz tool on Unix systems.
    if re.match(r"xz", extension):
        return _lzma_decomp

    # Catch tar.xz/tar.Z files here for Windows
    # as the tar utility on Windows cannot handle such
    # compression types directly
    if ("xz" in extension or "Z" in extension) and sys.platform == "win32":
        return _win_compressed_tarball_handler

    return _untar


class FileTypeInterface:
    """
    Base interface class for describing and querying file type information.
    FileType describes information about a single file type
    such as extension, and byte header properties, and provides an interface
    to check a given file against said type based on magic number.

    This class should be subclassed each time a new type is to be
    described.

    Note: This class should not be used directly as it does not define any specific
    file. Attempts to directly use this class will fail, as it does not define
    a magic number or extension string.

    Subclasses should each describe a different
    type of file. In order to do so, they must define
    the extension string, magic number, and header offset (if non zero).
    If a class has multiple magic numbers, it will need to
    override the method describin that file types magic numbers and
    the method that checks a types magic numbers against a given file's.
    """

    OFFSET = 0
    compressed = False

    @staticmethod
    def name():
        raise NotImplementedError

    @classmethod
    def magic_number(cls):
        """Return a list of all potential magic numbers for a filetype"""
        return [x[1] for x in inspect.getmembers(cls) if x[0].startswith("_MAGIC_NUMBER")]

    @classmethod
    def header_size(cls):
        """Return size of largest magic number associated with file type"""
        return max([len(x) for x in cls.magic_number()])

    @classmethod
    def _bytes_check(cls, magic_bytes):
        for magic in cls.magic_number():
            if magic_bytes.startswith(magic):
                return True
        return False

    @classmethod
    def is_file_of_type(cls, iostream):
        """Query byte stream for appropriate magic number

        Args:
            iostream: file byte stream

        Returns:
            Bool denoting whether file is of class file type
            based on magic number
        """
        if not iostream:
            return False
        # move to location of magic bytes
        iostream.seek(cls.OFFSET)
        magic_bytes = iostream.read(cls.header_size())
        # return to beginning of file
        iostream.seek(0)
        if cls._bytes_check(magic_bytes):
            return True
        return False


class CompressedFileTypeInterface(FileTypeInterface):
    """Interface class for FileTypes that include compression information"""

    compressed = True

    @staticmethod
    def decomp_in_memory(stream):
        """This method decompresses and loads the first 200 or so bytes of a compressed file
        to check for compressed archives. This does not decompress the entire file and should
        not be used for direct expansion of archives/compressed files
        """
        raise NotImplementedError("Implementation by compression subclass required")


class BZipFileType(CompressedFileTypeInterface):
    _MAGIC_NUMBER = b"\x42\x5a\x68"
    extension = "bz2"

    @staticmethod
    def name():
        return "bzip2 compressed data"

    @staticmethod
    def decomp_in_memory(stream):
        if is_bz2_supported():
            # checking for underlying archive, only decomp as many bytes
            # as is absolutely neccesary for largest archive header (tar)
            comp_stream = stream.read(TarFileType.OFFSET + TarFileType.header_size())
            return io.BytesIO(initial_bytes=bz2.BZ2Decompressor().decompress(comp_stream))
        return None


class ZCompressedFileType(CompressedFileTypeInterface):
    _MAGIC_NUMBER_LZW = b"\x1f\x9d"
    _MAGIC_NUMBER_LZH = b"\x1f\xa0"
    extension = "Z"

    @staticmethod
    def name():
        return "compress'd data"

    @staticmethod
    def decomp_in_memory(stream):
        # python has no method of decompressing `.Z` files in memory
        return None


class GZipFileType(CompressedFileTypeInterface):
    _MAGIC_NUMBER = b"\x1f\x8b\x08"
    extension = "gz"

    @staticmethod
    def name():
        return "gzip compressed data"

    @staticmethod
    def decomp_in_memory(stream):
        if is_gzip_supported():
            # checking for underlying archive, only decomp as many bytes
            # as is absolutely neccesary for largest archive header (tar)
            return io.BytesIO(
                initial_bytes=gzip.GzipFile(fileobj=stream).read(
                    TarFileType.OFFSET + TarFileType.header_size()
                )
            )
        return None


class LzmaFileType(CompressedFileTypeInterface):
    _MAGIC_NUMBER = b"\xfd7zXZ"
    extension = "xz"

    @staticmethod
    def name():
        return "xz compressed data"

    @staticmethod
    def decomp_in_memory(stream):
        if is_lzma_supported():
            # checking for underlying archive, only decomp as many bytes
            # as is absolutely neccesary for largest archive header (tar)
            max_size = TarFileType.OFFSET + TarFileType.header_size()
            return io.BytesIO(
                initial_bytes=lzma.LZMADecompressor().decompress(
                    stream.read(max_size), max_length=max_size
                )
            )
        return None


class TarFileType(FileTypeInterface):
    OFFSET = 257
    _MAGIC_NUMBER_GNU = b"ustar  \0"
    _MAGIC_NUMBER_POSIX = b"ustar\x0000"
    extension = "tar"

    @staticmethod
    def name():
        return "tar archive"


class ZipFleType(FileTypeInterface):
    _MAGIC_NUMBER = b"PK\003\004"
    extension = "zip"

    @staticmethod
    def name():
        return "Zip archive data"


# collection of valid Spack recognized archive and compression
# file type identifier classes.
VALID_FILETYPES = [
    BZipFileType,
    ZCompressedFileType,
    GZipFileType,
    LzmaFileType,
    TarFileType,
    ZipFleType,
]


def extension_from_stream(stream, decompress=False):
    """Return extension represented by stream corresponding to archive file
    If stream does not represent an archive type recongized by Spack
    (see `spack.util.compression.ALLOWED_ARCHIVE_TYPES`) method will return None

    Extension type is derived by searching for identifying bytes
    in file stream.

    Args:
        stream : stream representing a file on system
        decompress (bool) : if True, compressed files are checked
                            for archive types beneath compression i.e. tar.gz
                            default is False, otherwise, return top level type i.e. gz

    Return:
        A string represting corresponding archive extension
            or None as relevant.

    """
    for arc_type in VALID_FILETYPES:
        if arc_type.is_file_of_type(stream):
            suffix_ext = arc_type.extension
            prefix_ext = ""
            if arc_type.compressed and decompress:
                # stream represents compressed file
                # get decompressed stream (if possible)
                decomp_stream = arc_type.decomp_in_memory(stream)
                prefix_ext = extension_from_stream(decomp_stream, decompress=decompress)
                if not prefix_ext:
                    # We were unable to decompress or unable to derive
                    # a nested extension from decompressed file.
                    # Try to use filename parsing to check for
                    # potential nested extensions if there are any
                    tty.debug(
                        "Cannot derive file extension from magic number;"
                        " falling back to regex path parsing."
                    )
                    return extension_from_path(stream.name)
            resultant_ext = suffix_ext if not prefix_ext else ".".join([prefix_ext, suffix_ext])
            tty.debug("File extension %s successfully derived by magic number." % resultant_ext)
            return resultant_ext
    return None


def extension_from_file(file, decompress=False):
    """Return extension from archive file path
    Extension is derived based on magic number parsing similar
    to the `file` utility. Attempts to return abbreviated file extensions
    whenever a file has an abbreviated extension such as `.tgz` or `.txz`.
    This distinction in abbreivated extension names is accomplished
    by string parsing.

    Args:
        file (os.PathLike): path descibing file on system for which ext
            will be determined.
        decompress (bool): If True, method will peek into compressed
            files to check for archive file types. default is False.
            If false, method will be unable to distinguish `.tar.gz` from `.gz`
            or similar.
    Return:
        Spack recognized archive file extension as determined by file's magic number and
         file name. If file is not on system or is of an type not recognized by Spack as
         an archive or compression type, None is returned.
    """
    if os.path.exists(file):
        with open(file, "rb") as f:
            ext = extension_from_stream(f, decompress)
            # based on magic number, file is compressed
            # tar archive. Check to see if file is abbreviated as
            # t[xz|gz|bz2|bz]
            if ext and ext.startswith("tar."):
                suf = ext.split(".")[1]
                abbr = "t" + suf
                if check_extension(file, abbr):
                    return abbr
            if not ext:
                # If unable to parse extension from stream,
                # attempt to fall back to string parsing
                ext = extension_from_path(file)
            return ext
    return None


def extension_from_path(path):
    """Get the allowed archive extension for a path.
    If path does not include a valid archive extension
    (see`spack.util.compression.ALLOWED_ARCHIVE_TYPES`) return None
    """
    if path is None:
        raise ValueError("Can't call extension() on None")

    for t in ALLOWED_ARCHIVE_TYPES:
        if check_extension(path, t):
            return t
    return None


def strip_last_extension(path):
    """Strips last supported archive extension from path"""
    if path:
        for ext in ALLOWED_SINGLE_EXT_ARCHIVE_TYPES:
            mod_path = check_and_remove_ext(path, ext)
            if mod_path != path:
                return mod_path
    return path


def strip_extension(path, ext=None):
    """Get the part of a path that does not include its compressed
    type extension."""
    if ext:
        return check_and_remove_ext(path, ext)
    for t in ALLOWED_ARCHIVE_TYPES:
        mod_path = check_and_remove_ext(path, t)
        if mod_path != path:
            return mod_path
    return path


def check_extension(path, ext):
    """Check if extension is present in path"""
    # Strip sourceforge suffix.
    prefix, _ = spath.find_sourceforge_suffix(path)
    if not ext.startswith(r"\."):
        ext = r"\.%s$" % ext
    if re.search(ext, prefix):
        return True
    return False


def reg_remove_ext(path, ext):
    """Regex remove ext from path"""
    if path and ext:
        suffix = r"\.%s$" % ext
        return re.sub(suffix, "", path)
    return path


def check_and_remove_ext(path, ext):
    """If given extension is present in path, remove and return,
    otherwise just return path"""
    if check_extension(path, ext):
        return reg_remove_ext(path, ext)
    return path
