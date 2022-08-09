# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import pytest

import llnl.util.filesystem as fs

import spack.platforms
from spack.hooks.absolutify_elf_sonames import SharedLibrariesVisitor, patch_sonames
from spack.util.executable import Executable


def skip_unless_linux(f):
    return pytest.mark.skipif(
        str(spack.platforms.real_host()) != "linux", reason="only tested on linux for now"
    )(f)


class ExecutableIntercept:
    def __init__(self):
        self.calls = []

    def __call__(self, *args, **kwargs):
        self.calls.append(args)

    @property
    def returncode(self):
        return 0


@pytest.mark.requires_executables("/usr/bin/gcc")
@skip_unless_linux
def test_absolutify_elf_sonames(tmpdir):
    """Integration test for soname rewriting"""
    gcc = Executable("gcc")
    with fs.working_dir(str(tmpdir)):
        with open("hello.c", "w") as f:
            f.write("int main(){return 0;}")
        gcc("hello.c", "-o", "no-soname.so", "--shared")
        gcc("hello.c", "-o", "soname.so", "--shared", "-Wl,-soname,example.so")
        gcc("hello.c", "-pie", "-o", "executable.so")

    visitor = SharedLibrariesVisitor(exclude_list=[])
    fs.visit_directory_tree(str(tmpdir), visitor)
    relative_paths = visitor.get_shared_libraries_relative_paths()

    assert "no-soname.so" in relative_paths
    assert "soname.so" in relative_paths
    assert "executable.so" not in relative_paths

    patchelf = ExecutableIntercept()

    patch_sonames(patchelf, str(tmpdir), relative_paths)

    assert len(patchelf.calls) == 2
    elf_1 = tmpdir.join("no-soname.so")
    elf_2 = tmpdir.join("soname.so")
    assert ("--set-soname", elf_1, elf_1) in patchelf.calls
    assert ("--set-soname", elf_2, elf_2) in patchelf.calls
