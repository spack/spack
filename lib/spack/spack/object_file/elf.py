# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import struct
import sys
from struct import unpack_from


class RPathType(object):
    #: Don't force an rpath
    NONE = 0
    #: Force RPATH
    RPATH = 1
    #: Force RUNPATH
    RUNPATH = 2


def get_byte_at(byte_array, idx):
    if sys.version_info[0] < 3:
        return ord(byte_array[idx])
    return byte_array[idx]


class ElfParsingError(Exception):
    pass


class ElfFile(object):
    __slots__ = ['is_64_bit', 'is_little_endian', 'rpath_offset', 'dt_offset',
                 'is_runpath']

    def __init__(self, is_64_bit, is_little_endian, rpath_offset, dt_offset,
                 is_runpath):
        self.is_64_bit = is_64_bit
        self.is_little_endian = is_little_endian
        self.rpath_offset = rpath_offset
        self.dt_offset = dt_offset
        self.is_runpath = is_runpath


def get_rpaths_byte_string_and_offset(f):
    """
    Given a file handle f for an ELF file, return the rpath as a (byte) string, as well
    as the offset into the file at which it occurs, in case it has to be overwritten
    in-place later.
    """
    # Go to the e_ident header
    f.seek(0)

    # Read the 32/64 bit class independent part of the header and validate
    e_ident = f.read(16)

    # Require ELF magic bytes.
    if len(e_ident) != 16 or e_ident[:4] != b'\x7fELF':
        raise ElfParsingError("No ELF file")

    # Defensively require a valid class and data.
    e_ident_class, e_ident_data = get_byte_at(e_ident, 4), get_byte_at(e_ident, 5)
    if e_ident_class != 0x1 and e_ident_class != 0x2:
        raise ElfParsingError("Invalid class found")
    if e_ident_data != 0x1 and e_ident_data != 0x2:
        raise ElfParsingError("Invalid data type")

    is_64_bit = e_ident_class == 0x02
    is_little_endian = e_ident_data == 0x01

    # Set up byte order and types for unpacking
    bo = '<' if is_little_endian else '>'
    t_half_half_half_half = bo + 'HHHH'
    t_word = bo + 'I'
    if is_64_bit:
        t_off = bo + 'Q'
        t_off_addr = bo + 'QQ'
        t_off_off = t_off_addr
        t_Dyn = bo + 'qQ'

        header_remainder_size = 48
        e_phoff_offset = 16
        e_phentsize_offset = 38
        p_offset_offset = 8
        Dyn_size = 16
        sh_offset_offset = 24

    else:
        t_off = bo + 'L'
        t_off_addr = bo + 'LL'
        t_off_off = t_off_addr
        t_Dyn = bo + 'lL'

        e_phoff_offset = 12
        header_remainder_size = 36
        e_phentsize_offset = 26
        p_offset_offset = 4
        Dyn_size = 8
        sh_offset_offset = 16

    # read the remaining bytes of the header
    header = f.read(header_remainder_size)
    if len(header) != header_remainder_size:
        raise ElfParsingError("ELF header malformed")

    e_type = get_byte_at(header, 0)

    if e_type != 0x02 and e_type != 0x03:
        raise ElfParsingError("Not an ET_DYN or ET_EXEC type")

    # Find program header and segment header offsets, size and count.
    e_phoff, e_shoff = unpack_from(
        t_off_off, buffer=header, offset=e_phoff_offset)
    e_phentsize, e_phnum, e_shentsize, e_shnum, = unpack_from(
        t_half_half_half_half, buffer=header, offset=e_phentsize_offset)

    # go over the sections
    f.seek(e_phoff)

    # Here we have to make a mapping from virtual address to offset in the file.
    offsets = []
    virtual_addresses = []

    found = False
    for _ in range(e_phnum):
        prog_header = f.read(e_phentsize)
        if len(prog_header) != e_phentsize:
            raise ElfParsingError("Malformed program header")
        p_type, = unpack_from(t_word, buffer=prog_header, offset=0)

        # For PT_LOAD entries: Save offsets and virtual addrs of the loaded ELF segments
        if p_type == 0x1:
            p_offset_load, p_vaddr_load, = unpack_from(
                t_off_addr, buffer=prog_header, offset=p_offset_offset)
            offsets.append(p_offset_load)
            virtual_addresses.append(p_vaddr_load)

        # Find a PT_DYNAMIC
        if p_type == 0x2:
            p_offset, = unpack_from(t_off, buffer=prog_header, offset=p_offset_offset)
            found = True

    # It doesn't do dynamic linking
    if not found:
        return None

    # Try to find the dt_rpath / dt_runpath, and the text section.
    # Also keep track of the offset rpath/runpath array entry, in case we later want
    # to force rpath or runpath.
    current_offset = p_offset
    f.seek(p_offset)
    found_rpath, found_runpath, found_strtab = 0, 0, 0
    while True:
        dyn = f.read(Dyn_size)
        if len(dyn) != Dyn_size:
            raise ElfParsingError("Malformed dynamic array entry")
        tag, val, = unpack_from(t_Dyn, buffer=dyn, offset=0)
        if tag == 0:  # DT_NULL -- end of the section.
            break
        if tag == 15:  # DT_RPATH
            found_rpath += 1
            rpath = val
            dt_rpath_offset = current_offset
        if tag == 29:  # DT_RUNPATH
            found_runpath += 1
            rpath = val
            dt_rpath_offset = current_offset
        if tag == 5:
            found_strtab += 1
            strtab = val
        current_offset += Dyn_size

    # No rpath/runpath, that happens.
    if found_rpath + found_runpath == 0:
        return None

    # We don't know how to handle with more than 1 entry of rpath/runpath.
    if found_rpath + found_runpath != 1:
        return ElfParsingError("Could not find a unique rpath/runpath.")

    if found_strtab != 1:
        raise ElfParsingError("Could not find a unique strtab of the rpath string")

    # Find the largest virtual address smaller than strtab's.
    try:
        idx = next(i for i, x in enumerate(virtual_addresses) if x > strtab) - 1
    except StopIteration:
        idx = len(virtual_addresses) - 1

    strtab_file_offset = offsets[idx] - virtual_addresses[idx] + strtab

    # Find the strtab section, so we know its size, so we can read that. This is
    # to work around a limitation in Python where you can't do f.readline(b'\0'), or
    # at least, not in an efficient way.
    found = False
    f.seek(e_shoff)
    for _ in range(e_shnum):
        sect_header = f.read(e_shentsize)
        if len(sect_header) != e_shentsize:
            raise ElfParsingError("Malformed section header")
        sh_type, = unpack_from(
            t_word, buffer=sect_header, offset=4)
        sh_offset, sh_size, = unpack_from(
            t_off_addr, buffer=sect_header, offset=sh_offset_offset)

        # find the SHT_STRTAB and in particular its size.
        if sh_type == 0x3 and sh_offset == strtab_file_offset:
            found = True
            break

    if not found:
        raise ElfParsingError("Could not determine strtab size")

    # Read the strtab section
    f.seek(strtab_file_offset)
    data = f.read(sh_size)
    if len(data) != sh_size:
        raise ElfParsingError("Could not read string table")

    rpath_binary_string = data[rpath:].split(b'\0')[0]

    return rpath_binary_string, ElfFile(
        is_64_bit=is_64_bit,
        is_little_endian=is_little_endian,
        rpath_offset=strtab_file_offset + rpath,
        dt_offset=dt_rpath_offset,
        is_runpath=found_runpath == 1
    )


