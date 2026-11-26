"""Fast, safe, streaming extraction of tar archives that distribute software.

Archives are read front to back in a single pass from a file path or any readable binary stream,
parsing only the header fields required for extraction. Owners, groups, timestamps, and full mode
bits from the archive are ignored; extracted files and directories receive caller-specified
permissions.
"""

import contextlib
import errno
import gzip
import os
import stat
import sys
import zlib
from typing import IO, Any, Dict, Iterable, Iterator, List, Optional, Set, Tuple, Union

if sys.platform == "win32":
    import _winapi
    import msvcrt

    _GENERIC_READ = 0x80000000
    _GENERIC_WRITE = 0x40000000
    _FILE_SHARE_READ_WRITE = 0x1 | 0x2
    _CREATE_NEW = 1
    _OPEN_EXISTING = 3
    _FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
    _FILE_ATTRIBUTE_READONLY = 0x1
    _FILE_ATTRIBUTE_NORMAL = 0x80
    _FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000

__version__ = "0.5.0"
__all__ = ["Error", "Member", "TarReader", "extract"]

REGTYPE = b"0"
AREGTYPE = b"\0"
LNKTYPE = b"1"
SYMTYPE = b"2"
DIRTYPE = b"5"
_PAX_HEADER = b"x"
_PAX_GLOBAL_HEADER = b"g"
_GNU_LONGNAME = b"L"
_GNU_LONGLINK = b"K"
# Solaris 'X' extended headers are omitted so they are rejected as an unsupported member type.
_EXTENDED = (_PAX_HEADER, _PAX_GLOBAL_HEADER, _GNU_LONGNAME, _GNU_LONGLINK)
# Contiguous files ('7') are omitted because implementations disagree on whether they carry data.
_DATA_TYPES = (REGTYPE, AREGTYPE)
# Directories, devices, and FIFOs never carry a data payload.
_NO_DATA_TYPES = (DIRTYPE, b"3", b"4", b"6")

_WINDOWS = sys.platform == "win32"
_BLOCK = 512
_EOF_BLOCK = bytes(_BLOCK)
# Minimum file size (8 GiB) that does not fit in an 11-digit octal ustar size field.
_PAX_SIZE = 8**11
_CHUNK = 64 * 1024
_BUF = 1024 * 1024
# Pax keys that alter file contents, encoding, or permissions in ways that only some readers apply.
_REFUSED_KEYS = frozenset(
    (
        b"hdrcharset",
        b"mode",
        b"SCHILY.realsize",
        b"SUN.holesdata",
        b"SCHILY.xattr.system.posix_acl_access",
        b"SCHILY.xattr.system.posix_acl_default",
        b"LIBARCHIVE.xattr.system.posix_acl_access",
        b"LIBARCHIVE.xattr.system.posix_acl_default",
    )
)
_REFUSED_PREFIXES = (b"GNU.sparse.", b"SCHILY.acl.")
# Per-member pax keys that are ambiguous when placed in a global pax header.
_MEMBER_KEYS = frozenset((b"path", b"linkpath", b"size"))
_MAX_EXTENDED = 1024 * 1024
# Cap pax decimal lengths to avoid quadratic int() conversion on huge digit strings.
_MAX_DIGITS = 32
# POSIX ustar magic with version "00", or "\0\0" as emitted by some Java archivers.
_POSIX_MAGICS = (b"ustar\x0000", b"ustar\0\0\0")
_V7_MAGIC = bytes(8)
_OTHER_MAGICS = (b"ustar  \0", _V7_MAGIC)
_MAX_OPEN_DIRS = 64
# Limit directory nesting depth; deep paths degrade to quadratic creation time on macOS.
_MAX_DEPTH = 1024
_DRIVES = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
_BadGzipFile = getattr(gzip, "BadGzipFile", OSError)


class Error(ValueError):
    """The archive is invalid or cannot be extracted safely."""


class Member:
    """A tar archive member containing only the fields needed for extraction."""

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


def _int(field: bytes, terminated: bool = True) -> int:
    """Parse a size field encoded in octal or positive GNU base-256."""
    if field[0] == 0o200:
        return int.from_bytes(field[1:], "big")
    elif field[0] == 0o377:
        raise Error("Archive contains a negative number")
    return _octal(field, terminated)


