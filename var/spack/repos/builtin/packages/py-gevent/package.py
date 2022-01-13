# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGevent(PythonPackage):
    """gevent is a coroutine-based Python networking library."""

    homepage = "https://www.gevent.org"
    pypi = "gevent/gevent-1.3a2.tar.gz"

    version('1.5.0', sha256='b2814258e3b3fb32786bb73af271ad31f51e1ac01f33b37426b66cb8491b4c29')
    version('1.3a2', sha256='f7ab82697111ea233c7beeadf5240f669dfad9c4bbc89a3ec80a49e2c48a65bd')

    depends_on('py-setuptools@24.2:',   type='build', when='@:1.4')
    depends_on('py-setuptools@40.8:', type='build', when='@1.5:')
    depends_on('py-cython@0.27:',       type='build', when='@:1.4')
    depends_on('py-cython@0.29.14:',    type='build', when='@1.5:')
    depends_on('py-cffi@1.4:',        type=('build', 'run'), when='@:1.4')
    depends_on('py-cffi@1.12.2:',        type=('build', 'run'), when='@1.5:')
    depends_on('py-greenlet@0.4.13:',   type=('build', 'run'), when='@:1.4')
    depends_on('py-greenlet@0.4.14:',   type=('build', 'run'), when='@1.5:')
    depends_on('python@2.7:2.8,3.4:',   type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:',   type=('build', 'run'), when='@1.5:')
