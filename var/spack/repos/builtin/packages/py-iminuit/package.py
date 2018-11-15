# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIminuit(PythonPackage):
    """Interactive IPython-Friendly Minimizer based on SEAL Minuit2."""

    homepage = "https://pypi.python.org/pypi/iminuit"
    url      = "https://pypi.io/packages/source/i/iminuit/iminuit-1.2.tar.gz"

    version('1.2', '4701ec472cae42015e26251703e6e984')

    # Required dependencies
    depends_on('py-setuptools', type='build')

    # Optional dependencies
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-cython', type='build')