def _octal(field: bytes, terminated: bool = True) -> int:
    """Parse an octal field with optional leading spaces and trailing spaces or NULs."""
    digits = field.rstrip(b" \0")
    if not terminated or len(digits) < len(field):
        if digits.isdigit():
            try:
                return int(digits, 8)
            except ValueError:
                pass
        else:
            digits = digits.lstrip(b" ")
            if not digits.strip(b"01234567"):
                return int(digits, 8) if digits else 0
    raise Error(f"Archive contains an invalid number {field!r}")


def _name(raw: bytes) -> str:
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        raise Error(f"Archive contains a name that is not UTF-8 {raw!r}") from None


def _long_name(data: bytes) -> str:
    """Parse a NUL-terminated GNU long name or link target without embedded NULs."""
    name = data.rstrip(b"\0")
    if not name:
        raise Error("Archive contains an empty GNU long name")
    if len(name) == len(data):
        raise Error(
            f"Archive contains a GNU long name without a NUL at its end {name!r}"
        )
    if 0 in name:
        raise Error(f"Archive contains a GNU long name with a NUL inside {name!r}")
    return _name(name)


def _pax_name(key: str, value: bytes) -> str:
    """Parse a pax path or linkpath, rejecting empty values, NULs, and newlines."""
    if not value or 0 in value:
        raise Error(f"Archive contains an invalid pax {key} {value!r}")
    # Line-based pax parsers split records on newlines even when the record length spans past them.
    if 0x0A in value:
        raise Error(f"Archive contains a newline in the pax {key}")
    return _name(value)


def _pax_size(value: bytes) -> int:
    """Parse a pax size: ASCII decimal digits without leading zeros."""
    if (
        not value
        or value.strip(b"0123456789")
        or len(value) > _MAX_DIGITS
        or (value[0] == 0x30 and len(value) > 1)
    ):
        raise Error(f"Archive contains an invalid pax size {value[:_MAX_DIGITS]!r}")
    return int(value)


def _checksum_ok(header: bytes) -> bool:
    # Some writers emit an 8-digit octal checksum without a trailing NUL or space.
    field = header[148:156]
    expected = _octal(field, False)
    # The low 16 bits of adler32 compute the exact unsigned byte sum mod 65521 (safe for <= 256 B).
    total = (zlib.adler32(header[:256], 0) & 0xFFFF) + (
        zlib.adler32(header[256:], 0) & 0xFFFF
    )
    return expected == total - sum(field) + 256


def _pax_records(data: bytes) -> Dict[bytes, bytes]:
    """Parse ``<length> <key>=<value>\\n`` records from a pax extended header."""
    records: Dict[bytes, bytes] = {}
    pos = 0
    while pos < len(data):
        space = data.find(b" ", pos, pos + _MAX_DIGITS + 1)
        length = data[pos:space]
        if space < 0 or not length.isdigit() or length[0] == 0x30:
            raise Error("Archive contains an invalid pax header")
        end = pos + int(length)
        if end <= space or end > len(data) or data[end - 1] != 0x0A:
            raise Error("Archive contains an invalid pax header")
        key, equals, value = data[space + 1 : end - 1].partition(b"=")
        if not key or not equals or key[0] in b" \t" or 0 in key:
            raise Error("Archive contains an invalid pax record")
        if key in records:
            raise Error(f"Archive contains the pax {key!r} twice in one header")
        if key in _REFUSED_KEYS or key.startswith(_REFUSED_PREFIXES):
            raise Error(f"Archive contains the pax {key!r}, which is not supported")
        records[key] = value
        pos = end
    return records


def _fill(stream: IO[bytes], size: int) -> bytes:
    """Read up to size bytes from stream, looping across short reads until EOF."""
    data = stream.read(size)
    while 0 < len(data) < size:
        more = stream.read(size - len(data))
        if not more:
            break
        data += more
    return data


