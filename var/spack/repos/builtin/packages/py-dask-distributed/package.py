# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyDaskDistributed(PythonPackage):
    """Dask.distributed is a lightweight library for distributed computing
       in Python."""

    homepage = "https://distributed.dask.org"
    url      = "https://github.com/dask/distributed/archive/2020.12.0.tar.gz"

    version('2020.12.0', sha256='8fb95db799d30ad32d955a70333881fa9f1c076aa75d145cb632013d4e6d9358')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-click@6.6:', type=('build', 'run'))
    depends_on('py-cloudpickle@1.5.0:', type=('build', 'run'))
    depends_on('py-contextvars', type=('build', 'run'), when='^python@:3.6')
    depends_on('py-dask@2020.12.0:', type=('build', 'run'))
    depends_on('py-msgpack@0.6.0:', type=('build', 'run'))
    depends_on('py-psutil@5.0:', type=('build', 'run'))
    depends_on('py-sortedcontainers@:1.999,2.0.2:', type=('build', 'run'))
    depends_on('py-tblib@1.6.0:', type=('build', 'run'))
    depends_on('py-toolz@0.8.2:', type=('build', 'run'))
    depends_on('py-tornado@5:', type=('build', 'run'), when='^python@:3.7')
    depends_on('py-tornado@6.0.3:', type=('build', 'run'), when='^python@3.8:')
    depends_on('py-zict@0.1.3:', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
