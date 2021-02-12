# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyperf(PythonPackage):
    """The Python perf module is a toolkit to write, run and
    analyze benchmarks.
    """

    homepage = "https://github.com/vstinner/pyperf"
    url = "https://github.com/vstinner/pyperf/archive/1.5.1.tar.gz"

    version('2.1.0', sha256='4877cbd324d4a7fdd59832229e0b92d0f6c63b6187f5526c5b0207ebd86fa2d5')
    version('2.0.0', sha256='5212d0685246cd555fb72680601a42a741126684df779e3a93f9abf766c018d2')
    version('1.7.1', sha256='151b6c3950d2fb3f161aa79997f7dec0e967b00e435530373c3e7ece240e0bfd')
    version('1.7.0', sha256='67caab39f99f34fd6387dd59e63bb498a941d8e2da3cd389fbfc8d4d6bf5e97e')
    version('1.6.1', sha256='fbe793f6f2e036ab4dcca105b5c5aa34fd331dd881e7a3e158e5e218c63cfc32')
    version('1.6.0', sha256='7af7b9cfd9d26548ab7127f8e51791357ecd78cda46aad5b2d9664a70fc58878')
    version('1.5.1', sha256='9c271862bc2911be8eb01031a4a86cbc3f5bb615971514383802d3dcf46f18ed')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
