# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCfUnits(PythonPackage):
    """Units of measure as required by the Climate and Forecast (CF) metadata conventions."""

    homepage = "https://scitools.org.uk"
    url      = "https://pypi.io/packages/source/c/cf-units/cf-units-2.1.1.tar.gz"
    git      = "https://github.com/SciTools/cf-units.git"

    version('2.1.1', extension='tar.gz', sha256='fa0ef8efd84546e61088aa23e76ebbaf7043167dc3a7f35f34549c234b543530')
    version('master', branch='master')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-six',        type=('build', 'run'))
    depends_on('py-cftime', type=('build', 'run'))
    depends_on('py-cython', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-antlr4-python3-runtime', type=('build', 'run'))
    depends_on('udunits2')

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
