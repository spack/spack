# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyXarray(PythonPackage):
    """N-D labeled arrays and datasets in Python"""

    homepage = "https://github.com/pydata/xarray"
    url      = "https://pypi.io/packages/source/x/xarray/xarray-0.9.1.tar.gz"

    version('0.14.0', sha256='a8b93e1b0af27fa7de199a2d36933f1f5acc9854783646b0f1b37fed9b4da091')
    version('0.13.0', sha256='80e5746ffdebb96b997dba0430ff02d98028ef3828e6db6106cbbd6d62e32825')
    version('0.12.0', sha256='856fd062c55208a248ac3784cac8d3524b355585387043efc92a4188eede57f3')
    version('0.11.0', sha256='636964baccfca0e5d69220ac4ecb948d561addc76f47704064dcbe399e03a818')
    version('0.9.1', sha256='89772ed0e23f0e71c3fb8323746374999ecbe79c113e3fadc7ae6374e6dc0525')

    depends_on('py-setuptools',      type='build')
    depends_on('py-pandas@0.15.0:',  type=('build', 'run'))
    depends_on('py-numpy@1.7:',      type=('build', 'run'))
