# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTyping(PythonPackage):
    """This is a backport of the standard library typing module to Python
    versions older than 3.6."""

    homepage = "https://docs.python.org/3/library/typing.html"
    url      = "https://pypi.io/packages/source/t/typing/typing-3.6.1.tar.gz"

    import_modules = ['typing']

    version('3.6.4', sha256='d400a9344254803a2368533e4533a4200d21eb7b6b729c173bc38201a74db3f2')
    version('3.6.1', sha256='c36dec260238e7464213dcd50d4b5ef63a507972f5780652e835d0228d0edace')

    # You need Python 2.7 or 3.3+ to install the typing package
    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
