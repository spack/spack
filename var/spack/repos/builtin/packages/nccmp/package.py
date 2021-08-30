# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Nccmp(CMakePackage):
    """Compare NetCDF Files"""
    homepage = "http://nccmp.sourceforge.net/"
    url = "https://gitlab.com/remikz/nccmp/-/archive/1.9.0.1/nccmp-1.9.0.1.tar.gz"

    version('1.9.0.1', sha256='81e9753cf451afe8248d44c841e102349e07cde942b11d1f91b5f85feb622b99')
    version('1.8.9.0', sha256='da5d2b4dcd52aec96e7d96ba4d0e97efebbd40fe9e640535e5ee3d5cd082ae50')
    version('1.8.2.0', sha256='7f5dad4e8670568a71f79d2bcebb08d95b875506d3d5faefafe1a8b3afa14f18')

    depends_on('netcdf-c')
