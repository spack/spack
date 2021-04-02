# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# ----------------------------------------------------------------------------

from spack import *
import os
import tempfile
import shutil
import llnl.util.tty as tty

class WrfHydro(Package):
    """
    WRF-Hydro is a community modeling system and framework
    for hydrologic modeling and model coupling.
    """

    # NCAR WRF-Hydro homepage and release tarball
    homepage = "https://ral.ucar.edu/projects/wrf_hydro/overview"
    git = "https://github.com/NCAR/wrf_hydro_nwm_public.git"
    maintainers = ['daniellivingston']
    
    url = "https://github.com/NCAR/wrf_hydro_nwm_public/archive/v5.1.2.tar.gz"

    version("master", branch="master")
    version(
        "5.1.2",
        sha256="203043916c94c597dd4204033715d0b2dc7907e2168cbe3dfef3cd9eef950eb7",
    )

    # WRF-Hydro supports multiple build configs, ostensibly
    # set as flags in trunk/NDHMS/template/setEnvar.sh.
    # Override here.
    variant(
        "hydro_d",
        default="0",
        values=("0", "1"),
        description="Enhanced diagnostic output for debugging: 0=Off, 1=On.",
    )
    variant(
        "spatial_soil",
        default="1",
        values=("0", "1"),
        description="Spatially distributed parameters for NoahMP: 0=Off, 1=On.",
    )
    variant(
        "wrf_hydro_rapid",
        default="0",
        values=("0", "1"),
        description="RAPID model: 0=Off, 1=On.",
    )
    variant(
        "wrfio_ncd_large_file_support",
        default="1",
        values=("0", "1"),
        description="Allow netCDF I/O of files larger than 2 GiB.",
    )
    variant(
        "ncep_wcoss",
        default="0",
        values=("0", "1"),
        description="WCOSS file units: 0=Off, 1=On.",
    )
    variant(
        "wrf_hydro_nudging",
        default="0",
        values=("0", "1"),
        description="Streamflow nudging: 0=Off, 1=On.",
    )

    depends_on("pkgconfig", type=("build"))
    depends_on("libtirpc")
    # WRF-Hydro dependencies
    depends_on("autoconf")
    depends_on("automake")
    depends_on("hdf5+fortran+hl+mpi")
    depends_on("m4", type="build")
    depends_on("libtool", type="build")
    depends_on("mpi")
    depends_on("netcdf-c@4.4.1.1:")
    depends_on("netcdf-fortran@4.4.4:")
    depends_on("jasper")

    def setup_environment(self, spack_env, run_env):
        nc_c_home = self.spec["netcdf-c"].prefix
        nc_f_home = self.spec["netcdf-fortran"].prefix

        spack_env.append_path("LD_LIBRARY_PATH", nc_c_home.lib)
        spack_env.append_path("LD_LIBRARY_PATH", nc_f_home.lib)
        spack_env.append_path("CPATH", nc_c_home.include)
        spack_env.set("NETCDF_INC", nc_f_home.include)
        spack_env.set("NETCDF_LIB", nc_f_home.lib)

        spack_env.set("NETCDF", self.spec["netcdf-c"].prefix)

        tty.msg("NetCDF-F installed to: " + str(nc_f_home))
        tty.msg("NetCDF-C installed to: " + str(nc_c_home))

    def install(self, spec, prefix):
        # Initialize variables used in WRF-Hydro compilation
        wrf_envar = {
            "WRF_HYDRO": "1",
            "HYDRO_D": spec.variants["hydro_d"].value,
            "SPATIAL_SOIL": spec.variants["spatial_soil"].value,
            "WRF_HYDRO_RAPID": spec.variants["wrf_hydro_rapid"].value,
            "NCEP_WCOSS": spec.variants["ncep_wcoss"].value,
            "WRFIO_NCD_LARGE_FILE_SUPPORT": spec.variants["wrfio_ncd_large_file_support"].value,
            "WRF_HYDRO_NUDGING": spec.variants["wrf_hydro_nudging"].value,
        }

        # Set the compiler flag for ./configure based on active
        # compiler family
        compiler_config = {"pgi": "1", "gcc": "2", "intel": "3"}

        try:
            configure_args = [compiler_config[self.spec.compiler.name]]
        except KeyError:
            raise InstallError(
                "Compiler not recognized nor supported: {}".format(
                    self.spec.compiler.name
                )
            )

        # Reconstruct the dict as a bash script
        set_envar_sh = ["#!/bin/bash"] + ["export %s=%s" % (key, wrf_envar[key]) for key in wrf_envar.keys()]

        tty.msg("WRF-Hydro environment variables set to: ")
        tty.msg("\n".join(set_envar_sh))

        # Configure and build in trunk/NDHMS rather than root source
        with working_dir(join_path("trunk", "NDHMS")):
            copy(join_path("template", "setEnvar.sh"), "setEnvar.sh")
            configure(*configure_args)
            start_build = Executable("./compile_offline_NoahMP.sh")

            with tempfile.NamedTemporaryFile(mode="w") as fp:
                fp.write("\n".join(set_envar_sh))
                fp.flush()
                start_build(fp.name)

        # Install compiled binaries
        mkdir(prefix.bin)

        install(
            join_path("trunk", "NDHMS", "Run", "wrf_hydro.exe"), prefix.bin
        )
        install(
            join_path("trunk", "NDHMS", "Run", "wrf_hydro_NoahMP.exe"),
            prefix.bin,
        )

        # Install the entire tree as many files are needed for running
        install_tree(".", prefix)

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def build_test(self):
        '''
        Downloads and runs the Croton NY WRF-Hydro test case, 
        as outlined in the "WRF-Hydro V5 Test Case User Guide" [0].

        [0]: https://ral.ucar.edu/sites/default/files/public/WRF-HydroV5TestCaseUserGuide_3.pdf
        '''
        from glob import glob

        check_test_success = lambda msg, infile: msg.lower() in open(infile,'r').read().lower()

        mkdir(prefix.testing)
        test_dir = prefix.testing
        src_dir = os.getcwd()

        success_msg = "model finished successfully"
        TESTCASE_URL = "https://github.com/NCAR/wrf_hydro_nwm_public/releases/download/v5.0.3/croton_NY_example_testcase.tar.gz"
        wget = which("wget")
        mpirun = which("mpirun") #self.spec['mpirun']
        tar = which("tar")

        # Download and untar test case
        with working_dir(test_dir):
            testcase = "croton_NY_example_testcase.tar.gz"
            wget("-O", testcase, TESTCASE_URL)
            tar("-xf", testcase)

        with working_dir(join_path(test_dir, "example_case")):

            for file in glob(join_path(src_dir, "trunk", "NDHMS", "Run", "*.TBL")):
                tty.msg("Copying " + file)
                shutil.copy(file, "Gridded/")

            shutil.copy(join_path(prefix.bin, "wrf_hydro.exe"), join_path("Gridded", "wrf_hydro.exe"))

        with working_dir(join_path(test_dir, "example_case", "Gridded")):
            shutil.copytree("../FORCING/", "FORCING/")

            # Run test case
            mpirun("-np", "2", "./wrf_hydro.exe")

            assert check_test_success(success_msg, "diag_hydro.00000") \
                   and check_test_success(success_msg, "diag_hydro.00001"),\
                   'Test cases failed!'

        tty.msg("WRF-Hydro test case passed")

