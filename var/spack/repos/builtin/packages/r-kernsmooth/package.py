# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RKernsmooth(RPackage):
    """Functions for kernel smoothing (and density estimation)."""

    homepage = "https://cloud.r-project.org/package=KernSmooth"
    url      = "https://cloud.r-project.org/src/contrib/KernSmooth_2.23-15.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/KernSmooth"

    version('2.23-15', '746cdf26dec72004cf19978e87dcc982')

    depends_on('r@2.5.0:', type=('build', 'run'))
