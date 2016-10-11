from spack import *

import os

class Abinit(Package):
    """ABINIT is a package whose main program allows one to find the total energy,
    charge density and electronic structure of systems made of electrons and nuclei
    (molecules and periodic solids) within Density Functional Theory (DFT), using
    pseudopotentials and a planewave or wavelet basis. ABINIT also includes options
    to optimize the geometry according to the DFT forces and stresses, or to perform
    molecular dynamics simulations using these forces, or to generate dynamical
    matrices, Born effective charges, and dielectric tensors, based on
    Density-Functional Perturbation Theory, and many more properties. Excited states
    can be computed within the Many-Body Perturbation Theory (the GW approximation
    and the Bethe-Salpeter equation), and Time-Dependent Density Functional Theory
    (for molecules). In addition to the main ABINIT code, different utility programs
    are provided."""

    homepage = "http://www.abinit.org"
    url      = "http://ftp.abinit.org/abinit-8.0.8b.tar.gz"

    # Versions before 8.0.8b are not supported.
    version("8.0.8b", "abc9e303bfa7f9f43f95598f87d84d5d")

    variant('mpi', default=True, description='Builds with mpi support. Requires MPI2+')
    variant('openmp', default=False, description='Enables OpenMP threads. Use threaded FFTW3')
    variant('scalapack', default=False, description='Enables scalapack support. Requires MPI')
    #variant('elpa', default=False, description='Uses elpa instead of scalapack. Requires MPI')

    # Add dependencies
    depends_on("blas", when="~openmp")
    depends_on("blas+openmp", when="+openmp")
    depends_on("lapack")

	# Require MPI2+
    depends_on("mpi@2:", when="+mpi")

    depends_on("scalapack", when="+scalapack+mpi")
    #depends_on("elpa", when="+elpa+mpi~openmp")
    #depends_on("elpa+openmp", when="+elpa+mpi+openmp")

    depends_on("fftw+float", when="~openmp")
    depends_on("fftw+float+openmp", when="+openmp")

    depends_on("netcdf-fortran")
    depends_on("hdf5+mpi", when='+mpi')  # required for NetCDF-4 support

    # pin libxc version
    depends_on("libxc@2.2.1")

    def check_variants(self, spec):
        error = 'you cannot ask for \'+{variant}\' when \'+mpi\' is not active'

        if '+scalapack' in spec and '~mpi' in spec:
            raise RuntimeError(error.format(variant='scalapack'))

        if '+elpa' in spec and ('~mpi' in spec or '~scalapack' in spec):
            raise RuntimeError(error.format(variant='elpa'))

    def install(self, spec, prefix):
        self.check_variants(spec)

        options = ['--prefix=%s' % prefix]
        oapp = options.append

        if '+mpi' in spec:
            # MPI version: let the configure script auto-detect MPI support from mpi_prefix
            oapp("--with-mpi-prefix=%s" % spec["mpi"].prefix)
            oapp("--enable-mpi=yes")
            oapp("--enable-mpi-io=yes")

		# Activate OpenMP in Abinit Fortran code.
        if '+openmp' in spec:
            options.append('--enable-openmp=yes')

        # BLAS/LAPACK
        if '+scalapack' in spec:
            oapp("--with-linalg-flavor=custom+scalapack")
            linalg_fc_link = "--with-linalg-libs=-L%s -llapack -L%s -lblas " % (
                spec["lapack"].prefix.lib, spec["blas"].prefix.lib)
            linalg_fc_link += spec['scalapack'].fc_link

        #elif '+elpa' in spec:
        else:
            oapp("--with-linalg-flavor=custom")
            linalg_fc_link = "--with-linalg-libs=-L%s -llapack -L%s -lblas " % (
               spec["lapack"].prefix.lib, spec["blas"].prefix.lib)

        oapp(linalg_fc_link)

        # FFTW3: select sequential or threaded version if +openmp
        fftlibs = "-lfftw3 -lfftw3f"
        if '+openmp' in spec:
            fftlibs = "-lfftw3_omp -lfftw3 -lfftw3f"

        options.extend([
            "--with-fft-flavor=fftw3", # threads
            "--with-fft-incs=-I%s" % spec["fftw"].prefix.include,
            "--with-fft-libs=-L%s %s" % (spec["fftw"].prefix.lib, fftlibs),
        ])

        oapp("--with-dft-flavor=atompaw+libxc")

        # LibXC library
        options.extend([
            "with_libxc_incs=-I%s" % spec["libxc"].prefix.include,
            "with_libxc_libs=-L%s -lxcf90 -lxc" % spec["libxc"].prefix.lib,
        ])

        # Netcdf4/HDF5
        oapp("--with-trio-flavor=netcdf")
        hdf_libs = "-L%s -lhdf5_hl -lhdf5" % spec["hdf5"].prefix.lib  
        options.extend([
            "--with-netcdf-incs=-I%s" % spec["netcdf-fortran"].prefix.include,
            "--with-netcdf-libs=-L%s -lnetcdff -lnetcdf %s" % (
               spec["netcdf-fortran"].prefix.lib, hdf_libs),
        ])

        configure(*options)
        make()
        make("install")
