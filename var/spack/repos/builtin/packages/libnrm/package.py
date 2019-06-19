# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libnrm(AutotoolsPackage):
    """Libnrm, the application instrumentation library for the Node
    Resource Manager(NRM)."""

    homepage = "https://xgitlab.cels.anl.gov/argo/libnrm"
    url = "https://www.mcs.anl.gov/research/projects/argo/downloads/libnrm-0.1.0.tar.gz"
    version('0.1.0', '9261a55e58fd6350d9382dd09001cfd4')

    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    depends_on('zeromq')
    depends_on('mpich')
