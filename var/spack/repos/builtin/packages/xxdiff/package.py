# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xxdiff(MakefilePackage):
    """Graphical File And Directories Comparator And Merge Tool."""

    homepage = "https://furius.ca/xxdiff/"
    git = "https://github.com/blais/xxdiff.git"

    maintainers("vanderwb")

    version("latest", branch = "master")

    depends_on("flex@2.5.31:")
    depends_on("bison")
    depends_on("qt@5:", type=("build", "link", "run"))

    def edit(self, spec, prefix):
        env['QMAKE'] = 'qmake'

    def build(self, spec, prefix):
        with working_dir("src"):
            # Create the makefile
            make("-f", "Makefile.bootstrap")
            make()

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('bin/xxdiff', prefix.bin)
