"""Fast, safe, streaming extraction of tar archives that distribute software.

Archives are read front to back exactly once, from a file or any readable binary stream, and
only the header fields that extraction needs are parsed. ``extract`` can strip a leading
directory that is only known from the archive's contents: the parent of the shallowest member
with a given name. Owners, groups, timestamps and permissions in the archive are not restored:
files are created with the permissions given by the caller.
"""

import contextlib
import errno
import gzip
import os
import stat
import struct
import sys
import zlib
from typing import IO, Dict, Iterable, Iterator, List, Optional, Tuple, Union

__version__ = "0.2.0"
__all__ = ["Error", "Member", "TarReader", "extract"]

REGTYPE = b"0"
AREGTYPE = b"\0"
LNKTYPE = b"1"
SYMTYPE = b"2"
DIRTYPE = b"5"
CONTTYPE = b"7"
_PAX_HEADER = b"x"
_SOLARIS_PAX_HEADER = b"X"
_PAX_GLOBAL_HEADER = b"g"
_GNU_LONGNAME = b"L"
_GNU_LONGLINK = b"K"
_EXTENDED = (
    _PAX_HEADER,
    _SOLARIS_PAX_HEADER,
    _PAX_GLOBAL_HEADER,
    _GNU_LONGNAME,
    _GNU_LONGLINK,
)
_DATA_TYPES = (REGTYPE, AREGTYPE, CONTTYPE)
#: Like tarfile, members of other types than these have data, also unknown ones
_NO_DATA_TYPES = (LNKTYPE, SYMTYPE, DIRTYPE, b"3", b"4", b"6")

_WINDOWS = sys.platform == "win32"
_BLOCK = 512
_EOF_BLOCK = bytes(_BLOCK)
_CHUNK = 64 * 1024
_BUF = 1024 * 1024
#: Pax and GNU long name headers are read into memory: limit their size per member
_MAX_EXTENDED = 1024 * 1024
#: Dirs on the stack that stay open: the deepest ones, and shallower ones are reopened if needed
_MAX_OPEN_DIRS = 64
_BadGzipFile = getattr(gzip, "BadGzipFile", OSError)


class Error(ValueError):
    """The archive is invalid, or cannot be extracted safely."""


class Member:
    """A member of a tar archive, with only the fields that extraction needs."""

    __slots__ = ("linkname", "mode", "name", "size", "type")

    def __init__(
        self, name: str, type: bytes, mode: int, size: int, linkname: str
    ) -> None:
        self.name = name
        self.type = type
        self.mode = mode
        self.size = size
        self.linkname = linkname

    def isreg(self) -> bool:
        return self.type in _DATA_TYPES

    def isdir(self) -> bool:
        return self.type == DIRTYPE

    def issym(self) -> bool:
        return self.type == SYMTYPE

    def islnk(self) -> bool:
        return self.type == LNKTYPE

    def __repr__(self) -> str:
        return f"Member({self.name!r}, type={self.type!r}, mode={oct(self.mode)}, size={self.size})"


def _str(field: bytes) -> str:
    return field.split(b"\0", 1)[0].decode("utf-8", "surrogateescape")


def _int(field: bytes) -> int:
    """A numeric header field: NUL or space terminated octal, or base-256 (GNU)."""
    if field[0] == 0o200:
        return int.from_bytes(field[1:], "big")
    elif field[0] == 0o377:
        raise Error("Archive contains a negative number")
    digits = field.split(b"\0", 1)[0].strip()
    # Only octal digits, like tar
    if digits.strip(b"01234567"):
        raise Error(f"Archive contains an invalid number {digits!r}")
    return int(digits, 8) if digits else 0


def _long_name(data: bytes) -> str:
    """A GNU long name or link, which ends with NULs. Readers disagree on a NUL inside it: some
    stop there, others keep the rest."""
    name = data.rstrip(b"\0")
    if not name:
        raise Error("Archive contains an empty GNU long name")
    if b"\0" in name:
        raise Error(f"Archive contains a GNU long name with a NUL inside {name!r}")
    return name.decode("utf-8", "surrogateescape")


def _decimal(value: str, key: str) -> int:
    """A pax decimal number, of ASCII digits only."""
    if not value or value.strip("0123456789"):
        raise Error(f"Archive contains an invalid pax {key} {value!r}")
    return int(value)


