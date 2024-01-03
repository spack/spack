# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMemoize(PerlPackage):
    """Memoize - Make functions faster by trading space for time."""

    homepage = "https://metacpan.org/pod/Memoize"
    url = "https://cpan.metacpan.org/authors/id/A/AR/ARISTOTLE/Memoize-1.16.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.16", sha256="091952bcf492ecee35b9e5b8d72920c58023441d79208c1db87837c5c57807be")

    depends_on("perl-extutils-makemaker", type="build")
    depends_on("perl-scalar-list-utils")
