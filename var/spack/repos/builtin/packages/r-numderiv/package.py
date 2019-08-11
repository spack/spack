# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RNumderiv(RPackage):
    """Methods for calculating (usually) accurate numerical first and
    second order derivatives."""

    homepage = "https://cloud.r-project.org/package=numDeriv"
    url      = "https://cloud.r-project.org/src/contrib/numDeriv_2016.8-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/numDeriv"

    version('2016.8-1.1', sha256='d8c4d19ff9aeb31b0c628bd4a16378e51c1c9a3813b525469a31fe89af00b345')
    version('2016.8-1', '30e486298d5126d86560095be8e8aac1')

    depends_on('r@2.11.1:', type=('build', 'run'))
