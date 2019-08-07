# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonDateutil(PythonPackage):
    """Extensions to the standard Python datetime module."""

    homepage = "https://dateutil.readthedocs.io/"
    url      = "https://pypi.io/packages/source/p/python-dateutil/python-dateutil-2.8.0.tar.gz"

    import_modules = [
        'dateutil', 'dateutil.zoneinfo', 'dateutil.parser', 'dateutil.tz'
    ]

    version('2.8.0', sha256='c89805f6f4d64db21ed966fda138f8a5ed7a4fdbc1a8ee329ce1b74e3c74da9e')
    version('2.7.5', sha256='88f9287c0174266bb0d8cedd395cfba9c58e87e5ad86b2ce58859bc11be3cf02')
    version('2.5.2', 'eafe168e8f404bf384514f5116eedbb6')
    version('2.4.2', '4ef68e1c485b09e9f034e10473e5add2')
    version('2.4.0', '75714163bb96bedd07685cdb2071b8bc')
    version('2.2',   'c1f654d0ff7e33999380a8ba9783fd5c')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools@24.3:', type='build')
    depends_on('py-setuptools-scm', type='build', when='@2.7.0:')
    depends_on('py-six@1.5:', type=('build', 'run'))
    # depends_on('py-pytest', type='test')
    # depends_on('py-hypothesis', type='test')
    # depends_on('py-freezegun', type='test')

    def test(self):
        # Tests require freezegun, which depends on python-dateutil,
        # creating circular dependency
        # pytest = which('pytest')
        # pytest()
        pass
