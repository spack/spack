# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install sensei
#
# You can edit this file again by typing:
#
#     spack edit sensei
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Sensei(CMakePackage):
    """SENSEI is a platform for scalable in-situ analysis and visualization."""

    homepage = "https://sensei-insitu.org"
    url      = "https://gitlab.kitware.com/sensei/sensei/-/archive/v2.1.1/sensei-v2.1.1.tar.gz"
    git      = "https://gitlab.kitware.com/sensei/sensei.git"

    version('master', branch='master')
    version('2.1.1', sha256='8a27ebf133fef00a59e4b29433762e6560bf20214072de7808836eb668bb5687')
    version('2.1.0', sha256='b7af21a25523cf6cd8934d797471b75ca32881166625d71f24b5c8b6d727ca99')
    version('2.0.0', sha256='df48eab035e1acdd8edf5159955c05306f9ca48117effacc4a6b77c3fb24f62b')
    version('1.1.0', sha256='e5a4ba691573ff6c7b0d4793665e218ee5868ebcc0198915d1f16a4b7b92a368')
    version('1.0.0', sha256='bdcb03c56b51f2795ec5a7e85a5abb01d473d192fac50f2a8bf2608cc3564ff8')

    variant('build_type', default='RelWithDebInfo', description='CMake build type', values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))
    variant('catalyst', default=True, description='Build with ParaView-Catalyst support')
    variant('libsim', default=False, description='Build with VisIt-Libsim support')
    variant('vtkio', default=True, description='Enable adaptors to write to VTK XML format')
    variant('adios', default=False, description='Enable ADIOS adaptors and endpoints')
    variant('python', default=False, description='Enables Python bindings')
    variant('miniapps', default=True, description='Enable the parallel 3D and oscillators miniapp')

    depends_on("paraview@5.5:5.6", when="+catalyst")
    depends_on("visit", when="+libsim")
    depends_on("vtk", when="+libsim")
    depends_on("vtk", when="+adios ~libsim ~catalyst")
    depends_on("adios", when="+adios")
    depends_on("vtk", when="+python ~libsim ~catalyst")
    depends_on("python", when="+python")
    depends_on("py-numpy", when="+python")
    depends_on("py-mpi4py", when="+python")
    depends_on("swig", when="+python")
    
    # Can have either LibSim or Catalyst, but not both
    conflicts('+libsim', when='+catalyst')

    def cmake_args(self):
        spec = self.spec
        
        args = [
            '-DCMAKE_CXX_STANDARD=11',
            '-DCMAKE_C_STANDARD=11',
            '-DCMAKE_CXX_FLAGS=-fPIC -Wall -Wextra -O3 -mtune=generic',
            '-DCMAKE_C_FLAGS=-fPIC -Wall -Wextra -O3 -mtune=generic'
        ]

        if 'catalyst' in spec:
            args.append('-DENABLE_CATALYST:BOOL=ON')
            args.append('-DENABLE_CATALYST_PYTHON:BOOL=ON')
            args.append('-DParaView_DIR:PATH={0}' % spec['paraview'].prefix)
        else:
            args.append('-DENABLE_CATALYST:BOOL=OFF')

        if 'libsim' in spec:
            args.append('-DENABLE_LIBSIM:BOOL=ON')
            args.append('-DVISIT_DIR:PATH={0}' % spec['visit'].prefix)
            args.append('-DVTK_DIR:PATH={0}' % spec['vtk'].prefix)
        else:
            args.append('-DENABLE_LIBSIM:BOOL=OFF')

        args.append('-DENABLE_VTK_IO:BOOL={0}' % str('vtkio' in spec))
        
        if spec.variants['adios'].value:
            args.append('-DENABLE_ADIOS:BOOL=ON')
            if not 'catalyst' in spec and not 'libsim' in spec:
                args.append('-DVTK_DIR:PATH={0}' % spec['vtk'].prefix)
            args.append('-DADIOS_DIR:PATH={0}' % spec['adios'].prefix)
            
        if 'python' in spec:
            args.append('-DENABLE_PYTHON:BOOL=ON')
            if not 'catalyst' in spec and not 'libsim' in spec:
                args.append('-DVTK_DIR:PATH={0}' % spec['vtk'].prefix)
        
        if 'miniapps' in spec:
            args.append('-DENABLE_PARALLEL3D:BOOL=ON')
            args.append('-DENABLE_OSCILLATORS:BOOL=ON')
        else:
            args.append('-DENABLE_PARALLEL3D:BOOL=OFF')
            args.append('-DENABLE_OSCILLATORS:BOOL=OFF')

        return args
