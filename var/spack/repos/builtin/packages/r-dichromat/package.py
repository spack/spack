# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDichromat(RPackage):
    """Collapse red-green or green-blue distinctions to simulate the effects of
    different types of color-blindness."""

    homepage = "https://cloud.r-project.org/package=dichromat"
    url      = "https://cloud.r-project.org/src/contrib/dichromat_2.0-0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/dichromat"

    version('2.0-0', '84e194ac95a69763d740947a7ee346a6')

    depends_on('r@2.10:', type=('build', 'run'))
