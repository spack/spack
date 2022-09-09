# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlTidy(PerlPackage):
    """Indent and reformat perl scripts."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/S/SH/SHANCOCK"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/S/SH/SHANCOCK/Perl-Tidy-20220613.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("20220613", sha256="50496a6952904ef28f495919fc0a67801a63c87779c61308ce1ca5b32467c5d4")
    version("20220217", sha256="bd8bc63043c8bc94aa04811b29f93af794d8871c793c8bd36015dcbdd8a51e83")

    provides("perl-perl-tidy-debugger")  # AUTO-CPAN2Spack
    provides("perl-perl-tidy-devnull")  # AUTO-CPAN2Spack
    provides("perl-perl-tidy-diagnostics")  # AUTO-CPAN2Spack
    provides("perl-perl-tidy-filewriter")  # AUTO-CPAN2Spack
    provides("perl-perl-tidy-formatter")  # AUTO-CPAN2Spack
    provides("perl-perl-tidy-htmlwriter")  # AUTO-CPAN2Spack
    provides("perl-perl-tidy-ioscalar")  # AUTO-CPAN2Spack
    provides("perl-perl-tidy-ioscalararray")  # AUTO-CPAN2Spack
    provides("perl-perl-tidy-indentationitem")  # AUTO-CPAN2Spack
    provides("perl-perl-tidy-linebuffer")  # AUTO-CPAN2Spack
    provides("perl-perl-tidy-linesink")  # AUTO-CPAN2Spack
    provides("perl-perl-tidy-linesource")  # AUTO-CPAN2Spack
    provides("perl-perl-tidy-logger")  # AUTO-CPAN2Spack
    provides("perl-perl-tidy-tokenizer")  # AUTO-CPAN2Spack
    provides("perl-perl-tidy-verticalaligner")  # AUTO-CPAN2Spack
    provides("perl-perl-tidy-verticalaligner-alignment")  # AUTO-CPAN2Spack
    provides("perl-perl-tidy-verticalaligner-line")  # AUTO-CPAN2Spack
    depends_on("perl@5.8:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
