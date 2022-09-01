# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class PerlMathBigrat(PerlPackage):
    """Math::BigRat - arbitrary size rational number math package"""

    homepage = "https://metacpan.org/pod/Math::BigRat"
    url = "https://cpan.metacpan.org/authors/id/P/PJ/PJACKLAM/Math-BigRat-0.2624.tar.gz"

    version("0.260805", sha256="9e41be24272e262fadc1921c7f51ff218384c92e5628cb53bf62b3026710fd41")

    depends_on("perl@5.6.0:", type=("build", "run"))
    depends_on("perl-module-install", type=("build"))

    def fetch_remote_versions(self, concurrency=128):
        """Handle unfortunate versions."""
        remote_versions = super(PerlMathBigrat, self).fetch_remote_versions(concurrency)
        if not remote_versions:
            return remote_versions
        result = {}
        for version, url in remote_versions.items():
            ver_match = re.match(r"^(\d+)\.260\.(\d)0(\d)((?:-TRIAL|_\d+)?)$", version.string)
            if ver_match:
                set_ver = ver("{0}.26.0{1}.0{2}{3}".format(*ver_match.group(1, 2, 3, 4)))
            else:
                set_ver = version
            result[set_ver] = url
        return result
