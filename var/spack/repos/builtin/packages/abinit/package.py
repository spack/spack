##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
#
# Author: Matteo Giantomassi <matteo.giantomassiNOSPAM AT uclouvain.be>
# Date: October 11, 2016
from spack import *


class Abinit(Package):
    """ABINIT is a package whose main program allows one to find the total
    energy, charge density and electronic structure of systems made of
    electrons and nuclei (molecules and periodic solids) within
    Density Functional Theory (DFT), using pseudopotentials and a planewave
    or wavelet basis. ABINIT also includes options to optimize the geometry
    according to the DFT forces and stresses, or to perform molecular dynamics
    simulations using these forces, or to generate dynamical matrices,
    Born effective charges, and dielectric tensors, based on Density-Functional
    Perturbation Theory, and many more properties. Excited states can be
    computed within the Many-Body Perturbation Theory (the GW approximation and
    the Bethe-Salpeter equation), and Time-Dependent Density Functional Theory
    (for molecules). In addition to the main ABINIT code, different utility
    programs are provided.
    """

    homepage = "http://www.abinit.org"
    url      = "http://ftp.abinit.org/abinit-8.0.8b.tar.gz"

    # Versions before 8.0.8b are not supported.
    version("8.0.8b", "abc9e303bfa7f9f43f95598f87d84d5d")

    variant('mpi', default=True,
            description='Builds with MPI support. Requires MPI2+')
    variant('openmp', default=False,
            description='Enables OpenMP threads. Use threaded FFTW3')
    variant('scalapack', default=False,
            description='Enables scalapack support. Requires MPI')
    # variant('elpa', default=False,
    # description='Uses elpa instead of scalapack. Requires MPI')

    # TODO: To be tested.
    # It was working before the last `git pull` but now all tests crash.
    # For the time being, the default is netcdf3 and the internal fallbacks
    # FIXME: rename (trio?) and use multivalued variants to cover
    # --with-trio-flavor={netcdf, none}
    # Note that Abinit@8: does not support etsf_io anymore because it is not
    # compatible with HDF5 and MPI-IO
    variant('hdf5', default=False,
            description='Enables HDF5+Netcdf4 with MPI. WARNING: experimental')

    # Add dependencies
    # currently one cannot forward options to virtual packages, see #1712.
    # depends_on("blas", when="~openmp")
    # depends_on("blas+openmp", when="+openmp")
    depends_on('blas')
    depends_on("lapack")

    # Require MPI2+
    depends_on("mpi@2:", when="+mpi")

    depends_on("scalapack", when="+scalapack+mpi")
    # depends_on("elpa", when="+elpa+mpi~openmp")
    # depends_on("elpa+openmp", when="+elpa+mpi+openmp")

    depends_on("fftw+float", when="~openmp")
    depends_on("fftw+float+openmp", when="+openmp")

    depends_on("netcdf-fortran", when="+hdf5")
    depends_on("hdf5+mpi", when='+mpi+hdf5')  # required for NetCDF-4 support

    # pin libxc version
    depends_on("libxc@2.2.1")

    def validate(self, spec):
        """
        Checks if incompatible variants have been activated at the same time

        :param spec: spec of the package
        :raises RuntimeError: in case of inconsistencies
        """
        error = 'you cannot ask for \'+{variant}\' when \'+mpi\' is not active'

        if '+scalapack' in spec and '~mpi' in spec:
            raise RuntimeError(error.format(variant='scalapack'))

        if '+elpa' in spec and ('~mpi' in spec or '~scalapack' in spec):
            raise RuntimeError(error.format(variant='elpa'))

    def install(self, spec, prefix):
        self.validate(spec)

        options = ['--prefix=%s' % prefix]
        oapp = options.append

        if '+mpi' in spec:
            # MPI version:
            # let the configure script auto-detect MPI support from mpi_prefix
            oapp("--with-mpi-prefix=%s" % spec["mpi"].prefix)
            oapp("--enable-mpi=yes")
            oapp("--enable-mpi-io=yes")

        # Activate OpenMP in Abinit Fortran code.
        if '+openmp' in spec:
            oapp('--enable-openmp=yes')

        # BLAS/LAPACK
        if '+scalapack' in spec:
            oapp("--with-linalg-flavor=custom+scalapack")
            linalg = (spec['scalapack'].libs +
                      spec['lapack'].libs + spec['blas'].libs)

        # elif '+elpa' in spec:
        else:
            oapp("--with-linalg-flavor=custom")
            linalg = spec['lapack'].libs + spec['blas'].libs

        oapp("--with-linalg-libs=%s" % linalg.ld_flags)

        # FFTW3: use sequential or threaded version if +openmp
        fftflavor, fftlibs = "fftw3", "-lfftw3 -lfftw3f"
        if '+openmp' in spec:
            fftflavor = "fftw3-threads"
            fftlibs = "-lfftw3_omp -lfftw3 -lfftw3f"

        options.extend([
            "--with-fft-flavor=%s" % fftflavor,
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
        if "+hdf5" in spec:
            oapp("--with-trio-flavor=netcdf")
            # Since version 8, Abinit started to use netcdf4 + hdf5 and we have
            # to link with -lhdf5_hl -lhdf5
            hdf_libs = "-L%s -lhdf5_hl -lhdf5" % spec["hdf5"].prefix.lib
            options.extend([
                "--with-netcdf-incs=-I%s" % (
                    spec["netcdf-fortran"].prefix.include),
                "--with-netcdf-libs=-L%s -lnetcdff -lnetcdf %s" % (
                    spec["netcdf-fortran"].prefix.lib, hdf_libs),
            ])
        else:
            # In Spack we do our best to avoid building any internally provided
            # dependencies, such as netcdf3 in this case.
            oapp("--with-trio-flavor=none")

        configure(*options)
        make()

        # make("check")
        # make("tests_in")
        make("install")
