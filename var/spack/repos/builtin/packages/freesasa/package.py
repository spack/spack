# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Freesasa(AutotoolsPackage):
    """C-library for calculating Solvent Accessible Surface Areas"""

    homepage = "http://freesasa.github.io"
    url = "https://github.com/mittinatten/freesasa/releases/download/2.1.2/freesasa-2.1.2.zip"
    git = "https://github.com/mittinatten/freesasa.git"
    maintainers("RMeli")

    version("2.1.2", sha256="a031c4eb8cd59e802d715a37ef72930ec2d90ec53dfcf1bea0b0255980490fd5")

    variant("json", default=True)
    variant("xml", default=True)
    variant("threads", default=True)

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    # https://github.com/mittinatten/freesasa/issues/88
    depends_on("pkg-config", type="build")

    depends_on("json-c", when="+json")
    depends_on("libxml2", when="+xml")

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = []
        args.extend(self.enable_or_disable("json"))
        args.extend(self.enable_or_disable("xml"))
        args.extend(self.enable_or_disable("threads"))
        return args
