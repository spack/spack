# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDatetimeLocale(PerlPackage):
    """DateTime::Locale - Localization support for DateTime.pm"""

    homepage = "https://metacpan.org/pod/DateTime::Locale"
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/DateTime-Locale-1.40.tar.gz"

    version("1.40", sha256="7490b4194b5d23a4e144976dedb3bdbcc6d3364b5d139cc922a86d41fdb87afb")

    depends_on("perl-file-sharedir-install", type=("build", "run"))
