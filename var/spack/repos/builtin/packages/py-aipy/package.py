# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAipy(PythonPackage):
    """AIPY (Astronomical Interferometry in PYthon)
    collects together tools for radio astronomical interferometry."""

    homepage = "https://github.com/HERA-Team/aipy"
    url      = "https://github.com/HERA-Team/aipy/archive/v3.0.1.tar.gz"

    version('3.0.1', sha256='27b61f565ce135812fef4f9fed5b9ec88f6aae635e326b21613ce675f876f16c')

    depends_on('py-setuptools', type='build')
    depends_on('py-basemap', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-astropy', type=('build', 'run'))
    depends_on('py-matplotlib@:2.9.9', type=('build', 'run'), when='^python@2.7:2.9')
    depends_on('py-matplotlib', type=('build', 'run'), when='^python@3.4:')
    depends_on('py-ephem@3.7.3.2:', type=('build', 'run'))
