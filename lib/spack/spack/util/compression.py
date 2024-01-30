# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect
import io
import os
import re
import shutil
import sys

import llnl.url
from llnl.util import tty

from spack.error import SpackError
from spack.util.executable import CommandNotFoundError, which

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


def _system_untar(archive_file, remove_archive_file=False):
    """Returns path to unarchived tar file.
    Untars archive via system tar.

    Args:
        archive_file (str): absolute path to the archive to be extracted.
        Can be one of .tar(.[gz|bz2|xz|Z]) or .(tgz|tbz|tbz2|txz).
    """
    archive_file_no_ext = llnl.url.strip_extension(archive_file)
    outfile = os.path.basename(archive_file_no_ext)
    if archive_file_no_ext == archive_file:
        # the archive file has no extension. Tar on windows cannot untar onto itself
        # archive_file can be a tar file (which causes the problem on windows) but it can
        # also have other extensions (on Unix) such as tgz, tbz2, ...
        archive_file = archive_file_no_ext + "-input"
        shutil.move(archive_file_no_ext, archive_file)
    tar = which("tar", required=True)
    tar.add_default_arg("-oxf")
    tar(archive_file)
    if remove_archive_file:
        # remove input file to prevent two stage
        # extractions from being treated as exploding
        # archives by the fetcher
        os.remove(archive_file)
    return outfile


def _bunzip2(archive_file):
    """Returns path to decompressed file.
    Uses Python's bz2 module to decompress bz2 compressed archives
    Fall back to system utility failing to find Python module `bz2`

    Args:
        archive_file (str): absolute path to the bz2 archive to be decompressed
    """
    if is_bz2_supported():
        return _py_bunzip(archive_file)
    else:
        return _system_bunzip(archive_file)


def _py_bunzip(archive_file):
    """Returns path to decompressed file.
    Decompresses bz2 compressed archives/files via python's bz2 module"""
    decompressed_file = os.path.basename(llnl.url.strip_compression_extension(archive_file, "bz2"))
    working_dir = os.getcwd()
    archive_out = os.path.join(working_dir, decompressed_file)
    f_bz = bz2.BZ2File(archive_file, mode="rb")
    with open(archive_out, "wb") as ar:
        shutil.copyfileobj(f_bz, ar)
    f_bz.close()
    return archive_out


def _system_bunzip(archive_file):
    """Returns path to decompressed file.
    Decompresses bz2 compressed archives/files via system bzip2 utility"""
    compressed_file_name = os.path.basename(archive_file)
    decompressed_file = os.path.basename(llnl.url.strip_compression_extension(archive_file, "bz2"))
    working_dir = os.getcwd()
    archive_out = os.path.join(working_dir, decompressed_file)
    copy_path = os.path.join(working_dir, compressed_file_name)
    shutil.copy(archive_file, copy_path)
    bunzip2 = which("bunzip2", required=True)
    bunzip2.add_default_arg("-q")
    bunzip2(copy_path)
    return archive_out


def _gunzip(archive_file):
    """Returns path to gunzip'd file
    Decompresses `.gz` extensions. Prefer native Python `gzip` module.
    Failing back to system utility gunzip.
    Like gunzip, but extracts in the current working directory
    instead of in-place.

    Args:
        archive_file (str): absolute path of the file to be decompressed
    """
    if is_gzip_supported():
        return _py_gunzip(archive_file)
    else:
        return _system_gunzip(archive_file)


