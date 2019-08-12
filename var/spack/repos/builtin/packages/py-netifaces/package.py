# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNetifaces(PythonPackage):
    """Portable network interface information"""

    homepage = "https://bitbucket.org/al45tair/netifaces"
    url      = "https://pypi.io/packages/source/n/netifaces/netifaces-0.10.5.tar.gz"

    version('0.10.5', '5b4d1f1310ed279e6df27ef3a9b71519')

    depends_on('py-setuptools', type='build')
