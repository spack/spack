# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Mustang(MakefilePackage):
    """Mustang is a program that implements an algorithm for structural
    alignment of multiple protein structures. Given a set of PDB files, the
    program uses the spatial information in the Calpha atoms of the set to
    produce a sequence alignment"""

    homepage = "https://lcb.infotech.monash.edu/mustang/"
    url = "https://lcb.infotech.monash.edu/mustang/mustang_v3.2.4.tgz"

    license_url = "https://lcb.infotech.monash.edu/mustang/"

    version("3.2.4", sha256="c05e91c955f491a1fddc404a36ef963b057fd725bcc6d22ef6df1c23b26ce237")

    def edit(self, spec, prefix):
        filter_file("CCP = .*", f"CCP = {spack_cxx}", "Makefile")

    def build(self, spec, prefix):
        make("all")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        binary = f"mustang-{self.version}"
        install(join_path("bin", binary), prefix.bin)
        os.symlink(join_path(prefix.bin, binary), prefix.bin.mustang)
