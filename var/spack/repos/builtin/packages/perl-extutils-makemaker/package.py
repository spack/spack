# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExtutilsMakemaker(PerlPackage):
    """ExtUtils::MakeMaker - Create a module Makefile. This utility is designed
    to write a Makefile for an extension module from a Makefile.PL. It is based
    on the Makefile.SH model provided by Andy Dougherty and the perl5-porters.
    """

    homepage = "https://github.com/Perl-Toolchain-Gang/ExtUtils-MakeMaker"
    url = "https://cpan.metacpan.org/authors/id/B/BI/BINGOS/ExtUtils-MakeMaker-7.24.tar.gz"

    version("7.65_02", sha256="a933a21ec1fe340dad272334e6a0623d3140cb649568ec0d2aa1f0c00a423986")
    version("7.64", sha256="4a6ac575815c0413b1f58967043cc9f2e166446b73c687f9bc62b5eaed9464a0", preferred=True)
    version("7.24", sha256="416abc97c3bb2cc72bef28852522f2859de53e37bf3d0ae8b292067d78755e69")

    provides("perl-dynaloader")  # AUTO-CPAN2Spack
    provides("perl-extutils-command")  # AUTO-CPAN2Spack
    provides("perl-extutils-command-mm")  # AUTO-CPAN2Spack
    provides("perl-extutils-liblist")  # AUTO-CPAN2Spack
    provides("perl-extutils-liblist-kid")  # AUTO-CPAN2Spack
    provides("perl-extutils-mm")  # AUTO-CPAN2Spack
    provides("perl-extutils-mm-aix")  # AUTO-CPAN2Spack
    provides("perl-extutils-mm-any")  # AUTO-CPAN2Spack
    provides("perl-extutils-mm-beos")  # AUTO-CPAN2Spack
    provides("perl-extutils-mm-cygwin")  # AUTO-CPAN2Spack
    provides("perl-extutils-mm-dos")  # AUTO-CPAN2Spack
    provides("perl-extutils-mm-darwin")  # AUTO-CPAN2Spack
    provides("perl-extutils-mm-macos")  # AUTO-CPAN2Spack
    provides("perl-extutils-mm-nw5")  # AUTO-CPAN2Spack
    provides("perl-extutils-mm-os2")  # AUTO-CPAN2Spack
    provides("perl-extutils-mm-os390")  # AUTO-CPAN2Spack
    provides("perl-extutils-mm-qnx")  # AUTO-CPAN2Spack
    provides("perl-extutils-mm-uwin")  # AUTO-CPAN2Spack
    provides("perl-extutils-mm-unix")  # AUTO-CPAN2Spack
    provides("perl-extutils-mm-vms")  # AUTO-CPAN2Spack
    provides("perl-extutils-mm-vos")  # AUTO-CPAN2Spack
    provides("perl-extutils-mm-win32")  # AUTO-CPAN2Spack
    provides("perl-extutils-mm-win95")  # AUTO-CPAN2Spack
    provides("perl-extutils-my")  # AUTO-CPAN2Spack
    provides("perl-extutils-makemaker-config")  # AUTO-CPAN2Spack
    provides("perl-extutils-makemaker-locale")  # AUTO-CPAN2Spack
    provides("perl-extutils-makemaker--version")  # AUTO-CPAN2Spack
    provides("perl-extutils-makemaker-charstar")  # AUTO-CPAN2Spack
    provides("perl-extutils-makemaker-version")  # AUTO-CPAN2Spack
    provides("perl-extutils-makemaker-version-regex")  # AUTO-CPAN2Spack
    provides("perl-extutils-makemaker-version-vpp")  # AUTO-CPAN2Spack
    provides("perl-extutils-mkbootstrap")  # AUTO-CPAN2Spack
    provides("perl-extutils-mksymlists")  # AUTO-CPAN2Spack
    provides("perl-extutils-testlib")  # AUTO-CPAN2Spack
    provides("perl-mm")  # AUTO-CPAN2Spack
    provides("perl-my")  # AUTO-CPAN2Spack
    provides("perl-version")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-data-dumper", type="run")  # AUTO-CPAN2Spack
