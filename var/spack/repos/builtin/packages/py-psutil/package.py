# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPsutil(PythonPackage):
    """psutil is a cross-platform library for retrieving information on
    running processes and system utilization (CPU, memory, disks, network)
    in Python."""

    homepage = "https://pypi.python.org/pypi/psutil"
    url      = "https://pypi.io/packages/source/p/psutil/psutil-5.4.5.tar.gz"

    version('5.5.1', sha256='72cebfaa422b7978a1d3632b65ff734a34c6b34f4578b68a5c204d633756b810')
    version('5.4.5', sha256='ebe293be36bb24b95cdefc5131635496e88b17fabbcf1e4bc9b5c01f5e489cfe')
    version('5.0.1', sha256='9d8b7f8353a2b2eb6eb7271d42ec99d0d264a9338a37be46424d56b4e473b39e')

    depends_on('python@2.6:')
    depends_on('py-setuptools', type='build')
