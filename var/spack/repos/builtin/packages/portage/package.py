# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Portage(CMakePackage):
    """Portage is a framework that computational physics applications can use
       to build a highly customized, hybrid parallel (MPI+X) conservative
       remapping library for transfer of field data between meshes.

       ***WARNING*** The older versions may not work and are not of much values.
       ***WARNING*** They are left here until a deprecation policy is instituted
    """
    homepage = "http://portage.lanl.gov/"
    git      = "https://github.com/laristra/portage.git"
    url      = "https://github.com/laristra/portage/releases/download/3.0.0/portage-3.0.0.tar.gz"


    maintainers = ['raovgarimella']
    
    # tarballs don't have submodules, so use git tags
    version('3.0.0', sha256='7a5a21ffbc35fa54a5136d937cfda6f836c7496ff2b5adf54deb4107501333da')
    version('1.2.2', sha256='48b789447a3726dabaf9e57478b8e810e93b8426a5616840b47ccf813eb183e0', submodules=True)
    version('1.1.1', sha256='79986c5155db03c7d1d716dbfd0444c32952646b80d7dc7f0ef940dbdd644ebd')
    version('1.1.0', sha256='340a20b26e475b6b3344f4c4dcef6e5bd17cfdc7b82ee32edf9e529f1c0b12b0')
    version('master', branch='master', submodules=True)



    # fabs() needs math.h for gcc-7, got fixed in
    # versions above 1.2.2
    patch('gcc-7.patch', when='@1.1.0:1.2.2 %gcc@7:')
    # part of https://github.com/laristra/cinch/commit/f87f848269fac25aa5b8d0bd5d9c9b2d2d6fb0ad
    # fixed in version above 1.2.2
    patch('p_lapacke_config.patch', when='@1.2.2')
    # don't enable debug prints in RelWithDebInfo build
    # fixed in version above 1.2.2
    patch('rel-with-deb-info.patch', when='@1.2.2')

    variant('mpi', default=True, description='Support MPI')
    variant('tangram', default=False, description='Use Tangram interface reconstruction package')
    variant('jali', default=False, description='Include support for Jali mesh framework')
    variant('flecsisp', default=False, description='Include support for FleCSI mesh framework')
    variant('thrust', default=False, description='Enable on-node parallelism using NVidia Thrust library')
    variant('kokkos', default=False, description='Enable on-node or device parallelism with Kokkos')
    variant('openmp', default=False, description="Enable on-node parallelism using OpenMP")
    variant('cuda', default=False, description="Enable GPU parallelism using CUDA")

    depends_on("cmake@3.13:", type='build')

    depends_on('mpi', when='+mpi')
    
    depends_on('tangram', when='+tangram')
    depends_on('tangram+mpi', when='+tangram+mpi')
    depends_on('tangram+jali', when='+tangram+jali')
    depends_on('tangram+flecsisp', when='+tangram+flecsisp')
    depends_on('tangram+thrust', when='+tangram+thrust')
    depends_on('tangram+kokkos', when='+tangram+kokkos')
    depends_on('tangram+cuda', when='+tangram+cuda')

    depends_on('wonton')
    depends_on('wonton+mpi', when='+mpi')
    depends_on('wonton+jali', when='+jali')
    depends_on('wonton+flecsisp', when='+flecsisp')
    depends_on('wonton+thrust', when='+thrust')
    depends_on('wonton+kokkos', when='+kokkos')
    depends_on('wonton+openmp', when='+openmp')
    depends_on('wonton+cuda', when='+cuda')

    # Jali needs MPI
    conflicts('+jali ~mpi')

    # Thrust with CUDA does not work as yet
    conflicts('+thrust +cuda')
    
    # Don't enable Kokkos and Thrust simultaneously
    conflicts('+thrust +kokkos')
     
    def cmake_args(self):
        options = []
        
        if '+mpi' in self.spec:
            options.append('-DPORTAGE_ENABLE_MPI=ON')
        else:
            options.append('-DPORTAGE_ENABLE_MPI=OFF')

        if '+thrust' in self.spec:
            options.append('-DPORTAGE_ENABLE_THRUST=ON')
        else:
            options.append('-DPORTAGE_ENABLE_THRUST=OFF')

        if '+kokkos' in self.spec:
            options.append('-DPORTAGE_ENABLE_Kokkos=ON')
        else:
            options.append('-DPORTAGE_ENABLE_Kokkos=OFF')

        if '+jali' in self.spec:
            options.append('-DPORTAGE_ENABLE_Jali=ON')
        else:
            options.append('-DPORTAGE_ENABLE_Jali=OFF')

        if '+flecsi' in self.spec:
            options.append('-DPORTAGE_ENABLE_FleCSI=ON')
        else:
            options.append('-DPORTAGE_ENABLE_FleCSI=OFF')

        if '+tangram' in self.spec:
            options.append('-DPORTAGE_ENABLE_TANGRAM=ON')
        else:
            options.append('-DPORTAGE_ENABLE_TANGRAM=OFF')

            
        # Unit test variant
        if self.run_tests:
            options.append('-DENABLE_UNIT_TESTS=ON')
            options.append('-DENABLE_APP_TESTS=ON')
        else:
            options.append('-DENABLE_UNIT_TESTS=OFF')
            options.append('-DENABLE_APP_TESTS=OFF')

        return options
