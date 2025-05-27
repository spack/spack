# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.hooks.sbang import filter_shebang
from spack.package import *


class Hip(CMakePackage):
    """HIP is a C++ Runtime API and Kernel Language that allows developers to
    create portable applications for AMD and NVIDIA GPUs from
    single source code."""

    homepage = "https://github.com/ROCm/HIP"
    git = "https://github.com/ROCm/HIP.git"
    url = "https://github.com/ROCm/HIP/archive/rocm-6.2.4.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath", "haampie", "afzpatel")
    libraries = ["libamdhip64"]

    license("MIT")

    version("master", branch="master", deprecated=True)
    version("6.4.0", sha256="bec899ba67df9aa7056297e5ad104b8e36938b1bab22f1f418f69a8e0043d07f")
    version("6.3.3", sha256="aa3a5466304d1dbee0d976b50fccb710dd12e2e1d5534793396447c0ff845e2c")
    version("6.3.2", sha256="66a4eba98bd74fc7126ce7cb4d59653b22075fe95a70412fe283dc806ae366e0")
    version("6.3.1", sha256="76f862493c4912a06e0e0b8da3917c2ba7481f1e05f2c23ffd5e05f8c44e3037")
    version("6.3.0", sha256="950bfaf108a0af44eb169646f81f564f75f49e974acd06139b77245cfd327267")
    version("6.2.4", sha256="7a88edd689230b422250852a391b3b377b4371bbaef1e4f36d7fb699fcb0562b")
    version("6.2.1", sha256="1f130fa8d0a60cfb3560892c50ed7c57902b1398b21d3168f4be2d7ee512da96")
    version("6.2.0", sha256="95de10ef1815e8076a94a53bae3752dfd0e9f0abe513ca3fb79969773cff12d4")
    version("6.1.2", sha256="34b168f34d8e4365ef160863c1c9deaa193bdbe8cc98726fe7481c85534a4f64")
    version("6.1.1", sha256="30cba362ee2487fe50159b12a777edfe76346cd81510963e25b655f37c865049")
    version("6.1.0", sha256="b5e209eff044b629c65d735ce7d92b4861bb321caa7d97e7be4054f1b943982a")
    version("6.0.2", sha256="84163ffb5d81f192f4a879f3f9722db2402d72c2a90f104c5b2b8a4212f4f9b0")
    version("6.0.0", sha256="ba8ce0d0960b260ff44ab47da58f98b8df9b659835aa62e32e018a63379bbc79")
    version("5.7.1", sha256="ea34c75d2cff366fcdd45109c5be460a48d4fcf72b8a534368b54eae5d05db0e")
    version("5.7.0", sha256="8974a436e7f1daf232a77e27a215bcb24a8cc132aa11b5b885a7417ad4246074")
    version("5.6.1", sha256="1b0178da8e997eb0cbf2af63e1940f56aeddc8b9715d822d2c87fd60dbc01173")
    version("5.6.0", sha256="befbfb4691d4331b1fdfe1f17a862e82e962eb9fb90457b2c61a5130b3e6b85b")
    version("5.5.1", sha256="674caca5d55cc96451d790729f6dab0a16682d2ae9e13359e8648afda0ff97b3")
    version("5.5.0", sha256="0f5bf69ea8ea8200e352efd83725f1976d36c2eb9661057000bcf6118d61e6f3")
    with default_args(deprecated=True):
        version("5.4.3", sha256="f74b6d6b85830e60d26503fa35b599537a9f4c5bcfc05b49632d9998abf094f4")
        version("5.4.0", sha256="2e422a06c312b88929cc3303e793ac8f037cf39dbcfe7b4640a7fbb4fc7905c2")
        version("5.3.3", sha256="0e6988f531ed83f8b2271e9b3d42b73da7ff536d34cdd89f74648335b3bc18c8")
        version("5.3.0", sha256="7bed30f6bc3e4e08bd29a5001c17de0ad3a92a6a948864d884b9341f4c90965b")

    variant("rocm", default=True, description="Enable ROCm support")
    variant("cuda", default=False, description="Build with CUDA")
    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")
    conflicts("+cuda +rocm", msg="CUDA and ROCm support are mutually exclusive")
    conflicts("~cuda ~rocm", msg="CUDA or ROCm support is required")
    conflicts("~rocm +asan", msg="ROCm must be enabled for asan")

    conflicts("+asan", when="os=rhel9")
    conflicts("+asan", when="os=centos7")
    conflicts("+asan", when="os=centos8")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cuda", when="+cuda")

    depends_on("cmake@3.16.8:", type="build")
    depends_on("libedit", type="build")
    depends_on("perl@5.10:", type=("build", "run"))

    test_requires_compiler = True

    with when("+rocm"):
        depends_on("gl@4.5:")
        depends_on("py-cppheaderparser", type="build", when="@5.3.3:")
        depends_on("libx11", when="+asan")
        depends_on("xproto", when="+asan")
        for ver in [
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
            "6.1.2",
            "6.2.0",
            "6.2.1",
            "6.2.4",
        ]:
            depends_on(f"hsakmt-roct@{ver}", when=f"@{ver}")

        for ver in [
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
            "6.1.2",
            "6.2.0",
            "6.2.1",
            "6.2.4",
            "6.3.0",
            "6.3.1",
            "6.3.2",
            "6.3.3",
            "6.4.0",
        ]:
            depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")
            depends_on(f"comgr@{ver}", when=f"@{ver}")
            depends_on(f"llvm-amdgpu@{ver} +rocm-device-libs", when=f"@{ver}")
            depends_on(f"rocminfo@{ver}", when=f"@{ver}")
            depends_on(f"roctracer-dev-api@{ver}", when=f"@{ver}")

        for ver in [
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
            "6.1.2",
            "6.2.0",
            "6.2.1",
            "6.2.4",
            "6.3.0",
            "6.3.1",
            "6.3.2",
            "6.3.3",
            "6.4.0",
        ]:
            depends_on(f"hipify-clang@{ver}", when=f"@{ver}")

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
            "6.1.2",
            "6.2.0",
            "6.2.1",
            "6.2.4",
            "6.3.0",
            "6.3.1",
            "6.3.2",
            "6.3.3",
            "6.4.0",
        ]:
            depends_on(f"rocm-core@{ver}", when=f"@{ver}")

        # hipcc likes to add `-lnuma` by default :(
        # ref https://github.com/ROCm/HIP/pull/2202
        depends_on("numactl", when="@3.7.0:")
    for ver in [
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
        "6.1.2",
        "6.2.0",
        "6.2.1",
        "6.2.4",
        "6.3.0",
        "6.3.1",
        "6.3.2",
        "6.3.3",
        "6.4.0",
    ]:
        depends_on(f"hipcc@{ver}", when=f"@{ver}")

    for ver in ["6.2.0", "6.2.1", "6.2.4", "6.3.0", "6.3.1", "6.3.2", "6.3.3", "6.4.0"]:
        depends_on(f"rocprofiler-register@{ver}", when=f"@{ver}")

    # roc-obj-ls requirements
    depends_on("perl-file-which")
    depends_on("perl-uri-encode")

    # Add hip-amd sources thru the below
    for d_version, d_shasum in [
        ("5.5.1", "9c8cb7611b3a496a0e9db92269143ee33b608eb69a8384957ace04e135ac90e9"),
        ("5.5.0", "bf87ed3919987c1a3a3f293418d26b65b3f02b97464e48f0cfcdd8f35763a0b7"),
        ("5.4.3", "475edce0f29c4ccd82e5ee21d4cce4836f2b1e3b13cbc891475e423d38a0ebb9"),
        ("5.4.0", "c4b79738eb6e669160382b6c47d738ac59bd493fc681ca400ff012a2e8212955"),
        ("5.3.3", "36acce92af39b0fa06002e164f5a7f5a9c7daa19bf96645361325775a325499d"),
        ("5.3.0", "81e9bd5209a7b400c986f9bf1d7079bcf7169bbcb06fc4fe843644559a4d612e"),
    ]:
        resource(
            name="hipamd",
            url=f"https://github.com/ROCm/hipamd/archive/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="hipamd",
            when=f"@{d_version}",
        )
    # Add opencl sources thru the below
    for d_version, d_shasum in [
        ("5.5.1", "a8a62a7c6fc5398406d2203b8cb75621a24944688e545d917033d87de2724498"),
        ("5.5.0", "0df9fa0b8aa0c8e6711d34eec0fdf1ed356adcd9625bc8f1ce9b3e72090f3e4f"),
        ("5.4.3", "b0f8339c844a2e62773bd85cd1e7c5ecddfe71d7c8e8d604e1a1d60900c30873"),
        ("5.4.0", "a294639478e76c75dac0e094b418f9bd309309b07faf6af126cdfad9aab3c5c7"),
        ("5.3.3", "cab394e6ef16c35bab8de29a66b96a7dc0e7d1297aaacba3718fa1d369233c9f"),
        ("5.3.0", "d251e2efe95dc12f536ce119b2587bed64bbda013969fa72be58062788044a9e"),
    ]:
        resource(
            name="opencl",
            url=f"https://github.com/ROCm/ROCm-OpenCL-Runtime/archive/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="opencl",
            when=f"@{d_version}",
        )
    for d_version, d_shasum in [
        ("5.5.1", "1375fc7723cfaa0ae22a78682186d4804188b0a54990bfd9c0b8eb421b85e37e"),
        ("5.5.0", "efbae9a1ef2ab3de5ca44091e9bb78522e76759c43524c1349114f9596cc61d1"),
        ("5.4.3", "71d9668619ab57ec8a4564d11860438c5aad5bd161a3e58fbc49555fbd59182d"),
        ("5.4.0", "46a1579310b3ab9dc8948d0fb5bed4c6b312f158ca76967af7ab69e328d43138"),
        ("5.3.3", "f8133a5934f9c53b253d324876d74f08a19e2f5b073bc94a62fe64b0d2183a18"),
        ("5.3.0", "2bf14116b5e2270928265f5d417b3d0f0f2e13cbc8ec5eb8c80d4d4a58ff7e94"),
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
    # Add hip-clr sources thru the below
    for d_version, d_shasum in [
        ("6.4.0", "76fd0ad83da0dabf7c91ca4cff6c51f2be8ab259e08ad9743af47d1b3473c2ff"),
        ("6.3.3", "8e5adca8f8c2d99d4a4e49605dd6b56b7881b762ee8ce15b4a7000e3cd982fec"),
        ("6.3.2", "ec13dc4ffe212beee22171cb2825d2b16cdce103c835adddb482b9238cf4f050"),
        ("6.3.1", "bfb8a4a59e7bd958e2cd4bf6f14c6cdea601d9827ebf6dc7af053a90e963770f"),
        ("6.3.0", "829e61a5c54d0c8325d02b0191c0c8254b5740e63b8bfdb05eec9e03d48f7d2c"),
        ("6.2.4", "0a3164af7f997a4111ade634152957378861b95ee72d7060eb01c86c87208c54"),
        ("6.2.1", "e9cff3a8663defdbda833d49c9e7160171eca14dc285ffe4061378607d6c890d"),
        ("6.2.0", "620e4c6a7f05651cc7a170bc4700fef8cae002420307a667c638b981d00b25e8"),
        ("6.1.2", "1a1e21640035d957991559723cd093f0c7e202874423667d2ba0c7662b01fea4"),
        ("6.1.1", "2db02f335c9d6fa69befcf7c56278e5cecfe3db0b457eaaa41206c2585ef8256"),
        ("6.1.0", "49b23eef621f4e8e528bb4de8478a17436f42053a2f7fde21ff221aa683205c7"),
        ("6.0.2", "cb8ac610c8d4041b74fb3129c084f1e7b817ce1a5a9943feca1fa7531dc7bdcc"),
        ("6.0.0", "798b55b5b5fb90dd19db54f136d8d8e1da9ae1e408d5b12b896101d635f97e50"),
        ("5.7.1", "c78490335233a11b4d8a5426ace7417c555f5e2325de10422df06c0f0f00f7eb"),
        ("5.7.0", "bc2447cb6fd86dff6a333b04e77ce85755104d9011a14a044af53caf02449573"),
        ("5.6.1", "0b88af1e99643899d11b1c8cf8a3c46601051b328a5e0ffbd44ee88b7eb0db33"),
        ("5.6.0", "8dcd99110737a294f67a805639cf372890c8ca16c7603caaa793e71e84478fe4"),
    ]:
        resource(
            name="clr",
            url=f"https://github.com/ROCm/clr/archive/refs/tags/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="clr",
            when=f"@{d_version}",
        )

        # For avx build, the start address of values_ buffer in KernelParameters is not
        # correct as it is computed based on 16-byte alignment.
        patch(
            "https://github.com/ROCm/clr/commit/c4f773db0b4ccbbeed4e3d6c0f6bff299c2aa3f0.patch?full_index=1",
            sha256="5bb9b0e08888830ccf3a0a658529fe25f4ee62b5b8890f349bf2cc914236eb2f",
            working_dir="clr",
            when="@5.7:6.0",
        )
        patch(
            "https://github.com/ROCm/clr/commit/7868876db742fb4d44483892856a66d2993add03.patch?full_index=1",
            sha256="7668b2a710baf4cb063e6b00280fb75c4c3e0511575e8298a9c7ae5143f60b33",
            working_dir="clr",
            when="@5.7:6.0",
        )

    # Add hipcc sources thru the below
    for d_version, d_shasum in [
        ("5.7.1", "d47d27ef2b5de7f49cdfd8547832ac9b437a32e6fc6f0e9c1646f4b704c90aee"),
        ("5.7.0", "9f839bf7226e5e26f3150f8ba6eca507ab9a668e68b207736301b3bb9040c973"),
        ("5.6.1", "5800fac92b841ef6f52acda78d9bf86f83970bec0fb848a6265d239bdb7eb51a"),
        ("5.6.0", "fdb7fdc9e4648376120330f034ee8353038d34c8a015f9eb0c208c56eeddd097"),
    ]:
        resource(
            name="hipcc",
            url=f"https://github.com/ROCm/HIPCC/archive/refs/tags/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="hipcc",
            when=f"@{d_version}",
        )
    # Add hipother sources thru the below
    for d_version, d_shasum in [
        ("6.4.0", "53d5654d34e00f4bfa0846b291fe87ef6d43087349917159e663a842ea29a783"),
        ("6.3.3", "95cb2aab4bd996f0bd5f38427412cd768692a11fad70b97d20e402f32b1ef03e"),
        ("6.3.2", "1623d823de49471aae3ecb1fad0e9cdddf9301a4089f1fd44f78ac2ff0c20fb2"),
        ("6.3.1", "caa69147227bf72fa7b076867f84579456ef55af63efec29914265a80602df42"),
        ("6.3.0", "a28eb1e8fe239b41e744584d45d676925ca210968ecb21bfa60678cf8e86eeb7"),
        ("6.2.4", "b7ebcf8a2679e50d27c49ebec0dbea5a67573f8b8c3f4a29108c84b28b5bedee"),
        ("6.2.1", "5d99e498c1fece44a421574282fc89c6a2499979eaa9f850e5caa7fa3a8938b8"),
        ("6.2.0", "1f854b0c07d71b10450080e3bbffe47adaf10a9745a9212797d991756a100174"),
        ("6.1.2", "2740d1e3dcf1f2d07d2a8db6acf4c972941ae392172b83fd8ddcfe8706a40d0b"),
        ("6.1.1", "8b975623c8ed1db53feea2cfd5d29f2a615e890aee1157d0d17adeb97200643f"),
        ("6.1.0", "43a48ccc82f705a15852392ee7419e648d913716bfc04063a53d2d17979b1b46"),
        ("6.0.2", "0bebb3774debcecc0b29a0cc5aa98e373a3ee7acf161503d0d9c9d0ecc8b8010"),
        ("6.0.0", "d3bf62cc17c3c44fea52b34bcbf725e7af1afc3542c2884cefcd41f65371f552"),
    ]:
        resource(
            name="hipother",
            url=f"https://github.com/ROCm/hipother/archive/refs/tags/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="hipother",
            when=f"@{d_version} +cuda",
        )

    # Improve compilation without git repo and remove compiler rt linkage
    # for host and correction in CMake target path variable and
    # correcting the CMake path variable.
    patch("0013-remove-compiler-rt-linkage-for-host.5.3.0.patch", when="@5.3.0:5.4")
    patch("0014-hip-test-file-reorg-5.4.0.patch", when="@5.4.0:5.5")
    patch("0016-hip-sample-fix-hipMalloc-call.patch", when="@5.4.3:5.5")
    patch("0014-remove-compiler-rt-linkage-for-host.5.5.0.patch", when="@5.5")
    patch("0014-remove-compiler-rt-linkage-for-host.5.6.0.patch", when="@5.6.0:5.6")
    patch("0014-Remove-compiler-rt-linkage-for-host-for-5.7.0.patch", when="@5.7.0:5.7")
    patch("0014-remove-compiler-rt-linkage-for-host.6.0.patch", when="@6.0")
    patch("0014-remove-compiler-rt-linkage-for-host.6.1.patch", when="@6.1")
    patch("0015-reverting-operator-mixup-fix-for-slate.patch", when="@5.6:6.0")
    patch("0018-reverting-hipMemoryType-with-memoryType.patch", when="@6.0:6.2")

    # See https://github.com/ROCm/HIP/pull/3206
    patch(
        "https://github.com/ROCm/HIP/commit/50ee82f6bc4aad10908ce09198c9f7ebfb2a3561.patch?full_index=1",
        sha256="c469ddecbae6d4ee30132af7c37d5e7958420af2d083f2c50d93fc3a7d162c49",
        when="@5.2:5.7",
    )

    @property
    def root_cmakelists_dir(self):
        if self.spec.satisfies("@4.5:5.5"):
            return "hipamd"
        else:
            return "clr"

    def get_paths(self):
        if self.spec.external:
            # For external packages we only assume the `hip` prefix is known,
            # because spack does not set prefixes of dependencies of externals.
            hip_libs_at_top = os.path.basename(self.spec.prefix) != "hip"
            # We assume self.spec.prefix is  /opt/rocm-x.y.z for rocm-5.2.0 and newer
            # and /opt/rocm-x.y.z/hip for older versions
            # However, depending on how an external is found it can be at either level
            # of the installation path
            if self.spec.satisfies("@5.2.0:"):
                if hip_libs_at_top:
                    rocm_prefix = Prefix(self.spec.prefix)
                else:
                    rocm_prefix = Prefix(os.path.dirname(self.spec.prefix))
            else:
                # We assume self.spec.prefix is /opt/rocm-x.y.z/hip and rocm has a
                # default installation with everything installed under
                # /opt/rocm-x.y.z
                # Note that since the key hip library can also exist at the top of the
                # /opt/rocm-x.y.z/lib tree, it is possible that the package is detected
                # without the correct prefix.  Work around it.
                if hip_libs_at_top:
                    rocm_prefix = Prefix(self.spec.prefix)
                else:
                    rocm_prefix = Prefix(os.path.dirname(self.spec.prefix))

            if not os.path.isdir(rocm_prefix):
                msg = "Could not determine prefix for other rocm components\n"
                msg += "Either report a bug at github.com/spack/spack or "
                msg += "manually edit rocm_prefix in the package file as "
                msg += "a workaround."
                raise RuntimeError(msg)

            if hip_libs_at_top:
                hip_path = "{0}/hip".format(self.spec.prefix)
            else:
                hip_path = self.spec.prefix

            paths = {
                "hip-path": hip_path,
                "rocm-path": rocm_prefix,
                "llvm-amdgpu": rocm_prefix.llvm,
                "hsa-rocr-dev": rocm_prefix.hsa,
                "rocminfo": rocm_prefix,
                "comgr": rocm_prefix,
                "rocm-device-libs": rocm_prefix,
                "hipify-clang": rocm_prefix,
            }

            if self.spec.satisfies("@5.7:"):
                paths["hip-path"] = rocm_prefix
            if self.spec.satisfies("@6.0:"):
                paths["hsa-rocr-dev"] = rocm_prefix

        else:
            paths = {
                "hip-path": self.spec.prefix,
                "rocm-path": self.spec.prefix,
                "llvm-amdgpu": self.spec["llvm-amdgpu"].prefix,
                "hsa-rocr-dev": self.spec["hsa-rocr-dev"].prefix,
                "rocminfo": self.spec["rocminfo"].prefix,
                "comgr": self.spec["comgr"].prefix,
                "rocm-device-libs": self.spec["llvm-amdgpu"].prefix,
                "hipify-clang": self.spec["hipify-clang"].prefix,
            }
        paths["bitcode"] = paths["rocm-device-libs"].amdgcn.bitcode

        return paths

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

    def set_variables(self, env):
        if self.spec.satisfies("+rocm"):
            # Note: do not use self.spec[name] here, since not all dependencies
            # have defined prefixes when hip is marked as external.
            paths = self.get_paths()

            # Used in hipcc, but only useful when hip is external, since only then
            # there is a common prefix /opt/rocm-x.y.z.
            env.set("ROCM_PATH", paths["rocm-path"])
            if self.spec.satisfies("@5.4:"):
                env.set("HIPIFY_CLANG_PATH", paths["hipify-clang"])
            if self.spec.satisfies("@6.1:"):
                env.prepend_path("LD_LIBRARY_PATH", paths["hsa-rocr-dev"].lib)

            # hipcc recognizes HIP_PLATFORM == hcc and HIP_COMPILER == clang, even
            # though below we specified HIP_PLATFORM=rocclr and HIP_COMPILER=clang
            # in the CMake args.
            env.set("HIP_PLATFORM", "amd")

            env.set("HIP_COMPILER", "clang")

            # bin directory where clang++ resides
            env.set("HIP_CLANG_PATH", paths["llvm-amdgpu"].bin)

            # Path to hsa-rocr-dev prefix used by hipcc.
            env.set("HSA_PATH", paths["hsa-rocr-dev"])

            # This is a variable that does not exist in hipcc but was introduced
            # in a patch of ours since 3.5.0 to locate rocm_agent_enumerator:
            # https://github.com/ROCm/HIP/pull/2138
            env.set("ROCMINFO_PATH", paths["rocminfo"])

            # This one is used in hipcc to run `clang --hip-device-lib-path=...`
            env.set("DEVICE_LIB_PATH", paths["bitcode"])

            # And this is used in clang whenever the --hip-device-lib-path is not
            # used (e.g. when clang is invoked directly)
            env.set("HIP_DEVICE_LIB_PATH", paths["bitcode"])

            # Just the prefix of hip (used in hipcc)
            # Deprecated in 5.1.0 and breaks hipcc in 5.5.1+
            if self.spec.satisfies("@:5.4"):
                env.set("HIP_PATH", paths["hip-path"])

            # Used in comgr and seems necessary when using the JIT compiler, e.g.
            # hiprtcCreateProgram:
            # https://github.com/ROCm/ROCm-CompilerSupport/blob/rocm-4.0.0/lib/comgr/src/comgr-env.cpp
            env.set("LLVM_PATH", paths["llvm-amdgpu"])
            env.set("COMGR_PATH", paths["comgr"])

            # Finally we have to set --rocm-path=<prefix> ourselves, which is not
            # the same as --hip-device-lib-path (set by hipcc). It's used to set
            # default bin, include and lib folders in clang. If it's not set it is
            # infered from the clang install dir (and they try to find
            # /opt/rocm again...). If this path is set, there is no strict checking
            # and parsing of the <prefix>/bin/.hipVersion file. Let's just set this
            # to the hip prefix directory for non-external builds so that the
            # bin/.hipVersion file can still be parsed.
            # See also https://github.com/ROCm/HIP/issues/2223
            env.append_path(
                "HIPCC_COMPILE_FLAGS_APPEND", f"--rocm-path={paths['rocm-path']}", separator=" "
            )
            env.append_path(
                "HIPCC_LINK_FLAGS_APPEND", f"--rocm-path={paths['rocm-path']}", separator=" "
            )
        elif self.spec.satisfies("+cuda"):
            env.set("CUDA_PATH", self.spec["cuda"].prefix)
            env.set("HIP_PATH", self.spec.prefix)
            env.set("HIP_PLATFORM", "nvidia")

        # Set up hipcc/hip-clang to use the specific GCC toolchain that is
        # being used to compile. This is only important for external ROCm
        # installations, which may otherwise pick up the wrong GCC toolchain.
        if self.spec.external and self.spec.satisfies("%gcc"):
            # This is picked up by hipcc.
            env.append_path(
                "HIPCC_COMPILE_FLAGS_APPEND",
                f"--gcc-toolchain={self.compiler.prefix}",
                separator=" ",
            )
            env.append_path(
                "HIPCC_LINK_FLAGS_APPEND", f"--gcc-toolchain={self.compiler.prefix}", separator=" "
            )
            # This is picked up by CMake when using HIP as a CMake language.
            env.append_path("HIPFLAGS", f"--gcc-toolchain={self.compiler.prefix}", separator=" ")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        self.set_variables(env)

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        self.set_variables(env)

    def setup_dependent_build_environment(
        self, env: EnvironmentModifications, dependent_spec: Spec
    ) -> None:
        self.set_variables(env)

        if "amdgpu_target" in dependent_spec.variants:
            arch = dependent_spec.variants["amdgpu_target"]
            if "none" not in arch and "auto" not in arch:
                env.set("HCC_AMDGPU_TARGET", ",".join(arch.value))

    def setup_dependent_run_environment(
        self, env: EnvironmentModifications, dependent_spec: Spec
    ) -> None:
        self.setup_dependent_build_environment(env, dependent_spec)

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.hipcc = join_path(self.prefix.bin, "hipcc")

    def patch(self):
        if self.spec.satisfies("@5.2:5.4 +rocm"):
            filter_file(
                '"${ROCM_PATH}/llvm"',
                self.spec["llvm-amdgpu"].prefix,
                "hipamd/hip-config.cmake.in",
                string=True,
            )
        if self.spec.satisfies("@5.6.0:5.6 +rocm"):
            filter_file(
                '"${ROCM_PATH}/llvm"',
                self.spec["llvm-amdgpu"].prefix,
                "clr/hipamd/hip-config.cmake.in",
                string=True,
            )
        if self.spec.satisfies("@5.7:6.2 +rocm"):
            filter_file(
                '"${ROCM_PATH}/llvm"',
                self.spec["llvm-amdgpu"].prefix,
                "clr/hipamd/hip-config-amd.cmake",
                string=True,
            )
        if self.spec.satisfies("@6.3: +rocm"):
            filter_file(
                '"${ROCM_PATH}/llvm"',
                self.spec["llvm-amdgpu"].prefix,
                "clr/hipamd/hip-config-amd.cmake.in",
                string=True,
            )
        perl = self.spec["perl"].command

        if self.spec.satisfies("@:5.5"):
            with working_dir("bin"):
                filter_shebang("hipconfig")
            with working_dir("hipamd/bin"):
                filter_file("^#!/usr/bin/perl", f"#!{perl}", "roc-obj-extract", "roc-obj-ls")
        if self.spec.satisfies("@5.6:"):
            with working_dir("clr/hipamd/bin"):
                filter_file("^#!/usr/bin/perl", f"#!{perl}", "roc-obj-extract", "roc-obj-ls")
        if self.spec.satisfies("@5.6:5.7"):
            with working_dir("hipcc/bin"):
                filter_shebang("hipconfig")

        if self.spec.satisfies("+rocm"):
            numactl = self.spec["numactl"].prefix.lib
            if self.spec.satisfies("@:5.5"):
                with working_dir("bin"):
                    filter_file(" -lnuma", f" -L{numactl} -lnuma", "hipcc")
            elif self.spec.satisfies("@5.6:5.7"):
                with working_dir("hipcc/src"):
                    filter_file(" -lnuma", f" -L{numactl} -lnuma", "hipBin_amd.h")

    def cmake_args(self):
        args = [
            # Use the new behaviour of the policy CMP0074
            # (https://cmake.org/cmake/help/latest/policy/CMP0074.html) which will search
            # "prefixes specified by the <PackageName>_ROOT CMake variable".
            # From HIP 6.2 onwards the policy is set explicitly by HIP itself:
            # https://github.com/ROCm/clr/commit/a2a8dad980b0fa1a6086e0c0f95847ae80f5a2c6.
            self.define("CMAKE_POLICY_DEFAULT_CMP0074", "NEW")
        ]
        if self.spec.satisfies("+rocm"):
            # find_package(Clang) and find_package(LLVM) in clr/hipamd/src/hiprtc/CMakeLists.txt
            # should find llvm-amdgpu
            args.append(self.define("LLVM_ROOT", self.spec["llvm-amdgpu"].prefix))
            args.append(self.define("Clang_ROOT", self.spec["llvm-amdgpu"].prefix))

            args.append(self.define("HSA_PATH", self.spec["hsa-rocr-dev"].prefix))
            args.append(self.define("HIP_COMPILER", "clang"))
            args.append(
                self.define(
                    "PROF_API_HEADER_PATH",
                    self.spec["roctracer-dev-api"].prefix.roctracer.include.ext,
                )
            )
            args.append(self.define("HIP_RUNTIME", "rocclr"))
            args.append(self.define("HIP_PLATFORM", "amd"))
            if self.spec.satisfies("@5.6.0:"):
                args.append(self.define("HIP_LLVM_ROOT", self.spec["llvm-amdgpu"].prefix))
            if self.spec.satisfies("@6.1.0:") and self.spec.satisfies("+asan"):
                args.append(self.define("ADDRESS_SANITIZER", "ON"))
                args.append(
                    self.define("CMAKE_C_COMPILER", f"{self.spec['llvm-amdgpu'].prefix}/bin/clang")
                )
                args.append(
                    self.define(
                        "CMAKE_CXX_COMPILER", f"{self.spec['llvm-amdgpu'].prefix}/bin/clang++"
                    )
                )
                args.append(
                    self.define(
                        "CMAKE_CXX_FLAGS",
                        f"-I{self.spec['libx11'].prefix.include} "
                        f"-I{self.spec['mesa'].prefix.include} "
                        f"-I{self.spec['xproto'].prefix.include}",
                    )
                )

        if self.spec.satisfies("+cuda"):
            args.append(self.define("HIP_PLATFORM", "nvidia"))
            args.append(self.define("HIPNV_DIR", self.stage.source_path + "/hipother/hipnv"))

        args.append(self.define("HIP_COMMON_DIR", self.stage.source_path))
        args.append(self.define("HIP_CATCH_TEST", "OFF"))
        if self.spec.satisfies("@:5.5"):
            args.append(self.define("ROCCLR_PATH", self.stage.source_path + "rocclr"))
            args.append(self.define("AMD_OPENCL_PATH", self.stage.source_path + "opencl"))
        if self.spec.satisfies("@5.3.0:"):
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")
        if self.spec.satisfies("@5.6.0:"):
            args.append(self.define("ROCCLR_PATH", self.stage.source_path + "/clr/rocclr"))
            args.append(self.define("AMD_OPENCL_PATH", self.stage.source_path + "/clr/opencl"))
            args.append(self.define("CLR_BUILD_HIP", True))
            args.append(self.define("CLR_BUILD_OCL", False))
        if self.spec.satisfies("@5.6:5.7"):
            args.append(self.define("HIPCC_BIN_DIR", self.stage.source_path + "/hipcc/bin"))
        if self.spec.satisfies("@6.0:"):
            args.append(self.define("HIPCC_BIN_DIR", self.spec["hipcc"].prefix.bin))
        if self.spec.satisfies("@6.4.0:"):
            args.append(self.define("clang", f"{self.spec['llvm-amdgpu'].prefix}/bin/clang"))
        return args
