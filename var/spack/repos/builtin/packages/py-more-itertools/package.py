# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMoreItertools(PythonPackage):
    """Additions to the standard Python itertools package."""

    homepage = "https://github.com/erikrose/more-itertools"
    url      = "https://pypi.io/packages/source/m/more-itertools/more-itertools-4.3.0.tar.gz"

    import_modules = ['more_itertools', 'more_itertools.tests']

    version('4.3.0', '42157ef9b677bdf6d3609ed6eadcbd4a')
    version('4.1.0', '246f46686d95879fbad37855c115dc52')
    version('2.2',   'b8d328a33f966bf40bb829bcf8da35ce')

    depends_on('py-setuptools', type='build')
    depends_on('py-six@1.0.0:1.999', type=('build', 'run'))
