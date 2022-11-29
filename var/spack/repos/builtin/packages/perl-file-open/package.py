# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PerlFileOpen(PerlPackage):
    """File::Open - wrap open/sysopen/opendir and give them a nice and simple interface."""

    homepage = "https://metacpan.org/pod/File::Open"
    url = "https://cpan.metacpan.org/authors/id/M/MA/MAUKE/File-Open-1.0102.tar.gz"

    version("1.0102", sha256="55ab273ca646ba605d899ee2d738f3521f8b78f76b1e654bf3648ee118bc475d")