def _checksum_ok(header: bytes) -> bool:
    expected = _int(header[148:156])
    # adler32's low half is the byte sum mod 65521, which is exact for 256 bytes
    total = (zlib.adler32(header[:256], 0) & 0xFFFF) + (
        zlib.adler32(header[256:], 0) & 0xFFFF
    )
    if expected == total - sum(header[148:156]) + 256:
        return True
    # Some old tar implementations summed signed chars
    signed = struct.unpack("148b8x356b", header)
    return expected == sum(signed) + 256


def _pax_records(data: bytes) -> Dict[str, str]:
    """Parse the ``<length> <key>=<value>\\n`` records of a pax extended header."""
    records = {}
    pos = 0
    while pos < len(data) and data[pos] != 0:
        space = data.find(b" ", pos)
        length = data[pos:space]
        if space < 0 or not length or length.strip(b"0123456789"):
            raise Error("Archive contains an invalid pax header")
        end = pos + int(length)
        if end <= space or end > len(data) or data[end - 1] != 0x0A:
            raise Error("Archive contains an invalid pax header")
        key, equals, value = data[space + 1 : end - 1].partition(b"=")
        if not key or not equals:
            raise Error("Archive contains an invalid pax record")
        records[key.decode("utf-8", "surrogateescape")] = value.decode(
            "utf-8", "surrogateescape"
        )
        pos = end
    return records


def _fill(stream: IO[bytes], size: int) -> bytes:
    """Read size bytes, or fewer at the end of the stream."""
    data = stream.read(size)
    while 0 < len(data) < size:
        more = stream.read(size - len(data))
        if not more:
            break
        data += more
    return data


