# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import pytest

import spack.operating_systems.cray_backend as cray_backend
import spack.operating_systems.linux_distro as linux_distro
from spack.util.executable import Executable
from spack.version import Version


def test_read_cle_release_file(tmpdir, monkeypatch):
    """test reading the Cray cle-release file"""
    cle_release_path = tmpdir.join("cle-release")
    with cle_release_path.open("w") as f:
        f.write(
            """\
RELEASE=6.0.UP07
BUILD=6.0.7424
DATE=20190611
ARCH=noarch
NETWORK=ari
PATCHSET=35-201906112304
DUMMY=foo=bar
"""
        )

    monkeypatch.setattr(cray_backend, "_cle_release_file", str(cle_release_path))
    attrs = cray_backend.read_cle_release_file()

    assert attrs["RELEASE"] == "6.0.UP07"
    assert attrs["BUILD"] == "6.0.7424"
    assert attrs["DATE"] == "20190611"
    assert attrs["ARCH"] == "noarch"
    assert attrs["NETWORK"] == "ari"
    assert attrs["PATCHSET"] == "35-201906112304"
    assert attrs["DUMMY"] == "foo=bar"

    assert cray_backend.CrayBackend._detect_crayos_version() == 6


def test_read_clerelease_file(tmpdir, monkeypatch):
    """test reading the Cray clerelease file"""
    clerelease_path = tmpdir.join("clerelease")
    with clerelease_path.open("w") as f:
        f.write("5.2.UP04\n")

    monkeypatch.setattr(cray_backend, "_clerelease_file", str(clerelease_path))
    v = cray_backend.read_clerelease_file()

    assert v == "5.2.UP04"

    assert cray_backend.CrayBackend._detect_crayos_version() == 5


def test_cle_release_precedence(tmpdir, monkeypatch):
    """test that cle-release file takes precedence over clerelease file."""
    cle_release_path = tmpdir.join("cle-release")
    clerelease_path = tmpdir.join("clerelease")

    with cle_release_path.open("w") as f:
        f.write(
            """\
RELEASE=6.0.UP07
BUILD=6.0.7424
DATE=20190611
ARCH=noarch
NETWORK=ari
PATCHSET=35-201906112304
DUMMY=foo=bar
"""
        )

    with clerelease_path.open("w") as f:
        f.write("5.2.UP04\n")

    monkeypatch.setattr(cray_backend, "_clerelease_file", str(clerelease_path))
    monkeypatch.setattr(cray_backend, "_cle_release_file", str(cle_release_path))

    assert cray_backend.CrayBackend._detect_crayos_version() == 6


@pytest.mark.parametrize(
    "confstr_value,expected",
    [
        ("glibc 2.37", ("glibc", Version("2.37"))),
        ("glibc +1.2", None),
        ("glibc", None),
        ("somthing 2.37", None),
        ("glibc 2.37 helloworld", None),
    ],
)
def test_elf_libc_detect_confstr(confstr_value, expected):
    confstr = lambda x: confstr_value if x == "CS_GNU_LIBC_VERSION" else None
    assert linux_distro._confstr(confstr) == expected


@pytest.mark.requires_executables("gcc")
@pytest.mark.skipif(sys.platform != "linux", reason="only tested on linux")
@pytest.mark.parametrize(
    "interpreter_name,version,expected",
    [
        # Standard musl output
        ("ld-musl-x86_64.so.1", "Version 1.2.4", ("musl", Version("1.2.4"))),
        # Not musl
        ("ld-linux-x86_64.so.2", "Version 1.2.4", None),
        # Not matching regex
        ("ld-musl-x86_64.so.1", "Version 1.2.4 unexpected text", None),
    ],
)
def test_elf_libc_detect_dynamic_linker(interpreter_name, version, expected, tmpdir):
    # Create an interpreter, it just dumps version to stderr
    interpreter = tmpdir.join(interpreter_name)
    interpreter.write(
        f"""\
#!/bin/sh
echo "musl libc (x86_64)" >&2
echo "{version}" >&2
echo "Dynamic Program Loader" >&2
echo "Usage: ld-musl-x86_64.so.1 [options] [--] pathname" >&2
exit 1
"""
    )
    interpreter.chmod(0o755)

    # Compile a small hello world program, and create an ELF
    # file with the interpreter as the dynamic linker
    source, elf = tmpdir.join("source.c"), tmpdir.join("elf")
    source.write("int main() { return 0; }")
    gcc = Executable("gcc")
    gcc("-Wl,--dynamic-linker", interpreter.strpath, "-o", elf.strpath, source.strpath)

    # Run detection
    assert linux_distro._dynamic_linker(elf.strpath) == expected


@pytest.mark.skipif(sys.platform != "linux", reason="only tested on linux")
@pytest.mark.parametrize("stdout", [True, False])
def test_ldd_musl(stdout, tmpdir):
    # Create an ldd that just dumps version to stdout or stderr
    redirect = "" if stdout else ">&2"
    ldd = tmpdir.join("ldd")
    ldd.write(
        f"""\
#!/bin/sh
echo "musl libc (x86_64)" {redirect}
echo "Version 1.2.4" {redirect}
echo "Dynamic Program Loader" {redirect}
echo "Usage: ldd [options] [--] pathname" {redirect}
exit 1
"""
    )
    ldd.chmod(0o755)

    result = linux_distro._ldd(ldd.strpath)
    if stdout:
        assert result is None
    else:
        assert result == ("musl", Version("1.2.4"))


@pytest.mark.skipif(sys.platform != "linux", reason="only tested on linux")
@pytest.mark.parametrize("stdout", [True, False])
def test_ldd_glibc(stdout, tmpdir):
    # Create an ldd that just dumps version to stdout or stderr
    redirect = "" if stdout else ">&2"
    ldd = tmpdir.join("ldd")
    ldd.write(
        f"""\
#!/bin/sh
if [ "$1" = "--version" ]; then
    echo "ldd (Ubuntu GLIBC 2.37-0ubuntu2) 2.37" {redirect}
    exit 0
fi
exit 1
"""
    )
    ldd.chmod(0o755)

    result = linux_distro._ldd(ldd.strpath)
    if stdout:
        assert result == ("glibc", Version("2.37"))
    else:
        assert result is None
