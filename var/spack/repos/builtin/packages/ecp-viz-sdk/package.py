# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class EcpVizSdk(CMakePackage):
    """ECP Viz & Analysis SDK"""

    homepage = "https://github.com/chuckatkins/ecp-data-viz-sdk"
    git      = "https://github.com/chuckatkins/ecp-data-viz-sdk.git"

    maintainers = ['chuckatkins']

    version('1.0', branch='master')

    variant('catalyst', default=True, description="Enable Catalyst")
    variant('paraview', default=True, description="Enable ParaView")
    variant('sz', default=True, description="Enable SZ")
    variant('vtkm', default=True, description="Enable VTK-m")
    variant('zfp', default=True, description="Enable ZFP")

    # Broken dependency: vtk-h
    # variant('ascent', default=False, description="Enable Ascent")

    # Outstanding build issues
    # variant('visit', default=False, description="Enable VisIt")

    # Missing spack package
    # variant('cinema', default=False, description="Enable Cinema")
    # variant('rover', default=False, description="Enable ROVER")

    depends_on('ascent', when='+ascent')
    depends_on('catalyst', when='+catalyst')
    depends_on('paraview', when='+paraview')
    depends_on('sz', when='+sz')
    depends_on('visit', when='+visit')
    depends_on('vtk-m', when='+vtkm')
    depends_on('zfp', when='+zfp')

    def cmake_args(self):
        return ['-DVIZ=ON']
