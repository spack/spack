# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class Mmg(CMakePackage):
    """Mmg is an open source software for simplicial remeshing.
    It provides 3 applications and 4 libraries:
    - the mmg2d application and the libmmg2d library: adaptation
      and optimization of a two-dimensional triangulation and
      generation of a triangulation from a set of points or
      from given boundary edges
    - the mmgs application and the libmmgs library: adaptation
      and optimization of a surface triangulation and isovalue
      discretization
    - the mmg3d application and the libmmg3d library: adaptation
      and optimization of a tetrahedral mesh and implicit domain
      meshing
    - the libmmg library gathering the libmmg2d, libmmgs and
      libmmg3d libraries.
    """

    homepage = "https://www.mmgtools.org/"
    url      = "https://github.com/MmgTools/mmg/archive/v5.3.13.tar.gz"

    version('5.6.0',  sha256='bbf9163d65bc6e0f81dd3acc5a51e4a8c47a7fdae849abc26277e01154fe2437')
    version('5.5.2',  sha256='58e3b866101e6f0686758e16bcf9fb5fb06c85184533fc5054ef1c8adfd4be73')
    version('5.4.0',  sha256='2b5cc505018859856766be901797ff5d4789f89377038a0211176a5571039750')
    version('5.3.13', sha256='d9a5925b69b0433f942ab2c8e55659d9ccea758743354b43d54fdf88a6c3c191')

    variant('shared', default=True, description='Enables the build of shared libraries')
    variant('scotch', default=True, description='Enable SCOTCH library support')
    variant('doc', default=False, description='Build documentation')
    variant('vtk', default=False, when='@5.5.0:', description='Enable VTK I/O support')

    depends_on('scotch', when='+scotch')
    depends_on('doxygen', when='+doc')
    depends_on('vtk', when='+vtk')

    def cmake_args(self):
        args = []

        args.append(self.define_from_variant('USE_SCOTCH', 'scotch'))
        args.append(self.define_from_variant('USE_VTK', 'vtk'))

        if '+shared' in self.spec:
            args.append('-DLIBMMG3D_SHARED=ON')
            args.append('-DLIBMMG2D_SHARED=ON')
            args.append('-DLIBMMGS_SHARED=ON')
            args.append('-DLIBMMG_SHARED=ON')
        else:
            args.append('-DLIBMMG3D_STATIC=ON')
            args.append('-DLIBMMG2D_STATIC=ON')
            args.append('-DLIBMMGS_STATIC=ON')
            args.append('-DLIBMMG_STATIC=ON')

        return args
