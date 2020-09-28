# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyVermin(PythonPackage):
    """Concurrently detect the minimum Python versions needed to run code."""

    homepage = "https://github.com/netromdk/vermin"
    url      = "https://github.com/netromdk/vermin/archive/v0.10.5.tar.gz"

    maintainers = ['netromdk']
    import_modules = ['vermin']

    version('0.10.5', sha256='00601356e8e10688c52248ce0acc55d5b45417b462d5aa6887a6b073f0d33e0b')
    version('0.10.4', sha256='bd765b84679fb3756b26f462d2aab4af3183fb65862520afc1517f6b39dea8bf')
    version('0.10.0', sha256='3458a4d084bba5c95fd7208888aaf0e324a07ee092786ee4e5529f539ab4951f')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))

    def test(self):
        make('test')