class TarReader:
    """Single-pass streaming reader for ustar, pax, and GNU tar archives.

    Iterating over a ``TarReader`` yields ``Member`` objects. Call ``chunks()`` to read the
    payload of the current regular file; any unread payload is skipped automatically when
    advancing to the next member.
    """

    def __init__(self, stream: IO[bytes]) -> None:
        self.stream = stream
        self.remaining = 0
        self.buf = b""
        self.pos = 0

    def _more(self, size: int) -> None:
        """Buffer at least size bytes (or until EOF)."""
        rest = self.buf[self.pos :]
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
        """Verify that only zero padding follows the end-of-archive marker."""
        rest = self.buf[self.pos :]
        self.buf, self.pos = b"", 0
        while not rest.strip(b"\0"):
            rest = self.stream.read(_BUF)
            if not rest:
                return
        raise Error("Archive contains data after the end-of-archive marker")

    def _header(self) -> Optional[bytes]:
        """Read the next header block, or return None at the end of the archive."""
        if self.pos == len(self.buf):
            self._more(_BLOCK)
            if not self.buf:
                return None
        header = self._read(_BLOCK)
        if header == _EOF_BLOCK:
            if self._read(_BLOCK) != _EOF_BLOCK:
                raise Error("Archive contains a lone zero block")
            return None
        if not _checksum_ok(header):
            raise Error("Archive contains a header with an invalid checksum")
        return header

    def chunks(self, size: int = _CHUNK) -> Iterator[memoryview]:
        """Yield unread data from the current member in chunks of up to size bytes."""
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
        # Readers that classify the archive format from the first header treat later pax headers
        # as regular files if the first header is v7 (empty magic).
        v7 = self.buf[257:265] == _V7_MAGIC
        padding = 0
        while True:
            self._skip(self.remaining + padding)
            self.remaining = 0

            # A member's name and link target each come from one source, and pax headers and GNU
            # long names do not mix, so conflicting overrides cannot produce different trees
            # across implementations.
            name: Optional[str] = None
            linkname: Optional[str] = None
            pax_size: Optional[int] = None
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
                if type == _GNU_LONGNAME or type == _GNU_LONGLINK:
                    if type[0] in seen:
                        raise Error(
                            f"Archive contains two {type!r} headers for one member"
                        )
                    if _PAX_HEADER[0] in seen:
                        raise Error(
                            "Archive contains both a pax header and a GNU long name for "
                            "one member"
                        )
                    if type == _GNU_LONGNAME:
                        name = _long_name(data)
                    else:
                        linkname = _long_name(data)
                    seen += type
                    continue
                if v7 or header[257:265] == _V7_MAGIC:
                    raise Error(
                        "Archive contains a pax header, and a header without magic"
                    )
                pax = _pax_records(data)
                if type == _PAX_GLOBAL_HEADER:
                    if seen:
                        raise Error(
                            "Archive contains a global pax header after an extended header"
                        )
                    if not _MEMBER_KEYS.isdisjoint(pax):
                        raise Error(
                            "Archive contains a global pax path, linkpath or size"
                        )
                    continue
                if seen:
                    raise Error(
                        "Archive contains two pax headers for one member"
                        if _PAX_HEADER[0] in seen
                        else "Archive contains both a pax header and a GNU long name for "
                        "one member"
                    )
                seen = _PAX_HEADER
                if b"path" in pax:
                    name = _pax_name("path", pax[b"path"])
                if b"linkpath" in pax:
                    linkname = _pax_name("linkpath", pax[b"linkpath"])
                if b"size" in pax:
                    pax_size = _pax_size(pax[b"size"])

            nul = header.find(b"\0", 0, 100)
            raw_name = header[:nul] if nul >= 0 else header[:100]
            # Only ustar headers carry a path prefix at offset 345; GNU incremental headers store
            # timestamps there.
            magic = header[257:265]
            if magic in _POSIX_MAGICS:
                # star's xstar format splits offset 345..500 into a 131-byte prefix and timestamps.
                if header[508:512] == b"tar\0" and 0 not in header[345:476]:
                    raise Error("Archive contains a star header with a long prefix")
                if header[345]:
                    raw_name = header[345:500].split(b"\0", 1)[0] + b"/" + raw_name
            elif magic not in _OTHER_MAGICS:
                raise Error(f"Archive contains a header with the magic {magic!r}")
            elif header[345]:
                raise Error(
                    "Archive contains a name prefix in a header that is not ustar"
                )
            if name is None:
                if nul >= 0 and header.count(b"\0", nul, 100) != 100 - nul:
                    raise Error(
                        f"Archive contains bytes after the NUL of the name {header[:100]!r}"
                    )
                name = _name(raw_name)
            if "\\" in name:
                raise Error(f"Archive contains a backslash in the name {name}")
            if type == AREGTYPE and name.endswith("/"):
                # V7 archives represent directories as type '\0' with a trailing slash in the ustar
                # name field; reject if the trailing slash came only from an extended header.
                if not raw_name.endswith(b"/"):
                    raise Error(
                        f"Archive contains {name}, named like a directory by its extended "
                        "header only"
                    )
                type = DIRTYPE

            mode = _octal(header[100:108])
            if pax_size is None:
                size = _int(header[124:136])
            else:
                # A pax size must match the ustar size unless the file is >= 8 GiB, where writers
                # place either 0 or an unterminated 12-digit octal value (bsdtar) in the header.
                size = _int(header[124:136], False)
                if pax_size != size and (size or pax_size < _PAX_SIZE):
                    raise Error(
                        f"Archive contains {name} with pax size {pax_size} and size {size}"
                    )
                size = pax_size

            if type in _DATA_TYPES:
                linkname = ""
                self.remaining = size
            elif type == SYMTYPE or type == LNKTYPE:
                if linkname is None:
                    raw = header[157:257].rstrip(b"\0")
                    if 0 in raw:
                        raise Error(
                            f"Archive contains bytes after the NUL of the link target {raw!r}"
                        )
                    linkname = _name(raw)
                if size:
                    raise Error(
                        f"Archive contains {name} of type {type!r} with size {size}"
                    )
            else:
                if linkname is not None or header[157]:
                    raise Error(
                        f"Archive contains {name} of type {type!r} with a link target"
                    )
                linkname = ""
                if type == DIRTYPE:
                    name = name.rstrip("/") or name
                if type not in _NO_DATA_TYPES:
                    if type == b"S":
                        raise Error(
                            f"Archive contains a sparse file {name}, which is not supported"
                        )
                    self.remaining = size
                elif size:
                    raise Error(
                        f"Archive contains {name} of type {type!r} with size {size}"
                    )
            padding = -self.remaining % _BLOCK
            yield Member(name, type, mode, size, linkname)


