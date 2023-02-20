# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import bisect
import re
import struct
from collections import namedtuple
from struct import calcsize, unpack, unpack_from

ElfHeader = namedtuple(
    "ElfHeader",
    [
        "e_type",
        "e_machine",
        "e_version",
        "e_entry",
        "e_phoff",
        "e_shoff",
        "e_flags",
        "e_ehsize",
        "e_phentsize",
        "e_phnum",
        "e_shentsize",
        "e_shnum",
        "e_shstrndx",
    ],
)

SectionHeader = namedtuple(
    "SectionHeader",
    [
        "sh_name",
        "sh_type",
        "sh_flags",
        "sh_addr",
        "sh_offset",
        "sh_size",
        "sh_link",
        "sh_info",
        "sh_addralign",
        "sh_entsize",
    ],
)

ProgramHeader32 = namedtuple(
    "ProgramHeader32",
    ["p_type", "p_offset", "p_vaddr", "p_paddr", "p_filesz", "p_memsz", "p_flags", "p_align"],
)

ProgramHeader64 = namedtuple(
    "ProgramHeader64",
    ["p_type", "p_flags", "p_offset", "p_vaddr", "p_paddr", "p_filesz", "p_memsz", "p_align"],
)


class ELF_CONSTANTS:
    MAGIC = b"\x7fELF"
    CLASS32 = 1
    CLASS64 = 2
    DATA2LSB = 1
    DATA2MSB = 2
    ET_EXEC = 2
    ET_DYN = 3
    PT_LOAD = 1
    PT_DYNAMIC = 2
    PT_INTERP = 3
    DT_NULL = 0
    DT_NEEDED = 1
    DT_STRTAB = 5
    DT_SONAME = 14
    DT_RPATH = 15
    DT_RUNPATH = 29
    SHT_STRTAB = 3


class ElfFile(object):
    """Parsed ELF file."""

    __slots__ = [
        "is_64_bit",
        "is_little_endian",
        "byte_order",
        "elf_hdr",
        "pt_load",
        # pt_interp
        "has_pt_interp",
        "pt_interp_p_offset",
        "pt_interp_p_filesz",
        "pt_interp_str",
        # pt_dynamic
        "has_pt_dynamic",
        "pt_dynamic_p_offset",
        "pt_dynamic_p_filesz",
        "pt_dynamic_strtab_offset",  # string table for dynamic section
        # rpath
        "has_rpath",
        "dt_rpath_offset",
        "dt_rpath_str",
        "rpath_strtab_offset",
        "is_runpath",
        # dt needed
        "has_needed",
        "dt_needed_strtab_offsets",
        "dt_needed_strs",
        # dt soname
        "has_soname",
        "dt_soname_strtab_offset",
        "dt_soname_str",
    ]

    def __init__(self):
        self.dt_needed_strtab_offsets = []
        self.has_soname = False
        self.has_rpath = False
        self.has_needed = False
        self.pt_load = []
        self.has_pt_dynamic = False
        self.has_pt_interp = False


def parse_c_string(byte_string, start=0):
    """
    Retrieve a C-string at a given offset in a byte string

    Arguments:
        byte_string (bytes): String
        start (int): Offset into the string

    Returns:
        bytes: A copy of the C-string excluding the terminating null byte
    """
    str_end = byte_string.find(b"\0", start)
    if str_end == -1:
        raise ElfParsingError("C-string is not null terminated")
    return byte_string[start:str_end]


def read_exactly(f, num_bytes, msg):
    """
    Read exactly num_bytes at the current offset, otherwise raise
    a parsing error with the given error message.

    Arguments:
        f: file handle
        num_bytes (int): Number of bytes to read
        msg (str): Error to show when bytes cannot be read

    Returns:
        bytes: the ``num_bytes`` bytes that were read.
    """
    data = f.read(num_bytes)
    if len(data) != num_bytes:
        raise ElfParsingError(msg)
    return data


