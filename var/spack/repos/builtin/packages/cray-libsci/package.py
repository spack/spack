# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *
from spack.util.module_cmd import get_path_args_from_module_line, module


class CrayLibsci(Package):
    """The Cray Scientific Libraries package, LibSci, is a collection of
    numerical routines optimized for best performance on Cray systems."""

    homepage = "https://docs.nersc.gov/development/libraries/libsci/"
    has_code = False  # Skip attempts to fetch source that is not available

    version("23.02.1.1")
    version("22.11.1.2")
    version("21.08.1.2")
    version("20.06.1")
    version("20.03.1")
    version("19.06.1")
    version("18.12.1")
    version("18.11.1.2")
    version("16.11.1")
    version("16.09.1")
    version("16.07.1")
    version("16.06.1")
    version("16.03.1")

    variant("shared", default=True, description="enable shared libs")
    variant("openmp", default=False, description="link with openmp")
    variant("mpi", default=False, description="link with mpi libs")

    provides("blas")
    provides("lapack")
    provides("scalapack", when="+mpi")

    canonical_names = {
        "gcc": "GNU",
        "cce": "CRAY",
        "intel": "INTEL",
        "clang": "ALLINEA",
        "aocc": "AOCC",
        "nvhpc": "NVIDIA",
        "rocmcc": "AMD",
    }

    @property
    def modname(self):
        return "cray-libsci/{0}".format(self.version)

    @property
    def external_prefix(self):
        libsci_module = module("show", self.modname).splitlines()

        for line in libsci_module:
            if "CRAY_LIBSCI_PREFIX_DIR" in line:
                return get_path_args_from_module_line(line)[0]

    @property
    def blas_libs(self):
        shared = True if "+shared" in self.spec else False
        compiler = self.spec.compiler.name

        lib = []
        if "+openmp" in self.spec and "+mpi" in self.spec:
            lib = ["libsci_{0}_mpi_mp", "libsci_{0}_mp"]
        elif "+openmp" in self.spec:
            lib = ["libsci_{0}_mp"]
        elif "+mpi" in self.spec:
            lib = ["libsci_{0}_mpi", "libsci_{0}"]
        else:
            lib = ["libsci_{0}"]

        libname = []
        for lib_fmt in lib:
            libname.append(lib_fmt.format(self.canonical_names[compiler].lower()))

        return find_libraries(libname, root=self.prefix.lib, shared=shared, recursive=False)

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def scalapack_libs(self):
        return self.blas_libs

    @property
    def libs(self):
        return self.blas_libs

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format(
                "{name} is not installable, you need to specify "
                "it as an external package in packages.yaml"
            )
        )
