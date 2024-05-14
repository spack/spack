# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mivisionx(CMakePackage):
    """MIVisionX toolkit is a set of comprehensive computer
    vision and machine intelligence libraries, utilities, and
    applications bundled into a single toolkit."""

    homepage = "https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX"
    git = "https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX.git"
    url = "https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX/archive/rocm-6.1.1.tar.gz"

    maintainers("srekolam", "renjithravindrankannath")
    tags = ["rocm"]

    def url_for_version(self, version):
        if version == Version("1.7"):
            return "https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX/archive/1.7.tar.gz"

        url = "https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX/archive/rocm-{0}.tar.gz"
        return url.format(version)

    license("MIT")
    version("6.1.1", sha256="3483b5167c47047cca78581cc6c9685138f9b5b25edb11618b720814788fc2a0")
    version("6.1.0", sha256="f18a72c4d12c36ab50f9c3a5c22fc3641feb11c99fed513540a16a65cd149fd1")
    version("6.0.2", sha256="e39521b3109aa0900f652ae95a4421df0fa29fd57e816268cc6602d243c50779")
    version("6.0.0", sha256="01324a12f21ea0e29a4d7d7c60498ba9231723569fedcdd90f28ddffb5e0570e")
    version("5.7.1", sha256="bfc074bc32ebe84c72149ee6abb30b5b6499023d5b98269232de82e35d0505a8")
    version("5.7.0", sha256="07e4ec8a8c06a9a8bb6394a043c9c3e7176acd3b462a16de91ef9518a64df9ba")
    version("5.6.1", sha256="b2ff95c1488e244f379482631dae4f9ab92d94a513d180e03607aa1e184b5b0a")
    version("5.6.0", sha256="34c184e202b1a6da2398b66e33c384d5bafd8f8291089c18539715c5cb73eb1f")
    version("5.5.1", sha256="e8209f87a57c4222003a936240e7152bbfa496862113358f29d4c3e80d4cdf56")
    version("5.5.0", sha256="af266550ecccad80f08954f23e47e8264eb338b0928a5314bd6efca349fc5a14")
    version("5.4.3", sha256="4da82974962a70c326ce2427c664517b1efdff436efe222e6bc28817c222a082")
    version("5.4.0", sha256="caa28a30972704ddbf1a87cefdc0b0a35381d369961c43973d473a1573bd35cc")
    version("5.3.3", sha256="378fafcb327e17e0e11fe1d1029d1740d84aaef0fd59614ed7376499b3d716f6")
    version("5.3.0", sha256="58e68f1c78bbe5694e42bf61be177f9e94bfd3e0c113ec6284493c8684836c58")
    with default_args(deprecated=True):
        version("5.2.3", sha256="bbcdb5808d2bc880486dffa89f4111fb4b1d6dfe9b11fcd46fbd17939d057cf0")
        version("5.2.1", sha256="201996b31f59a8d5e4cc3f17d17a5b81158a34d2a1c833b65ccc3dceb21d176f")
        version("5.2.0", sha256="fee620a1edd3bce18b2cec9ef26ec2afe0a85d6da8a37ed713ab0d1342382503")
        version("5.1.3", sha256="62591d5caedc13832c3ccef629a88d9c2a43c884daad1124ddcb9c5f7d5470e9")
        version("5.1.0", sha256="e082415cc2fb859c53a6d6e5d72ca4529f6b4d56a4abe274dc374faaa5910513")

    # Adding 2 variants OPENCL ,HIP which HIP as default. earlier to 5.0.0,OPENCL
    # was the default but has change dto HIP from 5.0.0 onwards.
    # when tested with HIP as true for versions before 5.1.0, build errors were encountered
    # this was corrected with 5.2.0. Hence it was made as default starting with 5.2.0 onwards

    variant("opencl", default=False, description="Use OPENCL as the backend")
    variant("hip", default=True, description="Use HIP as backend")
    variant("add_tests", default=False, description="add tests and samples folder")

    patch("0001-add-half-include-path.patch", when="@5.5")
    patch("0001-add-half-include-path-5.6.patch", when="@5.6:")
    patch("0002-add-half-include-path-for-tests.patch", when="@5.5: +add_tests")

    patch(
        "https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX/commit/da24882438b91a0ae1feee23206b75c1a1256887.patch?full_index=1",
        sha256="41caff199224f904ef5dc2cd9c5602d6cfa41eba6af0fcc782942a09dd202ab4",
        when="@5.6",
    )

    conflicts("+opencl", when="@5.6.0:")
    conflicts("+add_tests", when="@:5.4")

    def patch(self):
        if self.spec.satisfies("@:5.1 + hip"):
            filter_file(
                r"${ROCM_PATH}/miopen",
                self.spec["miopen-hip"].prefix.miopen,
                "amd_openvx_extensions/CMakeLists.txt",
                string=True,
            )
            filter_file(
                r"${ROCM_PATH}/bin",
                self.spec["hip"].prefix.bin,
                "amd_openvx/openvx/hipvx/CMakeLists.txt",
                string=True,
            )
            filter_file(
                r"${ROCM_PATH}/bin",
                self.spec["hip"].prefix.bin,
                "amd_openvx_extensions/amd_nn/nn_hip/CMakeLists.txt",
                string=True,
            )
        if self.spec.satisfies("@5.1.3: + hip"):
            filter_file(
                r"${ROCM_PATH}/include/miopen/config.h",
                "{0}/include/miopen/config.h".format(self.spec["miopen-hip"].prefix),
                "amd_openvx_extensions/CMakeLists.txt",
                string=True,
            )
        if self.spec.satisfies("@5.1.3: + opencl"):
            filter_file(
                r"${ROCM_PATH}/include/miopen/config.h",
                "{0}/include/miopen/config.h".format(self.spec["miopen-opencl"].prefix),
                "amd_openvx_extensions/CMakeLists.txt",
                string=True,
            )
        if self.spec.satisfies("@5.3.0: + hip"):
            filter_file(
                r"${ROCM_PATH}/llvm/bin/clang++",
                "{0}/bin/clang++".format(self.spec["llvm-amdgpu"].prefix),
                "amd_openvx/openvx/hipvx/CMakeLists.txt",
                string=True,
            )
            filter_file(
                r"${ROCM_PATH}/llvm/bin/clang++",
                "{0}/bin/clang++".format(self.spec["llvm-amdgpu"].prefix),
                "amd_openvx_extensions/amd_nn/nn_hip/CMakeLists.txt",
                string=True,
            )
        if self.spec.satisfies("@5.5.0: + hip"):
            filter_file(
                r"${ROCM_PATH}/llvm/bin/clang++",
                "{0}/bin/clang++".format(self.spec["llvm-amdgpu"].prefix),
                "rocAL/rocAL/rocAL_hip/CMakeLists.txt",
                string=True,
            )
        if self.spec.satisfies("+add_tests"):
            filter_file(
                r"${ROCM_PATH}/include/mivisionx",
                "{0}/include/mivisionx".format(self.spec.prefix),
                "tests/amd_migraphx_tests/mnist/CMakeLists.txt",
                string=True,
            )
            filter_file(
                r"${ROCM_PATH}/lib",
                "{0}/lib".format(self.spec.prefix),
                "tests/amd_migraphx_tests/mnist/CMakeLists.txt",
                string=True,
            )
            filter_file(
                r"${ROCM_PATH}/include/mivisionx",
                "{0}/include/mivisionx".format(self.spec.prefix),
                "tests/amd_migraphx_tests/resnet50/CMakeLists.txt",
                string=True,
            )
            filter_file(
                r"${ROCM_PATH}/lib",
                "{0}/lib".format(self.spec.prefix),
                "tests/amd_migraphx_tests/resnet50/CMakeLists.txt",
                string=True,
            )
            filter_file(
                r"${ROCM_PATH}/include/mivisionx",
                "{0}/include/mivisionx".format(self.spec.prefix),
                "samples/inference/mv_objdetect/CMakeLists.txt",
                string=True,
            )
            filter_file(
                r"${ROCM_PATH}/lib",
                "{0}/lib".format(self.spec.prefix),
                "samples/inference/mv_objdetect/CMakeLists.txt",
                string=True,
            )
            filter_file(
                r"${ROCM_PATH}/include/mivisionx",
                "{0}/include/mivisionx".format(self.spec.prefix),
                "model_compiler/python/nnir_to_clib.py",
                string=True,
            )
            filter_file(
                r"/opt/rocm",
                "{0}".format(self.spec.prefix),
                "model_compiler/python/nnir_to_clib.py",
                string=True,
            )
            filter_file(
                r"${ROCM_PATH}/${CMAKE_INSTALL_INCLUDEDIR}/mivisionx/rocal",
                "{0}/include/mivisionx/rocal".format(self.spec.prefix),
                "utilities/rocAL/rocAL_unittests/CMakeLists.txt",
                string=True,
            )
            filter_file(
                r"${ROCM_PATH}/lib",
                "{0}/lib".format(self.spec.prefix),
                "utilities/rocAL/rocAL_unittests/CMakeLists.txt",
                string=True,
            )
            filter_file(
                r"${ROCM_PATH}/${CMAKE_INSTALL_INCLUDEDIR}/mivisionx/rocal",
                "{0}/include/mivisionx/rocal".format(self.spec.prefix),
                "utilities/rocAL/rocAL_video_unittests/CMakeLists.txt",
                string=True,
            )
            filter_file(
                r"${ROCM_PATH}/lib",
                "{0}/lib".format(self.spec.prefix),
                "utilities/rocAL/rocAL_video_unittests/CMakeLists.txt",
                string=True,
            )

    depends_on("cmake@3.5:", type="build")
    depends_on("ffmpeg@:4", type="build", when="@:5.3")
    depends_on("ffmpeg@4.4", type="build", when="@5.4:")
    depends_on("protobuf@:3", type="build")
    depends_on(
        "opencv@:3.4"
        "+calib3d+features2d+highgui+imgcodecs+imgproc"
        "+video+videoio+flann+photo+objdetect",
        type="build",
        when="@:5.2",
    )
    depends_on(
        "opencv@4.5:"
        "+calib3d+features2d+highgui+imgcodecs+imgproc"
        "+video+videoio+flann+photo+objdetect+png+jpeg",
        type="build",
        when="@5.3:",
    )
    depends_on("openssl")
    depends_on("libjpeg-turbo@2.0.6+partial_decoder", type="build")
    depends_on("rpp", when="@5.5:")
    depends_on("lmdb", when="@5.5:")
    depends_on("py-setuptools", when="@5.6:")
    depends_on("py-wheel", when="@5.6:")
    depends_on("py-pybind11", when="@5.6:")
    depends_on("py-google-api-python-client", when="+add_tests")
    depends_on("py-protobuf@3.20.3", type=("build", "run"), when="+add_tests")
    depends_on("py-future", when="+add_tests")
    depends_on("py-numpy", when="+add_tests")
    depends_on("py-pytz", when="+add_tests")
    depends_on("rapidjson", when="@5.7:")

    # need to choose atleast one backend and both cannot be set
    # HIP as backend did not build for older releases 5.1.0 where
    # OPENCL was default backend.
    conflicts("+opencl+hip")
    conflicts("+hip", when="@:5.1.0")

    with when("+opencl"):
        for ver in [
            "5.1.0",
            "5.1.3",
            "5.2.0",
            "5.2.1",
            "5.2.3",
            "5.3.0",
            "5.3.3",
            "5.4.0",
            "5.4.3",
            "5.5.0",
            "5.5.1",
        ]:
            depends_on(f"rocm-opencl@{ver}", when=f"@{ver}")
            depends_on(f"miopengemm@{ver}", when=f"@{ver}")
            depends_on(f"miopen-opencl@{ver}", when=f"@{ver}")
    with when("+hip"):
        for ver in [
            "5.1.0",
            "5.1.3",
            "5.2.0",
            "5.2.1",
            "5.2.3",
            "5.3.0",
            "5.3.3",
            "5.4.0",
            "5.4.3",
            "5.5.0",
            "5.5.1",
            "5.6.0",
            "5.6.1",
            "5.7.0",
            "5.7.1",
            "6.0.0",
            "6.0.2",
            "6.1.0",
            "6.1.1",
        ]:
            depends_on(f"miopen-hip@{ver}", when=f"@{ver}")
        for ver in [
            "5.3.3",
            "5.4.0",
            "5.4.3",
            "5.5.0",
            "5.5.1",
            "5.6.0",
            "5.6.1",
            "5.7.0",
            "5.7.1",
            "6.0.0",
            "6.0.2",
            "6.1.0",
            "6.1.1",
        ]:
            depends_on(f"migraphx@{ver}", when=f"@{ver}")
            depends_on(f"hip@{ver}", when=f"@{ver}")

    for ver in [
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
    ]:
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")
        depends_on("python@3.5:", type="build")

    def setup_run_environment(self, env):
        env.set("MIVISIONX_MODEL_COMPILER_PATH", self.spec.prefix.libexec.mivisionx.model_compiler)

    def flag_handler(self, name, flags):
        spec = self.spec
        protobuf = spec["protobuf"].prefix.include
        if name == "cxxflags":
            flags.append("-I{0}".format(protobuf))
        return (flags, None, None)

    def cmake_args(self):
        spec = self.spec
        protobuf = spec["protobuf"].prefix.include
        args = [self.define("CMAKE_CXX_FLAGS", "-I{0}".format(protobuf))]
        if self.spec.satisfies("+opencl"):
            args.append(self.define("BACKEND", "OPENCL"))
            args.append(self.define("HSA_PATH", spec["hsa-rocr-dev"].prefix))
        if self.spec.satisfies("+hip"):
            args.append(self.define("BACKEND", "HIP"))
            args.append(self.define("HSA_PATH", spec["hsa-rocr-dev"].prefix))
            args.append(self.define("HIP_PATH", spec["hip"].prefix))
        if self.spec.satisfies("~hip~opencl"):
            args.append(self.define("BACKEND", "CPU"))
        if self.spec.satisfies("@5.5:"):
            args.append(
                self.define("AMDRPP_LIBRARIES", "{0}/lib/librpp.so".format(spec["rpp"].prefix))
            )
            args.append(
                self.define("AMDRPP_INCLUDE_DIRS", "{0}/include/rpp".format(spec["rpp"].prefix))
            )
            args.append(
                self.define(
                    "TurboJpeg_LIBRARIES_DIRS", "{0}/lib64".format(spec["libjpeg-turbo"].prefix)
                )
            )
            args.append(self.define("CMAKE_INSTALL_PREFIX_PYTHON", spec.prefix))
        return args

    @run_after("install")
    def add_tests(self):
        if self.spec.satisfies("+add_tests"):
            install_tree("tests", self.spec.prefix.tests)
            install_tree("samples", self.spec.prefix.samples)
            install_tree("utilities", self.spec.prefix.utilities)