class _Prepend:
    """A stream wrapper that yields ``head`` before reading from ``stream``."""

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
    """A gzip stream wrapper that translates decompression errors into ``untar.Error``."""

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
    """Open a file path or binary stream, transparently decompressing gzip if detected."""
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
    """Return the number of leading elements shared by ``a`` and ``b``."""
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


def _parts(name: str) -> List[str]:
    """Split a member name into normalized path components, rejecting unsafe or overly deep paths."""
    parts = [p for p in name.split("/") if p and p != "."]
    if (
        name.startswith("/")
        or ".." in parts
        or name[1:2] == ":"
        and name[0] in _DRIVES
        or _WINDOWS
        and any("\\" in p or ":" in p for p in parts)
    ):
        raise Error(f"Archive contains unsafe path {name}")
    if len(parts) > _MAX_DEPTH:
        raise Error(f"Archive contains a path more than {_MAX_DEPTH} levels deep")
    return parts


def _resolve(parts: List[str], linkname: str) -> Optional[List[str]]:
    """Resolve a relative symlink target from ``parts``, or return None if it escapes the root."""
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


_DIR_FD = all(
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
_DEST_FLAGS = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
_DIR_FLAGS = _DEST_FLAGS | _O_NOFOLLOW
_FILE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_EXCL | _O_NOFOLLOW | _O_BINARY


def _create(path: str, dir_fd: Optional[int], mode: int) -> int:
    """Exclusively create and open a new file without following symlinks."""
    if sys.platform == "win32":
        # On Windows, os.open with O_CREAT | O_EXCL follows a dangling symlink and creates its
        # target; CreateFile with CREATE_NEW | FILE_FLAG_OPEN_REPARSE_POINT fails on any existing
        # reparse point.
        flags = _FILE_FLAG_OPEN_REPARSE_POINT | (
            _FILE_ATTRIBUTE_NORMAL if mode & stat.S_IWRITE else _FILE_ATTRIBUTE_READONLY
        )
        handle = _winapi.CreateFile(
            path, _GENERIC_WRITE, _FILE_SHARE_READ_WRITE, 0, _CREATE_NEW, flags, 0
        )
        try:
            return msvcrt.open_osfhandle(handle, os.O_NOINHERIT)
        except BaseException:
            _winapi.CloseHandle(handle)
            raise
    return os.open(path, _FILE_FLAGS, mode, dir_fd=dir_fd)


class _Pinned(str):
    """A directory path on Windows paired with an open handle that omits FILE_SHARE_DELETE,
    preventing the directory and its ancestors from being renamed, deleted, or replaced with a
    junction or symlink while open."""

    handle: int


_SetFileTime: Any = None


def _set_mtime(fd: int, mtime: float) -> None:
    """Set the access and modification times of an open file descriptor."""
    if sys.platform != "win32":
        os.utime(fd, (mtime, mtime))
    else:
        # Windows os.utime does not accept file descriptors; call SetFileTime on the OS handle
        # (in 100 ns intervals since 1601-01-01).
        import ctypes

        global _SetFileTime
        if _SetFileTime is None:
            _SetFileTime = ctypes.WinDLL("kernel32", use_last_error=True).SetFileTime
            _SetFileTime.argtypes = (ctypes.c_void_p,) * 4
        t = ctypes.c_uint64(int((mtime + 11644473600) * 10**7))
        handle = msvcrt.get_osfhandle(fd)
        if not _SetFileTime(handle, None, ctypes.byref(t), ctypes.byref(t)):
            raise ctypes.WinError(ctypes.get_last_error())


#: An open directory: an integer file descriptor on POSIX, or a path string (pinned on Windows).
Dir = Union[int, str]


def _at(parent: Dir, name: str) -> Tuple[str, Optional[int]]:
    if isinstance(parent, int):
        return name, parent
    return os.path.join(parent, name), None


def _open_dir(parent: Dir, name: str) -> Dir:
    """Open child directory ``name`` inside ``parent`` without following symlinks or junctions."""
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
    d = path
    if sys.platform == "win32":
        d = _Pinned(path)
        d.handle = _winapi.CreateFile(
            path,
            _GENERIC_READ,
            _FILE_SHARE_READ_WRITE,
            0,
            _OPEN_EXISTING,
            _FILE_FLAG_BACKUP_SEMANTICS | _FILE_FLAG_OPEN_REPARSE_POINT,
            0,
        )
    # Verify after pinning that the entry is a real directory and not a reparse point (junction).
    try:
        s = os.lstat(path)
        if not stat.S_ISDIR(s.st_mode) or getattr(s, "st_file_attributes", 0) & (
            stat.FILE_ATTRIBUTE_REPARSE_POINT
        ):
            raise Error(f"Archive writes through {name}, which is not a directory")
    except BaseException:
        _close(d)
        raise
    return d


def _lstat(parent: Dir, name: str) -> Optional[os.stat_result]:
    path, dir_fd = _at(parent, name)
    try:
        return os.stat(path, dir_fd=dir_fd, follow_symlinks=False)
    except FileNotFoundError:
        return None


def _close(d: Dir) -> None:
    if isinstance(d, int):
        os.close(d)
    elif sys.platform == "win32" and isinstance(d, _Pinned):
        _winapi.CloseHandle(d.handle)


def _rmdir(parent: Dir, name: str) -> bool:
    path, dir_fd = _at(parent, name)
    try:
        os.rmdir(path, dir_fd=dir_fd)
    except OSError:
        return False
    return True


def _remove_files(d: Dir) -> List[str]:
    """Unlink all non-directory entries in ``d`` and return the names of its subdirectories."""
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


_UNSUPPORTED = {
    errno.EPERM,
    errno.ENOSYS,
    errno.EOPNOTSUPP,
    getattr(errno, "ENOTSUP", 0),
}


def _unsupported(e: OSError) -> bool:
    """Return True if ``e`` indicates that the platform or filesystem does not support links."""
    return e.errno in _UNSUPPORTED or _WINDOWS and not isinstance(e, FileExistsError)


class _Extractor:
    """Extracts archive members into a temporary directory inside ``dest`` and moves the final
    root into place upon completion.

    Maintains a stack of open ancestor directories for the current member. On POSIX, at most the
    deepest ``_MAX_OPEN_DIRS`` descriptors are kept open at once to bound file descriptor usage;
    on Windows, every ancestor on the current path stays open so the entire chain remains pinned.
    """

    def __init__(
        self,
        dest: Union[str, int],
        root_marker: Optional[str],
        file_mode: int,
        dir_mode: int,
        gid: Optional[int],
        mtime: Optional[float],
    ) -> None:
        self.file_mode = file_mode
        self.dir_mode = dir_mode
        self.gid = gid
        self.mtime = mtime
        self.root: List[str] = []
        self.descending = True
        self.marker_name = root_marker
        self.marker: Optional[List[str]] = None
        # Deferred symlink copies (link path -> target path) when the OS does not support symlinks.
        self.links: Dict[Tuple[str, ...], Tuple[str, ...]] = {}
        # Paths of copied symlinks; no subsequent member may be extracted at or beneath them.
        self.copies: Set[Tuple[str, ...]] = set()
        self.names: List[str] = []
        self.dirs: List[Dir] = []

        if isinstance(dest, int):
            self.dest: Dir = os.dup(dest)
        else:
            os.makedirs(dest, exist_ok=True)
            # Resolve symlinks and junctions on the destination path once up front.
            dest = os.path.realpath(dest) if _WINDOWS else os.path.abspath(dest)
            if _WINDOWS and not dest.startswith("\\\\?\\"):
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
        if _WINDOWS:
            # Verify that no ancestor of dest was swapped for a junction or symlink before tmp was
            # pinned.
            path, _ = _at(self.dest, tmp_name)
            if os.path.normcase(os.path.realpath(path)) != os.path.normcase(path):
                _close(self.tmp)
                _rmdir(self.dest, tmp_name)
                raise Error(f"Destination {dest} changed while it was opened")

        # Probe the destination filesystem once to see whether umask, default ACLs, or setgid
        # inheritance require explicit fchmod/fchown calls after file and directory creation.
        path, dir_fd = _at(self.tmp, "probe")
        os.close(_create(path, dir_fd, file_mode))
        s = os.stat(path, dir_fd=dir_fd, follow_symlinks=False)
        os.unlink(path, dir_fd=dir_fd)
        self.chown = gid is not None and s.st_gid != gid
        self.chmod_files = not _WINDOWS and stat.S_IMODE(s.st_mode) != file_mode
        os.mkdir(path, dir_mode, dir_fd=dir_fd)
        s = os.stat(path, dir_fd=dir_fd, follow_symlinks=False)
        os.rmdir(path, dir_fd=dir_fd)
        self.chmod_dirs = not _WINDOWS and stat.S_IMODE(s.st_mode) != dir_mode

    def close(self) -> None:
        """Close all open directory handles and remove the temporary extraction directory."""
        while self.dirs:
            _close(self.dirs.pop())
            name = self.names.pop()
            n, parent = self._open_ancestor(len(self.names))
            if n < len(self.names) or not _rmdir(parent, name):
                break
        for d in self.dirs:
            _close(d)
        with contextlib.suppress(OSError):
            if os.listdir(self.tmp):
                self._remove_tmp()
        _close(self.tmp)
        _rmdir(self.dest, self.tmp_name)
        _close(self.dest)

    def _remove_tmp(self) -> None:
        """Empty ``self.tmp`` in O(N) time and with a single active directory descriptor by moving
        nested subdirectories directly into ``self.tmp`` before removing their parents."""
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
        if isinstance(d, str):
            if self.chown or chmod:
                fd = os.open(d, _DIR_FLAGS)
                try:
                    self._attrs(fd, mode, chmod)
                finally:
                    os.close(fd)
            return
        # Call fchown before fchmod because chown can clear setuid/setgid bits.
        if self.chown:
            os.fchown(d, -1, self.gid)  # type: ignore
        if chmod:
            os.fchmod(d, mode)  # type: ignore

    def _dir(self, parts: List[str]) -> Dir:
        """Navigate to ``tmp/parts``, creating any missing directories along the way."""
        n, parent = self._open_ancestor(_common(self.names, parts))
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
        path, dir_fd = _at(parent, name)
        os.mkdir(path, self.dir_mode, dir_fd=dir_fd)
        d = _open_dir(parent, name)
        self._attrs(d, self.dir_mode, self.chmod_dirs)
        return d

    def _push(self, name: str, d: Dir) -> None:
        self.names.append(name)
        self.dirs.append(d)
        if _DIR_FD and len(self.dirs) > _MAX_OPEN_DIRS:
            _close(self.dirs.pop(0))

    def _open_ancestor(self, n: int) -> Tuple[int, Dir]:
        """Return ``(n, dir)`` if ancestor depth ``n`` is still open on the stack, else ``(0, tmp)``."""
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
        fd = _create(path, dir_fd, mode)
        try:
            for data in chunks:
                view = memoryview(data)
                while view:
                    view = view[os.write(fd, view) :]
            self._attrs(fd, mode, self.chmod_files)
            if self.mtime is not None:
                _set_mtime(fd, self.mtime)
        finally:
            os.close(fd)

    def _track(self, member: Member, parts: List[str]) -> None:
        """Track the shallowest ``root_marker`` match and the common ancestor directory ``root``."""
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
            self.root = parts if member.isdir() else parts[:-1]
            self.descending = member.isdir()

    def add(self, member: Member, reader: TarReader) -> None:
        parts = _parts(member.name)
        self._track(member, parts)
        if not parts:
            return
        if self.copies:
            for i in range(1, len(parts) + 1):
                if tuple(parts[:i]) in self.copies:
                    raise Error(
                        f"Archive contains {member.name} at or below the symlink "
                        f"{'/'.join(parts[:i])}"
                    )
        if not member.isdir() and member.name.endswith(("/", "/.")):
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
            mode = self.file_mode if member.mode & 0o100 else self.file_mode & ~0o111
            self._file(parent, parts[-1], mode, reader.chunks(_BUF))
        elif member.issym():
            if not member.linkname:
                raise Error(f"Archive contains symlink {member.name} without a target")
            try:
                os.symlink(member.linkname, path, dir_fd=dir_fd)
            except OSError as e:
                if not _unsupported(e):
                    raise
                # Fall back to copying the file a symlink points to when symlinks are unavailable,
                # and refuse a symlink that cannot be copied rather than dropping it.
                target = _resolve(parts, member.linkname)
                if target is None:
                    raise Error(
                        f"Archive contains symlink {member.name} to {member.linkname}, "
                        "which cannot be copied"
                    )
                key = tuple(parts)
                self.copies.add(key)
                if not self._copy(target, parts):
                    self.links[key] = tuple(target)
                return
            if self.chown:
                os.chown(path, -1, self.gid, dir_fd=dir_fd, follow_symlinks=False)  # type: ignore
        elif member.islnk():
            if member.linkname.endswith(("/", "/.")):
                raise Error(
                    f"Archive hardlinks {member.linkname}, named like a directory"
                )
            source = _parts(member.linkname)
            if source == parts:
                raise Error(f"Archive hardlinks {member.name} to itself")
            if not self._copy(source, parts, link=True):
                raise Error(
                    f"Archive hardlinks {member.linkname}, which is not extracted"
                )
        else:
            raise Error(
                f"Archive contains {member.name} of unsupported type {member.type!r}"
            )

    def _open_existing(self, parts: List[str]) -> Tuple[Dir, List[Dir]]:
        """Open existing directory ``tmp/parts`` from the deepest open ancestor on the stack."""
        common, d = self._open_ancestor(_common(self.names, parts))
        opened: List[Dir] = []
        try:
            for name in parts[common:]:
                d = _open_dir(d, name)
                if _DIR_FD and opened:
                    _close(opened.pop())
                opened.append(d)
        except BaseException:
            for o in opened:
                _close(o)
            raise
        return d, opened

    def _copy(self, source: List[str], dest: List[str], link: bool = False) -> bool:
        """Hardlink or copy an already-extracted entry ``source`` to ``dest``, and return whether
        ``source`` is extracted. A directory can be neither hardlinked nor copied."""
        if not source:
            return False
        if link and tuple(source) in self.copies:
            raise Error(f"Archive hardlinks {'/'.join(source)}, which is a symlink")
        # Open dest's parent first because navigating the stack may close descriptors that source
        # would otherwise reuse.
        parent = self._dir(dest[:-1])
        try:
            source_parent, opened = self._open_existing(source[:-1])
        except (FileNotFoundError, Error):
            return False
        try:
            s = _lstat(source_parent, source[-1])
            if s is None:
                return False
            if link and stat.S_ISLNK(s.st_mode):
                raise Error(f"Archive hardlinks {'/'.join(source)}, which is a symlink")
            path, dir_fd = _at(source_parent, source[-1])
            if stat.S_ISDIR(s.st_mode):
                if link:
                    raise Error(
                        f"Archive hardlinks {'/'.join(source)}, which is a directory"
                    )
                # An empty directory in its place would silently lose what the symlink led to.
                raise Error(
                    f"Archive contains symlink {'/'.join(dest)} to the directory "
                    f"{'/'.join(source)}, which cannot be copied"
                )
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
            for d in opened:
                _close(d)

    def finish(self) -> str:
        """Resolve any deferred symlink copies, move the extracted root into ``dest``, and return
        its archive path."""
        root: List[str] = []
        if self.marker_name is not None:
            if self.marker is None:
                raise Error(f"Archive contains no member named {self.marker_name}")
            root = self.marker[:-1]
        if self.root[: len(root)] != root:
            raise Error(f"Archive contains members outside of {'/'.join(root) or '.'}")

        # Resolve deferred symlink chains in topological order.
        while self.links:
            chain = [self.links.popitem()]
            while chain[-1][1] in self.links:
                link = chain[-1][1]
                chain.append((link, self.links.pop(link)))
            for link, target in reversed(chain):
                if not self._copy(list(target), list(link)):
                    raise Error(
                        f"Archive contains symlink {'/'.join(link)} to "
                        f"{'/'.join(target)}, which is not extracted"
                    )

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
    mtime: Optional[float] = None,
) -> str:
    """Extract a tar archive ``src`` (a file path or readable binary stream) into ``dest`` (a
    directory path or open directory file descriptor).

    ``dest`` is created if it does not exist. Existing entries in ``dest`` are never overwritten;
    if any top-level entry from the archive already exists in ``dest``, ``untar.Error`` is raised
    and ``dest`` is left untouched.

    If ``root_marker`` is given, only the contents of the parent directory of the shallowest member
    with that filename are moved into ``dest``, and that directory's path in the archive is
    returned (or ``""`` when ``root_marker`` is omitted or at the archive root).

    Files are created with ``file_mode`` (clearing all execute bits unless the archive entry has
    owner execute permission ``0o100``), and directories with ``dir_mode`` (which must include
    owner ``0o700``). If ``gid`` is set, extracted entries are assigned to that group; if ``mtime``
    is set (in seconds since the epoch), all extracted files receive that modification time.

    Where links cannot be created, the file that a link points to is copied instead. A symlink
    that cannot be copied (one to a directory, or to a target outside the archive) is an error.

    Raises ``untar.Error`` for an archive that is invalid or unsafe, and ``OSError`` for an
    operation that the operating system refuses: notably ``FileExistsError`` for a name that
    occurs twice in the archive, since entries are never replaced. Catch
    ``(untar.Error, OSError)`` to handle every rejected archive, as the command line does.
    """
    if isinstance(dest, int) and not _DIR_FD:
        raise ValueError("dest cannot be a file descriptor on this platform")
    if gid is not None and _WINDOWS:
        raise ValueError("gid is not supported on Windows")
    if dir_mode & 0o700 != 0o700:
        raise ValueError(f"dir_mode {oct(dir_mode)} must give the owner rwx (0o700)")
    extractor = _Extractor(dest, root_marker, file_mode, dir_mode, gid, mtime)
    try:
        with _open_archive(src) as stream:
            reader = TarReader(stream)
            for member in reader:
                extractor.add(member, reader)
        return extractor.finish()
    finally:
        extractor.close()


def _main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point: ``python -m untar <archive> <dest>``."""
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
        print(f"untar: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_main())
