# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCython(PythonPackage):
    """The Cython compiler for writing C extensions for the Python language."""

    homepage = "https://pypi.python.org/pypi/cython"
    url      = "https://pypi.io/packages/source/c/cython/Cython-0.29.7.tar.gz"

    import_modules = [
        'cython', 'Cython', 'Cython.Build', 'Cython.Compiler',
        'Cython.Runtime', 'Cython.Distutils', 'Cython.Debugger',
        'Cython.Debugger.Tests', 'Cython.Plex', 'Cython.Tests',
        'Cython.Build.Tests', 'Cython.Compiler.Tests', 'Cython.Utility',
        'Cython.Tempita', 'pyximport',
    ]

    version('0.29.7', sha256='55d081162191b7c11c7bfcb7c68e913827dfd5de6ecdbab1b99dab190586c1e8')
    version('0.29.5', sha256='9d5290d749099a8e446422adfb0aa2142c711284800fb1eb70f595101e32cbf1')
    version('0.29',   sha256='94916d1ede67682638d3cc0feb10648ff14dc51fb7a7f147f4fedce78eaaea97')
    version('0.28.6', '3c3fb47806a4476f8e9429943439cc60')
    version('0.28.3', '586f0eb70ba1fcc34334e9e10c5e68c0')
    version('0.28.1', 'c549effadb52d90bdcb1affc1e5dbb97')
    version('0.25.2', '642c81285e1bb833b14ab3f439964086')
    version('0.23.5', '66b62989a67c55af016c916da36e7514')
    version('0.23.4', '157df1f69bcec6b56fd97e0f2e057f6e')
    version('0.22',   '1ae25add4ef7b63ee9b4af697300d6b6')
    version('0.21.2', 'd21adb870c75680dc857cd05d41046a4')

    depends_on('python@:2', type=('build', 'run'), when='@:0.22')
    depends_on('py-setuptools', type='build')
    depends_on('gdb@7.2:', type='test')

    @property
    def command(self):
        """Returns the Cython command"""
        return Executable(self.prefix.bin.cython)

    def test(self):
        # Warning: full suite of unit tests takes a very long time
        python('runtests.py', '-j', str(make_jobs))
