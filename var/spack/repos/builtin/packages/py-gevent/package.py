# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGevent(PythonPackage):
    """gevent is a coroutine-based Python networking library."""

    homepage = "http://www.gevent.org"
    url      = "https://pypi.io/packages/source/g/gevent/gevent-1.3a2.tar.gz"

    version('1.3a2', '8d73a7b0ceb0ca791b22e6f7b7061e9e')

    depends_on('py-setuptools@24.2:',   type='build')
    depends_on('py-cython@0.27:',       type='build')
    depends_on('py-cffi@1.4.0:',        type=('build', 'run'))
    depends_on('py-greenlet@0.4.13:',   type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:',   type=('build', 'run'))
