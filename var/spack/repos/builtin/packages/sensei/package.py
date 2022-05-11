# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class Sensei(CMakePackage):
    """SENSEI is a platform for scalable in-situ analysis and visualization.
    Its design motto is 'Write once, run everywhere', this means that once
    the application is instrumented with SENSEI it can use existing and
    future analysis backends. Existing backends include: Paraview/Catalyst,
    Visit/Libsim, ADIOS, Python scripts, and so on."""

    homepage = "https://sensei-insitu.org"
    url      = "https://github.com/SENSEI-insitu/SENSEI/releases/download/v3.2.1/SENSEI-3.2.1.tar.gz"
    git      = "https://github.com/SENSEI-insitu/SENSEI.git"
    maintainers = ['sshudler', 'kwryankrattiger']

    version('develop', branch='develop')
    version('3.2.2', sha256='d554b654880e899d97d572f02de87b0202faadaf899420ef871093b5bce320c0')
    version('3.2.1', sha256='7438fb4b148e4d1eb888c619366d0d8639122ecbbf1767e19549d6ca0c8698ca')
    version('3.2.0', sha256='fd1a69134d9f8151d85a7f84a67d6a648aef5580585b39f74a56367cff433c82')
    version('3.1.0', sha256='813075e033904835afa74231a841ab46424d4567157ee7366f3b785357ffc0ea')
    version('3.0.0', sha256='e9b4d7531bbe8848a7fb182f1d2706b397d18e1a580a51f79b4bf6793be195e5')
    version('2.1.1', sha256='7e211b3d9ce8576d33dbb39ea367c971bb8863e1cf53b9c0e13f00b53bd16526')
    version('2.1.0', sha256='3de667523d5a8e5576e29ff9528f7f341fcc799b55c9cd824dc61c7ca1a2a910')
    version('2.0.0', sha256='e985778ebbf0b9a103d11e069e58f8975f98a63dc2861b7cde34ea12a23fee20')
    version('1.1.0', sha256='769e0b5db50be25666c0d13176a7e4f89cbffe19cdc12349437d0efff615b200')
    version('1.0.0', sha256='5b8609352048e048e065a7b99f615a602f84b3329085e40274341488ef1b9522')

    variant('shared', default=True, description='Enables shared libraries')
    variant('ascent', default=False, description='Build with ParaView-Catalyst support')
    variant('catalyst', default=False, description='Build with ParaView-Catalyst support')
    variant('libsim', default=False, description='Build with VisIt-Libsim support')
    variant('vtkio', default=False, description='Enable adaptors to write to VTK XML format')
    variant('adios2', default=False, description='Enable ADIOS2 adaptors and endpoints')
    variant('hdf5', default=False, description='Enables HDF5 adaptors and endpoints')
    variant('vtkm', default=False, description='Enable VTKm adaptors and endpoints')
    variant('python', default=False, description='Enable Python bindings')
    variant('miniapps', default=False, description='Enable the parallel 3D and oscillators miniapps')

    # All SENSEI versions up to 2.1.1 support only Python 2, so in this case
    # Paraview 6 cannot be used since it requires Python 3. Starting from
    # version 3, SENSEI supports Python 3.
    depends_on("paraview@5.5.0:5.5.2+mpi+hdf5", when="@:2.1.1 +catalyst")
    depends_on("paraview@5.5.0:5.5.2+python+mpi+hdf5", when="@:2.1.1 +catalyst+python")
    depends_on("paraview@5.6:5.7+mpi+hdf5", when="@3:3.2.1 +catalyst")
    depends_on("paraview@5.6:5.7+python3+mpi+hdf5", when="@3:3.2.1 +catalyst+python")
    depends_on("paraview+mpi+hdf5", when="+catalyst")
    depends_on("paraview+python3+mpi+hdf5", when="+catalyst+python")
    depends_on("visit~gui~python", when="+libsim")
    depends_on("vtk@8.1.0:8.1.2", when="+libsim")
    depends_on("vtk", when="~libsim ~catalyst")
    depends_on("vtk+python", when="~libsim ~catalyst+python")
    depends_on("adios2", when="+adios2")
    depends_on("ascent", when="+ascent")

    # VTK needs +hl and currently spack cannot resolve +hl and ~hl
    depends_on("hdf5+hl", when="+hdf5")
    # SENSEI 3 supports Python 3, earlier versions upport only Python 2
    depends_on("python@:2.7.16", when="@:2.1.1 +python", type=('build', 'run'))
    depends_on("python@3:", when="@3: +python", type=('build', 'run'))
    extends('python', when='+python')
    depends_on("py-numpy", when="+python", type=('build', 'run'))
    depends_on("py-mpi4py", when="+python", type=('build', 'run'))
    depends_on("swig", when="+python", type='build')
    depends_on('cmake@3.6:', when="@3:", type='build')
    depends_on('pugixml')

    # Since sensei always has a VTK dependency, either directly or indirectly,
    # VTKm will also always be available via VTK so there's no scenario to
    # have a directl dependency on VTK,

    # Can have either LibSim or Catalyst, but not both
    conflicts('+libsim', when='+catalyst')
    # hdf5 variant is available only for SENSEI 3
    conflicts('+hdf5', when='@:2.1.1')

    def cmake_args(self):
        spec = self.spec

        # -Ox flags are set by default in CMake based on the build type
        args = [
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define('SENSEI_USE_EXTERNAL_pugixml', True),
            self.define('ENABLE_SENSEI', True),
            self.define_from_variant('ENABLE_ASCENT', 'ascent'),
            self.define_from_variant('ENABLE_VTKM', 'vtkm'),
            self.define_from_variant('ENABLE_CATALYST', 'catalyst'),
            self.define_from_variant('ENABLE_LIBSIM', 'libsim'),
            self.define_from_variant('ENABLE_VTK_IO', 'vtkio'),
            self.define_from_variant('ENABLE_PYTHON', 'python'),
            self.define_from_variant('ENABLE_ADIOS2', 'adios2'),
            self.define_from_variant('ENABLE_HDF5', 'hdf5'),
            self.define_from_variant('ENABLE_PARALLEL3D', 'miniapps'),
            self.define_from_variant('ENABLE_OSCILLATORS', 'miniapps')
        ]

        if '+libsim' in spec:
            args.append(
                '-DVISIT_DIR:PATH={0}/current/{1}-{2}'.format(
                    spec['visit'].prefix, spec.platform, spec.target.family)
            )

        if '+python' in spec:
            args.append(self.define('PYTHON_EXECUTABLE', spec['python'].command.path))
            if spec.satisfies('@3:'):
                args.append(self.define('SENSEI_PYTHON_VERSION', 3))
            args.append(self.define_from_variant('ENABLE_CATALYST_PYTHON', 'catalyst'))

        return args
