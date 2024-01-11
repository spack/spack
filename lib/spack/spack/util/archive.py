# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import errno
import hashlib
import io
import os
import pathlib
import tarfile
from contextlib import closing, contextmanager
from gzip import GzipFile
from typing import Callable, Dict, Tuple


class ChecksumWriter(io.BufferedIOBase):
    """Checksum writer computes a checksum while writing to a file."""

    myfileobj = None

    def __init__(self, fileobj, algorithm=hashlib.sha256):
        self.fileobj = fileobj
        self.hasher = algorithm()
        self.length = 0

    def hexdigest(self):
        return self.hasher.hexdigest()

    def write(self, data):
        if isinstance(data, (bytes, bytearray)):
            length = len(data)
        else:
            data = memoryview(data)
            length = data.nbytes

        if length > 0:
            self.fileobj.write(data)
            self.hasher.update(data)

        self.length += length

        return length

    def read(self, size=-1):
        raise OSError(errno.EBADF, "read() on write-only object")

    def read1(self, size=-1):
        raise OSError(errno.EBADF, "read1() on write-only object")

    def peek(self, n):
        raise OSError(errno.EBADF, "peek() on write-only object")

    @property
    def closed(self):
        return self.fileobj is None

    def close(self):
        fileobj = self.fileobj
        if fileobj is None:
            return
        self.fileobj.close()
        self.fileobj = None

    def flush(self):
        self.fileobj.flush()

    def fileno(self):
        return self.fileobj.fileno()

    def rewind(self):
        raise OSError("Can't rewind while computing checksum")

    def readable(self):
        return False

    def writable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self.fileobj.tell()

    def seek(self, offset, whence=io.SEEK_SET):
        # In principle forward seek is possible with b"0" padding,
        # but this is not implemented.
        if offset == 0 and whence == io.SEEK_CUR:
            return
        raise OSError("Can't seek while computing checksum")

    def readline(self, size=-1):
        raise OSError(errno.EBADF, "readline() on write-only object")


@contextmanager
def gzip_compressed_tarfile(path):
    """Create a reproducible, compressed tarfile"""
    # Create gzip compressed tarball of the install prefix
    # 1) Use explicit empty filename and mtime 0 for gzip header reproducibility.
    #    If the filename="" is dropped, Python will use fileobj.name instead.
    #    This should effectively mimick `gzip --no-name`.
    # 2) On AMD Ryzen 3700X and an SSD disk, we have the following on compression speed:
    # compresslevel=6 gzip default: llvm takes 4mins, roughly 2.1GB
    # compresslevel=9 python default: llvm takes 12mins, roughly 2.1GB
    # So we follow gzip.
    with open(path, "wb") as f, ChecksumWriter(f) as inner_checksum, closing(
        GzipFile(filename="", mode="wb", compresslevel=6, mtime=0, fileobj=inner_checksum)
    ) as gzip_file, ChecksumWriter(gzip_file) as outer_checksum, tarfile.TarFile(
        name="", mode="w", fileobj=outer_checksum
    ) as tar:
        yield tar, inner_checksum, outer_checksum


def reproducible_tarfile_from_prefix(
    tar: tarfile.TarFile,
    prefix: str,
    *,
    include_parent_directories: bool = False,
    skip: Callable[[os.DirEntry], bool] = lambda entry: False,
    path_to_name: Callable[[str], str] = lambda path: path,
) -> None:
    """Only adds regular files, symlinks and dirs. Skips devices, fifos. Preserves hardlinks.
    Normalizes permissions like git. Tar entries are added in depth-first pre-order, with
    dir entries partitioned by file | dir, and sorted alphabetically, for reproducibility.
    Partitioning ensures only one dir is in memory at a time, and sorting improves compression."""

    hardlink_to_tarinfo_name: Dict[Tuple[int, int], str] = dict()

    if include_parent_directories:
        parent_dirs = reversed(pathlib.Path(prefix).parents)
        next(parent_dirs)  # skip the root: slices are supported from python 3.10
        for parent_dir in parent_dirs:
            dir_info = tarfile.TarInfo(path_to_name(str(parent_dir)))
            dir_info.type = tarfile.DIRTYPE
            dir_info.mode = 0o755
            tar.addfile(dir_info)

    dir_stack = [prefix]
    while dir_stack:
        dir = dir_stack.pop()

        # Add the dir before its contents
        dir_info = tarfile.TarInfo(path_to_name(dir))
        dir_info.type = tarfile.DIRTYPE
        dir_info.mode = 0o755
        tar.addfile(dir_info)

        # Sort by name: reproducible & improves compression
        with os.scandir(dir) as it:
            entries = sorted(it, key=lambda entry: entry.name)

        new_dirs = []
        for entry in entries:
            if skip(entry):
                continue

            if entry.is_dir(follow_symlinks=False):
                new_dirs.append(entry.path)
                continue

            file_info = tarfile.TarInfo(path_to_name(entry.path))

            s = entry.stat(follow_symlinks=False)

            # Normalize the mode
            file_info.mode = 0o644 if s.st_mode & 0o100 == 0 else 0o755

            if entry.is_symlink():
                file_info.type = tarfile.SYMTYPE
                file_info.linkname = os.readlink(entry.path)
                tar.addfile(file_info)

            elif entry.is_file(follow_symlinks=False):
                # Deduplicate hardlinks
                if s.st_nlink > 1:
                    ident = (s.st_dev, s.st_ino)
                    if ident in hardlink_to_tarinfo_name:
                        file_info.type = tarfile.LNKTYPE
                        file_info.linkname = hardlink_to_tarinfo_name[ident]
                        tar.addfile(file_info)
                        continue
                    hardlink_to_tarinfo_name[ident] = file_info.name

                # If file not yet seen, copy it.
                file_info.type = tarfile.REGTYPE
                file_info.size = s.st_size

                with open(entry.path, "rb") as f:
                    tar.addfile(file_info, f)

        dir_stack.extend(reversed(new_dirs))  # we pop, so reverse to stay alphabetical