def _py_gunzip(archive_file):
    """Returns path to gunzip'd file
    Decompresses `.gz` compressed archvies via python gzip module"""
    decompressed_file = os.path.basename(llnl.url.strip_compression_extension(archive_file, "gz"))
    working_dir = os.getcwd()
    destination_abspath = os.path.join(working_dir, decompressed_file)
    f_in = gzip.open(archive_file, "rb")
    with open(destination_abspath, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    f_in.close()
    return destination_abspath


def _system_gunzip(archive_file):
    """Returns path to gunzip'd file
    Decompresses `.gz` compressed files via system gzip"""
    archive_file_no_ext = llnl.url.strip_compression_extension(archive_file)
    if archive_file_no_ext == archive_file:
        # the zip file has no extension. On Unix gunzip cannot unzip onto itself
        archive_file = archive_file + ".gz"
        shutil.move(archive_file_no_ext, archive_file)
    decompressed_file = os.path.basename(archive_file_no_ext)
    working_dir = os.getcwd()
    destination_abspath = os.path.join(working_dir, decompressed_file)
    compressed_file = os.path.basename(archive_file)
    copy_path = os.path.join(working_dir, compressed_file)
    shutil.copy(archive_file, copy_path)
    gzip = which("gzip", required=True)
    gzip.add_default_arg("-d")
    gzip(copy_path)
    return destination_abspath


def _unzip(archive_file):
    """Returns path to extracted zip archive
    Extract Zipfile, searching for unzip system executable
    If unavailable, search for 'tar' executable on system and use instead

    Args:
        archive_file (str): absolute path of the file to be decompressed
    """
    extracted_file = os.path.basename(llnl.url.strip_extension(archive_file, extension="zip"))
    if sys.platform == "win32":
        return _system_untar(archive_file)
    else:
        exe = "unzip"
        arg = "-q"
        unzip = which(exe, required=True)
        unzip.add_default_arg(arg)
        unzip(archive_file)
    return extracted_file


def _system_unZ(archive_file):
    """Returns path to decompressed file
    Decompress UNIX compress style compression
    Utilizes gunzip on unix and 7zip on Windows
    """
    if sys.platform == "win32":
        result = _system_7zip(archive_file)
    else:
        result = _system_gunzip(archive_file)
    return result


def _lzma_decomp(archive_file):
    """Returns path to decompressed xz file.
    Decompress lzma compressed files. Prefer Python native
    lzma module, but fall back on command line xz tooling
    to find available Python support."""
    if is_lzma_supported():
        return _py_lzma(archive_file)
    else:
        return _xz(archive_file)


def _win_compressed_tarball_handler(decompressor):
    """Returns function pointer to two stage decompression
    and extraction method
    Decompress and extract compressed tarballs on Windows.
    This method uses a decompression method in conjunction with
    the tar utility to perform decompression and extraction in
    a two step process first using decompressor to decompress,
    and tar to extract.

    The motivation for this method is Windows tar utility's lack
    of access to the xz tool (unsupported natively on Windows) but
    can be installed manually or via spack
    """

    def unarchive(archive_file):
        # perform intermediate extraction step
        # record name of new archive so we can extract
        decomped_tarball = decompressor(archive_file)
        # run tar on newly decomped archive
        outfile = _system_untar(decomped_tarball, remove_archive_file=True)
        return outfile

    return unarchive


def _py_lzma(archive_file):
    """Returns path to decompressed .xz files
    Decompress lzma compressed .xz files via python lzma module"""
    decompressed_file = os.path.basename(llnl.url.strip_compression_extension(archive_file, "xz"))
    archive_out = os.path.join(os.getcwd(), decompressed_file)
    with open(archive_out, "wb") as ar:
        with lzma.open(archive_file) as lar:
            shutil.copyfileobj(lar, ar)
    return archive_out


def _xz(archive_file):
    """Returns path to decompressed xz files
    Decompress lzma compressed .xz files via xz command line
    tool.
    """
    decompressed_file = os.path.basename(llnl.url.strip_extension(archive_file, extension="xz"))
    working_dir = os.getcwd()
    destination_abspath = os.path.join(working_dir, decompressed_file)
    compressed_file = os.path.basename(archive_file)
    copy_path = os.path.join(working_dir, compressed_file)
    shutil.copy(archive_file, copy_path)
    xz = which("xz", required=True)
    xz.add_default_arg("-d")
    xz(copy_path)
    return destination_abspath


def _system_7zip(archive_file):
    """Returns path to decompressed file
    Unpack/decompress with 7z executable
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
    outfile = os.path.basename(llnl.url.strip_compression_extension(archive_file))
    _7z = which("7z")
    if not _7z:
        raise CommandNotFoundError(
            "7z unavailable,\
unable to extract %s files. 7z can be installed via Spack"
            % llnl.url.extension_from_path(archive_file)
        )
    _7z.add_default_arg("e")
    _7z(archive_file)
    return outfile


def decompressor_for(path, extension=None):
    """Returns appropriate decompression/extraction algorithm function pointer
    for provided extension. If extension is none, it is computed
    from the `path` and the decompression function is derived
    from that information."""
    if not extension:
        extension = extension_from_file(path, decompress=True)

    if not llnl.url.allowed_archive(extension):
        raise CommandNotFoundError(
            "Cannot extract archive, \
unrecognized file extension: '%s'"
            % extension
        )
    if sys.platform == "win32":
        return decompressor_for_win(extension)
    else:
        return decompressor_for_nix(extension)


def decompressor_for_nix(extension):
    """Returns a function pointer to appropriate decompression
    algorithm based on extension type and unix specific considerations
    i.e. a reasonable expectation system utils like gzip, bzip2, and xz are
    available

    Args:
        path (str): path of the archive file requiring decompression
    """
    if re.match(r"zip$", extension):
        return _unzip

    if re.match(r"gz$", extension):
        return _gunzip

    if re.match(r"bz2$", extension):
        return _bunzip2

    # Python does not have native support
    # of any kind for .Z files. In these cases,
    # we rely on external tools such as tar,
    # 7z, or uncompressZ
    if re.match(r"Z$", extension):
        return _system_unZ

    # Python and platform may not have support for lzma
    # compression. If no lzma support, use tools available on systems
    if re.match(r"xz$", extension):
        return _lzma_decomp

    return _system_untar


def _determine_py_decomp_archive_strategy(extension):
    """Returns appropriate python based decompression strategy
    based on extension type"""
    # Only rely on Python decompression support for gz
    if re.match(r"gz$", extension):
        return _py_gunzip

    # Only rely on Python decompression support for bzip2
    if re.match(r"bz2$", extension):
        return _py_bunzip

    # Only rely on Python decompression support for xz
    if re.match(r"xz$", extension):
        return _py_lzma

    return None


def decompressor_for_win(extension):
    """Returns a function pointer to appropriate decompression
    algorithm based on extension type and Windows specific considerations

    Windows natively vendors *only* tar, no other archive/compression utilities
    So we must rely exclusively on Python module support for all compression
    operations, tar for tarballs and zip files, and 7zip for Z compressed archives
    and files as Python does not provide support for the UNIX compress algorithm

    Args:
        path (str): path of the archive file requiring decompression
        extension (str): extension
    """
    extension = llnl.url.expand_contracted_extension(extension)
    # Windows native tar can handle .zip extensions, use standard
    # unzip method
    if re.match(r"zip$", extension):
        return _unzip

    # if extension is standard tarball, invoke Windows native tar
    if re.match(r"tar$", extension):
        return _system_untar

    # Python does not have native support
    # of any kind for .Z files. In these cases,
    # we rely on 7zip, which must be installed outside
    # of spack and added to the PATH or externally detected
    if re.match(r"Z$", extension):
        return _system_unZ

    # Windows vendors no native decompression tools, attempt to derive
    # python based decompression strategy
    # Expand extension from contracted extension i.e. tar.gz from .tgz
    # no-op on non contracted extensions
    compression_extension = llnl.url.compression_ext_from_compressed_archive(extension)
    decompressor = _determine_py_decomp_archive_strategy(compression_extension)
    if not decompressor:
        raise SpackError(
            "Spack was unable to determine a proper decompression strategy for"
            f"valid extension: {extension}"
            "This is a bug, please file an issue at https://github.com/spack/spack/issues"
        )
    if "tar" not in extension:
        return decompressor

    return _win_compressed_tarball_handler(decompressor)


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
                    return llnl.url.extension_from_path(stream.name)
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
                if llnl.url.has_extension(file, abbr):
                    return abbr
            if not ext:
                # If unable to parse extension from stream,
                # attempt to fall back to string parsing
                ext = llnl.url.extension_from_path(file)
            return ext
    return None
