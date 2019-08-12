# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHttpbin(PythonPackage):
    """HTTP Request and Response Service"""

    homepage = "https://github.com/Runscope/httpbin"
    url = "https://pypi.io/packages/source/h/httpbin/httpbin-0.5.0.tar.gz"

    version('0.5.0', '923793df99156caa484975ade96ee115')

    depends_on('py-setuptools',         type='build')
    depends_on('py-decorator@3.4.0:',   type=('build', 'run'))
    depends_on('py-flask@0.10.1:',      type=('build', 'run'))
    depends_on('py-itsdangerous@0.24:', type=('build', 'run'))
    depends_on('py-markupsafe@0.23:',   type=('build', 'run'))
    depends_on('py-six@1.6.1:',         type=('build', 'run'))
