# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPodSpell(PerlPackage):
    """A formatter for spellchecking Pod."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/perl-pod/Pod-Spell"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/D/DO/DOLMEN/Pod-Spell-1.20.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.20", sha256="6383f7bfe22bc0d839a08057a0ce780698b046184aea935be4833d94986dd03c")
    version("1.19_91", sha256="b1e2f8303d2b01184ce189f45eedb0001bad4fd4707d42b6af507184ab6ddf42")

    provides("perl-pod-wordlist")  # AUTO-CPAN2Spack
    depends_on("perl-file-sharedir", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-path-tiny", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-text-wrap", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-class-tiny", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-lingua-en-inflect", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-deep", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl@5.8:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-pod-parser", type="run")  # AUTO-CPAN2Spack
