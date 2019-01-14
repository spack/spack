# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPymorph(PythonPackage):
    """This image morphology toolbox implements the basic binary and greyscale
       morphology operations, working with numpy arrays representing images"""

    homepage = "http://www.example.com"
    url = "https://pypi.org/packages/source/p/pymorph/pymorph-0.96.tar.gz"

    version('0.96', sha256='5dd648e4cb4c3495ee6031bc8020ed8216f3d6cb8c0dcd0427b215b75d7d29ad')

    depends_on('py-setuptools', type='build')
