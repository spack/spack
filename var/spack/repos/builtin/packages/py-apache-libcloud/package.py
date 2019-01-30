# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyApacheLibcloud(PythonPackage):
    """Python library for multiple cloud provider APIs"""

    homepage = "http://libcloud.apache.org"
    url      = "https://pypi.io/packages/source/a/apache-libcloud/apache-libcloud-1.2.1.tar.gz"

    version('1.2.1', '912e6fb1f2d13f7d3b58ee982b9f9d1f')

    depends_on('py-setuptools', type='build')
