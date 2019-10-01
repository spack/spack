# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMinqa(RPackage):
    """Derivative-free optimization by quadratic approximation based on an
    interface to Fortran implementations by M. J. D. Powell."""

    homepage = "http://optimizer.r-forge.r-project.org/"
    url      = "https://cloud.r-project.org/src/contrib/minqa_1.2.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/minqa"

    version('1.2.4', 'bcaae4fdba60a33528f2116e2fd51105')

    depends_on('r-rcpp@0.9.10:', type=('build', 'run'))
    depends_on('gmake', type='build')
