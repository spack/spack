# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from collections import namedtuple

import llnl.util.tty as tty
from llnl.util.filesystem import BaseDirectoryVisitor, visit_directory_tree
from llnl.util.lang import elide_list

import spack.bootstrap
import spack.config
import spack.relocate
from spack.util.elf import ElfFile, ElfParsingError, parse_elf
from spack.util.executable import Executable

ModifyElfAction = namedtuple("ModifyElfAction", "path set_soname replace_needed")


def get_elf(filepath):
    try:
        with open(filepath, "rb") as f:
            return parse_elf(f, interpreter=True, dynamic_section=True)
    except (IOError, OSError, ElfParsingError):
        return None


def library_is_compatible(parent: ElfFile, child: ElfFile):
    """Check whether the library has the same architecture as the parent
    that may use it. This check avoids picking up e.g. 32 bit libs when
    the parent is a 64 bit elf file."""
    return (
        parent.is_64_bit == child.is_64_bit
        and parent.is_little_endian == child.is_little_endian
        and parent.elf_hdr.e_machine == child.elf_hdr.e_machine
    )


def resolve_lib(parent: ElfFile, rpaths, lib):
    # If there's a / in
    if "/" in lib:
        return None
    for rpath in rpaths:
        library_path = os.path.join(rpath, lib)
        try:
            with open(library_path, "rb") as f:
                child = parse_elf(f, interpreter=False, dynamic_section=False)
                if library_is_compatible(parent, child):
                    return library_path
        except (OSError, ElfParsingError):
            continue
    return None


class SharedLibrariesVisitor(BaseDirectoryVisitor):
    """Visitor that collects all shared libraries in a prefix, with the
    exception of an exclude list."""

    def __init__(self, exclude_list):

        # List of file and directory names to be excluded
        self.exclude_list = frozenset(exclude_list)

        # Map from (ino, dev) -> [path, new_soname, ]. We need 1 path per file,
        # if there are hardlinks, we don't need to store the path multiple
        # times.
        self._actions = dict()

        # Set of (ino, dev) pairs (excluded by symlinks).
        self.excluded_through_symlink = set()

    def visit_file(self, root, rel_path, depth):
        # Check if excluded
        basename = os.path.basename(rel_path)
        if basename in self.exclude_list:
            return

        filepath = os.path.join(root, rel_path)
        s = os.lstat(filepath)
        identifier = (s.st_ino, s.st_dev)

        # We're hitting a hardlink or symlink of an excluded lib, no need to parse.
        if identifier in self._actions or identifier in self.excluded_through_symlink:
            return

        # Register the file if it's a shared lib that needs to be patched.
        elf = get_elf(filepath)
        if elf is None:
            return

        # Our definition of a shared library for ELF requires:
        # 1. a dynamic section,
        # 2. a soname OR lack of interpreter.
        # The problem is that PIE objects (default on Ubuntu) are
        # ET_DYN too, and not all shared libraries have a soname...
        # no interpreter is typically the best indicator then.
        is_library = elf.has_pt_dynamic and (elf.has_soname or not elf.has_pt_interp)

        # Resolve rpaths inside the spec's own prefix, and replace by absolute paths.
        replace_needed = []
        if elf.has_rpath and elf.has_needed:
            try:
                needed_libs = [s.decode("utf-8") for s in elf.dt_needed_strs]
                rpaths_in_spec_prefix = list(
                    filter(
                        lambda p: os.path.normpath(p).startswith(root),
                        elf.dt_rpath_str.decode("utf-8").split(":"),
                    )
                )

                for needed in needed_libs:
                    resolved = resolve_lib(elf, rpaths_in_spec_prefix, needed)
                    if resolved:
                        replace_needed.append((needed, resolved))
            except UnicodeDecodeError:
                # We simply skip if we can't decode rpath & needed as UTF-8,
                # even though in principle it would be better to stick to
                # binary mode, since paths and filenames are just a sequence
                # of bytes without encoding.
                pass

        self._actions[identifier] = ModifyElfAction(
            path=rel_path, set_soname=is_library, replace_needed=replace_needed
        )

    def visit_symlinked_file(self, root, rel_path, depth):
        # We don't need to follow the symlink and parse the file, since we will hit
        # it by recursing the prefix anyways. We only need to check if the target
        # should be excluded based on the filename of the symlink. E.g. when excluding
        # libf.so, which is a symlink to libf.so.1.2.3, we keep track of the stat data
        # of the latter.
        basename = os.path.basename(rel_path)
        if basename not in self.exclude_list:
            return

        # Register the (ino, dev) pair as ignored (if the symlink is not dangling)
        filepath = os.path.join(root, rel_path)
        try:
            s = os.stat(filepath)
        except OSError:
            return
        self.excluded_through_symlink.add((s.st_ino, s.st_dev))

    def before_visit_dir(self, root, rel_path, depth):
        # Allow skipping over directories. E.g. `<prefix>/lib/stubs` can be skipped by
        # adding `"stubs"` to the exclude list.
        return os.path.basename(rel_path) not in self.exclude_list

    def before_visit_symlinked_dir(self, root, rel_path, depth):
        # Never enter symlinked dirs, since we don't want to leave the prefix, and
        # we'll enter the target dir inside the prefix anyways since we're recursing
        # everywhere.
        return False

    @property
    def actions(self):
        """Get the actions."""
        for identifier in self.excluded_through_symlink:
            self._actions.pop(identifier, None)

        return list(self._actions.values())


