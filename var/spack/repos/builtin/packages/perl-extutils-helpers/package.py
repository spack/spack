# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExtutilsHelpers(PerlPackage):
    """ExtUtils::Helpers - Various portability utilities for module builders"""

    homepage = "https://metacpan.org/pod/ExtUtils::Helpers"
    url = "https://cpan.metacpan.org/authors/id/L/LE/LEONT/ExtUtils-Helpers-0.026.tar.gz"

    version("0.026", sha256="de901b6790a4557cf4ec908149e035783b125bf115eb9640feb1bc1c24c33416")
    provides("perl-extutils-helpers-unix")  # AUTO-CPAN2Spack
    provides("perl-extutils-helpers-vms")  # AUTO-CPAN2Spack
    provides("perl-extutils-helpers-windows")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
