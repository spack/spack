# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Hipsparselt(CMakePackage, ROCmPackage):
    """hipSPARSELt is a SPARSE marshalling library, with multiple supported backends.
    It sits between the application and a 'worker' SPARSE library, marshalling inputs into
    the backend library and marshalling results back to the application. hipSPARSELt exports
    an interface that does not require the client to change, regardless of the chosen backend.
    Currently, hipSPARSELt supports rocSPARSELt and cuSPARSELt v0.4 as backends."""

    homepage = "https://github.com/ROCm/hipsparselt"
    url = "https://github.com/ROCm/hipSPARSELt/archive/refs/tags/rocm-6.0.0.tar.gz"
    git = "https://github.com/ROCm/hipsparseLt.git"

    maintainers("srekolam", "afzpatel", "renjithravindrankannath")

    license("MIT")

    version("6.0.2", sha256="bdbceeae515f737131f0391ee3b7d2f7b655e3cf446e4303d93f083c59053587")
    version("6.0.0", sha256="cc4c7970601edbaa7f630b7ea24ae85beaeae466ef3e5ba63e11eab52465c157")

    amdgpu_targets = ROCmPackage.amdgpu_targets
    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=spack.variant.DisjointSetsOfValues(("auto",), ("none",), amdgpu_targets)
        .with_default("auto")
        .with_error(
            "the values 'auto' and 'none' are mutually exclusive with any of the other values"
        )
        .with_non_feature_values("auto", "none"),
        sticky=True,
    )
    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")

    for ver in ["6.0.0", "6.0.2"]:
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"hipsparse@{ver}", when=f"@{ver}")
        depends_on(f"rocm-openmp-extras@{ver}", when=f"@{ver}", type="test")

    depends_on("cmake@3.5:", type="build")
    depends_on("msgpack-c@3:")
    depends_on("python@3.6:")
    depends_on("py-virtualenv")
    depends_on("py-wheel")
    depends_on("py-pip")
    depends_on("py-pyyaml", type="test")
    depends_on("py-joblib")
    depends_on("googletest@1.10.0:", type="test")

    patch("0001-update-llvm-path-add-hipsparse-include-dir-for-spack.patch", when="@6.0")

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    def cmake_args(self):
        args = [
            self.define("Tensile_CODE_OBJECT_VERSION", "V3"),
            self.define("MSGPACK_DIR", self.spec["msgpack-c"].prefix),
            self.define_from_variant("BUILD_ADDRESS_SANITIZER", "asan"),
            self.define("BUILD_CLIENTS_TESTS", self.run_tests),
            self.define("BUILD_SHARED_LIBS", "ON"),
            self.define("BUILD_CLIENTS_SAMPLES", "OFF"),
        ]
        if "auto" not in self.spec.variants["amdgpu_target"]:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))
        if self.run_tests:
            args.append(
                self.define("ROCM_OPENMP_EXTRAS_DIR", self.spec["rocm-openmp-extras"].prefix)
            )
        return args
