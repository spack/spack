# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re

from spack_repo.builtin_mock.build_systems.compiler import CompilerPackage
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class Llvm(Package, CompilerPackage):
    """Simple compiler package."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/gcc-1.0.tar.gz"

    tags = ["compiler"]

    version("18.1.8", md5="0123456789abcdef0123456789abcdef")

    variant(
        "clang", default=True, description="Build the LLVM C/C++/Objective-C compiler frontend"
    )
    variant(
        "flang",
        default=False,
        description="Build the LLVM Fortran compiler frontend "
        "(experimental - parser only, needs GCC)",
    )
    variant("lld", default=True, description="Build the LLVM linker")

    provides("c", "cxx", when="+clang")
    provides("fortran", when="+flang")

    depends_on("c")

    compiler_version_argument = "--version"
    c_names = ["clang"]
    cxx_names = ["clang++"]

    clang_and_friends = "(?:clang|flang|flang-new)"

    compiler_version_regex = (
        # Normal clang compiler versions are left as-is
        rf"{clang_and_friends} version ([^ )\n]+)-svn[~.\w\d-]*|"
        # Don't include hyphenated patch numbers in the version
        # (see https://github.com/spack/spack/pull/14365 for details)
        rf"{clang_and_friends} version ([^ )\n]+?)-[~.\w\d-]*|"
        rf"{clang_and_friends} version ([^ )\n]+)|"
        # LLDB
        r"lldb version ([^ )\n]+)|"
        # LLD
        r"LLD ([^ )\n]+) \(compatible with GNU linkers\)"
    )
    fortran_names = ["flang", "flang-new"]

    @classmethod
    def determine_version(cls, exe):
        try:
            compiler = Executable(exe)
            output = compiler(cls.compiler_version_argument, output=str, error=str)
            if "Apple" in output:
                return None
            if "AMD" in output:
                return None
            match = re.search(cls.compiler_version_regex, output)
            if match:
                return match.group(match.lastindex)
        except ProcessError:
            pass
        except Exception as e:
            tty.debug(e)

        return None

    @classmethod
    def filter_detected_exes(cls, prefix, exes_in_prefix):
        # Executables like lldb-vscode-X are daemon listening on some port and would hang Spack
        # during detection. clang-cl, clang-cpp, etc. are dev tools that we don't need to test
        reject = re.compile(
            r"-(vscode|cpp|cl|ocl|gpu|tidy|rename|scan-deps|format|refactor|offload|"
            r"check|query|doc|move|extdef|apply|reorder|change-namespace|"
            r"include-fixer|import-test|dap|server|PerfectShuffle)"
        )
        return [x for x in exes_in_prefix if not reject.search(x)]

    def install(self, spec, prefix):
        # Create the minimal compiler that will fool `spack compiler find`
        mkdirp(prefix.bin)
        with open(prefix.bin.gcc, "w", encoding="utf-8") as f:
            f.write('#!/bin/bash\necho "%s"' % str(spec.version))
        set_executable(prefix.bin.gcc)

    def _cc_path(self):
        if self.spec.satisfies("+clang"):
            return os.path.join(self.spec.prefix.bin, "clang")
        return None

    def _cxx_path(self):
        if self.spec.satisfies("+clang"):
            return os.path.join(self.spec.prefix.bin, "clang++")
        return None

    def _fortran_path(self):
        if self.spec.satisfies("+flang"):
            return os.path.join(self.spec.prefix.bin, "flang")
        return None
