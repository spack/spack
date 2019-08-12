# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Units(AutotoolsPackage):
    """GNU units converts between different systems of units"""

    homepage = "https://www.gnu.org/software/units/"
    url      = "https://ftpmirror.gnu.org/units/units-2.13.tar.gz"

    version('2.13', '5cbf2a6af76e94ba0ac55fc8d99d5a3e')

    depends_on('python', type=('build', 'run'))
