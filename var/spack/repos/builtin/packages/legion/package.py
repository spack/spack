# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Legion(CMakePackage):
    """Legion is a data-centric parallel programming system for writing
       portable high performance programs targeted at distributed heterogeneous
       architectures. Legion presents abstractions which allow programmers to
       describe properties of program data (e.g. independence, locality). By
       making the Legion programming system aware of the structure of program
       data, it can automate many of the tedious tasks programmers currently
       face, including correctly extracting task- and data-level parallelism
       and moving data around complex memory hierarchies. A novel mapping
       interface provides explicit programmer controlled placement of data in
       the memory hierarchy and assignment of tasks to processors in a way
       that is orthogonal to correctness, thereby enabling easy porting and
       tuning of Legion applications to new architectures.
    """
    homepage = "http://legion.stanford.edu/"
    url      = "https://github.com/StanfordLegion/legion/tarball/legion-17.02.0"
    git      = "https://github.com/StanfordLegion/legion.git"

    version('develop', branch='master')
    version('ctrl-rep', commit='177584e77036c9913d8a62e33b55fa784748759c')
    version('19.06.0', sha256='31cd97e9264c510ab83b1f9e8e1e6bf72021a0c6ee4a028966fce08736e39fbf')
    version('19.04.0', sha256='279bbc8dcdab4c75be570318989a9fc9821178143e9db9c3f62e58bf9070b5ac')
    version('18.12.0', sha256='71f2c409722975c0ad92f2caffcc9eaa9260f7035e2b55b731d819eb6a94016c')
    version('18.09.0', sha256='58c5a3072d2b5086225982563c23524692ca5758cbfda8d0f0a4f00ef17b3b8d')
    version('18.05.0', 'ab5ac8cd4aa4c91e6187bf1333a031bf')
    version('18.02.0', '14937b386100347b051a5fc514636353')
    version('17.10.0', 'ebfc974dc82a9d7f3ba53242ecae62e1')
    version('17.08.0', 'acc1ea8c564c4a382a015e0c9cf94574')
    version('17.02.0', '31ac3004e2fb0996764362d2b6f6844a')

    variant('mpi', default=True,
            description='Build on top of mpi conduit for mpi inoperability')
    variant('ibv', default=False,
            description='Build on top of ibv conduit for InfiniBand support')
    variant('shared', default=True, description='Build shared libraries')
    variant('hdf5', default=True, description='Enable HDF5 support')
    variant('build_type', default='Release', values=('Debug', 'Release'),
            description='The build type to build')

    depends_on("cmake@3.1:", type='build')
    depends_on("gasnet~aligned-segments~pshm segment-mmap-max='16GB'", when='~mpi')
    depends_on("gasnet~aligned-segments~pshm segment-mmap-max='16GB' +mpi", when='+mpi')
    depends_on("gasnet~aligned-segments~pshm segment-mmap-max='16GB' +ibv", when='+ibv')
    depends_on("hdf5~mpi", when='+hdf5')

    def cmake_args(self):
        cmake_cxx_flags = [
            '-DPRIVILEGE_CHECKS',
            '-DBOUNDS_CHECKS',
            '-DENABLE_LEGION_TLS']

        options = [
            '-DLegion_USE_GASNet=ON',
            '-DLEGION_USE_CUDA=OFF',
            '-DLEGION_USE_OPENMP=OFF',
            '-DLegion_BUILD_EXAMPLES=ON',
            '-DBUILD_SHARED_LIBS=%s' % ('+shared' in self.spec)]

        if self.spec.variants['build_type'].value == 'Debug':
            cmake_cxx_flags.append('-DDEBUG_REALM', '-DDEBUG_LEGION', '-ggdb')

        options.append('-DCMAKE_CXX_FLAGS=%s' % (" ".join(cmake_cxx_flags)))

        if '+mpi' in self.spec:
            options.append('-DGASNet_CONDUIT=mpi')

        if '+hdf5' in self.spec:
            options.append('-DLegion_USE_HDF5=ON')
        else:
            options.append('-DLegion_USE_HDF5=OFF')

        return options
