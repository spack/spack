# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import itertools
import re

from spack.package import *


class Rocsolver(CMakePackage):
    """rocSOLVER is a work-in-progress implementation of a
    subset of LAPACK functionality on the ROCm platform."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocSOLVER"
    git = "https://github.com/ROCmSoftwarePlatform/rocSOLVER.git"
    url = "https://github.com/ROCmSoftwarePlatform/rocSOLVER/archive/rocm-5.5.0.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath", "haampie")
    libraries = ["librocsolver"]

    amdgpu_targets = ROCmPackage.amdgpu_targets

    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=auto_or_any_combination_of(*amdgpu_targets),
        sticky=True,
    )
    variant(
        "optimal",
        default=True,
        description="This option improves performance at the cost of increased binary \
            size and compile time by adding specialized kernels \
            for small matrix sizes",
    )

    version("develop", branch="develop")
    version("master", branch="master")
    version("5.6.1", sha256="6a8f366218aee599a0e56755030f94ee690b34f30e6d602748632226c5dc21bb")
    version("5.6.0", sha256="54baa7f35f3c53da9005054e6f7aeecece5526dafcb277af32cbcb3996b0cbbc")
    version("5.5.1", sha256="8bf843e42d2e89203ea5fdb6e6082cea90da8d02920ab4c09bcc2b6f69909760")
    version("5.5.0", sha256="6775aa5b96731208c12c5b450cf218d4c262a80b7ea20c2c3034c448bb2ca4d2")
    version("5.4.3", sha256="5308b68ea72f465239a4bb2ed1a0507f0df7c98d3df3fd1f392e6d9ed7975232")
    version("5.4.0", sha256="69690839cb649dee43353b739d3e6b2312f3d965dfe66705c0ea910e57c6a8cb")
    version("5.3.3", sha256="d2248b5e2e0b20e08dd1ee5408e38deb02ecd28096dc7c7f2539351df6cb6ad5")
    version("5.3.0", sha256="4569f860d240d50e94e77d498050f5cafe5ad11daddaead3e7e9eaa1957878a7")
    version("5.2.3", sha256="b278a1640f31fb1905f18dc5127d57e2b1d36fd2b4f39ae811b5537fa6ce87d4")
    version("5.2.1", sha256="74c127efaefec70a14dff6fa0e92276f38a6c313bf1271d68d03a4222d1fc3b6")
    version("5.2.0", sha256="94d46ebe1266eaa05df50c1789dc27d3f2dbf3cb5af156e757777a82ed6ef356")
    version("5.1.3", sha256="5a8f3b95ac9a131c31538196e954ea53b863009c092cce0c0ef869a0cd5dd554")
    version("5.1.0", sha256="88de515a6e75eaa3c50c9c8ae1e7ae8e3b46e712e388f44f79b63fefa9fc0831")
    version(
        "5.0.2",
        sha256="298e0903f1ba8074055ab072690f967062d6e06a9371574de23e4e38d2997688",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="d444ad5348eb8a2c04646ceae6923467a0e775441f2c73150892e228e585b2e1",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="4639322bd1e77fedfdeb9032633bde6211a0b1cc16a612db7754f873f18a492f",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="0295862da941f31f4d43b19195b79331bd17f5968032f75c89d2791a6f8c1e8c",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="c6e7468d7041718ce6e1c7f50ec80a552439ac9cfed2dc3f753ae417dda5724f",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="63cc88dd285c0fe01ec2394321ec3b4e1e59bb98ce05b06e4b4d8fadcf1ff028",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="e9ef72d7c29e7c36bf02be63a64ca23b444e1ca71751749f7d66647873d9fdea",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="da5cc800dabf7367b02b73c93780b2967f112bb45232e4b06e5fd07b4d5b8d88",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="be9a52644c276813f76d78f2c11eddaf8c2d7f9dd04f4570f23d328ad30d5880",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="bc72483656b6b23a1e321913a580ca460da3bc5976404647536a01857f178dd2",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="85fd77fe5acf5af518d11e90e2c03ee0c5abd61071cea86ef5df09f944879648",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="72aa74284944d8b454088e8c8d74cf05464a4e2e46d33a57017ddd009113025e",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="8c1c630595952806e658c539fd0f3056bd45bafc22b57f0dd10141abefbe4595",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="d655e8c762fb9e123b9fd7200b4258512ceef69973de4d0588c815bc666cb358",
        deprecated=True,
    )

    depends_on("cmake@3.8:", type="build", when="@4.1.0:")
    depends_on("cmake@3.5:", type="build")
    depends_on("fmt@7:", type="build", when="@4.5.0:")
    depends_on("fmt@7:8.0.1", type="test", when="@5.6:")

    depends_on("googletest@1.10.0:", type="test")
    depends_on("netlib-lapack@3.7.1:", type="test")

    patch("link-clients-blas.patch", when="@4.3.0:4.3.2")
    # Backport https://github.com/ROCmSoftwarePlatform/rocSOLVER/commit/2bbfb8976f6e4d667499c77e41a6433850063e88
    patch("fmt-8.1-compatibility.patch", when="@4.5.0:5.1.3")
    # Maximize compatibility with other libraries that are using fmt.
    patch("fmt-9-compatibility.patch", when="@5.2.0:5.5")

    depends_on("hip@4.1.0:", when="@4.1.0:")
    depends_on("rocm-cmake@master", type="build", when="@master:")
    depends_on("rocm-cmake@4.5.0:", type="build", when="@4.5.0:")
    depends_on("rocm-cmake@4.3.0:", type="build", when="@4.3.0:")
    depends_on("rocm-cmake@3.5.0:", type="build")

    for ver in ["master", "develop"]:
        depends_on("rocblas@" + ver, when="@" + ver)

    for ver in [
        "3.5.0",
        "3.7.0",
        "3.8.0",
        "3.9.0",
        "3.10.0",
        "4.0.0",
        "4.1.0",
        "4.2.0",
        "4.3.0",
        "4.3.1",
        "4.5.0",
        "4.5.2",
        "5.0.0",
        "5.0.2",
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
    ]:
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("rocblas@" + ver, when="@" + ver)
    for ver in ["5.6.0", "5.6.1"]:
        depends_on("rocsparse@5.2:", when="@5.6:")

    for tgt in itertools.chain(["auto"], amdgpu_targets):
        depends_on("rocblas amdgpu_target={0}".format(tgt), when="amdgpu_target={0}".format(tgt))

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            ver = "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        else:
            ver = None
        return ver

    def cmake_args(self):
        args = [
            self.define("BUILD_CLIENTS_SAMPLES", "OFF"),
            self.define("BUILD_CLIENTS_TESTS", self.run_tests),
            self.define("BUILD_CLIENTS_BENCHMARKS", "OFF"),
        ]
        if self.spec.satisfies("@4.1.0"):
            incl = self.spec["rocblas"].prefix
            args.append(self.define("CMAKE_CXX_FLAGS", "-I{0}/rocblas/include".format(incl)))

        if self.spec.satisfies("@3.7.0:"):
            args.append(self.define_from_variant("OPTIMAL", "optimal"))

        tgt = self.spec.variants["amdgpu_target"]
        if "auto" not in tgt:
            if "@:3.8.0" in self.spec:
                args.append(
                    self.define(
                        "CMAKE_CXX_FLAGS", "--amdgpu-target={0}".format(",".join(tgt.value))
                    )
                )
            else:
                args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))

        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        if self.spec.satisfies("@4.5.0:"):
            args.append(self.define("ROCSOLVER_EMBED_FMT", "ON"))

        if self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))
        if self.spec.satisfies("@5.3.0:"):
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")

        return args

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        exe = Executable(join_path(self.build_directory, "clients", "staging", "rocsolver-test"))
        exe("--gtest_filter=checkin*-*known_bug*")
