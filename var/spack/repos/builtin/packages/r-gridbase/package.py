# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGridbase(RPackage):
    """Integration of base and grid graphics."""

    homepage = "https://cloud.r-project.org/package=gridBase"
    url      = "https://cloud.r-project.org/src/contrib/gridBase_0.4-7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gridBase"

    version('0.4-7', '6d5064a85f5c966a92ee468ae44c5f1f')

    depends_on('r@2.3.0:', type=('build', 'run'))
