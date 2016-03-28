from spack import *
import sys

class Dealii(Package):
    """C++ software library providing well-documented tools to build finite element codes for a broad variety of PDEs."""
    homepage = "https://www.dealii.org"
    url      = "https://github.com/dealii/dealii/releases/download/v8.4.0/dealii-8.4.0.tar.gz"

    version('8.4.0', 'ac5dbf676096ff61e092ce98c80c2b00')

    depends_on ("cmake")
    depends_on ("blas")
    depends_on ("lapack")
    depends_on ("mpi")

    depends_on ("arpack-ng+mpi")
    depends_on ("boost")
    depends_on ("doxygen")
    depends_on ("hdf5+mpi~cxx") #FIXME NetCDF declares dependency with ~cxx, why?
    depends_on ("metis")
    depends_on ("muparser")
    depends_on ("netcdf-cxx")
    #depends_on ("numdiff") #FIXME
    depends_on ("oce")
    depends_on ("p4est")
    depends_on ("parmetis")
    depends_on ("petsc+mpi")
    depends_on ("slepc")
    depends_on ("suite-sparse")
    depends_on ("tbb")
    depends_on ("trilinos")

    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)

        # CMAKE_BUILD_TYPE should be DebugRelease | Debug | Release
        for word in options[:]:
            if word.startswith('-DCMAKE_BUILD_TYPE'):
                options.remove(word)

        dsuf = 'dylib' if sys.platform == 'darwin' else 'so'
        options.extend([
            '-DCMAKE_BUILD_TYPE=DebugRelease',
            '-DDEAL_II_WITH_THREADS:BOOL=ON'
            '-DDEAL_II_WITH_MPI:BOOL=ON',
            '-DCMAKE_C_COMPILER=%s' % join_path(self.spec['mpi'].prefix.bin, 'mpicc'), # FIXME: avoid hardcoding mpi wrappers names
            '-DCMAKE_CXX_COMPILER=%s' % join_path(self.spec['mpi'].prefix.bin, 'mpic++'),
            '-DCMAKE_Fortran_COMPILER=%s' % join_path(self.spec['mpi'].prefix.bin, 'mpif90'),
            '-DARPACK_DIR=%s' % spec['arpack-ng'].prefix,
            '-DBOOST_DIR=%s' % spec['boost'].prefix,
            '-DHDF5_DIR=%s' % spec['hdf5'].prefix,
            '-DMETIS_DIR=%s' % spec['metis'].prefix,
            '-DMUPARSER_DIR=%s ' % spec['muparser'].prefix,
            # since Netcdf is spread among two, need to do it by hand:
            '-DNETCDF_FOUND=true',
            '-DNETCDF_LIBRARIES=%s;%s' %
                (join_path(spec['netcdf-cxx'].prefix.lib,'libnetcdf_c++.%s' % dsuf),
                 join_path(spec['netcdf'].prefix.lib,'libnetcdf.%s' % dsuf)),
            '-DNETCDF_INCLUDE_DIRS=%s;%s' %
                (spec['netcdf-cxx'].prefix.include,
                 spec['netcdf'].prefix.include),
            '-DOPENCASCADE_DIR=%s' % spec['oce'].prefix,
            '-DP4EST_DIR=%s' % spec['p4est'].prefix,
            '-DPETSC_DIR=%s' % spec['petsc'].prefix,
            '-DSLEPC_DIR=%s' % spec['slepc'].prefix,
            '-DUMFPACK_DIR=%s' % spec['suite-sparse'].prefix,
            '-DTBB_DIR=%s' % spec['tbb'].prefix,
            '-DTRILINOS_DIR=%s' % spec['trilinos'].prefix
        ])

        cmake('.', *options)

        make()
        make("test")
        make("install")

        # run some MPI examples with different solvers from PETSc and Trilinos
        env['DEAL_II_DIR'] = prefix
        # take bare-bones step-3
        with working_dir('examples/step-3'):
            cmake('.')
            make('release')
            make('run',parallel=False)

        # take step-40 which can use both PETSc and Trilinos
        # FIXME: switch step-40 to MPI run
        with working_dir('examples/step-40'):
            # list the number of cycles to speed up
            filter_file(r'(const unsigned int n_cycles = 8;)',  ('const unsigned int n_cycles = 2;'), 'step-40.cc')
            cmake('.')
            make('release')
            make('run',parallel=False)

            # change Linear Algebra to Trilinos
            filter_file(r'(#define USE_PETSC_LA.*)',  (''), 'step-40.cc')
            make('release')
            make('run',parallel=False)

        with working_dir('examples/step-36'):
            cmake('.')
            make('release')
            make('run',parallel=False)

        with working_dir('examples/step-54'):
            cmake('.')
            make('release')
            # FIXME
            # make('run',parallel=False)