def apply_actions(patchelf, root, actions):
    """Run the actions (set soname, replace needed)
    for the executables and libraries we have detected
    in a prefix."""
    modified = []
    for rel_path, set_soname, replace_needed in actions:
        args = []
        filepath = os.path.join(root, rel_path)

        if set_soname:
            args.extend(["--set-soname", os.path.normpath(filepath)])

        for old_needed, new_needed in replace_needed:
            args.extend(["--replace-needed", old_needed, new_needed])

        # Nothing to do.
        if not args:
            continue

        # Positional arg: file we're modifying.
        args.append(filepath)

        output = patchelf(*args, output=str, error=str, fail_on_error=False)
        if patchelf.returncode == 0:
            modified.append(rel_path)
        else:
            # Note: treat as warning to avoid (long) builds to fail post-install.
            tty.warn("patchelf: failed to modify {}: {}".format(filepath, output.strip()))
    return modified


def absolutify_sonames(prefix, exclude_list, patchelf):
    # Locate all shared libraries in the prefix dir of the spec, excluding
    # the ones set in the non_bindable_shared_objects property.
    visitor = SharedLibrariesVisitor(exclude_list)
    visit_directory_tree(prefix, visitor)

    # Patch all sonames.
    return apply_actions(patchelf, prefix, visitor.actions)


def post_install(spec):
    # Skip if disabled
    if not spack.config.get("config:shared_linking:bind", False):
        return

    # Skip externals
    if spec.external:
        return

    # Only enable on platforms using ELF.
    if not spec.satisfies("platform=linux") and not spec.satisfies("platform=cray"):
        return

    # Disable this hook when bootstrapping, to avoid recursion.
    if spack.bootstrap.is_bootstrapping():
        return

    # Should failing to locate patchelf be a hard error?
    patchelf_path = spack.relocate._patchelf()
    if not patchelf_path:
        return
    patchelf = Executable(patchelf_path)

    modified = absolutify_sonames(spec.prefix, spec.package.non_bindable_shared_objects, patchelf)

    if not modified:
        return

    # Unfortunately this does not end up in the build logs.
    tty.info(
        "{}: Patched {} {}: {}".format(
            spec.name,
            len(modified),
            "binary" if len(modified) == 1 else "binaries",
            ", ".join(elide_list(modified, max_num=5)),
        )
    )
