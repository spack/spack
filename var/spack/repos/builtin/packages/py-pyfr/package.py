# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyfr(PythonPackage, CudaPackage, ROCmPackage):
    """PyFR is an open-source Python based framework for solving
    advection-diffusion type problems on streaming architectures
    using the Flux Reconstruction approach of Huynh."""

    homepage = "http://www.pyfr.org/"
    pypi = "pyfr/pyfr-1.13.0.tar.gz"
    git = "https://github.com/PyFR/PyFR/"
    maintainers = ["MichaelLaufer"]

    # git branches
    version("develop", branch="develop")
    version("master", branch="master")

    # pypi releases
    version(
        "1.15.0",
        sha256="6a634b9d32447f45d3c24c9de0ed620a0a0a781be7cc5e57b1c1bf44a4650d8d",
    )
    version(
        "1.14.0",
        sha256="ebf40ce0896cce9ac802e03fd9430b5be30ea837c31224531a6d5fd68f820766",
    )
    version(
        "1.13.0",
        sha256="ac6ecec738d4e23799ab8c50dea9bdbd7d37bc971bd33f22720c5a230b8e7b2f",
    )

    variant("metis", default=True, description="Metis for mesh partitioning")
    variant("scotch", default=False, description="Scotch for mesh partitioning")
    variant("cuda", default=False, description="CUDA backend support")
    variant("hip", default=False, description="HIP backend support")
    variant("libxsmm", default=True, description="LIBXSMM for OpenMP backend")
    variant("scipy", default=True, description="Scipy acceleration for point sampling")

    # Required dependencies
    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-gimmik@2.3:2", when="@:1.14.0", type=("build", "run"))
    depends_on("py-gimmik@3", when="@1.15.0:", type=("build", "run"))
    depends_on("py-h5py@2.10:", type=("build", "run"))
    depends_on("py-mako@1.0.0:", type=("build", "run"))
    depends_on("py-mpi4py@3.1.0:", type=("build", "run"))
    depends_on("py-numpy@1.20:+blas", type=("build", "run"))
    depends_on("py-platformdirs@2.2.0:", type=("build", "run"))
    depends_on("py-pytools@2016.2.1:", type=("build", "run"))

    # Optional dependencies
    depends_on("py-scipy", when="+scipy", type=("build", "run"))
    depends_on("metis@5.0:", when="+metis", type=("run"))
    depends_on("scotch@6.0:", when="+scotch", type=("run"))
    depends_on("cuda@8.0: +allow-unsupported-compilers", when="@:1.14.0 +cuda", type=("run"))
    depends_on("cuda@11.4.0: +allow-unsupported-compilers", when="@1.15.0: +cuda", type=("run"))
    depends_on("rocblas@5.2.0:", when="+hip", type=("run"))
    depends_on("libxsmm@1.18:+shared blas=0", when="+libxsmm", type=("run"))

    # Conflicts for compilers not supporting OpenMP 5.1+ from v1.15.0:
    conflicts("%gcc@:11", when="@1.15.0: +libxsmm", msg="OpenMP 5.1+ supported compiler required!")

    # Explicitly set library path for dependencies
    def setup_run_environment(self, env):
        if "+metis" in self.spec:
            lib_path = find_libraries(
                    "libmetis", root=self.spec["metis"].prefix.lib, recursive=False
                )
            env.set("PYFR_METIS_LIBRARY_PATH", lib_path[0])

        if "+scotch" in self.spec:
            lib_path = find_libraries(
                    "libscotch", root=self.spec["scotch"].prefix.lib, recursive=False
                )
            env.set("PYFR_SCOTCH_LIBRARY_PATH", lib_path[0])

        if "+libxsmm" in self.spec:
            lib_path = find_libraries(
                    "libxsmm", root=self.spec["libxsmm"].prefix.lib, recursive=False
                )
            env.set("PYFR_XSMM_LIBRARY_PATH", lib_path[0])

        if "+cuda" in self.spec:
            lib_path = find_libraries(
                    "libcublas", root=self.spec["cuda"].prefix, recursive=True
                )
            env.set("PYFR_CUBLAS_LIBRARY_PATH", lib_path[0])

        if "+hip" in self.spec:
            lib_path = find_libraries(
                    "libamdhip64", root=self.spec["hip"].prefix, recursive=True
                )
            env.set("PYFR_AMDHIP64_LIBRARY_PATH", lib_path[0])

            lib_path = find_libraries(
                    "librocblas", root=self.spec["rocblas"].prefix, recursive=True
                )
            env.set("PYFR_ROCBLAS_LIBRARY_PATH", lib_path[0])
