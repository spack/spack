# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFenicsUfl(PythonPackage):
    """The Unified Form Language (UFL) is a domain specific language for
    declaration of finite element discretizations of variational forms.
    It defines a flexible interface for choosing finite element spaces
    and defining expressions for weak forms in a notation close to
    mathematical notation.
    """

    homepage = "https://fenicsproject.org/"
    git      = "https://bitbucket.org/fenics-project/ufl.git"

    def url_for_version(self, version):
        url = "https://bitbucket.org/fenics-project/ufl/get"
        if version >= Version('2017.1.0'):
            url += "/{0}.tar.gz".format(version)
        else:
            url += "/ufl-{0}.tar.gz".format(version)
        return url

    version('2018.1.0',       sha256='1717ac7deacae7ac9cf5a9ff419bbab1550308fe6f05a5c8ea7c3ee62eaacae8')
    version('2017.2.0.post0', sha256='5d75adf2c9d15b92573aedfd0a011268830435f6808ad795136567c274382190')
    version('2017.2.0',       sha256='80032ee069923137badd8f5cd345db0aa36e9f3232c720072c4f1dfe8b6cf71c')
    version('2017.1.0.post1', sha256='1f8ff325921a4adb54832407cadb022556d3e8947c4db3674f618cd52d099054')
    version('2017.1.0',       sha256='152b9913656f64184873f40c4b201bd3118ee9e8943127ee22fbe19fe13c9d4e')
    version('2016.2.0',       sha256='1689223696e5fa4534a9db7a34bc33782fae9f5ae00d67d834d2ef16be6b1300')
    version('2016.1.0',       sha256='0321918a60809ed168081fd4345343fbb57ee6da333625629b9dc9230ab5c8a3')
    version('1.6.0',          sha256='4296997a6a940fe02d6543c3ff24c55daa03986de95110df5a270622c718c756')
    version('1.5.0',          sha256='846668ba5d869285a50be120cf78e05582ba1872d38989d6fef4e3680f79eb32')
    version('1.4.0',          sha256='92812a5884226ed8b87649edf53b781425dfd94920fd4ec13c341f0451785e76')
    version('1.3.0',          sha256='f99139962a901d185a66fd1f3fbbb363dff9319272b88b1d04e12aa2a6a5569d')
    version('1.2.1',          sha256='3ac4c6e12666f0b31403eb1213e23f552b6dc618a3f5536577b7b41d1e351e27')

    depends_on('python@3:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
