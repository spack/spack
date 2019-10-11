# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMoreItertools(PythonPackage):
    """Additions to the standard Python itertools package."""

    homepage = "https://github.com/erikrose/more-itertools"
    url      = "https://pypi.io/packages/source/m/more-itertools/more-itertools-4.3.0.tar.gz"

    import_modules = ['more_itertools', 'more_itertools.tests']

    version('4.3.0', sha256='c476b5d3a34e12d40130bc2f935028b5f636df8f372dc2c1c01dc19681b2039e')
    version('4.1.0', sha256='c9ce7eccdcb901a2c75d326ea134e0886abfbea5f93e91cc95de9507c0816c44')
    version('2.2',   sha256='93e62e05c7ad3da1a233def6731e8285156701e3419a5fe279017c429ec67ce0')

    depends_on('py-setuptools', type='build')
    depends_on('py-six@1.0.0:1.999', type=('build', 'run'))
