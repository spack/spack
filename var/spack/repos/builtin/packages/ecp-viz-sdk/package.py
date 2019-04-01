# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    variant('paraview', default=False, description="Enable ParaView")
    variant('vtkm', default=False, description="Enable VTK-m")
    variant('zfp', default=False, description="Enable ZFP")
    variant('sz', default=False, description="Enable SZ")

    # TODO: fix +osmesa~rendering conflict
    variant('catalyst', default=False, description="Enable Catalyst")

    # Unsatisfiable dependencies: hdf5 and netcdf
    # variant('visit', default=False, description="Enable VisIt")

    # Broken dependency: vtk-h
    # variant('ascent', default=False, description="Enable Ascent")

    # Missing spack package
    # variant('cinema', default=False, description="Enable Cinema")
    # variant('rover', default=False, description="Enable ROVER")

    depends_on('paraview', when='+paraview')
    depends_on('catalyst', when='+catalyst')
    depends_on('vtkm', when='+vtkm')
    depends_on('ascent', when='+ascent')
    depends_on('visit', when='+visit')
    depends_on('zfp', when='+zfp')
    depends_on('sz', when='+sz')

    def cmake_args(self):
        return ['-DVIZ=ON']
