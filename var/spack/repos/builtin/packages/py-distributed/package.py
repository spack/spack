# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDistributed(PythonPackage):
    """Distributed scheduler for Dask"""

    homepage = "https://distributed.dask.org/"
    url      = "https://pypi.io/packages/source/d/distributed/distributed-2.10.0.tar.gz"

    version('2.10.0', '300e5495d0306f472c1aa34a522273e3066b9f50d3eb25cee17cd3b6177eea54')

    depends_on('python@2.7:2.7.999,3.5:')
    depends_on('py-click@6.6:')
    depends_on('py-cloudpickle@0.2.2:')
    depends_on('py-msgpack')
    depends_on('py-psutil@5.0:')
    depends_on('py-six')
    depends_on('py-sortedcontainers')
    conflicts('py-sortedcontainers@2.0.0,2.0.1')
    depends_on('py-tblib')
    depends_on('py-toolz@0.7.4:')
    depends_on('py-tornado@5:')
    depends_on('py-zict@0.1.3:')
    depends_on('py-pyyaml')
    depends_on('py-futures', when='@:2.9.999')
    depends_on('py-singledispatch', when='@:3.3.999')
