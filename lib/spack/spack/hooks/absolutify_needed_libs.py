# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

import spack.util.executable

# for now just find patchelf in the path, cause we don't want to trigger
# infinite recursion during when bootstrapping patchelf.
patchelf = spack.util.executable.which('patchelf')

origin_regex = re.compile(r'\${ORIGIN}|\$ORIGIN')


def get_rpaths(path):
    return [
        origin_regex.sub(os.path.dirname(path), path) for
        path in patchelf('--print-rpath', path, output=str).strip('\n').split(':')]


def get_needed_sonames(path):
    needed = patchelf('--print-needed', path, output=str).strip('\n').split('\n')
    return [soname for soname in needed if '/' not in soname]


def is_64_bit_elf_exec_or_dyn(path):
    """
    Interprets the first 20 bytes from a file as an ELF header.

    Returns:
        True/False/None if 64-bit, 32-bit or not a ET_EXEC/ET_DYN type ELF file resp.
    """
    try:
        with open(path, 'rb') as original:
            header = original.read(20)
    except IOError:
        return None

    if len(header) != 20 or header[:4] != b'\x7fELF':
        return None

    is_little_endian = header[5] == 0x01

    # Only look at ET_EXEC and ET_DYN
    e_type = header[16 if is_little_endian else 17]

    if e_type != 0x02 and e_type != 0x03:
        return None

    is_64_bit = header[4] == 0x02
    return is_64_bit


def absolutify_needed_libs_for(path):
    elf_type = is_64_bit_elf_exec_or_dyn(path)

    # Skip everything which is not exec/dyn elf.
    if elf_type is None:
        return

    rpaths = get_rpaths(path)
    sonames = get_needed_sonames(path)

    # Replace sonames with rpaths
    for rpath in rpaths:
        for soname in sonames:
            candidate = os.path.join(rpath, soname)
            if elf_type == is_64_bit_elf_exec_or_dyn(candidate):
                patchelf('--replace-needed', soname, candidate, path)

    # Everything else is assumed to be a system library
    # Note: this breaks dlopen(...) search paths, so should be configurable.
    patchelf('--remove-rpath', path)


def check_elf_files(prefix):
    for dir, _, files in os.walk(prefix):
        for file in files:
            path = os.path.join(dir, file)

            if os.path.islink(path):
                continue

            absolutify_needed_libs_for(path)


def post_install(spec):
    if spec.external or patchelf is None:
        return

    check_elf_files(spec.prefix)
