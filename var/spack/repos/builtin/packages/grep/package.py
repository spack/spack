# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Grep(AutotoolsPackage):
    """Grep searches one or more input files for lines containing a match to
    a specified pattern"""

    homepage = "https://www.gnu.org/software/grep/"
    url = "https://ftp.gnu.org/gnu/grep/grep-3.3.tar.xz"

    version("3.9", sha256="abcd11409ee23d4caf35feb422e53bbac867014cfeed313bb5f488aca170b599")
    version("3.7", sha256="5c10da312460aec721984d5d83246d24520ec438dd48d7ab5a05dbc0d6d6823c")
    version("3.3", sha256="b960541c499619efd6afe1fa795402e4733c8e11ebf9fafccc0bb4bccdc5b514")

    variant("pcre", default=False, description="Enable Perl Compatible Regular Expression support")

    build_directory = "spack-build"

    depends_on("pcre", when="+pcre")

    def configure_args(self):
        args = []

        if "+pcre" in self.spec:
            args.append("--enable-perl-regexp")
        else:
            args.append("--disable-perl-regexp")

        return args
