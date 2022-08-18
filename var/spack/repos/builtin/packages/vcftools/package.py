# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vcftools(AutotoolsPackage):
    """VCFtools is a program package designed for working with VCF files,
    such as those generated by the 1000 Genomes Project. The aim of
    VCFtools is to provide easily accessible methods for working
    with complex genetic variation data in the form of VCF files.
    """

    homepage = "https://vcftools.github.io/"
    url = "https://github.com/vcftools/vcftools/releases/download/v0.1.14/vcftools-0.1.14.tar.gz"

    # this is "a pre-release"
    # version('0.1.15', sha256='31e47afd5be679d89ece811a227525925b6907cce4af2c86f10f465e080383e3')
    version("0.1.14", sha256="76d799dd9afcb12f1ed42a07bc2886cd1a989858a4d047f24d91dcf40f608582")

    depends_on("perl", type=("build", "run"))
    depends_on("zlib")

    # this needs to be in sync with what setup_run_environment adds to
    # PERL5LIB below
    def configure_args(self):
        return ["--with-pmdir={0}".format(self.prefix.lib)]

    @run_before("install")
    def filter_sbang(self):
        """Run before install so that the standard Spack sbang install hook
        can fix up the path to the perl binary.
        """

        with working_dir("src/perl"):
            match = "^#!/usr/bin/env perl"
            substitute = "#!{perl}".format(perl=self.spec["perl"].command.path)
            # tab-to-vcf added in 0.1.15
            files = [
                "fill-aa",
                "fill-an-ac",
                "fill-fs",
                "fill-ref-md5",
                "tab-to-vcf",
                "vcf-annotate",
                "vcf-compare",
                "vcf-concat",
                "vcf-consensus",
                "vcf-contrast",
                "vcf-convert",
                "vcf-fix-newlines",
                "vcf-fix-ploidy",
                "vcf-indel-stats",
                "vcf-isec",
                "vcf-merge",
                "vcf-phased-join",
                "vcf-query",
                "vcf-shuffle-cols",
                "vcf-sort",
                "vcf-stats",
                "vcf-subset",
                "vcf-to-tab",
                "vcf-tstv",
                "vcf-validator",
            ]
            kwargs = {"ignore_absent": True, "backup": False, "string": False}
            filter_file(match, substitute, *files, **kwargs)

    def setup_run_environment(self, env):
        env.prepend_path("PERL5LIB", self.prefix.lib)
