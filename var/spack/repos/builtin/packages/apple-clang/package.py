# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re

from spack.package import *


class AppleClang(BundlePackage):
    """Apple's Clang compiler"""

    homepage = "https://developer.apple.com/videos/developer-tools/compiler-and-llvm"
    has_code = False

    maintainers("alalazo")

    executables = ["^clang$", r"^clang\+\+$", "^ld.lld$", "^lldb$"]

    @classmethod
    def determine_version(cls, exe):
        version_regex = re.compile(
            # Apple's LLVM compiler has its own versions, which are
            # different from vanilla LLVM
            r"^Apple (?:LLVM|clang) version ([^ )]+)",
            # Multi-line, since 'Apple clang' may not be on the first line
            # in particular, when run as gcc, it seems to output
            # "Configured with: --prefix=..." as the first line
            re.M,
        )
        try:
            compiler = Executable(exe)
            output = compiler("--version", output=str, error=str)
            match = version_regex.search(output)
            if match:
                return match.group(match.lastindex)
        except Exception:
            pass

        return None

    @classmethod
    def determine_variants(cls, exes, version_str):
        compilers = {}
        for exe in exes:
            if "clang++" in exe:
                compilers["cxx"] = exe
            elif "clang" in exe:
                compilers["c"] = exe
            elif "ld.lld" in exe:
                compilers["ld"] = exe
            elif "lldb" in exe:
                compilers["lldb"] = exe

        return "", {"compilers": compilers}

    @classmethod
    def validate_detected_spec(cls, spec, extra_attributes):
        msg = f'the extra attribute "compilers" must be set for the detected spec "{spec}"'
        assert "compilers" in extra_attributes, msg
        compilers = extra_attributes["compilers"]
        for key in ("c", "cxx"):
            msg = f"{key} compiler not found for {spec}"
            assert key in compilers, msg

    @property
    def cc(self):
        msg = "apple-clang is expected to be an external spec"
        assert self.spec.concrete and self.spec.external, msg
        return self.spec.extra_attributes["compilers"].get("c", None)

    @property
    def cxx(self):
        msg = "apple-clang is expected to be an external spec"
        assert self.spec.concrete and self.spec.external, msg
        return self.spec.extra_attributes["compilers"].get("cxx", None)

    @classmethod
    def runtime_constraints(cls, *, spec, pkg):
        """Callback function to inject runtime-related rules into the solver.

        Rule-injection is obtained through method calls of the ``pkg`` argument.

        Documentation for this function is temporary. When the API will be in its final state,
        we'll document the behavior at https://spack.readthedocs.io/en/latest/

        Args:
            compiler: compiler object (node attribute) currently considered
            pkg: object used to forward information to the solver
        """
        pkg("*").depends_on(
            "llvm-openmp",
            when="+openmp %apple-clang ",
            type="link",
            description="If any package uses %apple-clang +openmp, it depends on llvm-openmp",
        )
