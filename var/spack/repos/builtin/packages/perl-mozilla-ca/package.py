# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMozillaCa(PerlPackage):
    """Mozilla's CA cert bundle in PEM format"""

    homepage = "https://metacpan.org/pod/Mozilla::CA"
    url = "https://cpan.metacpan.org/authors/id/A/AB/ABH/Mozilla-CA-20160104.tar.gz"

    version("20211001", sha256="122c8900000a9d388aa8e44f911cab6c118fe8497417917a84a8ec183971b449")
    version("20200520", sha256="b3ca0002310bf24a16c0d5920bdea97a2f46e77e7be3e7377e850d033387c726")
    version("20180117", sha256="f2cc9fbe119f756313f321e0d9f1fac0859f8f154ac9d75b1a264c1afdf4e406")
    version("20160104", sha256="27a7069a243162b65ada4194ff9d21b6ebc304af723eb5d3972fb74c11b03f2a")

    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
