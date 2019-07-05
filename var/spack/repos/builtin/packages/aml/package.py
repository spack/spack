# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Aml(AutotoolsPackage):
    """AML: Building Blocks for Memory Management."""

    homepage = "https://xgitlab.cels.anl.gov/argo/aml"
    url = "https://www.mcs.anl.gov/research/projects/argo/downloads/aml-0.1.0.tar.gz"
    version('0.1.0', 'f704397fe568bcb334ee0cbc4f9e066e')

    depends_on('numactl')

    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
