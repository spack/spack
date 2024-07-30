# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PerlBioEnsemblVariation(Package):
    """The Ensembl Variation Perl API and SQL schema."""

    homepage = "http://www.ensembl.org/info/docs/api/variation/"
    url = "https://github.com/Ensembl/ensembl-variation/archive/release/111.zip"

    maintainers("teaguesterling")

    license("APACHE-2.0", checked_by="teaguesterling")

    version("112", sha256="ad75ff0a9efbf2d5c10ab5087d414bac685819664d01fbe4a9765393bd742a7c")
    version("111", sha256="b2171b3f5f82a2b7e849c0ec8dc254f4bace4b3faba1b3ab75c5eea596e33bef")
    version("110", sha256="210d627dcb867d9fda3a0d94428da256f394c32e34df5171b9b9e604507e1f05")

    extends("perl")

    variant("sql", default=False, description="Install SQL files")
    variant("scripts", default=False, description="Install additional scripts")
    variant("tools", default=False, description="Install additional tools")
    variant("ld", default=False, description="Compile LD calculation tools")

    depends_on("perl-bioperl")
    depends_on("perl-bio-ensembl")
    depends_on("perl-bio-bigfile")
    depends_on("perl-bio-db-hts")
    depends_on("perl-sereal")
    depends_on("perl-json")
    depends_on("perl-set-intervaltree")
    depends_on("perl-string-approx")
    depends_on("perl-xml-hash-xs")
    depends_on("perl-xml-libxml")
    depends_on("perl-date-manip")

    with when("+ld"):
        depends_on("htslib", type=("build", "run"))
        depends_on("gmake", type="build")

    def build(self, spec):
        if spec.satisfies("+ld"):
            make = which("make")
            with working_dir("C_code"):
                make()

    def install(self, spec, prefix):
        install_tree("modules", prefix.lib.perl5)

        mkdirp(prefix.share.ensembl.variation)
        for extra in ["sql"]:
            if spec.satisfies(f"+{extra}"):
                target = join_path(prefix.share.ensembl, extra)
                install_tree(extra, target)

        if spec.satisfies("+ld"):
            mkdirp(prefix.bin)
            with working_dir("C_code"):
                install("calc_genotypes", prefix.bin.calc_genotypes)
                install("ld_vcf", prefix.bin.ld_vcf)
