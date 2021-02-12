# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPycurl(PythonPackage):
    """PycURL is a Python interface to libcurl. PycURL can be used to fetch
    objects identified by a URL from a Python program."""

    homepage = "http://pycurl.io/"
    pypi = "pycurl/pycurl-7.43.0.tar.gz"

    version('7.43.0.6', sha256='8301518689daefa53726b59ded6b48f33751c383cf987b0ccfbbc4ed40281325')
    version('7.43.0.5', sha256='ec7dd291545842295b7b56c12c90ffad2976cc7070c98d7b1517b7b6cd5994b3')
    version('7.43.0.4', sha256='bdc308ff2a16ede41921cb0d88f51bd6cb5208c6478be9db579789e2e4db2528')
    version('7.43.0.3', sha256='6f08330c5cf79fa8ef68b9912b9901db7ffd34b63e225dce74db56bb21deda8e')
    version('7.43.0.2', sha256='0f0cdfc7a92d4f2a5c44226162434e34f7d6967d3af416a6f1448649c09a25a4')
    version('7.43.0.1', sha256='43231bf2bafde923a6d9bb79e2407342a5f3382c1ef0a3b2e491c6a4e50b91aa')
    version('7.43.0', sha256='aa975c19b79b6aa6c0518c0cc2ae33528900478f0b500531dbcdbf05beec584c')

    depends_on('python@2.6:')
    depends_on('curl@7.19.0:')