class TarReader:
    """Reads the members of a tar archive front to back from a binary stream, without seeking.

    Parses ustar headers, pax extended headers and GNU long names, and verifies header
    checksums, the end-of-archive marker, and that only zeros follow it, up to the end of the
    stream. Iterate for members, and read the data of the current regular file with
    ``chunks()``; data that is not read is skipped."""

    def __init__(self, stream: IO[bytes]) -> None:
        self.stream = stream
        #: Unread data of the current member
        self.remaining = 0
        self.buf = b""
        self.pos = 0

    def _more(self, size: int) -> None:
        """Make sure size bytes are buffered, or fewer at the end of the stream."""
        rest = self.buf[self.pos :]
        # Not joined with an empty rest, which would copy what is read
        parts = [rest] if rest else []
        have = len(rest)
        while have < size:
            more = self.stream.read(max(_BUF, size - have))
            if not more:
                break
            parts.append(more)
            have += len(more)
        self.buf = b"".join(parts)
        self.pos = 0

    def _read(self, size: int) -> bytes:
        if self.pos + size > len(self.buf):
            self._more(size)
            if size > len(self.buf):
                raise Error("Archive is truncated")
        pos = self.pos
        self.pos = pos + size
        return self.buf[pos : pos + size]

    def _skip(self, size: int) -> None:
        if self.pos + size <= len(self.buf):
            self.pos += size
            return
        size -= len(self.buf) - self.pos
        self.buf, self.pos = b"", 0
        while size:
            more = self.stream.read(min(size, _BUF))
            if not more:
                raise Error("Archive is truncated")
            size -= len(more)

    def _end(self) -> None:
        """Read the rest of the stream, after the end-of-archive marker. Writers pad it with
        zeros, and anything else, like a second archive, would be ignored by every reader."""
        rest = self.buf[self.pos :]
        self.buf, self.pos = b"", 0
        while not rest.strip(b"\0"):
            rest = self.stream.read(_BUF)
            if not rest:
                return
        raise Error("Archive contains data after the end-of-archive marker")

    def _header(self) -> Optional[bytes]:
        """The next header, or None at the end-of-archive marker."""
        header = self._read(_BLOCK)
        if header == _EOF_BLOCK:
            # The marker is two zero blocks. tar and tarfile stop at one, and skip what follows.
            if self._read(_BLOCK) != _EOF_BLOCK:
                raise Error("Archive contains a lone zero block")
            return None
        if not _checksum_ok(header):
            raise Error("Archive contains a header with an invalid checksum")
        return header

    def chunks(self, size: int = _CHUNK) -> Iterator[memoryview]:
        """Yield the unread data of the current member, as views that stay valid."""
        while self.remaining:
            if self.pos >= len(self.buf):
                self._more(1)
                if not self.buf:
                    raise Error("Archive is truncated")
            pos = self.pos
            n = min(size, self.remaining, len(self.buf) - pos)
            self.pos = pos + n
            self.remaining -= n
            yield memoryview(self.buf)[pos : pos + n]

    def __iter__(self) -> Iterator[Member]:
        self._more(_BLOCK)
        if not self.buf:
            raise Error("Archive is empty")
        padding = 0
        while True:
            self._skip(self.remaining + padding)
            self.remaining = 0

            # Extended headers apply to the next member, and may give its name in one way only,
            # so that readers that resolve conflicts differently cannot see different members.
            pax: Dict[str, str] = {}
            long_name: Optional[str] = None
            long_link: Optional[str] = None
            seen = b""
            budget = _MAX_EXTENDED
            while True:
                header = self._header()
                if header is None:
                    if seen:
                        raise Error("Archive ends after an extended header")
                    self._end()
                    return
                type = header[156:157]
                if type not in _EXTENDED:
                    break
                size = _int(header[124:136])
                budget -= size
                if budget < 0:
                    raise Error("Archive contains extended headers of more than 1 MiB")
                data = self._read(size)
                self._read(-size % _BLOCK)
                if type == _PAX_GLOBAL_HEADER:
                    # Readers disagree on whether these apply to later members: refuse them.
                    if {"path", "linkpath", "size"} & _pax_records(data).keys():
                        raise Error(
                            "Archive contains a global pax path, linkpath or size"
                        )
                    continue
                kind = _PAX_HEADER if type == _SOLARIS_PAX_HEADER else type
                if kind in seen:
                    raise Error(f"Archive contains two {kind!r} headers for one member")
                seen += kind
                if kind == _PAX_HEADER:
                    pax = _pax_records(data)
                elif kind == _GNU_LONGNAME:
                    long_name = _long_name(data)
                else:
                    long_link = _long_name(data)
            if long_name is not None and "path" in pax:
                raise Error("Archive contains both a pax path and a GNU long name")
            if long_link is not None and "linkpath" in pax:
                raise Error("Archive contains both a pax linkpath and a GNU long link")
            for key in ("path", "linkpath"):
                if key in pax and (not pax[key] or "\0" in pax[key]):
                    raise Error(f"Archive contains an invalid pax {key} {pax[key]!r}")

            name = _str(header[0:100])
            # Like GNU tar, only POSIX ustar headers (version 00) have a name prefix
            if header[257:265] == b"ustar\x0000":
                prefix = _str(header[345:500])
                if prefix:
                    name = f"{prefix}/{name}"
            if type == AREGTYPE and name.endswith("/"):
                type = DIRTYPE
            if type == b"S" or any(key.startswith("GNU.sparse.") for key in pax):
                raise Error(
                    f"Archive contains a sparse file {name}, which is not supported"
                )

            name = long_name if long_name is not None else pax.get("path", name)
            if type == DIRTYPE:
                name = name.rstrip("/") or name
            if "size" in pax:
                size = _decimal(pax["size"], "size")
            else:
                size = _int(header[124:136])
            if long_link is None:
                long_link = pax.get("linkpath", _str(header[157:257]))
            member = Member(name, type, _int(header[100:108]), size, long_link)

            if type not in _NO_DATA_TYPES:
                self.remaining = member.size
            elif member.size and type != DIRTYPE:
                # Readers disagree on whether data follows. Some tar implementations give dirs
                # a size, which tar and tarfile ignore, so only those are read like tar.
                raise Error(
                    f"Archive contains {name} of type {type!r} with size {member.size}"
                )
            padding = -self.remaining % _BLOCK
            yield member


class _Prepend:
    """A stream that first returns ``head`` and then reads from ``stream``."""

    def __init__(self, head: bytes, stream: IO[bytes]) -> None:
        self.head = head
        self.stream = stream

    def read(self, size: int) -> bytes:
        if not self.head:
            return self.stream.read(size)
        data, self.head = self.head[:size], self.head[size:]
        if len(data) < size:
            data += self.stream.read(size - len(data))
        return data


