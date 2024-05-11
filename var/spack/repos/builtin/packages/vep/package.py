# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install vep
#
# You can edit this file again by typing:
#
#     spack edit vep
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Vep(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://useast.ensembl.org/info/docs/tools/vep/index.html"
    url = "https://github.com/Ensembl/ensembl-vep/archive/release/111.zip"

    maintainers("teaguesterling")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    license("UNKNOWN", checked_by="github_user1")

    version("111.0", sha256="9cb326a1fa0054ce1a417f8fd4f2325ba605c40ec10eefbf87f461c264a89407")
    version("110.0", sha256="391a1fe50139064c1044c09e013bb21437933d677537b5d3336807f3b131fb51")

    depends_on("gcc")
    depends_on("gmake")
    depends_on("perl@5.10:")

    depends_on("perl-archive-zip")
    depends_on("perl-dbd-mysql")
    depends_on("perl-dbi")
    depends_on("perl-bio-db-hts")
    depends_on("perl-json", when="+json")
    depends_on("perl-set-intervaltree", when="+nearest")
    depends_on("perl-perlio-gzip", when="+gzip")
    depends_on("perl-bioperl", when="~bioperl")

    variant("json", default=True)
    variant("nearest", default=True)
    variant("gzip", default=True)
    variant("bioperl", default=False)
    variant("cache", default=True)
    variant("cache", default=True)
    variant("fasta", default=True, when="+cache")
    variant(
        "species", 
        values=["human", "mouse", "all"], 
        default="human",
        when="+cache",
        multi=True
    ) 
    variant(
        "assembly", 
        values=["grch37", "grch38"], 
        default="grch38",
        when="+cache species=human"
    )

    def install_args(self):
        auto = "a"
        args = [
            "--DESTDIR", f"{self.spec.prefix.lib}",
            "--NO_HTSLIB",
            "--NO_UPDATE",
            "--NO_TEST",
        ]
        if self.spec.satisfies("~bioperl"):
            args += ["--NO_BIOPERL"]
        if self.spec.satisfies("+cache"):
            species = [f"{species}_refseq"
                for species in self.spec.variants['species'].value
            ]
            auto += "c"
            args += [
                "--CACHEDIR", f"{self.spec.prefix.cache}",
                "--CACHE_VERSION", f"{self.spec.version.up_to(1)}",
                "--SPECIES", f"{','.join(species)}",
            ]
            if self.spec.satisfies("species=human"):
                args += [
                    "--ASSEMBLY", f"{self.spec.variants['assembly'].value}"
                ]
        if self.spec.satisfies("+fasta"):
            auto += "f"
        args += [
            "--AUTO", auto,
        ]
        return args

    def install(self, spec, prefix):
        with working_dir(self.stage.source_path):
            install = which("./INSTALL.pl")
            install(*self.install_args())
#        1. add /home/teague/System/apps/spack/opt/spack/linux-pop22-zen3/gcc-13.1.0/vep-111.0-lvprwltnkq5n7dnnmm5dcpall3b7dkhi/lib to your PERL5LIB environment variable
#       2. add /home/teague/System/apps/spack/opt/spack/linux-pop22-zen3/gcc-13.1.0/vep-111.0-lvprwltnkq5n7dnnmm5dcpall3b7dkhi/lib/htslib to your PATH environment variable

