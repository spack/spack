# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os.path import dirname, isdir

from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiMkl(IntelOneApiLibraryPackage):
    """Intel oneAPI Math Kernel Library (Intel oneMKL; formerly Intel Math
    Kernel Library or Intel MKL), is a library of optimized math
    routines for science, engineering, and financial
    applications. Core math functions include BLAS, LAPACK,
    ScaLAPACK, sparse solvers, fast Fourier transforms, and vector
    math.

    """

    maintainers("rscohn2")

    homepage = (
        "https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onemkl.html"
    )

    version(
        "2024.0.0",
        url="https://registrationcenter-download.intel.com/akdlm//IRC_NAS/86d6a4c1-c998-4c6b-9fff-ca004e9f7455/l_onemkl_p_2024.0.0.49673_offline.sh",
        sha256="2a3be7d01d75ba8cc3059f9a32ae72e5bfc93e68e72e94e79d7fa6ea2f7814de",
        expand=False,
    )
    version(
        "2023.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/adb8a02c-4ee7-4882-97d6-a524150da358/l_onemkl_p_2023.2.0.49497_offline.sh",
        sha256="4a0d93da85a94d92e0ad35dc0fc3b3ab7f040bd55ad374c4d5ec81a57a2b872b",
        expand=False,
    )
    version(
        "2023.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/cd17b7fe-500e-4305-a89b-bd5b42bfd9f8/l_onemkl_p_2023.1.0.46342_offline.sh",
        sha256="cc28c94cab23c185520b93c5a04f3979d8da6b4c90cee8c0681dd89819d76167",
        expand=False,
    )
    version(
        "2023.0.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/19138/l_onemkl_p_2023.0.0.25398_offline.sh",
        sha256="0d61188e91a57bdb575782eb47a05ae99ea8eebefee6b2dfe20c6708e16e9927",
        expand=False,
    )
    version(
        "2022.2.1",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/19038/l_onemkl_p_2022.2.1.16993_offline.sh",
        sha256="eedd4b795720de776b1fc5f542ae0fac37ec235cdb567f7c2ee3182e73e3e59d",
        expand=False,
    )
    version(
        "2022.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18898/l_onemkl_p_2022.2.0.8748_offline.sh",
        sha256="07d7caedd4b9f025c6fd439a0d2c2f279b18ecbbb63cadb864f6c63c1ed942db",
        expand=False,
    )
    version(
        "2022.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18721/l_onemkl_p_2022.1.0.223_offline.sh",
        sha256="4b325a3c4c56e52f4ce6c8fbb55d7684adc16425000afc860464c0f29ea4563e",
        expand=False,
    )
    version(
        "2022.0.2",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18483/l_onemkl_p_2022.0.2.136_offline.sh",
        sha256="134b748825a474acc862bb4a7fada99741a15b7627cfaa6ba0fb05ec0b902b5e",
        expand=False,
    )
    version(
        "2022.0.1",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18444/l_onemkl_p_2022.0.1.117_offline.sh",
        sha256="22afafbe2f3762eca052ac21ec40b845ff2f3646077295c88c2f37f80a0cc160",
        expand=False,
    )
    version(
        "2021.4.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18222/l_onemkl_p_2021.4.0.640_offline.sh",
        sha256="9ad546f05a421b4f439e8557fd0f2d83d5e299b0d9bd84bdd86be6feba0c3915",
        expand=False,
    )
    version(
        "2021.3.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/17901/l_onemkl_p_2021.3.0.520_offline.sh",
        sha256="a06e1cdbfd8becc63440b473b153659885f25a6e3c4dcb2907ad9cd0c3ad59ce",
        expand=False,
    )
    version(
        "2021.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/17757/l_onemkl_p_2021.2.0.296_offline.sh",
        sha256="816e9df26ff331d6c0751b86ed5f7d243f9f172e76f14e83b32bf4d1d619dbae",
        expand=False,
    )
    version(
        "2021.1.1",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/17402/l_onemkl_p_2021.1.1.52_offline.sh",
        sha256="818b6bd9a6c116f4578cda3151da0612ec9c3ce8b2c8a64730d625ce5b13cc0c",
        expand=False,
    )

    variant("shared", default=True, description="Builds shared library")
    variant("ilp64", default=False, description="Build with ILP64 support")
    variant(
        "cluster", default=False, description="Build with cluster support: scalapack, blacs, etc"
    )
    variant(
        "mpi_family",
        default="none",
        values=("none", "mpich", "openmpi"),
        description="MPI family",
        multi=False,
    )

    variant(
        "threads",
        default="none",
        description="Multithreading support",
        values=("openmp", "tbb", "none"),
        multi=False,
    )

    depends_on("tbb")
    # cluster libraries need mpi
    depends_on("mpi", when="+cluster")

    provides("fftw-api@3")
    provides("scalapack", when="+cluster")
    provides("mkl")
    provides("lapack", "blas")

    @property
    def v2_layout_versions(self):
        return "@2024:"

    @property
    def component_dir(self):
        return "mkl"

    @property
    def libs(self):
        shared = self.spec.satisfies("+shared")

        libs = self._find_mkl_libs(shared)

        system_libs = find_system_libraries(["libpthread", "libm", "libdl"])
        if shared:
            return libs + system_libs
        else:
            return IntelOneApiStaticLibraryList(libs, system_libs)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Only if environment modifications are desired (default is +envmods)
        if self.spec.satisfies("+envmods"):
            env.set("MKLROOT", self.component_prefix)
            env.append_path("PKG_CONFIG_PATH", self.component_prefix.lib.pkgconfig)

    def _find_mkl_libs(self, shared):
        libs = []

        if self.spec.satisfies("+cluster"):
            libs.extend([self._xlp64_lib("libmkl_scalapack"), "libmkl_cdft_core"])

        libs.append(self._xlp64_lib("libmkl_intel"))
        if self.spec.satisfies("threads=tbb"):
            libs.append("libmkl_tbb_thread")
        elif self.spec.satisfies("threads=openmp"):
            if self.spec.satisfies("%oneapi") or self.spec.satisfies("%intel"):
                libs.append("libmkl_intel_thread")
            else:
                libs.append("libmkl_gnu_thread")
        else:
            libs.append("libmkl_sequential")

        libs.append("libmkl_core")

        if self.spec.satisfies("+cluster"):
            if any(
                self.spec.satisfies(m)
                for m in [
                    "^intel-oneapi-mpi",
                    "^intel-mpi",
                    "^mpich",
                    "^cray-mpich",
                    "mpi_family=mpich",
                ]
            ):
                libs.append(self._xlp64_lib("libmkl_blacs_intelmpi"))
            elif any(
                self.spec.satisfies(m) for m in ["^openmpi", "^hpcx-mpi", "mpi_family=openmpi"]
            ):
                libs.append(self._xlp64_lib("libmkl_blacs_openmpi"))
            else:
                raise RuntimeError(
                    (
                        "intel-oneapi-mkl +cluster requires one of ^intel-oneapi-mpi, "
                        "^intel-mpi, ^mpich, ^cray-mpich, mpi_family=mpich, ^openmpi, "
                        "^hpcx-mpi, or mpi_family=openmpi"
                    )
                )

        lib_path = (
            self.component_prefix.lib if self.v2_layout else self.component_prefix.lib.intel64
        )
        lib_path = lib_path if isdir(lib_path) else dirname(lib_path)

        resolved_libs = find_libraries(libs, lib_path, shared=shared)
        # Add MPI libraries for cluster support. If MPI is not in the
        # spec, then MKL is externally installed and application must
        # link with MPI libaries. If MPI is in spec, but there are no
        # libraries, then the package (e.g. hpcx-mpi) relies on the
        # compiler wrapper to add the libraries.
        try:
            if self.spec.satisfies("+cluster ^mpi"):
                resolved_libs = resolved_libs + self.spec["mpi"].libs
        except spack.error.NoLibrariesError:
            pass
        return resolved_libs

    def _xlp64_lib(self, lib):
        return lib + ("_ilp64" if self.spec.satisfies("+ilp64") else "_lp64")

    @run_after("install")
    def fixup_prefix(self):
        # The motivation was to provide a more standard layout so mkl
        # would be more likely to work as a virtual dependence. I am
        # not sure if this mechanism is useful and it became a problem
        # for mpi so disabling for v2_layout.
        if self.v2_layout:
            return
        self.symlink_dir(self.component_prefix.include, self.prefix.include)
        self.symlink_dir(self.component_prefix.lib, self.prefix.lib)
