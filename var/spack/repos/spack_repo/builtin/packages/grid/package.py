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
    variant("fermion-reps", default=True, description="Build non-fundamental fermion representations")
    variant("Sp", default=True, description="Build with support for symplectic gauge groups")
    variant("Nc", default="3", values=("2","3","4","5","8"), description="Instantiate for this number of colours")
    variant("alloc-align", default="2MB", values=("4k", "2MB"), description="Grid allocator alignment")
    variant("unified-device-memory", default=False, description="Enable unified device memory")
    variant("shared-memory", default="no", values=("shmopen", "shmget", "hugetlbfs", "nvlink", "no"), description="Interprocess shared memory allocation technique")
    variant("gpu-aware-mpi", default=False, description="Build with GPU aware MPI")

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
    conflicts("+gpu-aware-mpi", when="-cuda -rocm", msg="Cannot compile for GPU-aware MPI when not compiling for GPU")
    conflicts("shared-memory=nvlink", when="-cuda -rocm", msg="Cannot compile with nvlink when not compiling for GPU")
    
    def autoreconf(self, spec, prefix):
        Executable("./bootstrap.sh")()


    def configure_args(self):
        spec = self.spec
        args = ["--with-gmp", "--with-mpfr"]

        if spec.satisfies("+gparity"):
            args.append("--enable-gparity")
        else:
            args.append("--disable-gparity")
          
        if spec.satisfies("+fermion_reps"):
            args.append("--enable-fermion-reps")
        else:
            args.append("--disable-fermion-reps")
        
        if spec.satisfies("+Sp"):
            args.append("--enable-Sp")
        else:
            args.append("--disable-Sp")
          
        if spec.satisfies("+unified-device-memory"):
            args.append("--enable-unified")
        else:
            args.append("--disable-unified")
            
        args.append("--enable-Nc={}".format(spec.variants['Nc']))
        args.append("--enable-alloc-align={}".format(spec.variants['alloc-align']))
        args.append("--enable-shm={}".format(spec.variants['shared-memory']))
        
        if spec.satisfies("^[virtuals=lapack] intel-oneapi-mkl") or spec.satisfies(
            "^[virtuals=fftw-api] intel-oneapi-mkl"
        ):
            args.append("--enable-mkl")
        else:
            if spec.satisfies("+fftw"):
                args.append(f"--with-fftw={self.spec['fftw-api'].prefix}")
            if spec.satisfies("+lapack"):
                args.append(f"--enable-lapack={self.spec['lapack'].prefix}")
                # lapack is searched only as `-llapack`, so anything else
                # wouldn't be found, causing an error.
                args.append(f"LIBS={self.spec['lapack'].libs.ld_flags}")

        args += self.enable_or_disable("timers")
        args += self.enable_or_disable("chroma")
        args += self.enable_or_disable("doxygen-doc")

        # TODO: Add sycl support
        if spec.satisfies("+cuda") or spec.satisfies("+rocm"):
            args.append("--enable-simd=GPU")
            if spec.satisfies("+cuda"):
                args.append("--enable-accelerator=cuda")
                args.append("CXX={}".format(join_path(spec["cuda"].prefix, "bin", "nvcc")))
                args.append("LDFLAGS=\"-cudart shared\"")
                
                if "comms=none" not in spec:
                    host_compiler = "-ccbin {}".format(spec["mpi"].mpicxx)
                else:
                    host_compiler = ""
                
                gpu_archs = spec.variants["cuda_arch"].value[0]
                arch_config = ",".join(f"arch=compute_{arch},code=sm_{arch}" for arch in spec.variants["cuda_arch"].value)
                args.append("CXXFLAGS=\"-gencode {0} -std=c++17 -cudart shared {1}\"".format(arch_config, host_compiler))
            
            elif spec.satisfies("+rocm"):
                args.append("--enable-accelerator=hip")
                args.append("CXX={}".format(spec["hip"].prefix))
                if "comms=none" not in spec:
                    mpi_path = spec["mpi"].prefix
                    mpi_include = "-I{}/include".format(mpi_path)
                    mpi_ldflags = "-L{}/lib -lmpi".format(mpi_path)
                    args.append("MPICXX={}".format(spec["mpi"].mpicxx))
                else:
                    mpi_include = ""
                    mpi_ldflags = ""
                    
                args.append("CXXFLAGS=\"-fPIC --offload-arch={} -I{}/include {} -std=c++17\"".format(spec.variants["amdgpu_target"].value, spec["hip"].prefix, mpi_include))
                args.append("LDFLAGS=\"{} -lamdhip64\"".format(mpi_ldflags))
        else:
            if "comms=none" not in spec:
                # The build system can easily get very confused about MPI support
                # and what linker to use.  In many case it'd end up building the
                # code with support for MPI but without using `mpicxx` or linking to
                # `-lmpi`, wreaking havoc.  Forcing `CXX` to be mpicxx should help.
                args.extend(["CC={0}".format(spec["mpi"].mpicc), "CXX={0}".format(spec["mpi"].mpicxx)])

            if "avx512" in spec.target:
                args.append("--enable-simd=AVX512")
            elif "avx2" in spec.target:
                args.append("--enable-simd=AVX2")
            elif "avx" in spec.target:
                if "fma4" in spec.target:
                    args.append("--enable-simd=AVXFMA4")
                elif "fma" in spec.target:
                    args.append("--enable-simd=AVXFMA")
                else:
                    args.append("--enable-simd=AVX")
            elif "sse4_2" in spec.target:
                args.append("--enable-simd=SSE4")
            elif spec.target == "a64fx":
                args.append("--enable-simd=A64FX")
            elif "neon" in spec.target:
                args.append("--enable-simd=NEONv8")
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
