# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class RocmOpencl(CMakePackage):
    """OpenCL: Open Computing Language on ROCclr"""

    homepage = "https://github.com/ROCm/ROCm-OpenCL-Runtime"
    git = "https://github.com/ROCm/ROCm-OpenCL-Runtime.git"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["libOpenCL"]

    def url_for_version(self, version):
        if version == Version("3.5.0"):
            return (
                "https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime/archive/roc-3.5.0.tar.gz"
            )
        elif version <= Version("5.6.1"):
            url = (
                "https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime/archive/rocm-{0}.tar.gz"
            )
        else:
            url = "https://github.com/ROCm/clr/archive/refs/tags/rocm-{0}.tar.gz"
        return url.format(version)

    license("MIT")

    version("master", branch="main")
    version("6.0.2", sha256="cb8ac610c8d4041b74fb3129c084f1e7b817ce1a5a9943feca1fa7531dc7bdcc")
    version("6.0.0", sha256="798b55b5b5fb90dd19db54f136d8d8e1da9ae1e408d5b12b896101d635f97e50")
    version("5.7.1", sha256="c78490335233a11b4d8a5426ace7417c555f5e2325de10422df06c0f0f00f7eb")
    version("5.7.0", sha256="bc2447cb6fd86dff6a333b04e77ce85755104d9011a14a044af53caf02449573")
    version("5.6.1", sha256="ec26049f7d93c95050c27ba65472736665ec7a40f25920a868616b2970f6b845")
    version("5.6.0", sha256="52ab260d00d279c2a86c353901ffd88ee61b934ad89e9eb480f210656705f04e")
    version("5.5.1", sha256="a8a62a7c6fc5398406d2203b8cb75621a24944688e545d917033d87de2724498")
    version("5.5.0", sha256="0df9fa0b8aa0c8e6711d34eec0fdf1ed356adcd9625bc8f1ce9b3e72090f3e4f")
    version("5.4.3", sha256="b0f8339c844a2e62773bd85cd1e7c5ecddfe71d7c8e8d604e1a1d60900c30873")
    version("5.4.0", sha256="a294639478e76c75dac0e094b418f9bd309309b07faf6af126cdfad9aab3c5c7")
    version("5.3.3", sha256="cab394e6ef16c35bab8de29a66b96a7dc0e7d1297aaacba3718fa1d369233c9f")
    version("5.3.0", sha256="d251e2efe95dc12f536ce119b2587bed64bbda013969fa72be58062788044a9e")
    with default_args(deprecated=True):
        version("5.2.3", sha256="932ea3cd268410010c0830d977a30ef9c14b8c37617d3572a062b5d4595e2b94")
        version("5.2.1", sha256="eb4ff433f8894ca659802f81792646034f8088b47aca6ad999292bcb8d6381d5")
        version("5.2.0", sha256="80f73387effdcd987a150978775a87049a976aa74f5770d4420847b004dd59f0")
        version("5.1.3", sha256="44a7fac721abcd93470e1a7e466bdea0c668c253dee93e4f1ea9a72dbce4ba31")
        version("5.1.0", sha256="362d81303048cf7ed5d2f69fb65ed65425bc3da4734fff83e3b8fbdda51b0927")

    depends_on("cmake@3:", type="build")
    depends_on("gl@4.5:", type="link")
    depends_on("numactl", type="link")

    for d_version, d_shasum in [
        ("5.6.1", "cc9a99c7e4de3d9360c0a471b27d626e84a39c9e60e0aff1e8e1500d82391819"),
        ("5.6.0", "864f87323e793e60b16905284fba381a7182b960dd4a37fb67420c174442c03c"),
        ("5.5.1", "1375fc7723cfaa0ae22a78682186d4804188b0a54990bfd9c0b8eb421b85e37e"),
        ("5.5.0", "efbae9a1ef2ab3de5ca44091e9bb78522e76759c43524c1349114f9596cc61d1"),
        ("5.4.3", "71d9668619ab57ec8a4564d11860438c5aad5bd161a3e58fbc49555fbd59182d"),
        ("5.4.0", "46a1579310b3ab9dc8948d0fb5bed4c6b312f158ca76967af7ab69e328d43138"),
        ("5.3.3", "f8133a5934f9c53b253d324876d74f08a19e2f5b073bc94a62fe64b0d2183a18"),
        ("5.3.0", "2bf14116b5e2270928265f5d417b3d0f0f2e13cbc8ec5eb8c80d4d4a58ff7e94"),
        ("5.2.3", "0493c414d4db1af8e1eb30a651d9512044644244488ebb13478c2138a7612998"),
        ("5.2.1", "465ca9fa16869cd89dab8c2d66d9b9e3c14f744bbedaa1d215b0746d77a500ba"),
        ("5.2.0", "37f5fce04348183bce2ece8bac1117f6ef7e710ca68371ff82ab08e93368bafb"),
        ("5.1.3", "ddee63cdc6515c90bab89572b13e1627b145916cb8ede075ef8446cbb83f0a48"),
        ("5.1.0", "f4f265604b534795a275af902b2c814f416434d9c9e16db81b3ed5d062187dfa"),
    ]:
        resource(
            name="rocclr",
            url=f"https://github.com/ROCm/ROCclr/archive/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="rocclr",
            when=f"@{d_version}",
        )
    # For avx build, the start address of values_ buffer in KernelParameters is not
    # correct as it is computed based on 16-byte alignment.
    patch(
        "https://github.com/ROCm/clr/commit/c4f773db0b4ccbbeed4e3d6c0f6bff299c2aa3f0.patch?full_index=1",
        sha256="5bb9b0e08888830ccf3a0a658529fe25f4ee62b5b8890f349bf2cc914236eb2f",
        when="@5.7:",
    )
    patch(
        "https://github.com/ROCm/clr/commit/7868876db742fb4d44483892856a66d2993add03.patch?full_index=1",
        sha256="7668b2a710baf4cb063e6b00280fb75c4c3e0511575e8298a9c7ae5143f60b33",
        when="@5.7:",
    )

    # Patch to set package installation path for OpenCL.
    patch("0001-fix-build-error-rocm-opencl-5.1.0.patch", when="@5.1")

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
        "master",
    ]:
        depends_on(f"comgr@{ver}", type="build", when=f"@{ver}")
        depends_on(f"hsa-rocr-dev@{ver}", type="link", when=f"@{ver}")

    for ver in ["5.5.0", "5.5.1", "5.6.0", "5.6.1", "5.7.0", "5.7.1", "6.0.0", "6.0.2"]:
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            return "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        return None

    def cmake_args(self):
        args = ["-DUSE_COMGR_LIBRARY=yes", "-DBUILD_TESTS=ON"]
        if self.spec.satisfies("@:5.6"):
            args.append(self.define("ROCCLR_PATH", self.stage.source_path + "/rocclr"))
            args.append(self.define("AMD_OPENCL_PATH", self.stage.source_path))
        if self.spec.satisfies("@5.7:"):
            args.append(self.define("CLR_BUILD_HIP", False))
            args.append(self.define("CLR_BUILD_OCL", True))

        return args

    def setup_run_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib),
        env.set("OCL_ICD_VENDORS", self.prefix.vendors + "/")

    @run_after("install")
    def post_install(self):
        vendor_config_path = join_path(self.prefix + "/vendors")
        mkdirp(vendor_config_path)

        config_file_name = "amdocl64_30800.icd"
        with open(join_path(vendor_config_path, config_file_name), "w") as f:
            f.write("libamdocl64.so")

    test_src_dir = "tests/ocltst"

    def test(self):
        test_dir = join_path(self.spec["rocm-opencl"].prefix, self.test_src_dir)
        with working_dir(test_dir, create=True):
            os.environ["LD_LIBRARY_PATH"] += os.pathsep + test_dir
            args = ["-m", "liboclruntime.so", "-A", "oclruntime.exclude"]
            self.run_test("ocltst", args)
            args = ["-m", "liboclperf.so", "-A", "oclperf.exclude"]
            self.run_test("ocltst", args)
