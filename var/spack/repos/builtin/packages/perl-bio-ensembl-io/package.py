# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PerlBioEnsemblIo(Package):
    """File parsing and writing code for Ensembl."""

    homepage = "https://github.com/Ensembl/ensembl-io/"
    url = "https://github.com/Ensembl/ensembl-io/archive/release/111.zip"

    maintainers("teaguesterling")

    license("APACHE-2.0", checked_by="teaguesterling")

    version("112", sha256="ccbffe7c15318075463db46be348655a5914762e05ff47da2d72a4c99414d39a")
    version("111", sha256="f81d4c1aea88aac7105aaa3fec548e39b79f129c7abc08b55be7d0345aa5482c")
    version("110", sha256="83cf00ecdb6184be480fc3cbf0ffc322d3e9411e14602396fda8d153345d6c2e")

    extends("perl")

    variant("scripts", default=False, description="Install scripts")

    depends_on("perl-bio-db-bigfile")
    depends_on("perl-try-tiny")

    def install(self, spec, prefix):
        install_tree("modules", prefix.lib.perl5)
        mkdirp(prefix.share.ensembl)
        for extra in ["scripts"]:
            if spec.satisfies(f"+{extra}"):
                extra = extra.replace("_", "-")
                target = join_path(prefix.share.ensembl, extra)
                install_tree(extra, target)
