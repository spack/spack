# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyPyzmq(PythonPackage):
    """PyZMQ: Python bindings for zeromq."""
    homepage = "https://github.com/zeromq/pyzmq"
    pypi     = "pyzmq/pyzmq-22.3.0.tar.gz"

    import_modules = [
        'zmq', 'zmq.green', 'zmq.green.eventloop', 'zmq.sugar', 'zmq.auth',
        'zmq.auth.asyncio', 'zmq.utils', 'zmq.backend', 'zmq.backend.cffi',
        'zmq.backend.cython', 'zmq.ssh', 'zmq.eventloop',
        'zmq.eventloop.minitornado', 'zmq.eventloop.minitornado.platform',
        'zmq.log', 'zmq.asyncio', 'zmq.devices'
    ]

    version('22.3.0', sha256='8eddc033e716f8c91c6a2112f0a8ebc5e00532b4a6ae1eb0ccc48e027f9c671c')
    version('18.1.0', sha256='93f44739db69234c013a16990e43db1aa0af3cf5a4b8b377d028ff24515fbeb3')
    version('18.0.1', sha256='8b319805f6f7c907b101c864c3ca6cefc9db8ce0791356f180b1b644c7347e4c')
    version('17.1.2', sha256='a72b82ac1910f2cf61a49139f4974f994984475f771b0faa730839607eeedddf')
    version('16.0.2', sha256='0322543fff5ab6f87d11a8a099c4c07dd8a1719040084b6ce9162bcdf5c45c9d')
    version('14.7.0', sha256='77994f80360488e7153e64e5959dc5471531d1648e3a4bff14a714d074a38cc2')

    depends_on('python@3.6:', type=('build', 'run'), when='@22:')
    depends_on('python@2.7,3.3:', type=('build', 'run'), when='@18.1')
    # Python 3.9 build issues
    depends_on('python@2.7,3.3:3.8', type=('build', 'run'), when='@16:18.0')
    depends_on('python@2.6:2.7,3.2:3.8', type=('build', 'run'), when='@:14')
    depends_on('py-cython@0.16:', type='build')
    depends_on('py-cython@0.20:', type='build', when='@18:')
    depends_on('py-cython@0.29:', type='build', when='@22.3.0:')
    depends_on('py-gevent', type=('build', 'run'))
    depends_on('libzmq', type=('build', 'link'))
    depends_on('libzmq@3.2:', type=('build', 'link'), when='@22.3.0:')
    depends_on('py-setuptools', type='build', when='@22.3.0:')
    # Only when python is provided by 'pypy'
    depends_on('py-py', type=('build', 'run'), when='@:22')
    depends_on('py-cffi', type=('build', 'run'), when='@:22')

    @run_before('install')
    def setup(self):
        """Create config file listing dependency information."""

        with open('setup.cfg', 'w') as config:
            config.write("""\
[global]
zmq_prefix = {0}

[build_ext]
library_dirs = {1}
include_dirs = {2}
""".format(
                self.spec['libzmq'].prefix,
                self.spec['libzmq'].libs.directories[0],
                self.spec['libzmq'].headers.directories[0],
            ))

    def setup_build_environment(self, env):
        # Needed for `spack install --test=root py-pyzmq`
        # Fixes import failure for zmq.backend.cffi
        # https://github.com/zeromq/pyzmq/issues/395#issuecomment-22041019
        env.prepend_path(
            'C_INCLUDE_PATH', self.spec['libzmq'].headers.directories[0])
        env.prepend_path(
            'LIBRARY_PATH', self.spec['libzmq'].libs.directories[0])

    # Needed for `spack test run py-pyzmq`
    setup_run_environment = setup_build_environment
