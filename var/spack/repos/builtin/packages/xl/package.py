# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import re

import llnl.util.tty as tty

import spack.compiler
from spack.package import *


class Xl(Package, CompilerPackage):
    """IBM XL C/C++/Fortran is an advanced, high-performance compiler that can be
    used for developing complex, computationally intensive programs, including
    interlanguage calls with C and Fortran programs.
    """

    homepage = "https://www.ibm.com/support/knowledgecenter/SSXVZZ_16.1.1/com.ibm.compilers.linux.doc/welcome.html"

    variant("r", default=True, description="The _r version of compilers")

    def install(self, spec, prefix):
        raise InstallError(
            "XL compilers are not installable yet, but can be "
            "detected on a system where they are supplied by vendor"
        )

    languages = ["c", "cxx", "fortran"]
    c_names = ["xlc", "xlc_r"]
    cxx_names = ["xlc++", "xlc++_r"]
    fortran_names = ["xlf", "xlf_r"]  # TODO complete this
    version_argument = "-qversion"
    version_regex = r"([0-9]?[0-9]\.[0-9])"

    @classmethod
    def determine_variants(cls, exes, version_str):
        _r_exes = [e for e in exes if "_r" in e]
        _exes = [e for e in exes if "_r" not in e]

        _r_paths = cls.determine_paths(exes=_r_exes) if _r_exes else None
        _paths = cls.determine_paths(exes=_exes) if _exes else None

        results = []
        if _r_paths:
            results.append(("+r", {"paths": _r_paths}))
        if _paths:
            results.append(("~r", {"paths": _paths}))
        return results

    @property
    def cc(self):
        if self.spec.external:
            return self.spec.extra_attributes["compilers"]["c"]
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg

    @property
    def cxx(self):
        if self.spec.external:
            return self.spec.extra_attributes["compilers"]["cxx"]
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg

    @property
    def fortran(self):
        if self.spec.external:
            return self.spec.extra_attributes["compilers"]["fortran"]
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg
