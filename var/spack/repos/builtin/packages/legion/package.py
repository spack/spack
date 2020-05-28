# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    homepage = "http://legion.stanford.edu"
    git      = "https://gitlab.com/StanfordLegion/legion.git"

    version('master', branch='master')
    version('ctrl-rep', branch='control_replication')
    version('20.03.0', tag='legion-20.03.0')
    version('19.12.0', tag='legion-19.12.0')
    version('19.09.1', tag='legion-19.09.1')
    version('19.09.0', tag='legion-19.09.0')
    version('19.06.0', tag='legion-19.06.0')
    version('19.04.0', tag='legion-19.04.0')
    version('18.12.0', tag='legion-18.12.0')
    version('18.09.0', tag='legion-18.09.0')
    version('18.05.0', tag='legion-18.05.0')
    version('18.02.0', tag='legion-18.02.0')
    version('17.10.0', tag='legion-17.10.0')
    version('17.08.0', tag='legion-17.08.0')
    version('17.02.0', tag='legion-17.02.0')

    variant('mpi', default=True,
            description='Build on top of mpi conduit for mpi inoperability')
    variant('ibv', default=False,
            description='Build on top of ibv conduit for InfiniBand support')
    variant('shared', default=True, description='Build shared libraries')
    variant('hdf5', default=True, description='Enable HDF5 support')
    variant('build_type', default='Release',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'),
            description='The build type to build', multi=False)

    depends_on("cmake@3.1:", type='build')
    depends_on("gasnet~aligned-segments~pshm segment-mmap-max='16GB'", when='~mpi')
    depends_on("gasnet~aligned-segments~pshm segment-mmap-max='16GB' +mpi", when='+mpi')
    depends_on("gasnet~aligned-segments~pshm segment-mmap-max='16GB' +ibv", when='+ibv')
    depends_on("hdf5", when='+hdf5')

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
            cmake_cxx_flags.extend([
                '-DDEBUG_REALM',
                '-DDEBUG_LEGION',
                '-ggdb',
            ])

        options.append('-DCMAKE_CXX_FLAGS=%s' % (" ".join(cmake_cxx_flags)))

        if '+mpi' in self.spec:
            options.append('-DGASNet_CONDUIT=mpi')

        if '+hdf5' in self.spec:
            options.append('-DLegion_USE_HDF5=ON')
        else:
            options.append('-DLegion_USE_HDF5=OFF')

        return options
