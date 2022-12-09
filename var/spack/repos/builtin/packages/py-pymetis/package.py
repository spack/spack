# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)



class PyPymetis(PythonPackage):
    """
    A Graph Partitioning Package
    """

    homepage = "http://mathema.tician.de/software/pymetis"
    url      = "https://pypi.io/packages/source/P/PyMetis/PyMetis-2020.1.tar.gz"
    git      = "https://github.com/inducer/pymetis.git"

    maintainers = ['jayashripawar']

    version('main', branch='main')
    version('2020.1', sha256='d13e262e8ee20963e898c2c473b69502661a8727904a49b33689fb4d42248555')
    version('2019.1.1', sha256='b611c9b937c82788c4663cde1f5c3b28cfe353aab41806fbc1d1a173c73e20e5')
    version('2019.1', sha256='47b78a6cef7e3434a1001e232610d9bfe589d9d988cb24031429057d4bcf8fdc')
    version('2018.1', sha256='9b0242ecbde0970cd3fad78d96bea93fe9b46064932c0736c130d0d36c2283ca')
    version('2016.2', sha256='ebf68b865ed274f5c6db5ccfdf2fbec2123bf72171f3f0b54213fec4fa3b502a')
    version('2016.1', sha256='1d61a59c1c19da9325e6088c9a51aad0892f2122ff1ece7a0884f1abd7fa9a68')
    version('2014.1', sha256='547fbb6f1e281aaad48e72f61cd896d5a1944cae423d710e2aa3ab5853efb513')
    version('2011.1.1', sha256='c8077dc0077179343bea8e80cd4f98ab4f3f97f078bf7336f0d4a60e5e167bac')
    version('2011.1', sha256='a7ee72923e919d082babda4a613e07e063be78c05fdf23d30ce2608eb09aaf41')
    version('0.92', sha256='894b01185eb452262083fc8b780e4a06b4d7be37574fe1e5b97af9466a4d7e15')
    version('0.91', sha256='11df0499142b2d4192922bd27938c1217b5e417613afc790af988e61cb8560dd')

    depends_on('python@3.6:', type=('build', 'link', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pybind11', type=('build', 'run'))
    depends_on('py-meshpy', type=('build', 'run'))
    depends_on('py-pytest', type='test')

    conflicts('%gcc@:4.7', msg='GCC 4.8+ required')
