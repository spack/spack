# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDistributed(PythonPackage):
    """Distributed scheduler for Dask"""

    homepage = "https://distributed.dask.org/"
    pypi = "distributed/distributed-2.10.0.tar.gz"

    # 'distributed.dashboard.components' requires 'bokeh', but 'bokeh' is not listed as
    # a dependency. Leave out of 'import_modules' list to avoid unnecessary dependency.
    import_modules = [
        'distributed', 'distributed.deploy', 'distributed.comm',
        'distributed.comm.tests', 'distributed.protocol', 'distributed.cli',
        'distributed.dashboard', 'distributed.http', 'distributed.http.tests',
        'distributed.http.scheduler', 'distributed.http.scheduler.prometheus',
        'distributed.http.worker', 'distributed.diagnostics'
    ]

    version('2021.6.2', sha256='d7d112a86ab049dcefa3b21fd1baea4212a2c03d22c24bd55ad38d21a7f5d148')
    version('2021.6.1', sha256='67bf61fd6022a397625f69b20a1c7c1cf0167b6441e008f0ed86dc8785d46057')
    version('2021.6.0', sha256='0ad3db5d2618fc29291b02e8ebc7a1ff6cfce5013455143c3e1bce438b2b5a48')
    version('2021.5.1', sha256='f3b3d2091cf899658ae01f4fbc443ba86520ccdce8be64ce6087fcf48dbf50df')
    version('2021.5.0', sha256='4da09db7972120db0a8e7fc2b2f91bb4d952ce21b185ccc1356603613060a0b3')
    version('2021.4.1', sha256='4c1b189ec5aeaf770c473f730f4a3660dc655601abd22899e8a0662303662168')
    version('2021.4.0', sha256='7af2b77819a162d8f5973fb015be5a1641f47901d2e254409dafa2d7fcc3fce6')
    version('2021.3.1', sha256='1f36247744e375d5d11c44a3b18891dfde42832132de3cb94efcb06b6da31f68')
    version('2021.3.0', sha256='427fe7e047bbad7413c65d57e56fa4d6b1cf921fd206a3d2caab94bf9153c3db')
    version('2020.12.0', sha256='2a0b6acc921cd4e0143a7c4383cdcbed7defbc4bd9dc3aab0c7f1c45f14f80e1')
    version('2.10.0', sha256='2f8cca741a20f776929cbad3545f2df64cf60207fb21f774ef24aad6f6589e8b')
    version('1.28.1', sha256='3bd83f8b7eb5938af5f2be91ccff8984630713f36f8f66097e531a63f141c48a')

    depends_on('python@2.7:2.8,3.5:', when='@:1', type=('build', 'run'))
    depends_on('python@3.6:', when='@2:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@6.6:', type=('build', 'run'))
    depends_on('py-cloudpickle@0.2.2:', type=('build', 'run'), when='@:2.16.0')
    depends_on('py-cloudpickle@1.3.0:', type=('build', 'run'), when='@2.17.0:2.20.0')
    depends_on('py-cloudpickle@1.5.0:', type=('build', 'run'), when='@2.21.0:')
    depends_on('py-contextvars', type=('build', 'run'), when='@2020: ^python@:3.6')
    depends_on('py-msgpack', type=('build', 'run'), when='@:2.10.0')
    depends_on('py-msgpack@0.6.0:', type=('build', 'run'), when='@2.11.0:')
    depends_on('py-psutil@5.0:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'), when='@:1')
    depends_on('py-sortedcontainers@:1.999,2.0.2:', type=('build', 'run'))
    depends_on('py-tblib', type=('build', 'run'), when='@:2.10.0')
    depends_on('py-tblib@1.6.0:', type=('build', 'run'), when='@2.11.0:')
    depends_on('py-toolz@0.7.4:', type=('build', 'run'), when='@:2.12.0')
    depends_on('py-toolz@0.8.2:', type=('build', 'run'), when='@2.13.0:')
    depends_on('py-tornado@5:', type=('build', 'run'), when='^python@:3.7')
    depends_on('py-tornado@6.0.3:', type=('build', 'run'), when='^python@3.8:')
    depends_on('py-zict@0.1.3:', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-futures', when='@:1 ^python@2.7:2.8', type=('build', 'run'))
    depends_on('py-singledispatch', when='@:1 ^python@2.7:2.8', type=('build', 'run'))

    def patch(self):
        filter_file('^dask .*', '', 'requirements.txt')
