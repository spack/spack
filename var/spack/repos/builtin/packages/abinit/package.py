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
    url      = "http://ftp.abinit.org/abinit-7.10.5.tar.gz"

    version('7.10.5', '276db3ebad3f57952952b5235e5813cc')

    variant('openmp', default=False, description='Use OpenMP threads')

    # Add dependencies
    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi@2:")

    depends_on("gsl")
    #depends_on("libxc")
    depends_on("etsf_io")

    depends_on("scalapack")
    #depends_on("elpa", when="+elpa")
    depends_on("fftw +float")

    depends_on("netcdf-fortran")
    depends_on("hdf5+mpi~cxx", when='+mpi')  # required for NetCDF-4 support

    #depends_on('mpi', when='+mpi')
    #depends_on('fftw~mpi', when='~mpi')
    #depends_on('fftw+mpi', when='+mpi')

    def check_variants(self, spec):
        return
        #error = 'you cannot ask for \'+{variant}\' when \'+mpi\' is not active'
        #if '+scalapack' in spec and '~mpi' in spec:
        #    raise RuntimeError(error.format(variant='scalapack'))
        #if '+elpa' in spec and ('~mpi' in spec or '~scalapack' in spec):
        #    raise RuntimeError(error.format(variant='elpa'))

    def install(self, spec, prefix):
        self.check_variants(spec)

        options = ['--prefix=%s' % prefix]
        oapp = options.append

        # MPI: let the configure script auto-detect MPI support from mpi_prefix
        oapp("--with-mpi-prefix=%s" % spec["mpi"].prefix)
        oapp("--enable-mpi=yes")
        oapp("--enable-mpi-io=yes")

        # BLAS/LAPACK
        oapp("--with-linalg-flavor=netlib+scalapack")
        linalg_fc_link = "--with-linalg-libs=-L%s -llapack -L%s -lblas " % (
               spec["lapack"].prefix.lib, spec["blas"].prefix.lib)

        #if '+scalapack' in spec:
        linalg_fc_link += spec['scalapack'].fc_link
        #if '+elpa' in spec:

        oapp(linalg_fc_link)

        # FFTW3: select sequential or threaded version if +openmp
        fftlibs = "-lfftw3 -lfftw3f"
        if '+openmp' in spec:
            oapp('--enable-openmp=yes')
            fftlibs = "-lfftw3_omp -lfftw3 -lfftw3f"

        options.extend([
            "--with-fft-flavor=fftw3",
            "--with-fft-incs=-I%s" % spec["fftw"].prefix.include,
            "--with-fft-libs=-L%s %s" % (spec["fftw"].prefix.lib, fftlibs),
        ])

        # LibXC library
        #options.extend([
        #    "with_libxc_incs=-I%s" % spec["libxc"].prefix.include,
        #    "with_libxc_libs=-L%s -lxcf90 -lxc" % spec["libxc"].prefix.lib,
        #])

        #oapp("--with-trio-flavor=netcdf+etsf_io-fallback")
        oapp("--with-trio-flavor=netcdf+etsf_io")

        # ETSF_IO
        options.extend([
            "--with-etsf-io-incs=-I%s" % spec["etsf_io"].prefix.include,
            "--with-etsf-io-libs=-L%s -letsf_io_utils -letsf_io" % spec["etsf_io"].prefix.lib,
        ])

        # Netcdf4/HDF5
        hdf_libs = "-L%s -lhdf5_hl -lhdf5" % spec["hdf5"].prefix.lib  
        options.extend([
            "--with-netcdf-incs=-I%s" % spec["netcdf-fortran"].prefix.include,
            "--with-netcdf-libs=-L%s -lnetcdff -lnetcdf %s" % (spec["netcdf-fortran"].prefix.lib, hdf_libs),
        ])

        oapp("--with-dft-flavor=atompaw+libxc+wannier90")
        oapp("--with-math-flavor=gsl")

        # Add a list of directories to search
        #search_list = []
        #for name, dependency_spec in spec.dependencies.iteritems():
        #    search_list.extend([dependency_spec.prefix.lib,
        #                        dependency_spec.prefix.lib64])
        #search_list = " ".join(search_list)
        #options.append('LIBDIRS=%s' % search_list)

        configure(*options)
        make()
        make("install")
