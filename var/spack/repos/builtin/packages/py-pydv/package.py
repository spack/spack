# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------

from spack import *


class PyPydv(PythonPackage):
    """PDV is a 1D graphics and data analysis tool, heavily based on the
    ULTRA plotting tool"""

    homepage = "https://github.com/griffin28/PyDV"
    url      = "https://github.com/griffin28/PyDV.git"

    version('2.4.2', git=url, tag='pydv-2.4.2')

    depends_on('py-backports-functools-lru-cache')
    depends_on('py-cycler')
    depends_on('py-dateutil')
    depends_on('py-matplotlib')
    depends_on('py-pyside')
    depends_on('py-scipy')
