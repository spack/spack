# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Vrpn(CMakePackage):
    """The Virtual-Reality Peripheral Network (VRPN) is designed to implement a
       network-transparent interface between application programs and the set
       of physical devices (tracker, etc.) used in a virtual-reality (VR)
       system."""

    homepage = "https://github.com/vrpn/vrpn"
    url = "https://github.com/vrpn/vrpn/archive/version_07.34.tar.gz"

    version('07.34', '2fd6b418901e0f575099aea293274f5a61703ae37b55a335fc15fd3fe2779f84')

    def cmake_args(self):
        return ['-DVRPN_USE_JSONNET=OFF']
