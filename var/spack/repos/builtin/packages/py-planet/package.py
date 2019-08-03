# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT
#
# ----------------------------------------------------------------------------
#
#     spack install py-planet
#
# You can edit this file again by typing:
#
#     spack edit py-planet
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyPlanet(PythonPackage):
    """Python client library and CLI for Planet's public API"""

    # Add a proper url for your package's homepage here.
    homepage = "https://github.com/planetlabs/planet-client-python"
    url      = "https://github.com/planetlabs/planet-client-python/archive/1.3.0.tar.gz"
    
    version('1.3.0', 'd7ed6dcf77a5aa83f77dca129d126331')

    # Add dependencies if required.
    depends_on('py-setuptools', type='build')
    depends_on('py-click')
    depends_on('py-requests')

