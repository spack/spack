# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import pytest

import llnl.util.filesystem as fs

import spack.object_file.elf as elf
import spack.platforms
import spack.util.executable


# note that our elf parser is platform independent... but I guess creating an elf file
# is slightly more difficult with system tools on non-linux.
def skip_unless_linux(f):
    return pytest.mark.skipif(
        str(spack.platforms.real_host()) != 'linux',
        reason='implementation currently requires linux'
    )(f)


@pytest.mark.requires_executables('gcc')
@skip_unless_linux
def test_elf_get_rpaths(binary_with_rpaths):
    # Compile an "Hello world!" executable and set RPATHs
    long_rpaths = ['/very/long/prefix/x', '/very/long/prefix/y']
    executable = str(binary_with_rpaths(rpaths=long_rpaths))

    assert elf.get_rpaths(executable) == long_rpaths

    # Change the prefix, shortening the string.
    short_rpaths = ['/short/prefix/x', '/short/prefix/y']
    assert elf.replace_rpaths(executable, short_rpaths)

    # Make sure we've got them set properly
    assert elf.get_rpaths(executable) == short_rpaths

    # Enlarging the string fails (even if there was enough room initially... even when
    # the original rpath string was filled with null bytes, we couldn't assume that any
    # null byte can be used, as it may be part of another length 0 string)
    assert not elf.replace_rpaths(executable, long_rpaths)


@pytest.mark.requires_executables('gcc')
@skip_unless_linux
def test_elf_extract_runpath_or_rpath(tmpdir):
    gcc = spack.util.executable.which('gcc')

    with fs.working_dir(str(tmpdir)):
        # Create a library to link to so we can force a dynamic section in an ELF file
        with open('file.c', 'w') as f:
            f.write('int _start(){return 0;}')
        gcc('-shared', '-o', 'library.so', '-nostdlib', 'file.c')

        # Create an ELF file with a dynamic section and a DT_RPATH
        gcc('-Wl,--disable-new-dtags', '-Wl,-rpath,/first', '-Wl,-rpath,/second',
            '-Wl,--no-as-needed', '-nostdlib', 'library.so', 'file.c')

        with open('a.out', 'rb') as f:
            rpath, meta = elf.get_rpaths_byte_string_and_offset(f)
        assert rpath == b'/first:/second'
        assert not meta.is_runpath

        # Create an ELF file with a dynamic section and a DT_RUNPATH
        gcc('-Wl,--enable-new-dtags', '-Wl,-rpath,/first', '-Wl,-rpath,/second',
            '-Wl,--no-as-needed', '-nostdlib', 'library.so', 'file.c')
        with open('a.out', 'rb') as f:
            rpath, meta = elf.get_rpaths_byte_string_and_offset(f)
        assert rpath == b'/first:/second'
        assert meta.is_runpath

        # Create an executable without a dynamic section
        gcc('-Wl,--no-copy-dt-needed-entries', '-nostdlib', 'file.c')
        with open('a.out', 'rb') as f:
            assert elf.get_rpaths_byte_string_and_offset(f) is None


@pytest.mark.requires_executables('gcc')
@skip_unless_linux
def test_elf_force_rpath_or_runpath(tmpdir):
    gcc = spack.util.executable.which('gcc')

    with fs.working_dir(str(tmpdir)):
        with open('file.c', 'w') as f:
            f.write('int _start(){return 0;}')
        gcc('-shared', '-o', 'library.so', '-nostdlib', 'file.c')

        gcc('-Wl,--disable-new-dtags', '-Wl,-rpath,/first', '-Wl,-rpath,/second',
            '-Wl,--no-as-needed', '-nostdlib', 'library.so', 'file.c')
        elf.replace_rpaths('a.out', ['/a', '/b'], force=elf.RPathType.RUNPATH)
        with open('a.out', 'rb') as f:
            rpath, meta = elf.get_rpaths_byte_string_and_offset(f)
        assert rpath == b'/a:/b'
        assert meta.is_runpath

        gcc('-Wl,--enable-new-dtags', '-Wl,-rpath,/first', '-Wl,-rpath,/second',
            '-Wl,--no-as-needed', '-nostdlib', 'library.so', 'file.c')
        elf.replace_rpaths('a.out', ['/a', '/b'], force=elf.RPathType.RPATH)
        with open('a.out', 'rb') as f:
            rpath, meta = elf.get_rpaths_byte_string_and_offset(f)
        assert rpath == b'/a:/b'
        assert not meta.is_runpath


def test_broken_elf(tmpdir):
    with fs.working_dir(str(tmpdir)):
        # No elf magic
        with open('a.out', 'wb') as f:
            f.write(b'x')
        with open('a.out', 'rb') as f:
            with pytest.raises(elf.ElfParsingError, match="No ELF file"):
                elf.get_rpaths_byte_string_and_offset(f)

        # Broken elf header
        with open('a.out', 'wb') as f:
            f.write(b'\x7fELF')
        with open('a.out', 'rb') as f:
            with pytest.raises(elf.ElfParsingError, match="No ELF file"):
                elf.get_rpaths_byte_string_and_offset(f)

        # Invalid class
        with open('a.out', 'wb') as f:
            f.write(b'\x7fELF\x09\x01' + b'\x00' * 10)
        with open('a.out', 'rb') as f:
            with pytest.raises(elf.ElfParsingError, match="Invalid class"):
                elf.get_rpaths_byte_string_and_offset(f)

        # Invalid data type
        with open('a.out', 'wb') as f:
            f.write(b'\x7fELF\x01\x09' + b'\x00' * 10)
        with open('a.out', 'rb') as f:
            with pytest.raises(elf.ElfParsingError, match="Invalid data type"):
                elf.get_rpaths_byte_string_and_offset(f)

        # 64-bit needs at least 64 bytes of header
        with open('a.out', 'wb') as f:
            # this is 56 bytes
            f.write(b'\x7fELF\x02\x01' + b'\x00' * 50)
        with open('a.out', 'rb') as f:
            with pytest.raises(elf.ElfParsingError, match="ELF header malformed"):
                elf.get_rpaths_byte_string_and_offset(f)

        # 32-bit needs at least 52 bytes of header
        with open('a.out', 'wb') as f:
            # this is 46 bytes
            f.write(b'\x7fELF\x01\x01' + b'\x00' * 40)
        with open('a.out', 'rb') as f:
            with pytest.raises(elf.ElfParsingError, match="ELF header malformed"):
                elf.get_rpaths_byte_string_and_offset(f)

        # Not a ET_DYN/ET_EXEC on a 32-bit LE ELF
        with open('a.out', 'wb') as f:
            data = b'\x7fELF\x01\x01' + b'\x00' * 10  # 16 bytes
            # add the et_type + some null bytes to fill the header
            data += b'\x09' + b'\x00' * 35  # 36 more bytes
            f.write(data)
        with open('a.out', 'rb') as f:
            with pytest.raises(elf.ElfParsingError, match="Not an ET_DYN or ET_EXEC"):
                elf.get_rpaths_byte_string_and_offset(f)
