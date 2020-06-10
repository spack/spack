# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OpenclIcdLoader(CMakePackage):
    """
    OpenCL defines an Installable Client Driver (ICD) mechanism to allow developers to build applications against an Installable Client Driver loader (ICD loader) rather than linking their applications against a specific OpenCL implementation. The ICD Loader is responsible for:

    Exporting OpenCL API entry points
    Enumerating OpenCL implementations
    Forwarding OpenCL API calls to the correct implementation

    """

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "https://github.com/KhronosGroup/OpenCL-ICD-Loader/archive/v2020.03.13.tar.gz"

    version('2020.03.13', sha256='cafcfa9e48d523d0534e6879af2badd7006b3c646eab5f05314de72a2c542816')

    depends_on('opencl')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args