class _Gzip:
    """A gzip stream whose errors are untar errors."""

    def __init__(self, stream: _Prepend) -> None:
        self.gzip = gzip.GzipFile(fileobj=stream, mode="rb")  # type: ignore[call-overload]

    def read(self, size: int = -1) -> bytes:
        try:
            return self.gzip.read(size)
        except EOFError:
            raise Error("Archive is truncated") from None
        except (zlib.error, _BadGzipFile) as e:
            raise Error(f"Archive is not valid gzip: {e}") from e


@contextlib.contextmanager
def _open_archive(
    src: Union[str, "os.PathLike[str]", IO[bytes]],
) -> Iterator[IO[bytes]]:
    """Open a path or a binary file object as a stream of uncompressed tar data, which is
    detected from the first bytes. Use as a context manager; file objects are not closed."""
    file = open(src, "rb") if isinstance(src, (str, os.PathLike)) else None  # noqa: SIM115
    try:
        stream = file or src
        magic = _fill(stream, 2)  # type: ignore[arg-type]
        head = _Prepend(magic, stream)  # type: ignore[arg-type]
        yield _Gzip(head) if magic == b"\x1f\x8b" else head  # type: ignore
    finally:
        if file is not None:
            file.close()


def _common(a: List[str], b: List[str]) -> int:
    """The number of leading names a and b have in common."""
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


def _parts(name: str) -> List[str]:
    """Split a member name into path components, rejecting names that escape the destination."""
    parts = [p for p in name.split("/") if p and p != "."]
    if (
        name.startswith("/")
        or ".." in parts
        or _WINDOWS
        and any("\\" in p or ":" in p for p in parts)
    ):
        raise Error(f"Archive contains unsafe path {name}")
    return parts


def _resolve(parts: List[str], linkname: str) -> Optional[List[str]]:
    """The member a relative symlink at parts points to, or None if it points outside."""
    if linkname.startswith("/"):
        return None
    target = parts[:-1]
    for part in linkname.split("/"):
        if part == "..":
            if not target:
                return None
            target = target[:-1]
        elif part and part != ".":
            target = target + [part]
    return target


#: Whether entries are created relative to open dir file descriptors. Otherwise, as on Windows,
#: they are created by (extended-length) path.
_DIR_FD = all(
    # By name, since Windows has no os.chown
    getattr(os, name, None) in os.supports_dir_fd
    for name in (
        "open",
        "mkdir",
        "symlink",
        "link",
        "rename",
        "stat",
        "unlink",
        "rmdir",
        "chown",
    )
) and all(
    getattr(os, name, None) in os.supports_follow_symlinks
    for name in ("link", "stat", "chown")
)
_O_NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)
_O_BINARY = getattr(os, "O_BINARY", 0)
# os.open makes file descriptors non-inheritable, so O_CLOEXEC is implied
#: The caller chooses dest, so it may be a symlink, unlike the dirs in the archive
_DEST_FLAGS = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
_DIR_FLAGS = _DEST_FLAGS | _O_NOFOLLOW
_FILE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_EXCL | _O_NOFOLLOW | _O_BINARY

#: An open dir: a file descriptor, or a path where dir file descriptors are not supported
Dir = Union[int, str]


def _at(parent: Dir, name: str) -> Tuple[str, Optional[int]]:
    """The path and dir_fd arguments for name in parent."""
    if isinstance(parent, int):
        return name, parent
    return os.path.join(parent, name), None


def _open_dir(parent: Dir, name: str) -> Dir:
    """Open the dir name in parent, without following symlinks."""
    if isinstance(parent, int):
        try:
            return os.open(name, _DIR_FLAGS, dir_fd=parent)
        except OSError as e:
            if e.errno in (errno.ELOOP, errno.ENOTDIR):
                raise Error(
                    f"Archive writes through {name}, which is not a directory"
                ) from e
            raise
    path = os.path.join(parent, name)
    if not stat.S_ISDIR(os.lstat(path).st_mode):
        raise Error(f"Archive writes through {name}, which is not a directory")
    return path


def _lstat(parent: Dir, name: str) -> Optional[os.stat_result]:
    """Stat name in parent without following symlinks, or None if it does not exist."""
    path, dir_fd = _at(parent, name)
    try:
        return os.stat(path, dir_fd=dir_fd, follow_symlinks=False)
    except FileNotFoundError:
        return None


def _close(d: Dir) -> None:
    if isinstance(d, int):
        os.close(d)