def get_rpaths(path):
    """
    Returns list of rpaths of the given file, or None if it there was some error parsing
    the file.
    """
    try:
        with open(path, 'rb') as f:
            out = get_rpaths_byte_string_and_offset(f)
    except (IOError, DeprecationWarning, struct.error, ElfParsingError):
        # DeprectationWarning can be raised by Python < 3.1 in struct.unpack
        return None

    # This indicates there was no dynamic section or rpath at all
    if out is None:
        return []

    # If it does, split the string in components
    rpath, _ = out
    if sys.version_info[0] >= 3:
        rpath = rpath.decode('utf-8')
    return rpath.split(':')


def replace_rpaths(path, rpaths, force=RPathType.NONE):
    """
    Replaces an rpath in an ELF file with the ``rpaths`` list.

    Returns:
        True on success, False on failure of any kind
    """
    new_rpath = ":".join(rpaths)

    if sys.version_info[0] >= 3:
        new_rpath = new_rpath.encode('utf-8')

    try:
        with open(path, 'rb+') as f:
            result = get_rpaths_byte_string_and_offset(f)

            # If it has no rpath at all, we can't do much...
            if result is None:
                return False

            # Otherwise check if we can overwrite in-place
            # Both do not include the null byte, so this comparison is correct
            curr_rpath, elf = result
            if len(curr_rpath) < len(new_rpath):
                return False

            # Put the new rpath in place
            f.seek(elf.rpath_offset)
            f.write(new_rpath)
            f.write(b'\0')

            # Force an rpath or runpath?
            if force == RPathType.RPATH or force == RPathType.RUNPATH:
                tag = 15 if force == RPathType.RPATH else 29
                byte_order = ('<' if elf.is_little_endian else '>')
                type = ('q' if elf.is_64_bit else 'l')
                format_string = byte_order + type
                f.seek(elf.dt_offset)
                f.write(struct.pack(format_string, tag))
    except (IOError, struct.error, ElfParsingError):
        return False
    return True
