# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPycocotools(PythonPackage):
    """Official APIs for the MS-COCO dataset."""

    homepage = "https://github.com/cocodataset/cocoapi"
    pypi     = "pycocotools/pycocotools-2.0.2.tar.gz"

    version('2.0.2', sha256='24717a12799b4471c2e54aa210d642e6cd4028826a1d49fcc2b0e3497e041f1a')

    depends_on('python', type=('build', 'link', 'run'))
    depends_on('py-setuptools@18.0:', type='build')
    depends_on('py-cython@0.27.3:', type='build')
    depends_on('py-numpy', type=('build', 'link', 'run'))
    depends_on('py-matplotlib@2.1.0:', type=('build', 'run'))