def _rmdir(parent: Dir, name: str) -> bool:
    """Remove the dir name in parent if it is empty, and return whether it was removed."""
    path, dir_fd = _at(parent, name)
    try:
        os.rmdir(path, dir_fd=dir_fd)
    except OSError:
        return False
    return True


def _remove_files(d: Dir) -> List[str]:
    """Remove the entries of d that are not dirs, as far as possible, and return its subdirs."""
    subdirs = []
    for name in os.listdir(d):
        path, dir_fd = _at(d, name)
        with contextlib.suppress(OSError):
            s = os.stat(path, dir_fd=dir_fd, follow_symlinks=False)
            if stat.S_ISDIR(s.st_mode):
                subdirs.append(name)
            else:
                os.unlink(path, dir_fd=dir_fd)
    return subdirs


#: Errors of creating a link where the platform or filesystem does not support it
_UNSUPPORTED = {
    errno.EPERM,
    errno.ENOSYS,
    errno.EOPNOTSUPP,
    getattr(errno, "ENOTSUP", 0),
}


def _unsupported(e: OSError) -> bool:
    """Whether a link could not be created because links are not supported."""
    # Windows requires a privilege for symlinks, and some filesystems have no hardlinks
    return e.errno in _UNSUPPORTED or _WINDOWS and not isinstance(e, FileExistsError)