def parse_program_headers(f, elf):
    """
    Parse program headers

    Arguments:
        f: file handle
        elf (ElfFile): ELF file parser data
    """
    # Forward to the program header
    f.seek(elf.elf_hdr.e_phoff)

    # Here we have to make a mapping from virtual address to offset in the file.
    ProgramHeader = ProgramHeader64 if elf.is_64_bit else ProgramHeader32
    ph_fmt = elf.byte_order + ("LLQQQQQQ" if elf.is_64_bit else "LLLLLLLL")
    ph_size = calcsize(ph_fmt)
    ph_num = elf.elf_hdr.e_phnum

    # Read all program headers in one go
    data = read_exactly(f, ph_num * ph_size, "Malformed program header")

    for i in range(ph_num):
        ph = ProgramHeader._make(unpack_from(ph_fmt, data, i * ph_size))

        # Skip segments of size 0; we don't distinguish between missing segment and
        # empty segments. I've see an empty PT_DYNAMIC section for an ELF file that
        # contained debug data.
        if ph.p_filesz == 0:
            continue

        # For PT_LOAD entries: Save offsets and virtual addrs of the loaded ELF segments
        # This way we can map offsets by virtual address to offsets in the file.
        if ph.p_type == ELF_CONSTANTS.PT_LOAD:
            elf.pt_load.append((ph.p_offset, ph.p_vaddr))

        elif ph.p_type == ELF_CONSTANTS.PT_INTERP:
            elf.pt_interp_p_offset = ph.p_offset
            elf.pt_interp_p_filesz = ph.p_filesz
            elf.has_pt_interp = True

        elif ph.p_type == ELF_CONSTANTS.PT_DYNAMIC:
            elf.pt_dynamic_p_offset = ph.p_offset
            elf.pt_dynamic_p_filesz = ph.p_filesz
            elf.has_pt_dynamic = True

    # The linker sorts PT_LOAD segments by vaddr, but let's do it just to be sure, since
    # patchelf for example has a flag to leave them in an arbitrary order.
    elf.pt_load.sort(key=lambda x: x[1])


def parse_pt_interp(f, elf):
    """
    Parse the interpreter (i.e. absolute path to the dynamic linker)

    Arguments:
        f: file handle
        elf (ElfFile): ELF file parser data
    """
    f.seek(elf.pt_interp_p_offset)
    data = read_exactly(f, elf.pt_interp_p_filesz, "Malformed PT_INTERP entry")
    elf.pt_interp_str = parse_c_string(data)


def find_strtab_size_at_offset(f, elf, offset):
    """
    Retrieve the size of a string table section at a particular known offset

    Arguments:
        f: file handle
        elf (ElfFile): ELF file parser data
        offset (int): offset of the section in the file (i.e. ``sh_offset``)

    Returns:
        int: the size of the string table in bytes
    """
    section_hdr_fmt = elf.byte_order + ("LLQQQQLLQQ" if elf.is_64_bit else "LLLLLLLLLL")
    section_hdr_size = calcsize(section_hdr_fmt)
    f.seek(elf.elf_hdr.e_shoff)
    for _ in range(elf.elf_hdr.e_shnum):
        data = read_exactly(f, section_hdr_size, "Malformed section header")
        sh = SectionHeader._make(unpack(section_hdr_fmt, data))
        if sh.sh_type == ELF_CONSTANTS.SHT_STRTAB and sh.sh_offset == offset:
            return sh.sh_size

    raise ElfParsingError("Could not determine strtab size")


def retrieve_strtab(f, elf, offset):
    """
    Read a full string table at the given offset, which
    requires looking it up in the section headers.

    Arguments:
        elf (ElfFile): ELF file parser data
        vaddr (int): virtual address

    Returns:
        bytes: file offset
    """
    size = find_strtab_size_at_offset(f, elf, offset)
    f.seek(offset)
    return read_exactly(f, size, "Could not read string table")


def vaddr_to_offset(elf, vaddr):
    """
    Given a virtual address, find the corresponding offset in the ELF file itself.

    Arguments:
        elf (ElfFile): ELF file parser data
        vaddr (int): virtual address
    """
    idx = bisect.bisect_right([p_vaddr for (p_offset, p_vaddr) in elf.pt_load], vaddr) - 1
    p_offset, p_vaddr = elf.pt_load[idx]
    return p_offset - p_vaddr + vaddr


