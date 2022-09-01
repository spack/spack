# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDataUuid(PerlPackage):
    """Globally/Universally Unique Identifiers (GUIDs/UUIDs)."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Data-UUID-1.226.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.226", sha256="093d57ffa0d411a94bafafae495697db26f5c9d0277198fe3f7cf2be22996453")
    version("1.225", sha256="d2e4cdaddc12a2ea2e512585b537290d3067e5b742f1f0ba40f66d747c26ece9")

    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-digest-md5", type="run")  # AUTO-CPAN2Spack