class _Extractor:
    """Extracts members in a single pass, each to its full archive name in a temporary dir.

    Where supported, entries are created relative to open dir file descriptors, so paths are
    never longer than a single name, and nothing is written through a symlink, even one swapped
    in concurrently. The open dirs are a stack of the ancestors of the current member, which for
    the depth-first order of tar archives changes little from one member to the next. Only the
    deepest ``_MAX_OPEN_DIRS`` of them stay open, so that deep archives do not run out of file
    descriptors; closed ones are opened again from tmp when needed.

    The archive name of the final root is only known after the last member. Validation only
    needs ``root``, the deepest dir containing every member that is not a dir leading up to
    it. State is bounded by the depth of the archive, apart from links that could not be
    created."""

    def __init__(
        self,
        dest: Union[str, int],
        root_marker: Optional[str],
        file_mode: int,
        dir_mode: int,
        gid: Optional[int],
    ) -> None:
        self.file_mode = file_mode
        self.dir_mode = dir_mode
        self.gid = gid
        self.root: List[str] = []
        self.descending = True
        self.marker_name = root_marker
        #: The shallowest member with the marker name
        self.marker: Optional[List[str]] = None
        #: Symlinks that could not be created, to be copies of targets extracted later
        self.links: List[Tuple[List[str], List[str]]] = []
        #: The names of the dirs below tmp that lead to the current member
        self.names: List[str] = []
        #: The deepest of those dirs, at most _MAX_OPEN_DIRS, which are open
        self.dirs: List[Dir] = []

        if isinstance(dest, int):
            # A copy, so that the caller's file descriptor stays open
            self.dest: Dir = os.dup(dest)
        else:
            os.makedirs(dest, exist_ok=True)
            dest = os.path.abspath(dest)
            if _WINDOWS and not dest.startswith("\\\\?\\"):
                # an extended-length path, which may exceed MAX_PATH
                dest = "\\\\?\\" + dest
            self.dest = os.open(dest, _DEST_FLAGS) if _DIR_FD else dest
        while True:
            tmp_name = f".untar-{os.urandom(4).hex()}"
            path, dir_fd = _at(self.dest, tmp_name)
            try:
                os.mkdir(path, 0o700, dir_fd=dir_fd)
                break
            except FileExistsError:
                pass
        self.tmp_name = tmp_name
        self.tmp = _open_dir(self.dest, tmp_name)

        # Find out once what the filesystem does to new entries: mode bits the umask or default
        # ACLs strip, special bits it does not set, and the group they get.
        path, dir_fd = _at(self.tmp, "probe")
        os.close(os.open(path, _FILE_FLAGS, file_mode, dir_fd=dir_fd))
        s = os.stat(path, dir_fd=dir_fd, follow_symlinks=False)
        os.unlink(path, dir_fd=dir_fd)
        self.chown = gid is not None and s.st_gid != gid
        self.chmod_files = not _WINDOWS and stat.S_IMODE(s.st_mode) != file_mode
        os.mkdir(path, dir_mode, dir_fd=dir_fd)
        s = os.stat(path, dir_fd=dir_fd, follow_symlinks=False)
        os.rmdir(path, dir_fd=dir_fd)
        self.chmod_dirs = not _WINDOWS and stat.S_IMODE(s.st_mode) != dir_mode

    def close(self) -> None:
        """Remove tmp, as far as possible, and close the open dirs."""
        # After finish, the stack holds the now empty dirs leading up to the root: remove the open
        # ones bottom up, without listing them.
        while self.dirs:
            _close(self.dirs.pop())
            name = self.names.pop()
            n, parent = self._open_ancestor(len(self.names))
            if n < len(self.names) or not _rmdir(parent, name):
                break
        for d in self.dirs:
            _close(d)
        if not _rmdir(self.dest, self.tmp_name):
            with contextlib.suppress(OSError):
                self._remove_tmp()
            _rmdir(self.dest, self.tmp_name)
        _close(self.tmp)
        _close(self.dest)

    def _remove_tmp(self) -> None:
        """Remove what is in tmp, as far as possible. The subdirs of a dir are moved into tmp
        before it is removed, so that every dir is opened from tmp: without following symlinks,
        one at a time, and in time linear in the number of entries, whatever their depth."""
        todo = _remove_files(self.tmp)
        taken = set(todo)
        i = 0
        while todo:
            name = todo.pop()
            with contextlib.suppress(OSError, Error):
                d = _open_dir(self.tmp, name)
                try:
                    for sub in _remove_files(d):
                        while str(i) in taken:
                            i += 1
                        path, dir_fd = _at(d, sub)
                        new_path, new_dir_fd = _at(self.tmp, str(i))
                        os.rename(
                            path, new_path, src_dir_fd=dir_fd, dst_dir_fd=new_dir_fd
                        )
                        taken.add(str(i))
                        todo.append(str(i))
                finally:
                    _close(d)
                _rmdir(self.tmp, name)

    def _attrs(self, d: Dir, mode: int, chmod: bool) -> None:
        """Set the group and mode of an open file or dir, which never follows a symlink."""
        if isinstance(d, str):
            # A dir by path, where dir file descriptors are not supported, but it may still be
            # opened without following a symlink
            if self.chown or chmod:
                fd = os.open(d, _DIR_FLAGS)
                try:
                    self._attrs(fd, mode, chmod)
                finally:
                    os.close(fd)
            return
        # chown before chmod, since chown may clear set-user-ID and set-group-ID bits
        if self.chown:
            os.fchown(d, -1, self.gid)  # type: ignore
        if chmod:
            os.fchmod(d, mode)  # type: ignore

    def _dir(self, parts: List[str]) -> Dir:
        """Open tmp/parts, creating missing dirs, and keep its deepest ancestors open."""
        n, parent = self._open_ancestor(_common(self.names, parts))
        # The open dirs above depth n stay
        keep = max(n - len(self.names) + len(self.dirs), 0)
        for d in self.dirs[keep:]:
            _close(d)
        del self.names[n:], self.dirs[keep:]
        for name in parts[n:]:
            try:
                d = _open_dir(parent, name)
            except FileNotFoundError:
                d = self._mkdir(parent, name)
            self._push(name, d)
            parent = d
        return parent

    def _mkdir(self, parent: Dir, name: str) -> Dir:
        """Create the dir name in parent, and open it."""
        path, dir_fd = _at(parent, name)
        os.mkdir(path, self.dir_mode, dir_fd=dir_fd)
        d = _open_dir(parent, name)
        self._attrs(d, self.dir_mode, self.chmod_dirs)
        return d

    def _push(self, name: str, d: Dir) -> None:
        """Put an open dir on the stack, and close the one that is no longer among the deepest."""
        self.names.append(name)
        self.dirs.append(d)
        if len(self.dirs) > _MAX_OPEN_DIRS:
            _close(self.dirs.pop(0))

    def _open_ancestor(self, n: int) -> Tuple[int, Dir]:
        """The dir tmp/names[:n] and n if it is open, and otherwise tmp and 0: since only the
        deepest dirs are open, none of its ancestors is then."""
        closed = len(self.names) - len(self.dirs)
        if n > closed:
            return n, self.dirs[n - closed - 1]
        return 0, self.tmp

    def _file(
        self,
        parent: Dir,
        name: str,
        mode: int,
        chunks: Iterable[Union[bytes, memoryview]],
    ) -> None:
        path, dir_fd = _at(parent, name)
        fd = os.open(path, _FILE_FLAGS, mode, dir_fd=dir_fd)
        try:
            for data in chunks:
                view = memoryview(data)
                while view:
                    view = view[os.write(fd, view) :]
            self._attrs(fd, mode, self.chmod_files)
        finally:
            os.close(fd)

    def _track(self, member: Member, parts: List[str]) -> None:
        """Update root, which validation needs, and marker."""
        if parts[-1:] == [self.marker_name] and (
            self.marker is None or len(parts) < len(self.marker)
        ):
            self.marker = parts
        common = _common(parts, self.root)
        if common == len(parts):
            if not member.isdir():
                raise Error(
                    f"Archive contains non-directory {member.name} where a directory is"
                )
        elif common < len(self.root):
            self.root = self.root[:common]
            self.descending = False
        elif self.descending:
            # Nothing but dirs so far: descend to the deepest dir containing this member.
            self.root = parts if member.isdir() else parts[:-1]
            self.descending = member.isdir()

    def add(self, member: Member, reader: TarReader) -> None:
        parts = _parts(member.name)
        self._track(member, parts)
        if not parts:
            return
        if not member.isdir() and member.name.rstrip(".").endswith("/"):
            raise Error(
                f"Archive contains non-directory {member.name} named like a directory"
            )
        parent = self._dir(parts[:-1])
        path, dir_fd = _at(parent, parts[-1])
        if member.isdir():
            try:
                self._push(parts[-1], self._mkdir(parent, parts[-1]))
            except FileExistsError:
                self._dir(parts)
        elif member.isreg():
            # Like chmod +X: only executable if the member is executable by its owner
            mode = self.file_mode if member.mode & 0o100 else self.file_mode & ~0o111
            # Each write as large as what is buffered
            self._file(parent, parts[-1], mode, reader.chunks(_BUF))
        elif member.issym():
            if not member.linkname:
                raise Error(f"Archive contains symlink {member.name} without a target")
            try:
                os.symlink(member.linkname, path, dir_fd=dir_fd)
            except OSError as e:
                if not _unsupported(e):
                    raise
                # Like tarfile, copy the target instead where symlinks are not supported.
                target = _resolve(parts, member.linkname)
                if target is not None and not self._copy(target, parts):
                    self.links.append((target, parts))
                return
            if self.chown:
                os.chown(path, -1, self.gid, dir_fd=dir_fd, follow_symlinks=False)  # type: ignore
        elif member.islnk():
            if not self._copy(_parts(member.linkname), parts, link=True):
                raise Error(
                    f"Archive hardlinks {member.linkname}, which is not extracted"
                )
        else:
            raise Error(
                f"Archive contains {member.name} of unsupported type {member.type!r}"
            )

    def _open_existing(self, parts: List[str]) -> Tuple[Dir, bool]:
        """Open tmp/parts without creating anything, from the deepest dir on the stack that
        contains it. Returns the dir and whether it was opened here, and must be closed."""
        common, d = self._open_ancestor(_common(self.names, parts))
        owned = False
        for name in parts[common:]:
            try:
                child = _open_dir(d, name)
            finally:
                if owned:
                    _close(d)
            d, owned = child, True
        return d, owned

    def _copy(self, source: List[str], dest: List[str], link: bool = False) -> bool:
        """Hardlink or copy an extracted entry to dest, and return whether it was extracted."""
        if not source:
            return False
        # Open dest's parent first, since that may close dirs on the stack that source reuses.
        parent = self._dir(dest[:-1])
        try:
            source_parent, owned = self._open_existing(source[:-1])
        except (FileNotFoundError, Error):
            return False
        try:
            s = _lstat(source_parent, source[-1])
            if s is None:
                return False
            if source == dest:
                # tar archives an entry listed twice as a hardlink to itself
                return not stat.S_ISDIR(s.st_mode)
            path, dir_fd = _at(source_parent, source[-1])
            if stat.S_ISDIR(s.st_mode):
                if link:
                    raise Error(
                        f"Archive hardlinks {'/'.join(source)}, which is a directory"
                    )
                self._dir(dest)
                return True
            if link:
                dest_path, dest_fd = _at(parent, dest[-1])
                try:
                    os.link(
                        path,
                        dest_path,
                        src_dir_fd=dir_fd,
                        dst_dir_fd=dest_fd,
                        follow_symlinks=False,
                    )
                    return True
                except OSError as e:
                    if not _unsupported(e):
                        raise
                    # Like tarfile, copy where hardlinks are not supported
            if not stat.S_ISREG(s.st_mode):
                return False
            src = os.open(path, os.O_RDONLY | _O_BINARY, dir_fd=dir_fd)
            try:
                chunks = iter(lambda: os.read(src, _CHUNK), b"")
                self._file(parent, dest[-1], stat.S_IMODE(s.st_mode), chunks)
            finally:
                os.close(src)
            return True
        finally:
            if owned:
                _close(source_parent)

    def finish(self) -> str:
        """Move the contents of the final root into dest, and return its archive name."""
        root: List[str] = []
        if self.marker_name is not None:
            if self.marker is None:
                raise Error(f"Archive contains no member named {self.marker_name}")
            root = self.marker[:-1]
        if self.root[: len(root)] != root:
            raise Error(f"Archive contains members outside of {'/'.join(root) or '.'}")

        for source, dest in self.links:
            self._copy(source, dest)

        src = self._dir(root)
        names = os.listdir(src)
        for name in names:
            if _lstat(self.dest, name) is not None:
                raise Error(f"{name} exists in the destination")
        for name in names:
            path, dir_fd = _at(src, name)
            new_path, new_dir_fd = _at(self.dest, name)
            os.rename(path, new_path, src_dir_fd=dir_fd, dst_dir_fd=new_dir_fd)
        return "/".join(root)


