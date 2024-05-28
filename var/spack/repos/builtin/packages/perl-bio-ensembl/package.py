# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PerlBioEnsembl(Package):
    """The Ensembl Core Perl API and SQL schema"""

    homepage = "https://useast.ensembl.org/info/docs/api/index.html"
    url = "https://github.com/Ensembl/ensembl/archive/release/111.zip"

    def url_for_version(self, version):
        return f"https://github.com/Ensembl/ensembl/archive/release/{version.up_to(1)}.zip"

    maintainers("teaguesterling")

    license("APACHE-2.0", checked_by="teaguesterling")

    version("112", sha256="24ca424c583c168a78bfcc9536cbe2782216cff532540a9520c59a48f57a49b1")
    version("111", sha256="346c47c75a6fa8dcfd9f9d22e9f1e0ccc35b2fb99f75980a0c74d892e4ab2b6d")
    version("110", sha256="4264b8ebfe0aa03849a154673ba2ccbe647e6e7c156d7e781b70390280693e2d")

    extends("perl")

    variant("sql", default=False, description="Install SQL files")
    variant("misc_scripts", default=False, description="Install misc Ensembl scripts")

    depends_on("perl-dbi")
    depends_on("perl-dbd-mysql@:4")
    depends_on("perl-http-tiny")
    depends_on("perl-io-compress")
    depends_on("perl-uri")
    depends_on("perl-config-inifiles")
    depends_on("perl-gzip-faster")
    depends_on("perl-list-moreutils")

    def install(self, spec, prefix):
        install_tree("modules", prefix.lib.perl5)
        mkdirp(prefix.share.ensembl)
        for extra in ["sql", "misc_scripts"]:
            if spec.satisfies(f"+{extra}"):
                extra = extra.replace("_", "-")
                target = join_path(prefix.share.ensembl, extra)
                install_tree(extra, target)
