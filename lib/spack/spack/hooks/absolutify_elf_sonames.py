# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import struct
import sys

import llnl.util.tty as tty
from llnl.util.filesystem import BaseDirectoryVisitor, visit_directory_tree
from llnl.util.lang import elide_list

import spack.bootstrap
import spack.relocate
from spack.util.executable import Executable


class ELF:
    ELFCLASS32 = 1
    ELFCLASS64 = 2
    ELFDATA2LSB = 1
    ELFDATA2MSB = 2
    ET_DYN = 3
    PT_DYNAMIC = 2
    PT_INTERP = 3
    DT_NULL = 0
    DT_SONAME = 14


def get_byte_at(byte_array, idx):
    if sys.version_info[0] < 3:
        return ord(byte_array[idx])
    return byte_array[idx]


def is_probably_a_shared_library_elf_file(f):
    # Read the 32/64 bit class independent part of the header and validate
    e_ident = f.read(16)

    # Require ELF magic bytes.
    if len(e_ident) != 16 or e_ident[:4] != b"\x7fELF":
        return False

    # Defensively require a valid class and data.
    e_ident_class, e_ident_data = get_byte_at(e_ident, 4), get_byte_at(e_ident, 5)
    if e_ident_class not in (ELF.ELFCLASS32, ELF.ELFCLASS64):
        return False
    if e_ident_data not in (ELF.ELFDATA2LSB, ELF.ELFDATA2MSB):
        return False

    is_64_bit = e_ident_class == ELF.ELFCLASS64
    is_little_endian = e_ident_data == ELF.ELFDATA2LSB

    # Set up byte order and types for unpacking
    bo = "<" if is_little_endian else ">"
    t_half_half_half_half = bo + "HHHH"
    t_word = bo + "I"
    if is_64_bit:
        t_off = bo + "Q"
        t_off_addr = bo + "QQ"
        t_off_off = t_off_addr
        t_Dyn = bo + "qQ"
        header_remainder_size = 48
        e_phoff_offset = 16
        e_phentsize_offset = 38
        p_offset_offset = 8
        Dyn_size = 16

    else:
        t_off = bo + "L"
        t_off_addr = bo + "LL"
        t_off_off = t_off_addr
        t_Dyn = bo + "lL"
        e_phoff_offset = 12
        header_remainder_size = 36
        e_phentsize_offset = 26
        p_offset_offset = 4
        Dyn_size = 8

    # read the remaining bytes of the header
    header = f.read(header_remainder_size)

    # Malformed ELF heder
    if len(header) != header_remainder_size:
        return False

    e_type = get_byte_at(header, 0)

    # If it's not a shared object file we don't have to patch it
    if e_type != ELF.ET_DYN:
        return False

    # However, PIE exectubles are ET_DYN too, so we have to exclude those. To do so:
    # 1. We require a dynamic section
    # 2. We require either an existing soname OR a lacking PT_INTERP.
    # This should cover the following cases:
    # 1. Shared libraries without sonames: they're probably only shared libraries if
    #    they don't specify an interpreter executable.
    # 2. Executable shared libraries: apparently these exist, one known case is
    #    libQt5Core.so.5, which dumps info when executed, but can also be linked.
    #    It would be categorized as shared library because it specifies a soname.
    try:
        e_phoff, _ = struct.unpack_from(t_off_off, header, e_phoff_offset)
        (
            e_phentsize,
            e_phnum,
            _,
            _,
        ) = struct.unpack_from(t_half_half_half_half, header, e_phentsize_offset)

        # Forward to the program header offset.
        f.seek(e_phoff)

        has_dynamic_section = False
        has_interpreter = False

        # Iterate over each program header.
        for _ in range(e_phnum):
            prog_header = f.read(e_phentsize)
            # Bail on malformed program header
            if len(prog_header) != e_phentsize:
                return False
            (p_type,) = struct.unpack_from(t_word, prog_header, 0)

            if p_type == ELF.PT_INTERP:
                # Just keep track that we have a program interpreter.
                has_interpreter = True
            elif p_type == ELF.PT_DYNAMIC:
                # If we have a dynamic section, keep track of where it starts.
                (p_offset,) = struct.unpack_from(t_off, prog_header, p_offset_offset)
                has_dynamic_section = True

        # Does not partake in dynamic linking. Note that it's probably possible but
        # very uncommon to create a shared library without a dynamic section. Giving
        # it a soname would then require to create a new dynamic section in the binary,
        # which isn't great. So probably fine to exit here.
        if not has_dynamic_section:
            return False

        # Move to the dynamic section.
        f.seek(p_offset)

        # Look for an existing soname.
        while True:
            dyn = f.read(Dyn_size)
            if len(dyn) != Dyn_size:
                return False
            (
                tag,
                val,
            ) = struct.unpack_from(t_Dyn, buffer=dyn, offset=0)

            # Existing soname implies this is a shared library.
            if tag == ELF.DT_SONAME:
                return True

            # End of the section.
            if tag == ELF.DT_NULL:
                break

        # If we don't have a soname, the only way to categorize as a shared lib is if
        # we don't have an interpreter.
        return not has_interpreter
    except struct.error:
        return False


class SharedLibrariesVisitor(BaseDirectoryVisitor):
    def __init__(self, exclude_list):

        # List of file and directory names to be excluded
        self.exclude_list = set(exclude_list)

        # Map from (ino, dev) -> path. We need 1 path per file, if there are hardlinks,
        # we don't need to store the path multiple times.
        self.libraries = dict()

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
        if identifier in self.libraries or identifier in self.excluded_through_symlink:
            return

        # Register the file if it's a shared lib that needs to be patched.
        with open(filepath, "rb") as f:
            if is_probably_a_shared_library_elf_file(f):
                self.libraries[identifier] = rel_path

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

    def get_shared_libraries_relative_paths(self):
        """Get the libraries that should be patched, with the excluded libraries
        removed."""
        for identifier in self.excluded_through_symlink:
            self.libraries.pop(identifier, None)

        return [rel_path for rel_path in self.libraries.values()]


def patch_sonames(patchelf, root, rel_paths):
    fixed = []
    for rel_path in rel_paths:
        filepath = os.path.join(root, rel_path)
        normalized = os.path.normpath(filepath)
        args = ["--set-soname", normalized, normalized]
        output = patchelf(*args, output=str, error=str, fail_on_error=False)
        if patchelf.returncode == 0:
            fixed.append(rel_path)
        else:
            tty.warn("patchelf: failed to set soname of {}: {}".format(normalized, output.strip()))
    return fixed


def post_install(spec):
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

    # Locate all shared libraries in the prefix dir of the spec, excluding
    # the ones set in the non_bindable_shared_objects property.
    visitor = SharedLibrariesVisitor(spec.package.non_bindable_shared_objects)
    visit_directory_tree(spec.prefix, visitor)

    # Patch all sonames.
    relative_paths = visitor.get_shared_libraries_relative_paths()
    fixes = patch_sonames(patchelf, spec.prefix, relative_paths)

    if not fixes:
        return

    # Unfortunately this does not end up in the build logs.
    tty.info(
        "{}: Patched {} {}: {}".format(
            spec.name,
            len(fixes),
            "soname" if len(fixes) == 1 else "sonames",
            ", ".join(elide_list(fixes, max_num=5)),
        )
    )
