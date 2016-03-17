from spack import *

class Hpx(Package):
    """A general purpose C++ runtime system for parallel and distributed applications of any scale"""
    homepage = "http://stellar-group.org/libraries/hpx"
    url      = "http://github.com/STEllAR-GROUP/hpx/archive/0.9.11.tar.gz"

    version('0.9.11', '77767298f57805ee9eb710a2044ba829')

    patch('Werror.patch')

    # Highly recommended
    variant("gperftools", default=True)
    variant("libunwind", default=True)
    variant("openmpi", default=True)

    # Optional
    variant("hdf5", default=False)
    variant("jemalloc", default=False)
    variant("papi", default=False)

    # Build dependencies
    depends_on("cmake @2.8.10:")

    # Run-time dependencies
    # Because of a problem in Boost V1.54.0 this version can't be used for
    # compiling HPX if you use gcc V4.6.x
    depends_on("boost @1.49.0:")
    depends_on("hwloc @1.2:")

    # Highly recommended
    depends_on("gperftools @1.7.1:", when="+gperftools")
    depends_on("libunwind @0.97:", when="+libunwind")
    depends_on("openmpi @1.8.0:", when="+openmpi")

    # Optional
    depends_on("hdf5 +threadsafe @1.6.7:", when="+hdf5")
    depends_on("jemalloc @2.1.0:", when="+jemalloc")
    depends_on("papi", when="+papi")

    def install(self, spec, prefix):
        if spec.satisfies('@:0.9.11') and spec['boost'].satisfies('@1.60.0:'):
            die("HPX <= 0.9.11 does not work with Boost >= 1.60.0")
        cmake_opts = std_cmake_args
        cmake_opts.extend([
            '-DCMAKE_CXX_COMPILER=c++',
            '-DCMAKE_CXX_FLAGS=-std=c++0x',   # enable C++11
            '-DBOOST_ROOT=%s' % spec['boost'].prefix,
            # '-DBOOST_INCLUDE_DIR=%s' % spec['boost'].prefix.include,
            # '-DBOOST_LIBRARY_DIR=%s' % spec['boost'].prefix.lib,
            '-DBOOST_SUFFIX=-mt',   # use the multi-threaded version
            # '-DHWLOC_ROOT=%s' % spec['hwloc'].prefix,
        ])
        if spec.satisfies("+openmpi"):
            cmake_opts.extend([
                '-DMPI_C_COMPILER=mpicc',
                '-DMPI_CXX_COMPILER=mpicxx',
                '-DMPI_Fortran_COMPILER=mpifort',
            ])
        if spec.satisfies("=darwin-x86_64"):
            # RelWithDebugInfo does not work
            cmake_opts = [opt for opt in cmake_opts if not opt.startswith('-DCMAKE_BUILD_TYPE=')]
            cmake_opts.extend([
                '-DCMAKE_BUILD_TYPE=Release',
            ])

        # TODO: Take other variants into account

        with working_dir('spack-build', create=True):
            cmake('..', *cmake_opts)
            make()
            make("install")
