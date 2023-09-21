# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from collections import defaultdict
from llnl.util import lang
from spack.package import *


class Rttov(Package):
    """RTTOV (Radiative Transfer for TOVS) is a very fast radiative transfer
    model for passive visible, infrared and microwave downward-viewing satellite
    radiometers, spectrometers and interferometers."""

    homepage = "https://nwp-saf.eumetsat.int/site/software/rttov/"
    manual_download = True

    version("13.1", sha256="f3bec1ca3ba952bc49e19d851144f9d51126bfe59f473be4992eac0b3366dbb2")
    version("12.3", sha256="c9e71861c2fae7b6e793405dc23f0fe42ced98b0a8313865ed480edd71f12f57")

    variant("hdf5", default=False, description="Enable HDF5 support")
    variant("netcdf", default=False, description="Enable NetCDF support")
    variant("openmp", default=False, description="Enable OpenMP support")

    depends_on("lapack")
    # There is no direct dependency on BLAS API but we might not be able to link
    # to 'lapack:fortran' libraries without linking to 'blas:fortran' ones when
    # using an external customized installation of LAPACK. For example, in case
    # of libraries that are shipped together with PGI/NVIDIA compilers,
    # subroutine DGETRF, which is part of the LAPACK API, is implemented not in
    # liblapack.so but in libblas.so.
    depends_on("blas")

    depends_on("netcdf-fortran", when="+netcdf")
    depends_on("hdf5+fortran+hl", when="+hdf5")

    depends_on("perl", type="build")

    # Fix kind inconsistency:
    patch("kind_inconsistency/mod_brdf_atlas.patch", when="@12.1:")
    patch("kind_inconsistency/rttov_types.patch", when="@12.3")

    def url_for_version(self, version):
        return "file://{0}/rttov{1}.tar.{2}".format(
            os.getcwd(), version.joined, "gz" if int(str(version.up_to(1))) <= 12 else "xz"
        )

    @when("%nag")
    def patch(self):
        # A number of source files assume that the kinds of integer and real
        # variables are specified in bytes. However, the NAG compiler accepts
        # such code only with an additional compiler flag -kind=byte. We do not
        # simply add the flag because all user applications would have to be
        # compiled with this flag too, which goes against one of the purposes of
        # using the NAG compiler: make sure the code does not contradict the
        # Fortran standards. The following logic could have been implemented as
        # regular patch files, which would, however, be quite large. We would
        # also have to introduce several versions of each patch file to support
        # different versions of the package.

        patch_kind_files = [
            "src/main/rttov_fastem5.F90",
            "src/main/rttov_fastem5_ad.F90",
            "src/main/rttov_fastem5_k.F90",
            "src/main/rttov_fastem5_tl.F90",
        ]

        filter_file(
            r"(?i)(real\(\d+,)8(\))",
            "\\1selected_real_kind(13, 300)\\2",
            *patch_kind_files,
            ignore_absent=True,
        )

    @property
    def libs(self):
        basenames = ["other", "emis_atlas", "brdf_atlas", "parallel", "coef_io"]
        if "+hdf5" in self.spec:
            basenames.append("hdf")
        basenames.append("main")
        return find_libraries(
            ["librttov{0}_{1}".format(self.spec.version.up_to(1), n) for n in basenames],
            root=self.prefix.lib,
            shared=False,
        )

    def install(self, spec, prefix):
        build_aux_dir = join_path(self.stage.source_path, "build")

        arch_filename = "spack"
        # We provide the variables on the command line or via the environment
        # instead of writing them to an arch file:
        with open(join_path(build_aux_dir, "arch", arch_filename), "w"):
            pass

        build_dirname = "spack-build"

        makefile_args = [
            "ARCH={0}".format(arch_filename),
            "INSTALLDIR={0}".format(build_dirname),
            "AR=ar r",
        ]

        makefile_vars = defaultdict(list)

        # Paths to the compilers are set by Spack automatically via the
        # environment variables: CC, FC and F77. However the makefile of the
        # package expects the Fortran 77 compiler to be set as FC77. Therefore,
        # we provide the value on the command line:
        makefile_vars["FC77"].append(self.compiler.f77)

        # The following is taken from files in the 'build/arch' directory:
        if self.compiler.name == "gcc" or self._compiler_is_mixed_gfortran():
            makefile_vars["FFLAGS_ARCH"].append("-O3 -ffree-line-length-none")
        elif self.compiler.name == "intel":
            common_flags = "-O3 -fp-model source"
            makefile_vars["FFLAGS_ARCH"].append(common_flags)
            target_basenames = ["rttov_opdep_9_ad", "rttov_opdep_9_k"]
            if self.spec.satisfies("@13:"):
                target_basenames.extend(["rttov_opdep_13_ad", "rttov_opdep_13_k"])
            for f in target_basenames:
                makefile_vars["FFLAGS_ARCH_{0}".format(f)].extend(["-unroll0", common_flags])
            if "+openmp" in self.spec:
                for f in ["rttov_mfasis_ad", "rttov_mfasis_k"]:
                    makefile_vars["FFLAGS_ARCH_{0}".format(f)].append("-O2 -fp-model source")
        elif self.compiler.name == "nag":
            common_flags = "-maxcontin=500"
            makefile_vars["FFLAGS_ARCH"].extend(["-O4", common_flags])
            makefile_vars["FFLAGS_ARCH_rttov_unix_env"].extend(
                ["-DRTTOV_USE_F90_UNIX_ENV", "-O4", common_flags]
            )
            if self.spec.satisfies("@13:"):
                for f in ["rttov_fresnel_ad", "rttov_fresnel_k"]:
                    makefile_vars["FFLAGS_ARCH_{0}".format(f)].extend(["-O0", common_flags])
        elif self.compiler.name in ["pgi", "nvhpc"]:
            common_flags = "-Kieee -notraceback"
            makefile_vars["FFLAGS_ARCH"].extend(
                ["-O2", "-fast" if "+openmp" in self.spec else "-fastsse", common_flags]
            )
            makefile_vars["FFLAGS_ARCH_rttov_dom_setup_profile"].extend(["-O1", common_flags])
        else:
            makefile_vars["FFLAGS_ARCH"].append("-O2")

        if "+openmp" in self.spec:
            openmp_flag = self.compiler.openmp_flag
            if self._compiler_is_mixed_gfortran():
                from spack.compilers.gcc import Gcc

                openmp_flag = Gcc.openmp_flag

            for var, val in makefile_vars.items():
                if var.startswith("FFLAGS_ARCH"):
                    val.append(openmp_flag)
            makefile_vars["LDFLAGS_ARCH"].append(openmp_flag)

        if "+netcdf" in self.spec:
            makefile_vars["FFLAGS_EXTERN"].append("-D_RTTOV_NETCDF")
            makefile_vars["LDFLAGS_EXTERN"].append(self.spec["netcdf-fortran"].libs.link_flags)

        if "+hdf5" in self.spec:
            makefile_vars["FFLAGS_EXTERN"].append("-D_RTTOV_HDF")
            makefile_vars["LDFLAGS_EXTERN"].append(self.spec["hdf5:fortran,hl"].libs.link_flags)

        lapack_libs = self.spec["lapack:fortran"].libs
        lapack_libs += self.spec["blas:fortran"].libs
        makefile_vars["LDFLAGS_EXTERN"].append(lapack_libs.link_flags)

        makefile_args.extend(
            ["{0}={1}".format(var, " ".join(val)) for var, val in makefile_vars.items()]
        )

        with working_dir(join_path(self.stage.source_path, "src")):
            makefile_pl = Executable(join_path(build_aux_dir, "Makefile.PL"))
            makefile_pl(
                "RTTOV_HDF={0}".format("1" if "+hdf5" in self.spec else "0"),
                "RTTOV_F2PY=0",
                "RTTOV_USER_LAPACK=1",
            )
            make(*makefile_args, parallel=False)

        build_dir = join_path(self.stage.source_path, build_dirname)

        install_tree(join_path(build_dir, "bin"), prefix.bin)
        install_tree(join_path(build_dir, "lib"), prefix.lib)

        # Install the Fortran module and include files to the same directory:
        install_tree(join_path(build_dir, "include"), prefix.include)
        install_tree(join_path(build_dir, "mod"), prefix.include)

    @lang.memoized
    def _compiler_is_mixed_gfortran(self):
        if self.compiler.name == "gcc" or not self.compiler.fc:
            return False

        fc_name, _, _ = os.path.basename(self.compiler.fc).partition("-")

        if not fc_name:
            return False

        from spack.compilers.gcc import Gcc

        return fc_name in Gcc.fc_names
