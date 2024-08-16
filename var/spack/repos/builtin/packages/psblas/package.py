# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class Psblas(AutotoolsPackage):
    """The PSBLAS library, developed with the aim to facilitate the
    parallelization of computationally intensive scientific applications, is
    designed to address parallel implementation of iterative solvers for sparse
    linear systems through the distributed memory paradigm. It includes routines
    for multiplying sparse matrices by dense matrices, solving block diagonal
    systems with triangular diagonal entries, preprocessing sparse matrices,
    and contains additional routines for dense matrix operations. The current
    implementation of PSBLAS addresses a distributed memory execution model
    operating with message passing.
    """

    homepage = "https://psctoolkit.github.io/products/psblas/"
    url = "https://github.com/sfilippone/psblas3/archive/refs/tags/v3.8.0.tar.gz"
    git = "https://github.com/sfilippone/psblas3.git"

    tags = ["sparse-blas", "matrices", "vectors", "linear-equation", "spmv"]

    maintainers = ["ivan-pi"]

    version("development", branch="development")

    version('3.8.0-2', sha256="86a76bb0987edddd4c10c810d7f18e13742aadc66ac14ad3679669809c1184fa")
    version("3.8.0-1", sha256="dca593010f258af669eb40d92c4934eaaa016ef17280d4ab1208afc3d5aa13f0")
    version("3.8.0", sha256="0eaef8f5fd41313ee1925a54bda33c5e1756a6d14b679c54e8423556881875e8")
    version("3.7.1", sha256="a440eac162728f4943dde24c92c10abdae3c2aca00fe94f862b68772a010d73d")
    version("3.7.0", sha256="55f6f663c0cd8c54f46c45dfe448e5e95e6ebcf4de6cf86b0a9c769357357d74")

    variant("serial", default=False, description="Build serial version with fake MPI stubs")
    variant(
        "int64",
        default=True,
        description="Use int64 (8-byte) for global indices of distributed matrices",
    )
    variant("metis", default=True, description="Build with METIS support for graph partitioning")
    variant("amd", default=False, description="Build with AMD package of Davis, Duff and Amestoy")
    variant("openmp", default=False, description="Enable OpenMP support")

    depends_on("autoconf@2.59:", type="build")
    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")

    # TODO: handle metis integer sizes
    depends_on("metis+int64", when="+metis+int64")
    depends_on("metis~int64", when="+metis~int64")

    # ENH: Suite-sparse is a large package, but only AMD is used.
    #      It may be possible to build a minimal package for AMD
    depends_on("suite-sparse", when="+amd")

    def setup_build_environment(self, env):
        spec = self.spec

        # CC, CXX, and FC are set automatically by Spack

        env.set("MPICC", spec["mpi"].mpicc)
        env.set("MPICXX", spec["mpi"].mpicxx)
        env.set("MPIFC", spec["mpi"].mpifc)

    def configure_args(self):
        """Produces a list containing all arguments that must be passed to
        configure, except --prefix which will be pre-pended to the list
        automatically"""

        spec = self.spec

        # See: https://www.gnu.org/software/automake/manual/html_node/Dependency-Tracking.html
        # Dependency tracking is useless for one-time builds. Turning it off
        # can speed up the build process
        args = ["--disable-dependency-tracking"]

        blas = spec["blas"].libs
        args.append("--with-blas={0}".format(blas.link_flags))
        args.append("--with-blasdir={0}".format(";".join(blas.directories)))

        lapack = spec["lapack"].libs
        args.append("--with-lapack={0}".format(lapack.link_flags))

        if "+serial" in spec:
            args.append("--enable-serial")

        if "~int64" in spec:
            args.append("--with-lpk=4")

        if "+metis" in spec:
            args.append("--with-metisincdir={0}".format(spec["metis"].prefix.include))
            args.append("--with-metislibdir={0}".format(spec["metis"].prefix.lib))

        if "+amd" in spec:
            args.append("--with-amdincdir={}".format(spec["suite-sparse"].prefix.include))
            args.append("--with-amdlibdir={}".format(spec["suite-sparse"].prefix.lib))

        if "+openmp" in spec:
            args.append("--enable-openmp")
        else:
            args.append("--disable-openmp")

        return args

    def build_args(spec, prefix):

        args = []

        # See: https://github.com/sfilippone/psblas3/issues/23
        if spec.satisfies("@3.7.0:3.8.0"):
            args.appends("-j1")

        return args

    def install_args(spec, prefix):

        args = []

        # See: https://github.com/sfilippone/psblas3/issues/23
        if spec.satisfies("@3.7.0:3.8.0-1"):
            args.appends("-j1")

        return args
