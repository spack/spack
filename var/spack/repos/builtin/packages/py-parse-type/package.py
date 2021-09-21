# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyParseType(PythonPackage):
    """parse_type extends the parse module (opposite of string.format()).
    """

    homepage = "https://github.com/jenisys/parse_type"
    url = "https://pypi.io/packages/source/p/parse-type/parse_type-0.5.2.tar.gz"

    version('0.5.2', sha256='7f690b18d35048c15438d6d0571f9045cffbec5907e0b1ccf006f889e3a38c0b')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.6:2.999,3.2:', type=('build', 'run'))
    depends_on('py-parse@1.8.4:', type=('build', 'run'))
    depends_on('py-enum34', when='python@2.6:3.4', type=('build', 'run'))
    depends_on('py-six@1.11:', type=('build', 'run'))
    depends_on('py-ordereddict', when='python@2.6:2.7', type=('build', 'run'))
