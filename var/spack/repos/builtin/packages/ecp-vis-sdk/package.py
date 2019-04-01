# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class EcpVisSdk(CMakePackage):
    """ECP Vis & Analysis SDK"""

    homepage = "https://github.com/chuckatkins/ecp-data-viz-sdk"
    git      = "https://github.com/chuckatkins/ecp-data-viz-sdk.git"

    version('1.0', branch='master')

    variant('paraview', default=False, description="Enable ParaView")
    variant('catalyst', default=False, description="Enable Catalyst")
    variant('cinema', default=False, description="Enable Cinema")
    variant('vtk-m', default=False, description="Enable VTK-m")
    variant('ascent', default=False, description="Enable Ascent")
    variant('visit', default=False, description="Enable VisIt")
    variant('zfp', default=False, description="Enable ZFP")
    variant('sz', default=False, description="Enable SZ")
    #variant('rover', default=False, description="Enable ROVER")

    depends_on('paraview', when='+paraview')
    depends_on('catalyst', when='+catalyst')
    depends_on('cinema', when='+cinema')
    depends_on('vtk-m', when='+vtk-m')
    depends_on('ascent', when='+ascent')
    depends_on('visit', when='+visit')
    depends_on('zfp', when='+zfp')
    depends_on('sz', when='+sz')

    def cmake_args(self):
        return [ '-DVIS=ON' ]
