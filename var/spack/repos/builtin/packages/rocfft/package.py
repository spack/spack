# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Rocfft(CMakePackage):
    """Radeon Open Compute FFT library"""

    homepage = "https://github.com/ROCm/rocFFT/"
    git = "https://github.com/ROCm/rocFFT.git"
    url = "https://github.com/ROCm/rocfft/archive/rocm-6.1.1.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath", "haampie")
    libraries = ["librocfft"]

    license("MIT")
    version("6.1.1", sha256="d517a931d49a1e59df4e494ab2b68e301fe7ebf39723863985567467f111111c")
    version("6.1.0", sha256="9e6643174a2b0f376127f43454e78d4feba6fac695d4cda9796da50005ecac66")
    version("6.0.2", sha256="d3e1f7a4dc661f1e5ffce02e2e01ae6c3c339bac8e93deaf175e4c03ddfea459")
    version("6.0.0", sha256="fb8ba56572702e77e4383d922cd1fee4ad3fa5f63a5ebdb3d9c354439a446992")
    version("5.7.1", sha256="202f11f60dc8738e29bbd1b397d419e032794f8bffb7f48f2b31f09cc5f08bc2")
    version("5.7.0", sha256="3c4a1537a6ec76dc9b622644fe3890647306bf9f28f61c5d2028259c31bb964f")
    version("5.6.1", sha256="a65861e453587c3e6393da75b0b1976508c61f968aecda77fbec920fea48489e")
    version("5.6.0", sha256="e3d4a6c1bdac78f9a22033f57011af783d560308103f73542f9e0e4dd133d38a")
    version("5.5.1", sha256="57423a64f5cdb1c37ff0891b6c17b59f73198d46be42db4ae23781ef2c0cd49d")
    version("5.5.0", sha256="9288152e66504b06082e4eed8cdb791b4f9ae2836b3defbeb4d2b54901b96485")
    version("5.4.3", sha256="ed9664adc9825c237327497bc4b23f020d50be7645647f14a45f4d943dd506e7")
    version("5.4.0", sha256="d35a67332f4425fba1824eed78cf98d5c9a17a422614ff3f4cba2461df952336")
    version("5.3.3", sha256="678c18710578c1fb36a0009311bb79de7607c3468f9102cfba56a866ebb7ff78")
    version("5.3.0", sha256="d655c5541c4aff4267e80e36d002fc3a55c2f84a0ae8631197c12af3bf03fa7d")
    with default_args(deprecated=True):
        version("5.2.3", sha256="0cee37886f01f1afb3ae5dad1164c819573c13c6675bff4eb668de334adbff27")
        version("5.2.1", sha256="6302349b6cc610a9a939377e2c7ffba946656a8d43f2e438ff0b3088f0f963ad")
        version("5.2.0", sha256="ebba280b7879fb4bc529a68072b98d4e815201f90d24144d672094bc241743d4")
        version("5.1.3", sha256="b4fcd03c1b07d465bb307ec33cc7fb50036dff688e497c5e52b2dec37f4cb618")
        version("5.1.0", sha256="dc11c9061753ae43a9d5db9c4674aa113a8adaf50818b2701cbb940894147f68")

    amdgpu_targets = ROCmPackage.amdgpu_targets

    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=auto_or_any_combination_of(*amdgpu_targets),
        sticky=True,
    )
    variant(
        "amdgpu_target_sram_ecc",
        description="AMD GPU architecture",
        values=auto_or_any_combination_of(*amdgpu_targets),
        sticky=True,
    )

    depends_on("cmake@3.16:", type="build")
    depends_on("python@3.6:", type="build")
    depends_on("sqlite@3.36:")

    depends_on("googletest@1.10.0:", type="test")
    depends_on("fftw@3.3.8:", type="test")
    depends_on("boost@1.64.0: +program_options", type="test")
    depends_on("rocm-openmp-extras", type="test")
    depends_on("hiprand", type="test")
    depends_on("rocrand", type="test")

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
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"rocm-cmake@{ver}:", type="build", when=f"@{ver}")

    # Patch to add spack build test support. No longer required from 5.2
    patch("0003-Fix-clients-fftw3-include-dirs-rocm-4.5.patch", when="@:5.1")
    # Patch to add install prefix header location for sqlite for 5.4
    patch("0004-fix-missing-sqlite-include-paths.patch", when="@5.4.0:5.5")
    # Patch to fix the build issue when --test=root is enabled
    # This adds  the include headers from the rocrand and fftw in the cmakelists.txt
    # issue is seen from 5.7.0 onwards
    patch(
        "0005-Fix-clients-tests-include-rocrand-fftw-include-dir-rocm-6.0.0.patch", when="@5.7.0:"
    )

    # Set LD_LIBRARY_PATH for executing the binaries from build directoryfix missing type
    # https://github.com/ROCm/rocFFT/pull/449)
    patch(
        "https://github.com/ROCm/rocFFT/commit/0ec78f1daac2d7fa1415f4deff0d129252c1c9de.patch?full_index=1",
        sha256="bac7873185ac60f2aaa50e278f0b8d52b4d79d586bf7f52db1da33559569ba54",
        when="@6.0.0",
    )

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        exe = Executable(join_path(self.build_directory, "clients", "staging", "rocfft-test"))
        exe("--gtest_filter=mix*:adhoc*")

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            return "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        return None

    def cmake_args(self):
        args = [
            self.define("BUILD_CLIENTS_TESTS", self.run_tests),
            self.define("SQLITE_USE_SYSTEM_PACKAGE", True),
        ]

        tgt = self.spec.variants["amdgpu_target"]

        if "auto" not in tgt:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))

        # See https://github.com/ROCm/rocFFT/issues/322
        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        if self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))

        if self.spec.satisfies("@5.3.0:"):
            args.append(self.define("CMAKE_INSTALL_LIBDIR", "lib"))

        return args
