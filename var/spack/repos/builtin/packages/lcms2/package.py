# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lcms2(AutotoolsPackage):
    """Little cms color engine"""

    homepage = "https://sourceforge.net/projects/lcms/"
    url = "https://sourceforge.net/projects/lcms/files/lcms/2.13/lcms2-2.13.1.tar.gz/download"

    maintainers = ["JBlaschke"]

    version("2.13.1", sha256="d473e796e7b27c5af01bd6d1552d42b45b43457e7182ce9903f38bb748203b88")

    def configure_args(self):
        args = []
        return args
