# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlCriticPulp(PerlPackage):
    """Some add-on policies for Perl::Critic."""  # AUTO-CPAN2Spack

    homepage = "http://user42.tuxfamily.org/perl-critic-pulp/index.html"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/K/KR/KRYDE/Perl-Critic-Pulp-99.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("99", sha256="b8fda842fcbed74d210257c0a284b6dc7b1d0554a47a3de5d97e7d542e23e7fe")
    version("98", sha256="476f00aea58ca8a10a09ff709e90506ddb70ae35f6574ae184e08eb944413da0")

    provides("perl-perl-critic-podparser-prohibitverbatimmarkup")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-codelayout-prohibitfatcommanewline")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-codelayout-prohibitififsameline")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-codelayout-requirefinalsemicolon")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-codelayout-requiretrailingcommaatnewline")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-compatibility-constantleadingunderscore")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-compatibility-constantpragmahash")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-compatibility-gtk2constants")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-compatibility-perlminimumversionandwhy")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-compatibility-podminimumversion")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-compatibility-prohibitunixdevnull")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-documentation-prohibitadjacentlinks")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-documentation-prohibitadjacentlinks-parser")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-documentation-prohibitbadaproposmarkup")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-documentation-prohibitduplicateheadings")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-documentation-prohibitduplicateseealso")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-documentation-prohibitlinktoself")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-documentation-prohibitparagraphendcomma")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-documentation-prohibitparagraphtwodots")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-documentation-prohibitunbalancedparens")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-documentation-prohibitverbatimmarkup")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-documentation-requireendbeforelastpod")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-documentation-requirefilenamemarkup")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-documentation-requirefinalcut")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-documentation-requirelinkedurls")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-miscellanea-textdomainplaceholders")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-miscellanea-textdomainunused")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-modules-prohibitmoduleshebang")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-modules-prohibitposiximport")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-modules-prohibitusequotedversion")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-valuesandexpressions-constantbeforelt")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-valuesandexpressions-notwithcompare")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-valuesandexpressions-prohibitarrayassignaref")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-valuesandexpressions-prohibitbareworddoublecolon")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-valuesandexpressions-prohibitduplicatehashkeys")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-valuesandexpressions-prohibitemptycommas")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-valuesandexpressions-prohibitfiletest-f")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-valuesandexpressions-prohibitnullstatements")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-valuesandexpressions-prohibitunknownbackslash")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-valuesandexpressions-requirenumericversion")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-policy-valuesandexpressions-unexpandedspecialliteral")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-pulp-podminimumversionviolation")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-pulp-podparser")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-pulp-podparser-prohibitbadaproposmarkup")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-pulp-podparser-prohibitduplicateheadings")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-pulp-podparser-prohibitduplicateseealso")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-pulp-podparser-prohibitlinktoself")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-pulp-podparser-prohibitparagraphendcomma")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-pulp-podparser-prohibitparagraphtwodots")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-pulp-podparser-prohibitunbalancedparens")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-pulp-podparser-requirefilenamemarkup")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-pulp-podparser-requirefinalcut")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-pulp-podparser-requirelinkedurls")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-pulp-prohibitduplicatehashkeys-qword")  # AUTO-CPAN2Spack
    provides("perl-perl-critic-pulp-utils")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-io-string@1.2:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-pod-minimumversion@50:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppi@1.220:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-violation", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic@1.84:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppi-dumper", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-policy@1.84:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-utils@1.100:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppi-document", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-list-moreutils@0.24:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-list-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-perl-critic-utils-ppi", type="run")  # AUTO-CPAN2Spack

