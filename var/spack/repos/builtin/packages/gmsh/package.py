# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gmsh(CMakePackage):
    """Gmsh is a free 3D finite element grid generator with a built-in CAD engine
    and post-processor. Its design goal is to provide a fast, light and
    user-friendly meshing tool with parametric input and advanced visualization
    capabilities. Gmsh is built around four modules: geometry, mesh, solver and
    post-processing. The specification of any input to these modules is done
    either interactively using the graphical user interface or in ASCII text
    files using Gmsh's own scripting language.
    """

    homepage = 'https://gmsh.info'
    url = 'https://gmsh.info/src/gmsh-4.4.1-source.tgz'
    git = 'https://gitlab.onelab.info/gmsh/gmsh.git'

    version('master', branch='master')
    version('4.8.4', sha256='760dbdc072eaa3c82d066c5ba3b06eacdd3304eb2a97373fe4ada9509f0b6ace')
    version('4.7.1', sha256='c984c295116c757ed165d77149bd5fdd1068cbd7835e9bcd077358b503891c6a')
    version('4.7.0', sha256='e27f32f92b374ba2a746a9d9c496401c13f66ac6e3e70753e16fa4012d14320e')
    version('4.6.0', sha256='0f2c55e50fb6c478ebc8977f6341c223754cbf3493b7b0d683b4395ae9f2ad1c')
    version('4.5.6', sha256='46eaeb0cdee5822fdaa4b15f92d8d160a8cc90c4565593cfa705de90df2a463f')
    version('4.5.5', sha256='899d3cded664124fa387da57b6f170f47a7e712c7744aa3562779897e2b9e251')
    version('4.5.4', sha256='ccf8c74f43cbe3c371abe79862025d41642b3538a0148f018949494e3b3e2ecd')
    version('4.4.1', sha256='853c6438fc4e4b765206e66a514b09182c56377bb4b73f1d0d26eda7eb8af0dc')
    version('4.2.2', sha256='e9ee9f5c606bbec5f2adbb8c3d6023c4e2577f487fa4e4ecfcfc94a241cc8dcc')
    version('4.0.0',  sha256='fb0c8afa37425c6f4315ab3b3124e9e102fcf270a35198423a4002796f04155f')
    version('3.0.6',  sha256='9700bcc440d7a6b16a49cbfcdcdc31db33efe60e1f5113774316b6fa4186987b')
    version('3.0.1',  sha256='830b5400d9f1aeca79c3745c5c9fdaa2900cdb2fa319b664a5d26f7e615c749f')
    version('2.16.0', sha256='e829eaf32ea02350a385202cc749341f2a3217c464719384b18f653edd028eea')
    version('2.15.0', sha256='992a4b580454105f719f5bc05441d3d392ab0b4b80d4ea07b61ca3bdc974070a')

    variant('external',    default=False,
            description='Use system versions of contrib libraries, when possible')
    variant('shared',      default=True,  description='Enables the build of shared libraries')
    variant('mpi',         default=False, description='Builds MPI support for parser and solver')
    variant('openmp',      default=False, description='Enable OpenMP support')
    variant('fltk',        default=True,  description='Enables the build of the FLTK GUI')
    variant('hdf5',        default=False, description='Enables HDF5 support')
    variant('gmp',         default=True,  description='Enable GMP for Kbipack (advanced)')
    variant('cairo',       default=False, description='Enable Cairo to render fonts (experimental)')
    variant('compression', default=True,  description='Enables IO compression through zlib')
    variant('med',         default=True,  description='Build with MED(HDF5)')
    variant('mmg',         default=True,  description='Build with Mmg3d')
    variant('netgen',      default=True,  description='Build with Netgen (built-in)')
    variant('opencascade', default=False, description='Build with OpenCASCADE')
    variant('oce',         default=False, description='Build with OCE')
    variant('petsc',       default=False, description='Build with PETSc')
    variant('slepc',       default=False, description='Build with SLEPc (only when PETSc is enabled)')
    variant('tetgen',      default=False, description='Build with Tetgen (built-in)')
    variant('metis',       default=True,  description='Build with Metis (built-in)')
    variant('privateapi',  default=False, description='Enable the private API')
    variant('alglib',      default=True,  description='Build with Alglib (built-in or 3rd party)')
    variant('eigen',       default=False, description='Build with Eigen (built-in or 3rd party)')
    variant('voropp',      default=True,  description='Build with voro++ (built-in or 3rd party')
    variant('cgns',        default=True,  description='Build with CGNS')

    # https://gmsh.info/doc/texinfo/gmsh.html#Compiling-the-source-code
    # We make changes to the GMSH default, such as external blas.
    depends_on('blas',    when='~eigen')
    depends_on('lapack',  when='~eigen')
    depends_on('eigen@3:', when='+eigen+external')
    depends_on('alglib',  when='+alglib+external')
    depends_on('voropp',  when='+voropp+external')
    depends_on('cmake@2.8:', type='build')
    depends_on('gmp',     when='+gmp')
    depends_on('mpi',     when='+mpi')
    depends_on('fltk+gl', when='+fltk')
    depends_on('gl',      when='+fltk')
    depends_on('glu',     when='+fltk')
    depends_on('cairo',   when='+cairo')
    depends_on('hdf5',    when='+hdf5')
    depends_on('hdf5',    when='+med')
    depends_on('med',     when='+med')
    depends_on('mmg',     when='+mmg')
    depends_on('opencascade', when='+opencascade')
    depends_on('oce',     when='+oce')
    depends_on('freetype', when='+oce')
    depends_on('freetype', when='+opencascade')
    depends_on('petsc+mpi', when='+petsc+mpi')
    depends_on('petsc',    when='+petsc~mpi')
    depends_on('slepc',   when='+slepc+petsc')
    depends_on('zlib',    when='+compression')
    depends_on('metis',   when='+metis+external')
    depends_on('cgns',    when='+cgns')
    # Gmsh's high quality vector PostScript, PDF and SVG output is produced by GL2PS.
    # But Gmsh ships with its own version of this library, so it is not a
    # dependency of this package.
    # See https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/Graphics/gl2ps.h
    # and https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/Graphics/gl2ps.cpp

    conflicts('+slepc', when='~petsc')
    conflicts('+oce', when='+opencascade')
    conflicts('+metis', when='+external',
              msg="External Metis cannot build with GMSH")

    def cmake_args(self):
        spec = self.spec

        options = [
            self.define_from_variant('ENABLE_ALGLIB', 'alglib'),
            self.define_from_variant('ENABLE_CAIRO', 'cairo'),
            self.define_from_variant('ENABLE_CGNS', 'cgns'),
            self.define_from_variant('ENABLE_EIGEN', 'eigen'),
            self.define_from_variant('ENABLE_FLTK', 'fltk'),
            self.define_from_variant('ENABLE_GMP', 'gmp'),
            self.define_from_variant('ENABLE_MED', 'med'),
            self.define_from_variant('ENABLE_METIS', 'metis'),
            self.define_from_variant('ENABLE_MMG', 'mmg'),
            self.define_from_variant('ENABLE_MPI', 'mpi'),
            self.define_from_variant('ENABLE_NETGEN', 'netgen'),
            self.define_from_variant('ENABLE_OPENMP', 'openmp'),
            self.define_from_variant('ENABLE_PETSC', 'petsc'),
            self.define_from_variant('ENABLE_PRIVATE_API', 'privateapi'),
            self.define_from_variant('ENABLE_SLEPC', 'slepc'),
            self.define_from_variant('ENABLE_VOROPP', 'voropp'),
        ]

        # Use system versions of contrib libraries, when possible:
        if '+external' in spec:
            options.append(self.define('ENABLE_SYSTEM_CONTRIB', True))

        # Make sure native file dialogs are used
        options.append('-DENABLE_NATIVE_FILE_CHOOSER=ON')

        options.append('-DCMAKE_INSTALL_NAME_DIR:PATH=%s' % self.prefix.lib)

        # Prevent GMsh from using its own strange directory structure on OSX
        options.append('-DENABLE_OS_SPECIFIC_INSTALL=OFF')

        # Make sure GMSH picks up correct BlasLapack by providing linker flags
        if '~eigen' in spec:
            options.append('-DENABLE_BLAS_LAPACK=ON')
            blas_lapack = spec['lapack'].libs + spec['blas'].libs
            options.append(
                '-DBLAS_LAPACK_LIBRARIES={0}'.format(blas_lapack.ld_flags))

        if '+oce' in spec:
            options.append('-DENABLE_OCC=ON')
        elif '+opencascade' in spec:
            options.append('-DENABLE_OCC=ON')
        else:
            options.append('-DENABLE_OCC=OFF')

        if '@:3.0.6' in spec:
            options.append(self.define_from_variant('ENABLE_TETGEN', 'tetgen'))

        if '@:4.6' in spec:
            options.append(self.define_from_variant('ENABLE_MMG3D', 'mmg'))

        if '+shared' in spec:
            # Builds dynamic executable and installs shared library
            options.append(self.define('ENABLE_BUILD_SHARED', True))
            options.append(self.define('ENABLE_BUILD_DYNAMIC', True))
        else:
            # Builds and installs static library
            options.append(self.define('ENABLE_BUILD_LIB', True))

        if '+compression' in spec:
            options.append(self.define('ENABLE_COMPRESSED_IO', True))

        return options
