# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPpft(PythonPackage):
    """Distributed and parallel python """

    homepage = "https://github.com/uqfoundation/ppft"
    url      = "https://pypi.io/packages/source/p/ppft/ppft-1.6.4.7.1.zip"

    version('1.6.4.7.1',  '2b196a03bfbc102773f849c6b21e617b')
    version('1.6.4.6',   'e533432bfba4b5a523a07d58011df209')
    version('1.6.4.5',   'd2b1f9f07eae22b31bfe90f544dd3044')

    depends_on('python@2.5:2.8,3.1:')

    depends_on('py-setuptools@0.6:', type='build')
    depends_on('py-six@1.7.3:', type=('build', 'run'))
    depends_on('py-dill@0.2.6:', type=('build', 'run'))
