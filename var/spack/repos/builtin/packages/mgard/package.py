from spack import *


class Mgard(CMakePackage, CudaPackage):
    """MGARD error bounded lossy compressor"""

    homepage = "https://github.com/CODARcode/MGARD"
    git      = "https://github.com/CODARcode/MGARD"

    version('master', branch='master')
    version('robertu94', git="https://github.com/robertu94/MGARD", branch="master", prefered=True)
    version('2020-10-01', commit="b67a0ac")

    depends_on("zlib")
    depends_on("zstd")
    depends_on("libarchive", when="@robertu94:")
    depends_on("tclap", when="@robertu94:")
    depends_on("yaml-cpp", when="@robertu94:")
    depends_on("cmake@3.19:")
    depends_on("nvcomp@robertu", when="+cuda")
    conflicts('cuda_arch=none', when="+cuda")

    def cmake_args(self):
        args = [
            "-DBUILD_TESTING=OFF"
        ]
        if "+cuda" in self.spec:
            args.append("-DMGARD_ENABLE_CUDA=ON")
            cuda_arch = self.spec.variants["cuda_arch"].value
            args.append("-DCUDA_ARCH_STRING={}".format(";".join(cuda_arch)))
            if "75" in cuda_arch:
                args.append("-DMGARD_ENABLE_CUDA_OPTIMIZE_TURING=ON")
            if "70" in cuda_arch:
                args.append("-DMGARD_ENABLE_CUDA_OPTIMIZE_VOLTA=ON")


        return args
