# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Find the shared libraries an ELF file loads, in the order the glibc dynamic loader searches
for them, without running the loader.
"""

import collections
import os
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple

import spack.util.elf as elf_utils


class ElfInfo(NamedTuple):
    """The parts of an ELF file that determine which libraries it loads."""

    #: (is_64_bit, is_little_endian, e_machine), a library is loadable only if it matches
    compat: Tuple[bool, bool, int]
    #: whether the file has a ``PT_INTERP`` segment, which is the case for executables
    has_interpreter: bool
    soname: Optional[str]
    needed: List[str]
    rpath: List[str]
    runpath: List[str]


class LoadedObject(NamedTuple):
    """A file in the closure of a root, and what its ``DT_NEEDED`` entries resolve to."""

    #: path the file was found at, before resolving symlinks
    path: str
    #: real paths of the files the ``DT_NEEDED`` entries resolve to, in order
    needed: List[str]
    #: ``DT_NEEDED`` entries that do not resolve to any file
    missing: List[str]


def read_elf_info(path: str) -> Optional[ElfInfo]:
    """Returns the loading information of an ELF file, or None if ``path`` is not a readable
    ELF executable or shared library.
    """
    try:
        with open(path, "rb") as f:
            elf = elf_utils.parse_elf(f, interpreter=False, dynamic_section=True)
    except (OSError, elf_utils.ElfParsingError):
        return None

    rpath: List[str] = []
    runpath: List[str] = []
    if elf.has_rpath:
        entries = os.fsdecode(elf.dt_rpath_str).split(":")
        if elf.is_runpath:
            runpath = entries
        else:
            rpath = entries
    return ElfInfo(
        compat=(elf.is_64_bit, elf.is_little_endian, elf.elf_hdr.e_machine),
        has_interpreter=elf.has_pt_interp,
        soname=os.fsdecode(elf.dt_soname_str) if elf.has_soname else None,
        needed=[os.fsdecode(x) for x in elf.dt_needed_strs] if elf.has_needed else [],
        rpath=rpath,
        runpath=runpath,
    )


def _expand_search_path(entries: List[str], origin: str) -> List[str]:
    """Expands ``$ORIGIN`` in RPATH or RUNPATH entries. Entries that are relative, or contain
    other dynamic string tokens such as ``$LIB`` or ``$PLATFORM``, are dropped.
    """
    result = []
    for entry in entries:
        entry = entry.replace("${ORIGIN}", origin).replace("$ORIGIN", origin)
        if "$" not in entry and os.path.isabs(entry):
            result.append(entry)
    return result


class DynamicLoader:
    """Computes which files the dynamic loader loads for an ELF file, searching each
    ``DT_NEEDED`` entry in:

    1. the RPATH of the requesting file, and of the files that loaded it, when the requesting
       file has no RUNPATH
    2. ``LD_LIBRARY_PATH``
    3. the RUNPATH of the requesting file
    4. the default directories of the loader

    A library already loaded under the same name or soname is not searched again. Candidates of
    another ELF class or architecture than the root are skipped, as the loader does.

    Parsed files are cached, so one instance can be used for many roots.
    """

    def __init__(self, *, ld_library_path: Sequence[str], default_dirs: Sequence[str]) -> None:
        """
        Arguments:
            ld_library_path: directories in ``LD_LIBRARY_PATH``, in order
            default_dirs: directories from ``ld.so.conf`` and the loader's default directories
        """
        self.ld_library_path = [d for d in ld_library_path if os.path.isabs(d)]
        self.default_dirs = list(default_dirs)
        self._info: Dict[str, Optional[ElfInfo]] = {}

    def elf_info(self, path: str) -> Optional[ElfInfo]:
        """Returns the cached loading information of the file at ``path``."""
        if path not in self._info:
            self._info[path] = read_elf_info(path)
        return self._info[path]

    def load(self, root: str) -> Dict[str, LoadedObject]:
        """Returns the files loaded for ``root``, keyed by real path. The result is empty if
        ``root`` is not an ELF file.
        """
        root_info = self.elf_info(root)
        if root_info is None:
            return {}

        root_key = os.path.realpath(root)
        # The loader takes $ORIGIN of an executable from /proc/self/exe, which has no symlinks
        root_path = root_key if root_info.has_interpreter else root
        paths = {root_key: root}
        infos = {root_key: root_info}
        origins = {root_key: os.path.dirname(root_path)}
        loaded_by: Dict[str, Optional[str]] = {root_key: None}
        by_name: Dict[str, str] = {}
        if root_info.soname:
            by_name[root_info.soname] = root_key

        result: Dict[str, LoadedObject] = {}
        queue = collections.deque([root_key])
        while queue:
            key = queue.popleft()
            needed, missing = [], []
            for name in infos[key].needed:
                if name not in by_name:
                    found = self._search(name, key, root_info.compat, infos, origins, loaded_by)
                    if found is None:
                        missing.append(name)
                        continue
                    path, info = found
                    real = os.path.realpath(path)
                    if real not in infos:
                        paths[real] = path
                        infos[real] = info
                        origins[real] = os.path.dirname(path)
                        loaded_by[real] = key
                        if info.soname:
                            by_name.setdefault(info.soname, real)
                        queue.append(real)
                    by_name[name] = real
                needed.append(by_name[name])
            result[key] = LoadedObject(path=paths[key], needed=needed, missing=missing)
        return result

    def _search(
        self,
        name: str,
        key: str,
        compat: Tuple[bool, bool, int],
        infos: Dict[str, ElfInfo],
        origins: Dict[str, str],
        loaded_by: Dict[str, Optional[str]],
    ) -> Optional[Tuple[str, ElfInfo]]:
        """Returns the path and loading information of the first loadable file for the
        ``DT_NEEDED`` entry ``name`` of the file ``key``, or None if there is none.
        """
        if "/" in name:
            candidates = [name] if os.path.isabs(name) else []
        else:
            dirs: List[str] = []
            if not infos[key].runpath:
                current: Optional[str] = key
                while current is not None:
                    dirs.extend(_expand_search_path(infos[current].rpath, origins[current]))
                    current = loaded_by[current]
            dirs.extend(self.ld_library_path)
            dirs.extend(_expand_search_path(infos[key].runpath, origins[key]))
            dirs.extend(self.default_dirs)
            candidates = [os.path.join(d, name) for d in dirs]

        for candidate in candidates:
            info = self.elf_info(candidate)
            if info is not None and info.compat == compat:
                return candidate, info
        return None
