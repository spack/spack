# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDatetime(PerlPackage):
    """DateTime - A date and time object for Perl"""

    homepage = "https://metacpan.org/pod/DateTime"
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/DateTime-1.63.tar.gz"

    version("1.63", sha256="1b11e49ec6e184ae2a10eccd05eda9534f32458fc644c12ab710c29a3a816f6f")

    depends_on("perl-namespace-autoclean", type=("run"))
