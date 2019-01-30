# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyMacs2(PythonPackage):
    """MACS2 Model-based Analysis of ChIP-Seq"""

    homepage = "https://github.com/taoliu/MACS"
    url      = "https://pypi.io/packages/source/M/MACS2/MACS2-2.1.1.20160309.tar.gz"

    version('2.1.1.20160309', '2008ba838f83f34f8e0fddefe2a3a0159f4a740707c68058f815b31ddad53d26')

    depends_on('python@2.7:2.8')

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-macs2 requires py-setuptools during runtime as well.
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-numpy@1.6:', type=('build', 'run'))
