# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVscBase(PythonPackage):
    """Common Python libraries tools created by HPC-UGent"""

    homepage = 'https://github.com/hpcugent/vsc-base/'
    url      = 'https://pypi.io/packages/source/v/vsc-base/vsc-base-2.5.8.tar.gz'

    version('2.5.8', '57f3f49eab7aa15a96be76e6c89a72d8')

    depends_on('py-setuptools', type=('build', 'run'))