def extract(
    src: Union[str, "os.PathLike[str]", IO[bytes]],
    dest: Union[str, int],
    *,
    root_marker: Optional[str] = None,
    file_mode: int = 0o755,
    dir_mode: int = 0o755,
    gid: Optional[int] = None,
) -> str:
    """Extract the tar archive ``src``, a path or a binary file object that is read front to
    back once, into ``dest``: a path, which is created if it does not exist and may be a symlink
    to a dir, or the file descriptor of an open dir, which stays open. Entries already in
    ``dest`` are not replaced: an archive with one of the same name is an error.

    With ``root_marker``, only the contents of the parent of the shallowest member with that
    name are extracted, and the archive name of that parent is returned. Other members must be
    in it, except for the dirs leading up to it. Without, everything is extracted and ``""`` is
    returned. Nothing is written through a symlink, and except on Windows, no path longer than a
    single name is passed to the operating system.

    Files are created with ``file_mode``, without executable bits if the member is not
    executable by its owner, and dirs with ``dir_mode``, which must give the owner rwx; with
    ``gid``, both get that group. Timestamps and ownership in the archive are not restored.
    Members must be regular files, dirs, symlinks or hardlinks, and cannot be absolute or
    contain ``..``. Where links cannot be created, their targets are copied."""
    if isinstance(dest, int) and not _DIR_FD:
        raise ValueError("dest cannot be a file descriptor on this platform")
    if gid is not None and _WINDOWS:
        raise ValueError("gid is not supported on Windows")
    # Dir modes are set when dirs are created, and entries are then created in them
    if dir_mode & 0o700 != 0o700:
        raise ValueError(f"dir_mode {oct(dir_mode)} must give the owner rwx (0o700)")
    extractor = _Extractor(dest, root_marker, file_mode, dir_mode, gid)
    try:
        with _open_archive(src) as stream:
            reader = TarReader(stream)
            # The reader reads the stream to its end, which verifies a gzip checksum
            for member in reader:
                extractor.add(member, reader)
        return extractor.finish()
    finally:
        extractor.close()


def _main(argv: Optional[List[str]] = None) -> int:
    """``python -m untar <archive> <dest>``, like ``tar xf <archive> -C <dest>``."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="python -m untar",
        description="Extract a tar archive, optionally gzip compressed, into a directory.",
    )
    parser.add_argument("archive", help="the archive, or - to read standard input")
    parser.add_argument(
        "dest", help="the directory to extract into, created if it does not exist"
    )
    args = parser.parse_args(argv)
    src = sys.stdin.buffer if args.archive == "-" else args.archive
    try:
        extract(src, args.dest)
    except (Error, OSError) as e:
        # Like tar, exit with 2 on errors
        print(f"untar: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_main())
