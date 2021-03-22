# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os

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
    url = "https://github.com/StanfordLegion/legion/tarball/legion-20.12.0"
    git = "https://github.com/StanfordLegion/legion.git"

    # !!! NOTE: 'master' is the only spot were the embedded gasnet builds is currently 
    # supported. 
    #version('stable', branch='stable')
    version('master', branch='master')
    version('cr', branch='control_replication')



    depends_on("cmake@3.16:", type='build')  # rest of legion to be updated to match.


    # Network transport layer: the underlying data transport API should be used for
    # distributed data movement.  For Legion, gasnet is the currently the most
    # mature.  We have many users that default to using no network layer for
    # day-to-day development thus we default to 'none'.  MPI support is new and
    # should be considered as a beta release.
    variant('network', default='none', 
            values=('gasnet', 'mpi', 'none'),
            description="The network communications/transport layer to use.",
            multi=False)

    # TODO: Need to pick a version of MPI v3 below. 
    depends_on('mpi', when='network=mpi')
    depends_on('mpi', when='network=gasnet')  # MPI is required to build gasnet (needs mpicc).

    # We default to automatically embedding a gasnet build. To override this 
    # point the package a pre-installed version of GASNet-Ex via the gasnet_root
    # variant. 
    # 
    # make sure we have a valid directory provided for gasnet_root...  
    def validate_gasnet_root(value):
        if value == 'none':
            return True

        if not os.path.isdir(value):
            print("gasnet_root:", value, "-- no such directory.")
            return False
        else:
            return True

    variant('gasnet_root', 
            default='none',
            values=validate_gasnet_root,
            description="Path to a pre-installed version of GASNet (prefix directory).",
            multi=False)
    conflicts('gasnet_root', when="network=mpi")

    # The preferred mechanism for gasnet is to embed the build within the
    # package.  As such, we prefer to use a resource vs. a package dependency 
    # (i.e., there is currently not an officially supported gasnet(ex) package that 
    # follows the preferred/supported mechanisms.
    resource(name='gasnet_res',
             git='https://github.com/StanfordLegion/gasnet.git',
             branch='control',
             placement='gasnet',
             when='network=gasnet')

    variant('conduit', default='none',
            values=('aries', 'ibv', 'udp', 'mpi', 'ucx', 'none'),
            description="The gasnet conduit(s) to enable.",
            multi=False)

    conflicts('conduit=none', when='network=gasnet', 
              msg="a conduit must be selected when 'network=gasnet'")

    gasnet_conduits=('aries', 'ibv', 'udp', 'mpi', 'ucx')
    for c in gasnet_conduits:
        conflict_str='conduit=%s' % c
        conflicts(conflict_str, when='network=mpi', 
            msg="conduit attribute requires 'network=gasnet'.")
        conflicts(conflict_str, when='network=none', 
            msg="conduit attribute requires 'network=gasnet'.")
    depends_on('ucx', when='conduit=ucx')
    depends_on('mpi', when='conduit=mpi')  # TODO: need to ferret out MPI 3.x support details.

    variant('gasnet_debug', default=False,
            description="Build gasnet with debugging enabled.")
    conflicts('+gasnet_debug', when='network=mpi')
    conflicts('+gasnet_debug', when='network=none')

    variant('shared_libs', default=False,
            description="Build shared libraries.")

    variant('bounds_checks', default=False,
            description="Enable bounds checking in Legion accessors.")

    variant('privilege_checks', default=False,
            description="Enable runtime privildge checks in Legion accessors.")

    variant('enable_tls', default=False,
            description="Enable thread-local-storage of the Legion context.")

    variant('output_level', default='warning',
            # Note: these values are dependent upon those used in the cmake config.
            values=("spew", "debug", "info", "print", "warning", "error", "fatal", "none"),
            description="Set the compile-time logging level.",
            multi=False)

    variant('spy', default=False,
            description="Enable detailed logging for Legion Spy debugging.")


    # reminder for arch numbers to names: 60=pascal, 70=volta, 75=turing, 80=ampere
    cuda_arch_list = ('60', '70', '75', '80')
    # note: we will be dependent upon spack's latest-and-greatest cuda version...
    variant('cuda', default=False,
            description="Enable CUDA support.")
    variant('cuda_hijack', default=False,
            description="Hijack application calls into the CUDA runtime (implies +cuda).")
    variant('cuda_arch', default='70',
            values=cuda_arch_list,
            description="GPU/CUDA architecture to build for.",
            multi=False)

    depends_on('cuda@10:11', when='+cuda')
    conflicts('+cuda_hijack', when='~cuda')


    variant('fortran', default=False,
            description="Enable Fortran bindings.")

    variant('hdf5', default=False,
            description="Enable support for HDF5.")
    depends_on('hdf5', when='+hdf5')

    variant('hwloc', default=False,
            description="Use hwloc for topology awareness.")
    depends_on('hwloc', when='+hwloc')



    variant('kokkos', default=False,
            description="Enable support for interoperability with Kokkos.")

    depends_on('kokkos@3.2~cuda', when='+kokkos~cuda')
    for nvarch in cuda_arch_list:
        depends_on('kokkos@3.2+cuda+cuda_lambda+wrapper cuda_arch={0}'.format(nvarch),
                   when='%gcc+kokkos+cuda cuda_arch={0}'.format(nvarch))
        depends_on("kokkos@3.2+cuda+cuda_lambda~wrapper cuda_arch={0}".format(nvarch),
                   when="%clang+kokkos+cuda cuda_arch={0}".format(nvarch))

    depends_on("kokkos@3.2~cuda+openmp", when='kokkos+openmp')

    variant('bindings', default=False,
            description="Build language bindings to the Legion runtime (excluding Fortran).")

    variant('libdl', default=True,
            description="Enable support for dynamic object/library loading.")

    variant('openmp', default=False,
            description="Enable support for OpenMP within Legion tasks.")

    variant('papi', default=False,
            description="Enable PAPI performance measurements.")
    depends_on('papi', when='+papi')

    variant('python', default=False,
            description="Enable Python support.")
    depends_on('python@3', when='+python')

    variant('zlib', default=True,
            description="Enable zlib support.")
    depends_on('zlib', when='+zlib')

    variant('redop_complex', default=False,
            description="Use reduction operators for complex types.")


    variant('max_dims', values=int, default=3,
            description="Set the maximum number of dimensions available in a logical region.")
    variant('max_fields', values=int, default=512,
            description="Maximum number of fields allowed in a logical region.")


    variant('native', default=False,
            description="Enable native/host processor optimizaton target.")


    def cmake_args(self):
        spec = self.spec
        cmake_cxx_flags = []
        options = []
        
        if 'network=gasnet' in spec:
            options.append('-DLegion_NETWORKS=gasnetex')
            if spec.variants['gasnet_root'].value != 'none':
                gasnet_dir = spec.variants['gasnet_root'].value
                options.append('-DGASNet_ROOT_DIR=%s' % gasnet_dir)
            else:
                options.append('-DLegion_EMBED_GASNet=ON')
                gasnet_dir=join_path(self.stage.source_path, 'gasnet')
                options.append('-DLegion_EMBED_GASNet_LOCALSRC=%s' % gasnet_dir)

            gasnet_conduit = spec.variants['conduit'].value
            options.append('-DGASNet_CONDUIT=%s' % gasnet_conduit)

            if '+gasnet_debug' in spec:
                options.append('-DLegion_EMBED_GASNet_CONFIGURE_ARGS=--enable-debug')
        elif 'network=mpi' in spec:
            options.append('-DLegion_NETWORKS=mpi')
            if spec.variants['gasnet_root'].value != 'none':
                raise InstallError("'gasnet_root' is only valid when 'network=gasnet'.")
        else:
            if spec.variants['gasnet_root'].value != 'none':
                raise InstallError("'gasnet_root' is only valid when 'network=gasnet'.")
            options.append('-DLegion_EMBED_GASNet=OFF')

        if '+shared_libs' in spec:
            options.append('-DBUILD_SHARED_LIBS=ON')
        else:
            options.append('-DBUILD_SHARED_LIBS=OFF')

        if '+bounds_checks' in spec:
            # default is off.
            options.append('-DLegion_BOUNDS_CHECKS=ON')
        if '+privilege_checks' in spec:
            # default is off.
            options.append('-DLegion_PRIVILEGE_CHECKS=ON')
        if '+enable_tls' in spec:
            # default is off.
            options.append('-DLegion_ENABLE_TLS=ON')
        if 'output_level' in spec:
            level = str.upper(spec.variants['output_level'].value)
            options.append('-DLegion_OUTPUT_LEVEL=%s' % level)
        if '+spy' in spec:
            # default is off.
            options.append('-DLegion_SPY=ON')

        if '+cuda' in spec:
            cuda_arch = spec.variants['cuda_arch'].value
            options.append('-DLegion_USE_CUDA=ON')
            options.append('-DLegion_GPU_REDUCTIONS=ON')
            options.append('-DLegion_CUDA_ARCH=%s' % cuda_arch)
            if '+cuda_hijack' in spec:
                options.append('-DLegion_HIJACK_CUDART=ON')
            else:
                options.append('-DLegion_HIJACK_CUDART=OFF')

        if '+fortran' in spec:
            # default is off.
            options.append('-DLegion_USE_Fortran=ON')

        if '+hdf5' in spec:
            # default is off.
            options.append('-DLegion_USE_HDF5=ON')

        if '+hwloc' in spec:
            # default is off.
            options.append('-DLegion_USE_HWLOC=ON')

        if '+kokkos' in spec:
            # default is off.
            options.append('-DLegion_USE_Kokkos=ON')
            os.environ['KOKKOS_CXX_COMPILER'] = spec['kokkos'].kokkos_cxx

        if '+libdl' in spec:
            # default is on.
            options.append('-DLegion_USE_LIBDL=ON')
        else:
            options.append('-DLegion_USE_LIBDL=OFF')

        if '+openmp' in spec:
            # default is off.
            options.append('-DLegion_USE_OpenMP=ON')

        if '+papi' in spec:
            # default is off.
            options.append('-DLegion_USE_PAPI=ON')

        if '+python' in spec:
            # default is off.
            options.append('-DLegion_USE_Python=ON')

        if '+zlib' in spec:
            # default is on.
            options.append('-DLegion_USE_ZLIB=ON')
        else:
            options.append('-DLegion_USE_ZLIB=OFF')

        if '+redop_complex' in spec:
            # default is off.
            options.append('-DLegion_REDOP_COMPLEX=ON')

        if '+bindings' in spec:
            # default is off.
            options.append('-DLegion_BUILD_BINDINGS=ON')
            options.append('-DLegion_REDOP_COMPLEX=ON') # required for bindings
            options.append('-DLegion_USE_Fortran=ON')

        if spec.variants['build_type'].value == 'Debug':
            cmake_cxx_flags.extend([
                '-DDEBUG_REALM',
                '-DDEBUG_LEGION',
                '-ggdb',
            ])

        maxdims = int(spec.variants['max_dims'].value)
        # TODO: sanity check if maxdims < 0 || > 9???
        options.append('-DLegion_MAX_DIM=%d' % maxdims)

        maxfields = int(spec.variants['max_fields'].value)
        if (maxfields <= 0):
            maxfields = 512
        # make sure maxfields is a power of two.  if not,
        # find the next largest power of two and use that...
        if (maxfields & (maxfields - 1) != 0):
            while maxfields & maxfields - 1:
                maxfields = maxfields & maxfields - 1
            maxfields = maxfields << 1
        options.append('-DLegion_MAX_FIELDS=%d' % maxfields)

        if '+native' in spec:
            # default is off.
            options.append('-DBUILD_MARCH:STRING=native')

        return options