def parse_pt_dynamic(f, elf):
    """
    Parse the dynamic section of an ELF file

    Arguments:
        f: file handle
        elf (ElfFile): ELF file parse data
    """
    dynamic_array_fmt = elf.byte_order + ("qQ" if elf.is_64_bit else "lL")
    dynamic_array_size = calcsize(dynamic_array_fmt)

    current_offset = elf.pt_dynamic_p_offset
    count_rpath = 0
    count_runpath = 0
    count_strtab = 0

    f.seek(elf.pt_dynamic_p_offset)

    # In case of broken ELF files, don't read beyond the advertized size.
    for _ in range(elf.pt_dynamic_p_filesz // dynamic_array_size):
        data = read_exactly(f, dynamic_array_size, "Malformed dynamic array entry")
        tag, val = unpack(dynamic_array_fmt, data)
        if tag == ELF_CONSTANTS.DT_NULL:
            break
        elif tag == ELF_CONSTANTS.DT_RPATH:
            count_rpath += 1
            elf.rpath_strtab_offset = val
            elf.dt_rpath_offset = current_offset
            elf.is_runpath = False
            elf.has_rpath = True
        elif tag == ELF_CONSTANTS.DT_RUNPATH:
            count_runpath += 1
            elf.rpath_strtab_offset = val
            elf.dt_rpath_offset = current_offset
            elf.is_runpath = True
            elf.has_rpath = True
        elif tag == ELF_CONSTANTS.DT_STRTAB:
            count_strtab += 1
            strtab_vaddr = val
        elif tag == ELF_CONSTANTS.DT_NEEDED:
            elf.has_needed = True
            elf.dt_needed_strtab_offsets.append(val)
        elif tag == ELF_CONSTANTS.DT_SONAME:
            elf.has_soname = True
            elf.dt_soname_strtab_offset = val
        current_offset += dynamic_array_size

    # No rpath/runpath, that happens.
    if count_rpath == count_runpath == 0:
        elf.has_rpath = False
    elif count_rpath + count_runpath != 1:
        raise ElfParsingError("Could not find a unique rpath/runpath.")

    if count_strtab != 1:
        raise ElfParsingError("Could not find a unique strtab of for the dynamic section strings")

    # Nothing to retrieve, so don't bother getting the string table.
    if not (elf.has_rpath or elf.has_soname or elf.has_needed):
        return

    elf.pt_dynamic_strtab_offset = vaddr_to_offset(elf, strtab_vaddr)
    string_table = retrieve_strtab(f, elf, elf.pt_dynamic_strtab_offset)

    if elf.has_needed:
        elf.dt_needed_strs = list(
            parse_c_string(string_table, offset) for offset in elf.dt_needed_strtab_offsets
        )

    if elf.has_soname:
        elf.dt_soname_str = parse_c_string(string_table, elf.dt_soname_strtab_offset)

    if elf.has_rpath:
        elf.dt_rpath_str = parse_c_string(string_table, elf.rpath_strtab_offset)


def parse_header(f, elf):
    # Read the 32/64 bit class independent part of the header and validate
    e_ident = f.read(16)

    # Require ELF magic bytes.
    if len(e_ident) != 16 or e_ident[:4] != ELF_CONSTANTS.MAGIC:
        raise ElfParsingError("Not an ELF file")

    # Defensively require a valid class and data.
    e_ident_class, e_ident_data = e_ident[4], e_ident[5]

    if e_ident_class not in (ELF_CONSTANTS.CLASS32, ELF_CONSTANTS.CLASS64):
        raise ElfParsingError("Invalid class found")

    if e_ident_data not in (ELF_CONSTANTS.DATA2LSB, ELF_CONSTANTS.DATA2MSB):
        raise ElfParsingError("Invalid data type")

    elf.is_64_bit = e_ident_class == ELF_CONSTANTS.CLASS64
    elf.is_little_endian = e_ident_data == ELF_CONSTANTS.DATA2LSB

    # Set up byte order and types for unpacking
    elf.byte_order = "<" if elf.is_little_endian else ">"

    # Parse the rest of the header
    elf_header_fmt = elf.byte_order + ("HHLQQQLHHHHHH" if elf.is_64_bit else "HHLLLLLHHHHHH")
    hdr_size = calcsize(elf_header_fmt)
    data = read_exactly(f, hdr_size, "ELF header malformed")
    elf.elf_hdr = ElfHeader._make(unpack(elf_header_fmt, data))


def _do_parse_elf(f, interpreter=True, dynamic_section=True):
    # We don't (yet?) allow parsing ELF files at a nonzero offset, we just
    # jump to absolute offsets as they are specified in the ELF file.
    if f.tell() != 0:
        raise ElfParsingError("Cannot parse at a nonzero offset")

    elf = ElfFile()
    parse_header(f, elf)

    # We don't handle anything but executables and shared libraries now.
    if elf.elf_hdr.e_type not in (ELF_CONSTANTS.ET_EXEC, ELF_CONSTANTS.ET_DYN):
        raise ElfParsingError("Not an ET_DYN or ET_EXEC type")

    parse_program_headers(f, elf)

    # Parse PT_INTERP section
    if interpreter and elf.has_pt_interp:
        parse_pt_interp(f, elf)

    # Parse PT_DYNAMIC section.
    if dynamic_section and elf.has_pt_dynamic and len(elf.pt_load) > 0:
        parse_pt_dynamic(f, elf)

    return elf


def parse_elf(f, interpreter=False, dynamic_section=False):
    """Given a file handle f for an ELF file opened in binary mode, return an ElfFile
    object that is stores data about rpaths"""
    try:
        return _do_parse_elf(f, interpreter, dynamic_section)
    except (DeprecationWarning, struct.error):
        # According to the docs old versions of Python can throw DeprecationWarning
        # instead of struct.error.
        raise ElfParsingError("Malformed ELF file")


def get_rpaths(path):
    """Returns list of rpaths of the given file as UTF-8 strings, or None if the file
    does not have any rpaths."""
    try:
        with open(path, "rb") as f:
            elf = parse_elf(f, interpreter=False, dynamic_section=True)
    except ElfParsingError:
        return None

    if not elf.has_rpath:
        return None

    # If it does, split the string in components
    rpath = elf.dt_rpath_str
    rpath = rpath.decode("utf-8")
    return rpath.split(":")


def replace_rpath_in_place_or_raise(path, substitutions):
    regex = re.compile(b"|".join(re.escape(p) for p in substitutions.keys()))

    try:
        with open(path, "rb+") as f:
            elf = parse_elf(f, interpreter=False, dynamic_section=True)

            # If there's no RPATH, then there's no need to replace anything.
            if not elf.has_rpath:
                return False

            # Get the non-empty rpaths. Sometimes there's a bunch of trailing
            # colons ::::: used for padding, we don't add them back to make it
            # more likely that the string doesn't grow.
            rpaths = list(filter(len, elf.dt_rpath_str.split(b":")))

            num_rpaths = len(rpaths)

            if num_rpaths == 0:
                return False

            changed = False
            for i in range(num_rpaths):
                old_rpath = rpaths[i]
                match = regex.match(old_rpath)
                if match:
                    changed = True
                    rpaths[i] = substitutions[match.group()] + old_rpath[match.end() :]

            # Nothing to replace!
            if not changed:
                return False

            new_rpath_string = b":".join(rpaths)

            pad = len(elf.dt_rpath_str) - len(new_rpath_string)

            if pad < 0:
                raise ElfDynamicSectionUpdateFailed(elf.dt_rpath_str, new_rpath_string)

            # We zero out the bits we shortened because (a) it should be a
            # C-string and (b) it's nice not to have spurious parts of old
            # paths in the output of `strings file`. Note that we're all
            # good when pad == 0; the original terminating null is used.
            new_rpath_string += b"\x00" * pad

            # The rpath is at a given offset in the string table used by the
            # dynamic section.
            rpath_offset = elf.pt_dynamic_strtab_offset + elf.rpath_strtab_offset

            f.seek(rpath_offset)
            f.write(new_rpath_string)
            return True

    except ElfParsingError:
        # This just means the file wasnt an elf file, so there's no point
        # in updating its rpath anyways; ignore this problem.
        return False


class ElfDynamicSectionUpdateFailed(Exception):
    def __init__(self, old, new):
        self.old = old
        self.new = new
        super(ElfDynamicSectionUpdateFailed, self).__init__(
            "New rpath {} is longer than old rpath {}".format(
                new.decode("utf-8"), old.decode("utf-8")
            )
        )


class ElfParsingError(Exception):
    pass
