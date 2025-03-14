# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Psblas(AutotoolsPackage):
    """PSBLAS: Parallel Sparse BLAS. A library of distributed sparse
    linear algebra with support for GPU and Multithread acceleration.
    Part of the PSCToolkit: Parallel Sparse Computation Toolkit."""

    # Url for your package's homepage here.
    homepage = "https://psctoolkit.github.io/"
    git = "https://github.com/sfilippone/psblas3.git"
    url = "https://github.com/sfilippone/psblas3/archive/refs/tags/v3.9.0-rc1.tar.gz"

    # List of GitHub accounts to notify when the package is updated.
    maintainers("cirdans-home", "sfilippone")

    # SPDX identifier of the project's license below.
    license("BSD-3-Clause", checked_by="cirdans-home")

    version("development", branch="development")
    version(
        "3.9.0-rc1",
        sha256="7a7091ce52582b6fc442e8793e36461be36c0947272ea803ad72736ec2d56da8",
        preferred=True,
    )
    version("3.8.1-2", sha256="285ddb7c9a793ea7ecb428d68cf23f4cc04f1c567631aa84bc2bedb65a3d1b0c")
    version("3.8.1", sha256="02e1f00e644426eb15eb08c735cf9c8ae692392f35c2cfe4f7474e1ab91575dc")
    version("3.8.0-2", sha256="86a76bb0987edddd4c10c810d7f18e13742aadc66ac14ad3679669809c1184fa")

    # Explicit phases: autoreconf, configure, build, install, and post_install
    # which compiles the examples in the prefix/samples folder
    phases = ["configure", "build", "install", "samples"]

    # Variants:
    # LPK/IPK: Integer precision variants
    variant("LPK", default=8, values=int, description="Length in bytes for long integers (8 or 4)")
    variant(
        "IPK", default=4, values=int, description="Length in bytes for short integers (8 or 4)"
    )
    # MPI
    variant("mpi", default=True, description="Activates MPI support")
    # CUDA
    variant(
        "cuda", default=False, description="Activate CUDA support", when="@development,3.9.0-rc1"
    )
    variant(
        "cudacc",
        default="70,75,80,86,89,90",
        multi=True,
        description="Specify CUDA Compute Capabilities",
        when="+cuda",
    )
    # METIS
    variant("metis", default=False, description="Activate METIS support")
    # SuiteSparse: Enable AMD library support via SuiteSparse
    variant("amd", default=False, description="Activate AMD support via SuiteSparse")
    # OpenMP
    variant(
        "openmp",
        default=False,
        description="Activates OpenMP support",
        when="@development,3.9.0-rc1",
    )
    # OpenACC support (requires GCC >= 14.2.0)
    variant(
        "openacc",
        default=False,
        description="Activate OpenACC support",
        when="@development,3.9.0-rc1",
    )
    # Additional configure options
    variant("ccopt", default="none", description="Additional CCOPT flags")
    variant("cxxopt", default="none", description="Additional CXXOPT flags")
    variant("fcopt", default="none", description="Additional FCOPT flags")
    variant("extra_opt", default="none", description="Additional EXTRA_OPT flags")
    variant("libs", default="none", description="Additional link flags")
    variant("clibs", default="none", description="Additional CLIBS flags")
    variant("flibs", default="none", description="Additional FLIBS flags")
    variant("extra_nvcc", default="none", description="Additional EXTRA_NVCC flags", when="+cuda")
    variant(
        "extraopenacc",
        default="none",
        description="Additional EXTRAOPENACC flags",
        when="+openacc",
    )
    variant("ccopenacc", default="none", description="Additional CCOPENACC flags", when="+openacc")
    variant(
        "cxxopenacc", default="none", description="Additional CXXOPENACC flags", when="+openacc"
    )
    variant("fcopenacc", default="none", description="Additional FCOPENACC flags", when="+openacc")

    # Dependencies:
    # Languages: Fortran for much of the library, c for the interfaces,
    # c++ for the matching routines
    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
    # MPI
    depends_on("mpi", when="+mpi")
    # BLAS/LAPACK
    depends_on("blas")
    depends_on("lapack")
    # CUDA
    depends_on("cuda", when="+cuda")
    # Metis
    depends_on("metis@5:+int64", when="+metis LPK=8")
    depends_on("metis@5:~int64", when="+metis LPK=4")
    depends_on("metis@5:+int64", when="+metis")
    # SuiteSparse: Enable AMD library support via SuiteSparse
    depends_on("suite-sparse", when="+amd")
    # OpenACC support (requires GCC >= 14.2.0)
    depends_on("gcc@14.2.0:+nvptx", when="+openacc", type="build")

    def configure_args(self):
        args = [f"--prefix={self.prefix}"]
        # LPK/IPK Choice for integer configuration
        args.append(f"--with-lpk={self.spec.variants['LPK'].value}")
        args.append(f"--with-ipk={self.spec.variants['IPK'].value}")
        # MPI/serial configuration
        if "+mpi" in self.spec:
            pass
        else:
            args.append("--enable-serial")
        # OPENMP
        args.extend(self.enable_or_disable("openmp"))
        # CUDA
        args.extend(self.enable_or_disable("cuda"))
        if "+cuda" in self.spec:
            cudacc_values = ",".join(self.spec.variants["cudacc"].value)
            args.append(f"--with-cudacc={cudacc_values}")
            args.append(f"--with-cudadir={self.spec['cuda'].prefix}")
            for opt in ["extra_nvcc"]:
                val = self.spec.variants[opt].value
                if val != "none":
                    args.append(f"--with-{opt.replace('_', '-')}={val}")
        # OpenACC configuration
        args.extend(self.enable_or_disable("openacc"))
        if "+openacc" in self.spec:
            for opt in ["extraopenacc", "ccopenacc", "cxxopenacc", "fcopenacc"]:
                val = self.spec.variants[opt].value
                if val != "none":
                    args.append(f"--with-{opt.replace('_', '-')}={val}")
        # METIS configuration
        if "+metis" in self.spec:
            args.append(f"--with-metisincdir={self.spec['metis'].prefix}/include")
            args.append(f"--with-metislibdir={self.spec['metis'].prefix}/lib")
        # SuiteSparse configuration for AMD library support
        if "+amd" in self.spec:
            args.append(f"--with-amddir={self.spec['suite-sparse'].prefix}")
        # All the other options
        for opt in ["ccopt", "cxxopt", "fcopt", "extra_opt", "libs", "clibs", "flibs"]:
            val = self.spec.variants[opt].value
            if val != "none":
                args.append(f"--with-{opt.replace('_', '-')}={val}")
        return args

    def configure(self, spec, prefix):
        configure = Executable("./configure")
        configure(*self.configure_args())

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make("install")

    def samples(self, spec, prefix):
        with working_dir(prefix.samples.fileread):
            make()
        with working_dir(prefix.samples.pargen):
            make()
