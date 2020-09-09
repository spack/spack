# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class OpenclHeaders(BundlePackage):
    """Bundled OpenCL (Open Computing Language) header files"""

    homepage = "https://www.khronos.org/registry/OpenCL/"

    version('2.2')

    depends_on('opencl-c-headers')
    depends_on('opencl-clhpp')
