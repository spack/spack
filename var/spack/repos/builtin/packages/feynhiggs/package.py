# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Feynhiggs(AutotoolsPackage):
    """FeynHiggs is a Fortran code for the (diagrammatic/EFT/hybrid) calculation
    of the masses, mixings and much more of the Higgs bosons in the MSSM
    with real/complex parameters at the highest level of accuracy."""

    homepage = "https://wwwth.mpp.mpg.de/members/heinemey/feynhiggs/cFeynHiggs.html"
    url = "https://wwwth.mpp.mpg.de/members/heinemey/feynhiggs/newversion/FeynHiggs-2.18.1.tar.gz"

    maintainers = ["vvolkl"]
    tags = ["hep"]

    version("2.18.1", sha256="a9cdc4e2759f96fb9bd981b7be1ba8df070fb20c46d5b95e0c9700fccafe5ee6")

    def configure_args(self):
        return ["FFLAGS=-fPIC", "CFLAGS=-fPIC"]
