# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyClustershell(PythonPackage):
    """Scalable cluster administration Python framework - Manage node sets
    node groups and execute commands on cluster nodes in parallel.
    """

    homepage = "http://cea-hpc.github.io/clustershell/"
    url      = "https://github.com/cea-hpc/clustershell/archive/v1.8.tar.gz"

    version('1.8.3', sha256='5659adf458de56a4926ed3da0522936bff38ddcbabaa177292fceb310e7cace1')
    version('1.8.2', sha256='e5703ce3f6d2138c8456cbb653974277f800f8280787715db065cccb0b7ae2bf')
    version('1.8.1', sha256='0c3da87108de8b735f40b5905b8dcd8084a234849aee2a8b8d2e20b99b57100c')
    version('1.8', sha256='ad5a13e2d107b4095229810c35365e22ea94dfd2baf4fdcfcc68ce58ee37cee3')

    depends_on('py-setuptools', type='build')
    depends_on('py-pyyaml')
