# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class EtsfIo(Package):
    """ETSF_IO is a library implementing the Nanoquanta/ETSF file
    format specifications.

    ETSF_IO enables an architecture-independent exchange of crystallographic
    data, electronic wavefunctions, densities and potentials, as well as
    spectroscopic data. It is meant to be used by quantum-physical and
    quantum-chemical applications relying upon Density Functional Theory (DFT).
    """

    homepage = "https://github.com/ElectronicStructureLibrary/libetsf_io"
    url = "https://launchpad.net/etsf-io/1.0/1.0.4/+download/etsf_io-1.0.4.tar.gz"

    version("1.0.4", sha256="3140c2cde17f578a0e6b63acb27a5f6e9352257a1371a17b9c15c3d0ef078fa4")

    variant("mpi", default=True, description="Add MPI support")

    depends_on("netcdf-fortran")
    depends_on("hdf5+mpi~cxx", when="+mpi")  # required for NetCDF-4 support

    patch("tests_module.patch")
    patch("tests_init.patch")

    def install(self, spec, prefix):
        options = ["--prefix=%s" % prefix]
        oapp = options.append

        # Specify installation directory for Fortran module files
        # Default is [INCLUDEDIR/FC_TYPE]
        oapp("--with-moduledir=%s" % prefix.include)

        # Netcdf4/HDF
        hdf_libs = "-L%s -lhdf5_hl -lhdf5" % spec["hdf5"].prefix.lib
        options.extend(
            [
                "--with-netcdf-incs=-I%s" % spec["netcdf-fortran"].prefix.include,
                "--with-netcdf-libs=-L%s -lnetcdff -lnetcdf %s"
                % (spec["netcdf-fortran"].prefix.lib, hdf_libs),
            ]
        )

        configure(*options)

        make()
        make("check")
        make("install")

    def test(self):
        """Run this smoke test when requested explicitly"""

        # Test is to run "etsf_io --help"
        spec = self.spec
        exe = join_path(spec["etsf-io"].prefix.bin, "etsf_io")
        options = ["--help"]
        purpose = "Check etsf_io can execute (--help)"
        expected = ["Usage: etsf_io"]

        self.run_test(
            exe,
            options=options,
            expected=expected,
            status=[0],
            installed=False,
            purpose=purpose,
            skip_missing=False,
            work_dir=None,
        )
