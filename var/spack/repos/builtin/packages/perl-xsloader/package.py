# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXsloader(PerlPackage):
    """XSLoader - Dynamically load C libraries into Perl code."""

    homepage = "https://metacpan.org/pod/XSLoader"
    url = "https://cpan.metacpan.org/authors/id/S/SA/SAPER/XSLoader-0.24.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.24", sha256="e819a35a6b8e55cb61b290159861f0dc00fe9d8c4f54578eb24f612d45c8d85f")

    depends_on("perl-extutils-makemaker", type="build")
