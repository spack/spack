# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Grid(AutotoolsPackage, CudaPackage, ROCmPackage):
    """Data parallel C++ mathematical object library."""

    homepage = "https://github.com/paboyle/Grid"
    url = "https://github.com/paboyle/Grid/archive/refs/tags/0.8.2.tar.gz"
    git = "https://github.com/paboyle/Grid.git"

    maintainers("giordano")

    license("GPL-2.0-only")

    version("develop", branch="develop")

    variant(
        "comms",
        default="mpi",
        values=("none", "mpi", "mpi3", conditional("shmem", when="^cray-mpich")),
        description="Choose communication interface",
    )
    variant("fftw", default=True, description="Activate FFTW support")
    variant("lapack", default=False, description="Activate LAPACK support")
    variant("hdf5", default=False, description="Activate HDF5 support")
    variant("lime", default=False, description="Activate LIME support")
    variant("doxygen-doc", default=False, description="Build the documentation with doxygen")
    variant(
        "gen-simd-width",
        default="64",
        description="Size (in bytes) of the generic SIMD vector type",
    )
    variant(
        "rng",
        default="sitmo",
        values=("sitmo", "ranlux48", "mt19937"),
        multi=False,
        description="RNG setting",
    )
    variant("timers", default=True, description="System dependent high-resolution timers")
    variant("chroma", default=False, description="Chroma regression tests")
    variant("cuda", default=False, description="Build with CUDA support")
    variant("gparity", default=True, description="Build with gparity support")
    variant(
        "fermion-reps", default=True, description="Build non-fundamental fermion representations"
    )
    variant("Sp", default=True, description="Build with support for symplectic gauge groups")
    variant(
        "Nc",
        default="3",
        values=("2", "3", "4", "5", "8"),
        description="Instantiate for this number of colours",
    )
    variant(
        "alloc-align", default="2MB", values=("4k", "2MB"), description="Grid allocator alignment"
    )
    variant("unified-device-memory", default=False, description="Enable unified device memory")
    variant(
        "shared-memory",
        default="no",
        values=("shmopen", "shmget", "hugetlbfs", "nvlink", "no"),
        description="Interprocess shared memory allocation technique",
    )
    variant("accelerator-aware-mpi", default=False, description="Build with GPU aware MPI")
    variant(
        "tracing",
        default="none",
        values=("none", "nvtx", "roctx", "timer"),
        description="Enable tracing",
    )

    # Prefer 4 colours by default when enabling Sp.
    requires("Nc=4", "Nc=5", "Nc=8", "Nc=2", "Nc=3", "@:", when="+Sp", policy="any_of")

    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("gmp")
    depends_on("mpfr")
    depends_on("openssl")

    depends_on("mpi", when="comms=mpi")
    depends_on("cray-mpich", when="comms=shmem")
    depends_on("mpi@3:", when="comms=mpi3")

    depends_on("fftw-api@3", when="+fftw")

    depends_on("lapack", when="+lapack")

    depends_on("hdf5", when="+hdf5")

    depends_on("c-lime", when="+lime")

    depends_on("doxygen", type="build", when="+doxygen-doc")

    conflicts(
        "+cuda",
        when="+rocm",
        msg="CUDA / ROCm are mututally exclusive. At most 1 GPU platform can be configured",
    )
    conflicts("+cuda", when="platform=darwin", msg="There is no GPU support for macOS")
    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="Must specify CUDA compute capabilities of your GPU, see https://developer.nvidia.com/cuda-gpus",
    )
    conflicts(
        "+accelerator-aware-mpi",
        when="-cuda -rocm",
        msg="Cannot compile for GPU-aware MPI when not compiling for GPU",
    )
    conflicts(
        "shared-memory=nvlink",
        when="-cuda -rocm",
        msg="Cannot compile with nvlink when not compiling for GPU",
    )

    def autoreconf(self, spec, prefix):
        Executable("./bootstrap.sh")()

    def setup_build_environment(self, env):
        spec = self.spec
        env.set("CXXFLAGS", self.compiler.cxx17_flag)

        if spec.satisfies("+cuda"):
            arch_config = ",".join(
                f"arch=compute_{arch},code=sm_{arch}" for arch in spec.variants["cuda_arch"].value
            )
            if "comms=none" in spec:
                host_compiler = ""
            else:
                host_compiler = f"-ccbin {spec['mpi'].mpicxx}"
            env.set("CXX", join_path(spec["cuda"].prefix, "bin", "nvcc"))
            env.append_flags("CXXFLAGS", f"-gencode {arch_config} -cudart shared {host_compiler}")
            env.set("LDFLAGS", "-cudart shared -lcublas")
        elif spec.satisfies("+rocm"):
            archs = ",".join(self.spec.variants["amdgpu_target"].value)
            if "comms=none" in spec:
                mpi_include = ""
                mpi_ldflags = ""
            else:
                mpi_include = spec["mpi"].headers.cpp_flags
                mpi_ldflags = f"{spec['mpi'].libs.ld_flags} -lmpi"
            env.set("CXX", join_path(spec["hip"].prefix, "bin", "hipcc"))
            env.set("LDFLAGS", f"{mpi_ldflags} -lamdhip64")
            env.append_flags(
                "CXXFLAGS", f"--offload-arch={archs} {spec['hip'].headers.cpp_flags} {mpi_include}"
            )
        else:
            if "comms=none" not in spec:
                env.append_flags("CXXFLAGS", "-fPIC")
                # The build system can easily get very confused about MPI support
                # and what linker to use.  In many case it'd end up building the
                # code with support for MPI but without using `mpicxx` or linking to
                # `-lmpi`, wreaking havoc.  Forcing `CXX` to be mpicxx should help.
                env.set("CC", spec["mpi"].mpicc)
                env.set("CXX", spec["mpi"].mpicxx)

        if spec.satisfies("+lapack") and not spec.satisfies("^intel-mkl"):
            # lapack is searched only as `-llapack`, so anything else
            # wouldn't be found, causing an error.
            env.set("LIBS", self.spec["lapack"].libs.ld_flags)

    def configure_args(self):
        spec = self.spec
        args = []

        args.append(f"--with-gmp={self.spec['gmp'].prefix}")
        args.append(f"--with-mpfr={self.spec['mpfr'].prefix}")

        args.extend(self.enable_or_disable("gparity"))
        args.extend(self.enable_or_disable("accelerator-aware-mpi"))
        args.extend(self.enable_or_disable("fermion-reps"))
        args.extend(self.enable_or_disable("Sp"))
        args.extend(self.enable_or_disable("unified", variant="unified-device-memory"))

        args.append(f"--enable-tracing={spec.variants['tracing'].value}")
        args.append(f"--enable-Nc={spec.variants['Nc'].value}")
        args.append(f"--enable-alloc-align={spec.variants['alloc-align'].value}")
        args.append(f"--enable-shm={spec.variants['shared-memory'].value}")

        if spec.satisfies("^[virtuals=lapack] intel-oneapi-mkl") or spec.satisfies(
            "^[virtuals=fftw-api] intel-oneapi-mkl"
        ):
            args.append("--enable-mkl")
        else:
            if spec.satisfies("+fftw"):
                args.append(f"--with-fftw={self.spec['fftw-api'].prefix}")
            if spec.satisfies("+lapack"):
                args.append(f"--enable-lapack={self.spec['lapack'].prefix}")

        args += self.enable_or_disable("timers")
        args += self.enable_or_disable("chroma")
        args += self.enable_or_disable("doxygen-doc")

        # TODO: Add sycl support
        if spec.satisfies("+cuda") or spec.satisfies("+rocm"):
            args.append("--enable-simd=GPU")
            args.append(f"--enable-gen-simd-width={spec.variants['gen-simd-width'].value}")
            if spec.satisfies("+cuda"):
                args.append("--enable-accelerator=cuda")

            elif spec.satisfies("+rocm"):
                args.append("--enable-accelerator=hip")

        else:
            if "avx512" in spec.target:
                args.extend(["--enable-simd=AVX512", "--enable-gen-simd-width=64"])
            elif "avx2" in spec.target:
                args.extend(["--enable-simd=AVX2", "--enable-gen-simd-width=32"])
            elif "avx" in spec.target:
                if "fma4" in spec.target:
                    args.append("--enable-simd=AVXFMA4")
                elif "fma" in spec.target:
                    args.append("--enable-simd=AVXFMA")
                else:
                    args.append("--enable-simd=AVX")
                args.append("--enable-gen-simd-width=16")
            elif "sse4_2" in spec.target:
                args.extend(["--enable-simd=SSE4", "--enable-gen-simd-width=16"])
            elif spec.target == "a64fx":
                args.extend(["--enable-simd=A64FX", "--enable-gen-simd-width=64"])
            elif "neon" in spec.target:
                args.extend(["--enable-simd=NEONv8", "--enable-gen-simd-width=16"])
            else:
                args.extend(
                    [
                        "--enable-simd=GEN",
                        f"--enable-gen-simd-width={spec.variants['gen-simd-width'].value}",
                    ]
                )

        args.append(f"--enable-comms={spec.variants['comms'].value}")
        args.append(f"--enable-rng={spec.variants['rng'].value}")

        return args
