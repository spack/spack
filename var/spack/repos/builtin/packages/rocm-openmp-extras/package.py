# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *

tools_url = "https://github.com/ROCm"
compute_url = "https://github.com/ROCm"

# Arrays of hashes are in order of the versions array below
# For example array[0] = 3.9.0, array[1] = 3.10.0, etc.

aomp = [
    "e69fe0c933cb30daafe49d9f1df71fe16f387e0287bba921995feeefdf9ac262",
    "8bab3d621343f419b29043ac0cb56e062f114991dc3ec1e33e786f771deecc8f",
    "20e21312816272222d1f427ea72a99a9a67077078552f5e2638a40860d161d25",
    "c0aa6997e889d6ce0e37cfa6a2e91c5c0b54cda1673abdcabcf34da1ba78ba72",
    "4ba1792095427588c484feed01f2f48e66aaad26bc000cbc74a15032551699e7",
    "371ed037b95b83fac64fb2ff2fc17313fe7d3befc8671f0a08f0e2072393fa5b",
    "c86141fcde879fc78d06a41ba6a26ff528da539c6a1be8b714f635182c66e3f4",
    "bbca540897848fa95fd0f14fc05ab6deda31299a061424972d5e2bc09c7543dc",
    "7f90634fb621169b21bcbd920c2e299acc88ba0eeb1a33fd40ae26e13201b652",
    "23cc7d1c82e35c74f48285a0a1c27e7b3cae1767568bb7b9367ea21f53dd6598",
    "9ec03a69cc462ada43e1fd4ca905a765b08c10e0911fb7a202c893cc577855e6",
    "0673820a81986c9e2f28f15bbb45ad18934bca56a9d08aae6c49ec3895b38487",
    "6c051bf7625f682ba3d2ea80b46a38ca2cbcd20f5d89ae3433602d3e7ef0403a",
    "4f34fa02db410808c5e629f30f8804210b42c4ff7d31aa80606deaed43054c3c",
    "ed7bbf92230b6535a353ed032a39a9f16e9987397798100392fc25e40c8a1a4e",
    "1b2c0934ef16e17b2377944fae8c9b3db6dc64b7e43932ddfe2eeefdf6821410",
    "d6e13a15d5d25990d4bacbac8fabe2eb07973829f2e69abbc628e0736f95caf9",
    "832b7c48149a730619b577a2863b8d1bf1b2551eda5b815e1865a044929ab9fa",
    "62a5036a2299ed2e3053ee00b7ea1800469cd545fea486fa17266a8b3acfaf5d",
]

devlib = [
    "47dbcb41fb4739219cadc9f2b5f21358ed2f9895ce786d2f7a1b2c4fd044d30f",
    "c41958560ec29c8bf91332b9f668793463904a2081c330c0d828bf2f91d4f04e",
    "901674bc941115c72f82c5def61d42f2bebee687aefd30a460905996f838e16c",
    "e5855387ce73ed483ed0d03dbfef31f297c6ca66cf816f6816fd5ee373fc8225",
    "16b7fc7db4759bd6fb54852e9855fa16ead76c97871d7e1e9392e846381d611a",
    "f7e1665a1650d3d0481bec68252e8a5e68adc2c867c63c570f6190a1d2fe735c",
    "963c9a0561111788b55a8c3b492e2a5737047914752376226c97a28122a4d768",
    "d68813ded47179c39914c8d1b76af3dad8c714b10229d1e2246af67609473951",
    "f4f7281f2cea6d268fcc3662b37410957d4f0bc23e0df9f60b12eb0fcdf9e26e",
    "5ab95aeb9c8bed0514f96f7847e21e165ed901ed826cdc9382c14d199cbadbd3",
    "3b5f6dd85f0e3371f6078da7b59bf77d5b210e30f1cc66ef1e2de6bbcb775833",
    "efb5dcdca9b3a9fbe408d494fb4a23e0b78417eb5fa8eebd4a5d226088f28921",
    "f0dfab272ff936225bfa1e9dabeb3c5d12ce08b812bf53ffbddd2ddfac49761c",
    "0f8780b9098573f1c456bdc84358de924dcf00604330770a383983e1775bf61e",
    "703de8403c0bd0d80f37c970a698f10f148daf144d34f982e4484d04f7c7bbef",
    "198df4550d4560537ba60ac7af9bde31d59779c8ec5d6309627f77a43ab6ef6f",
    "c6d88b9b46e39d5d21bd5a0c1eba887ec473a370b1ed0cebd1d2e910eedc5837",
    "6bd9912441de6caf6b26d1323e1c899ecd14ff2431874a2f5883d3bc5212db34",
    "f1a67efb49f76a9b262e9735d3f75ad21e3bd6a05338c9b15c01e6c625c4460d",
]

llvm = [
    "db5d45c4a7842a908527c1b7b8d4a40c688225a41d23cfa382eab23edfffdd10",
    "d236a2064363c0278f7ba1bb2ff1545ee4c52278c50640e8bb2b9cfef8a2f128",
    "0f892174111b78a02d1a00f8f46d9f80b9abb95513a7af38ecf2a5a0882fe87f",
    "3644e927d943d61e22672422591c47a62ff83e3d87ced68439822156d8f79abf",
    "1b852711aec3137b568fb65f93606d37fdcd62e06f5da3766f2ffcd4e0c646df",
    "4e3fcddb5b8ea8dcaa4417e0e31a9c2bbdc9e7d4ac3401635a636df32905c93e",
    "5296d5e474811c7d1e456cb6d5011db248b79b8d0512155e8a6c2aa5b5f12d38",
    "ff54f45a17723892cd775c1eaff9e5860527fcfd33d98759223c70e3362335bf",
    "a844d3cc01613f6284a75d44db67c495ac1e9b600eacbb1eb13d2649f5d5404d",
    "5dc6c99f612b69ff73145bee17524e3712990100e16445b71634106acf7927cf",
    "7d7181f20f89cb0715191aa32914186c67a34258c13457055570d47e15296553",
    "e922bd492b54d99e56ed88c81e2009ed6472059a180b10cc56ce1f9bd2d7b6ed",
    "045e43c0c4a3f4f2f1db9fb603a4f1ea3d56e128147e19ba17909eb57d7f08e5",
    "4abdf00b297a77c5886cedb37e63acda2ba11cb9f4c0a64e133b05800aadfcf0",
    "6b54c422e45ad19c9bf5ab090ec21753e7f7d854ca78132c30eb146657b168eb",
    "c673708d413d60ca8606ee75c77e9871b6953c59029c987b92f2f6e85f683626",
    "7d35acc84de1adee65406f92a369a30364703f84279241c444cd93a48c7eeb76",
    "6bd9912441de6caf6b26d1323e1c899ecd14ff2431874a2f5883d3bc5212db34",
    "f1a67efb49f76a9b262e9735d3f75ad21e3bd6a05338c9b15c01e6c625c4460d",
]

flang = [
    "d95e36f3b93097ab6fb319c744ddc71cd94af0c358accc1e5224c2bbd431266d",
    "d7847b5c6e1344dc0b4723dbe76a859257b4c242644dedb34e425f07738530d4",
    "20f48cac9b58496230fa2428eba4e15ec0a6e92d429569b154a328b7a8c5da17",
    "012a9c10a7d2a248dc40510e2f5c02a54b5f6bc39961500dc48b6780dac5ad67",
    "496f00918721c72eae0bd926a5a8f1f35bd443f6b22bc08e2a42c67e44a4dbaf",
    "ef1256ddf6cd9de10a1b88df4736dce48295136983a7e31eadd942fb39b156f7",
    "ddccd866d0c01086087fe21b5711668f85bcf9cbd9f62853f8bda32eaedb5339",
    "fae8195a5e1b3778e31dbc6cbeedeae9998ea4b5a54215534af41e91fdcb8ba0",
    "b283d76244d19ab16c9d087ee7de0d340036e9c842007aa9d288aa4e6bf3749f",
    "a18522588686672150c7862f2b23048a429baa4a66010c4196e969cc77bd152c",
    "7c3b4eb3e95b9e2f91234f202a76034628d230a92e57b7c5ee9dcca1097bec46",
    "fcefebddca0b373da81ff84f0f5469a1ef77a05430a5195d0f2e6399d3af31c3",
    "5ebcbca2e03bd0686e677f44ea551e97bd9395c6b119f832fa784818733aa652",
    "cc4f1973b1b8e7bcc4f09e3381bae4e1a2e51ea4e2598fc1b520ccb8bf24d28c",
    "8fd618d81af092416b267c4d00c801731f7a00c0f8d4aedb795e52a4ec1bf183",
    "fcb319ddb2aa3004a6ae60370ab4425f529336b1cee50f29200e697e61b53586",
    "8e6469415880bb068d788596b3ed713a24495eb42788f98cca92e73a2998f703",
    "51ecd2c154568c971f5b46ff0e1e1b57063afe28d128fc88c503de88f7240267",
    "1bcaa73e73a688cb092f01987cf3ec9ace4aa1fcaab2b812888c610722c4501d",
]

extras = [
    "c3a2a83d8f586ee765df96a692ebe010631446f700273fa31738ea260dfc35f7",
    "2e3151a47d77166d071213af2a1691487691aae0abd5c1718d818a6d7d09cb2d",
    "817c2e8975e56a8875ff56f9d1ea34d5e7e50f1b541b7f1236e3e5c8d9eee47f",
    "8b738225f0be39f27bba64c014816cfa1b79f2c7cf2d0e31fbc0fffb6c26e429",
    "f42ca7d85b0b64e6890502f1cf8309ef97f707829876742da2ea5c2cdf3ad8ac",
    "b3beee383d9c130666c230595c950bdc2ce4c7a99d728b9ddf1bca3963152223",
    "b26b9f4b11a9ccfab53d0dd55aada7e5b98f7ab51981cb033b376321dd44bf87",
    "2546becd4b182d1e366f47660c731c8ff7366b6306782f04706b6a7bf4e2094c",
    "d393f27a85c9229433b50daee8154e11517160beb1049c1de9c55fc31dd11fac",
    "8f49026a80eb8685cbfb6d3d3b9898dd083df4d71893984ae5330d4804c685fb",
    "8955aa9d039fd6c1ff2e26d7298f0bf09bbcf03f09c6df92c91a9ab2510df9da",
    "017bfed52fbe08185d8dbde79377918454215683562519a9e47acf403d9a1c29",
    "437e2017cfe2ab73b15ada0fc1ea88f794f0b108cc5410f457268ae7e4e8985a",
    "be59433dd85d4b8f0eaff87e0cc424a814152c67f3a682d1343c4bd61dd49a0f",
    "8060c6879708faf5f7d417b19a479dec9b7b9583a1b885f12d247faf831f7f0b",
    "f37e1107e4da5b083e794244f3d0c9fd073ccb6fd6015e635349d8f0d679c4b8",
    "b2e117d703cefdc2858adaeee5bad95e9b6dab6263a9c13891a79a7b1e2defb6",
    "57d6d9d26c0cb6ea7f8373996c41165f463ae7936d32e5793822cfae03900f8f",
    "3dc837fbfcac64e000e1b5518e4f8a6b260eaf1a3e74152d8b8c22f128f575b7",
]

versions = [
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
]
versions_dict = dict()  # type: Dict[str,Dict[str,str]]
components = ["aomp", "devlib", "llvm", "flang", "extras"]
component_hashes = [aomp, devlib, llvm, flang, extras]

# Loop through versions and create necessary dictionaries of components
for outer_index, item in enumerate(versions):
    for inner_index, component in enumerate(component_hashes):
        versions_dict.setdefault(item, {})[components[inner_index]] = component_hashes[
            inner_index
        ][outer_index]


class RocmOpenmpExtras(Package):
    """OpenMP support for ROCm LLVM."""

    homepage = tools_url + "/aomp"
    url = tools_url + "/aomp/archive/rocm-6.1.1.tar.gz"
    tags = ["rocm"]

    license("Apache-2.0")

    maintainers("srekolam", "renjithravindrankannath", "estewart08")
    version("6.1.1", sha256=versions_dict["6.1.1"]["aomp"])
    version("6.1.0", sha256=versions_dict["6.1.0"]["aomp"])
    version("6.0.2", sha256=versions_dict["6.0.2"]["aomp"])
    version("6.0.0", sha256=versions_dict["6.0.0"]["aomp"])
    version("5.7.1", sha256=versions_dict["5.7.1"]["aomp"])
    version("5.7.0", sha256=versions_dict["5.7.0"]["aomp"])
    version("5.6.1", sha256=versions_dict["5.6.1"]["aomp"])
    version("5.6.0", sha256=versions_dict["5.6.0"]["aomp"])
    version("5.5.1", sha256=versions_dict["5.5.1"]["aomp"])
    version("5.5.0", sha256=versions_dict["5.5.0"]["aomp"])
    version("5.4.3", sha256=versions_dict["5.4.3"]["aomp"])
    version("5.4.0", sha256=versions_dict["5.4.0"]["aomp"])
    version("5.3.3", sha256=versions_dict["5.3.3"]["aomp"])
    version("5.3.0", sha256=versions_dict["5.3.0"]["aomp"])
    version("5.2.3", sha256=versions_dict["5.2.3"]["aomp"], deprecated=True)
    version("5.2.1", sha256=versions_dict["5.2.1"]["aomp"], deprecated=True)
    version("5.2.0", sha256=versions_dict["5.2.0"]["aomp"], deprecated=True)
    version("5.1.3", sha256=versions_dict["5.1.3"]["aomp"], deprecated=True)
    version("5.1.0", sha256=versions_dict["5.1.0"]["aomp"], deprecated=True)

    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")

    depends_on("cmake@3:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("python@3:", type="build")
    depends_on("perl-data-dumper", type="build")
    depends_on("awk", type="build")
    depends_on("elfutils", type=("build", "link"))
    depends_on("libffi", type=("build", "link"))
    depends_on("libdrm", when="@5.7:6.0")
    depends_on("numactl", when="@5.7:6.0")

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
    ]:
        depends_on(f"hsakmt-roct@{ver}", when=f"@{ver}")
        depends_on(f"comgr@{ver}", when=f"@{ver}")
        depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")
        depends_on(f"llvm-amdgpu@{ver}", when=f"@{ver}")

        resource(
            name="rocm-device-libs",
            url=f"{compute_url}/ROCm-Device-Libs/archive/rocm-{ver}.tar.gz",
            sha256=versions_dict[ver]["devlib"],
            expand=True,
            destination="rocm-openmp-extras",
            placement="rocm-device-libs",
            when=f"@{ver}",
        )
        resource(
            name="flang",
            url=f"{tools_url}/flang/archive/rocm-{ver}.tar.gz",
            sha256=versions_dict[ver]["flang"],
            expand=True,
            destination="rocm-openmp-extras",
            placement="flang",
            when=f"@{ver}",
        )

        resource(
            name="aomp-extras",
            url=f"{tools_url}/aomp-extras/archive/rocm-{ver}.tar.gz",
            sha256=versions_dict[ver]["extras"],
            expand=True,
            destination="rocm-openmp-extras",
            placement="aomp-extras",
            when=f"@{ver}",
        )

        resource(
            name="llvm-project",
            url=f"{compute_url}/llvm-project/archive/rocm-{ver}.tar.gz",
            sha256=versions_dict[ver]["llvm"],
            expand=True,
            destination="rocm-openmp-extras",
            placement="llvm-project",
            when=f"@{ver}",
        )
    for ver in ["6.1.0", "6.1.1"]:
        depends_on(f"hsakmt-roct@{ver}", when=f"@{ver}")
        depends_on(f"comgr@{ver}", when=f"@{ver}")
        depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")
        depends_on(f"llvm-amdgpu@{ver}", when=f"@{ver}")

        resource(
            name="flang",
            url=f"{tools_url}/flang/archive/rocm-{ver}.tar.gz",
            sha256=versions_dict[ver]["flang"],
            expand=True,
            destination="rocm-openmp-extras",
            placement="flang",
            when=f"@{ver}",
        )

        resource(
            name="aomp-extras",
            url=f"{tools_url}/aomp-extras/archive/rocm-{ver}.tar.gz",
            sha256=versions_dict[ver]["extras"],
            expand=True,
            destination="rocm-openmp-extras",
            placement="aomp-extras",
            when=f"@{ver}",
        )

        resource(
            name="llvm-project",
            url=f"{compute_url}/llvm-project/archive/rocm-{ver}.tar.gz",
            sha256=versions_dict[ver]["llvm"],
            expand=True,
            destination="rocm-openmp-extras",
            placement="llvm-project",
            when=f"@{ver}",
        )
    patch("0001-Linking-hsakmt-libdrm-and-numactl-libraries.patch", when="@5.7:6.0")
    patch(
        "0001-Linking-hsakmt-libdrm-and-numactl-libraries-6.1.patch",
        working_dir="rocm-openmp-extras/llvm-project/openmp/libomptarget",
        when="@6.1",
    )

    def setup_run_environment(self, env):
        devlibs_prefix = self.spec["llvm-amdgpu"].prefix
        openmp_extras_prefix = self.spec["rocm-openmp-extras"].prefix
        llvm_prefix = self.spec["llvm-amdgpu"].prefix
        hsa_prefix = self.spec["hsa-rocr-dev"].prefix
        env.set("AOMP", "{0}".format(llvm_prefix))
        env.set("HIP_DEVICE_LIB_PATH", "{0}/amdgcn/bitcode".format(devlibs_prefix))
        env.prepend_path("CPATH", "{0}/include".format(openmp_extras_prefix))
        env.prepend_path("LIBRARY_PATH", "{0}/lib".format(openmp_extras_prefix))
        if self.spec.satisfies("@5.3.0:"):
            env.prepend_path("LD_LIBRARY_PATH", "{0}/lib".format(openmp_extras_prefix))
            env.prepend_path("LD_LIBRARY_PATH", "{0}/lib".format(hsa_prefix))
        env.set("AOMP_GPU", "`{0}/bin/mygpu`".format(openmp_extras_prefix))

    def setup_build_environment(self, env):
        openmp_extras_prefix = self.spec["rocm-openmp-extras"].prefix
        llvm_prefix = self.spec["llvm-amdgpu"].prefix
        env.set("AOMP", "{0}".format(llvm_prefix))
        env.set("FC", "{0}/bin/flang".format(openmp_extras_prefix))
        if self.spec.satisfies("+asan"):
            env.set("SANITIZER", 1)
            env.set("VERBOSE", 1)
            env.set(
                "LDSHARED",
                self.spec["llvm-amdgpu"].prefix.bin.clang
                + " -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-z,relro -g -fwrapv -O2",
            )
        gfx_list = "gfx700 gfx701 gfx801 gfx803 gfx900 gfx902 gfx906 gfx908"

        if self.spec.version >= Version("4.3.1"):
            gfx_list = gfx_list + " gfx90a gfx1030 gfx1031"
        env.set("GFXLIST", gfx_list)

    def patch(self):
        src = self.stage.source_path
        aomp_extras = "{0}/rocm-openmp-extras/aomp-extras/aomp-device-libs"
        libomptarget = "{0}/rocm-openmp-extras/llvm-project/openmp/libomptarget"
        flang = "{0}/rocm-openmp-extras/flang/"

        plugin = "/plugins/amdgpu/CMakeLists.txt"

        if self.spec.version < Version("5.2.0"):
            filter_file(
                "{ROCM_DIR}/amdgcn/bitcode",
                "{DEVICE_LIBS_DIR}",
                aomp_extras.format(src) + "/aompextras/CMakeLists.txt",
                libomptarget.format(src) + "/deviceRTLs/amdgcn/CMakeLists.txt",
            )
        if self.spec.satisfies("@6.1"):
            filter_file(
                r"${HSAKMT_LIB_PATH}",
                "${HSAKMT_LIB_PATH} ${HSAKMT_LIB64}"
                + "${HSAKMT_LIB} ${LIBDRM_LIB} ${NUMACTL_DIR}/lib",
                libomptarget.format(src) + "/CMakeLists.txt",
            )
            filter_file(
                r"${LIBOMPTARGET_LLVM_INCLUDE_DIRS}",
                "${LIBOMPTARGET_LLVM_INCLUDE_DIRS} ${HSAKMT_INC_PATH}",
                libomptarget.format(src) + "/../CMakeLists.txt",
            )
            filter_file(
                r"${LIBOMPTARGET_LLVM_INCLUDE_DIRS}",
                "${LIBOMPTARGET_LLVM_INCLUDE_DIRS} ${HSAKMT_INC_PATH}",
                libomptarget.format(src) + "/CMakeLists.txt",
            )

        # Openmp adjustments
        # Fix relocation error with libffi by not using static lib.
        filter_file(
            "libffi.a",
            "",
            libomptarget.format(src) + "/cmake/Modules/LibomptargetGetDependencies.cmake",
        )

        filter_file(
            r"{OPENMP_INSTALL_LIBDIR}",
            "{OPENMP_INSTALL_LIBDIR}/libdevice",
            libomptarget.format(src) + "/deviceRTLs/amdgcn/CMakeLists.txt",
        )

        if self.spec.version <= Version("5.1.3"):
            filter_file(
                r"{ROCM_DIR}/amdgcn/bitcode",
                "{DEVICE_LIBS_DIR}",
                libomptarget.format(src) + "/deviceRTLs/libm/CMakeLists.txt",
            )

        filter_file(
            "-nogpulib",
            "-nogpulib -nogpuinc",
            libomptarget.format(src) + "/deviceRTLs/amdgcn/CMakeLists.txt",
        )

        filter_file(
            "-x hip",
            "-x hip -nogpulib -nogpuinc",
            libomptarget.format(src) + "/deviceRTLs/amdgcn/CMakeLists.txt",
        )

        filter_file(
            "-c ",
            "-c -nogpulib -nogpuinc -I{LIMIT}",
            libomptarget.format(src) + "/hostrpc/CMakeLists.txt",
        )

        filter_file(
            r"${ROCM_DIR}/hsa/include ${ROCM_DIR}/hsa/include/hsa",
            "${HSA_INCLUDE}/hsa/include ${HSA_INCLUDE}/hsa/include/hsa",
            libomptarget.format(src) + plugin,
            string=True,
        )

        filter_file("{ROCM_DIR}/hsa/lib", "{HSA_LIB}", libomptarget.format(src) + plugin)

        filter_file(
            r"{ROCM_DIR}/lib\)",
            "{HSAKMT_LIB})\nset(HSAKMT_LIB64 ${HSAKMT_LIB64})",
            libomptarget.format(src) + plugin,
        )

        filter_file(
            r"-L${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS}",
            "-L${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS} -L${HSAKMT_LIB64}",
            libomptarget.format(src) + plugin,
            string=True,
        )

        filter_file(
            r"-rpath,${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS}",
            "-rpath,${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS}" + ",-rpath,${HSAKMT_LIB64}",
            libomptarget.format(src) + plugin,
            string=True,
        )

        filter_file("{ROCM_DIR}/include", "{COMGR_INCLUDE}", libomptarget.format(src) + plugin)

        filter_file(
            r"-L${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX}",
            "-L${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX} -L${COMGR_LIB}",
            libomptarget.format(src) + plugin,
            string=True,
        )

        filter_file(
            r"rpath,${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX}",
            "rpath,${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX}" + "-Wl,-rpath,${COMGR_LIB}",
            libomptarget.format(src) + plugin,
            string=True,
        )

        filter_file(
            "ADDITIONAL_VERSIONS 2.7",
            "ADDITIONAL_VERSIONS 3",
            flang.format(src) + "CMakeLists.txt",
        )

    def install(self, spec, prefix):
        src = self.stage.source_path
        gfx_list = os.environ["GFXLIST"]
        gfx_list = gfx_list.replace(" ", ";")
        openmp_extras_prefix = self.spec["rocm-openmp-extras"].prefix
        devlibs_prefix = self.spec["llvm-amdgpu"].prefix
        if self.spec.satisfies("@6.1:"):
            devlibs_src = "{0}/rocm-openmp-extras/llvm-project/amd/device-libs".format(src)
        else:
            devlibs_src = "{0}/rocm-openmp-extras/rocm-device-libs".format(src)
        hsa_prefix = self.spec["hsa-rocr-dev"].prefix
        hsakmt_prefix = self.spec["hsakmt-roct"].prefix
        if self.spec.satisfies("@5.7:6.1"):
            libdrm_prefix = self.spec["libdrm"].prefix
            numactl_prefix = self.spec["numactl"].prefix
        comgr_prefix = self.spec["comgr"].prefix
        llvm_inc = "/rocm-openmp-extras/llvm-project/llvm/include"
        llvm_prefix = self.spec["llvm-amdgpu"].prefix
        omp_bin_dir = "{0}/bin".format(openmp_extras_prefix)
        omp_lib_dir = "{0}/lib".format(openmp_extras_prefix)
        bin_dir = "{0}/bin".format(llvm_prefix)
        lib_dir = "{0}/lib".format(llvm_prefix)
        flang_warning = "-Wno-incompatible-pointer-types-discards-qualifiers"
        libpgmath = "/rocm-openmp-extras/flang/runtime/libpgmath/lib/common"
        elfutils_inc = spec["elfutils"].prefix.include
        ffi_inc = spec["libffi"].prefix.include

        # flang1 and flang2 symlink needed for build of flang-runtime
        # libdevice symlink to rocm-openmp-extras for runtime
        # libdebug symlink to rocm-openmp-extras for runtime
        if os.path.islink((os.path.join(bin_dir, "flang1"))):
            os.unlink(os.path.join(bin_dir, "flang1"))
        if os.path.islink((os.path.join(bin_dir, "flang2"))):
            os.unlink(os.path.join(bin_dir, "flang2"))
        if os.path.islink((os.path.join(lib_dir, "libdevice"))):
            os.unlink(os.path.join(lib_dir, "libdevice"))
        if os.path.islink((os.path.join(llvm_prefix, "lib-debug"))):
            os.unlink(os.path.join(llvm_prefix, "lib-debug"))

        os.symlink(os.path.join(omp_bin_dir, "flang1"), os.path.join(bin_dir, "flang1"))
        os.symlink(os.path.join(omp_bin_dir, "flang2"), os.path.join(bin_dir, "flang2"))
        os.symlink(os.path.join(omp_lib_dir, "libdevice"), os.path.join(lib_dir, "libdevice"))
        os.symlink(
            os.path.join(openmp_extras_prefix, "lib-debug"), os.path.join(llvm_prefix, "lib-debug")
        )

        # Set cmake args
        components = dict()

        components["aomp-extras"] = [
            "../rocm-openmp-extras/aomp-extras",
            "-DLLVM_DIR={0}".format(llvm_prefix),
            "-DDEVICE_LIBS_DIR={0}/amdgcn/bitcode".format(devlibs_prefix),
            "-DCMAKE_C_COMPILER={0}/clang".format(bin_dir),
            "-DCMAKE_CXX_COMPILER={0}/clang++".format(bin_dir),
            "-DAOMP_STANDALONE_BUILD=0",
            "-DDEVICELIBS_ROOT={0}".format(devlibs_src),
            "-DNEW_BC_PATH=1",
            "-DAOMP={0}".format(llvm_prefix),
        ]

        # Shared cmake configuration for openmp, openmp-debug
        # Due to hsa-rocr-dev using libelf instead of elfutils
        # the build of openmp fails because the include path
        # for libelf is placed before elfutils in SPACK_INCLUDE_DIRS.
        # Passing the elfutils include path via cmake options is a
        # workaround until hsa-rocr-dev switches to elfutils.
        openmp_common_args = [
            "-DROCM_DIR={0}".format(hsa_prefix),
            "-DDEVICE_LIBS_DIR={0}/amdgcn/bitcode".format(devlibs_prefix),
            "-DAOMP_STANDALONE_BUILD=0",
            "-DDEVICELIBS_ROOT={0}".format(devlibs_src),
            "-DOPENMP_TEST_C_COMPILER={0}/clang".format(bin_dir),
            "-DOPENMP_TEST_CXX_COMPILER={0}/clang++".format(bin_dir),
            "-DCMAKE_C_COMPILER={0}/clang".format(bin_dir),
            "-DCMAKE_CXX_COMPILER={0}/clang++".format(bin_dir),
            "-DLIBOMPTARGET_AMDGCN_GFXLIST={0}".format(gfx_list),
            "-DLIBOMP_COPY_EXPORTS=OFF",
            "-DHSA_LIB={0}/lib".format(hsa_prefix),
            "-DHSAKMT_LIB={0}/lib".format(hsakmt_prefix),
            "-DHSAKMT_LIB64={0}/lib64".format(hsakmt_prefix),
            "-DCOMGR_INCLUDE={0}/include".format(comgr_prefix),
            "-DCOMGR_LIB={0}/lib".format(comgr_prefix),
            "-DOPENMP_ENABLE_LIBOMPTARGET=1",
            "-DOPENMP_ENABLE_LIBOMPTARGET_HSA=1",
            "-DLLVM_MAIN_INCLUDE_DIR={0}{1}".format(src, llvm_inc),
            "-DLLVM_INSTALL_PREFIX={0}".format(llvm_prefix),
            "-DCMAKE_C_FLAGS=-isystem{0} -I{1}".format(elfutils_inc, ffi_inc),
            "-DCMAKE_CXX_FLAGS=-isystem{0} -I{1}".format(elfutils_inc, ffi_inc),
            "-DNEW_BC_PATH=1",
            "-DHSA_INCLUDE={0}/include/hsa".format(hsa_prefix),
        ]
        if self.spec.satisfies("@5.7:6.1"):
            openmp_common_args += [
                "-DLIBDRM_LIB={0}/lib".format(libdrm_prefix),
                "-DHSAKMT_INC_PATH={0}/include".format(hsakmt_prefix),
                "-DNUMACTL_DIR={0}".format(numactl_prefix),
            ]

        if self.spec.satisfies("@5.3.0:"):
            openmp_common_args += ["-DLIBOMPTARGET_ENABLE_DEBUG=ON"]

        components["openmp"] = ["../rocm-openmp-extras/llvm-project/openmp"]
        components["openmp"] += openmp_common_args

        components["openmp-debug"] = [
            "../rocm-openmp-extras/llvm-project/openmp",
            "-DLIBOMPTARGET_NVPTX_DEBUG=ON",
            "-DCMAKE_CXX_FLAGS=-g",
            "-DCMAKE_C_FLAGS=-g",
        ]

        components["openmp-debug"] += openmp_common_args

        # Shared cmake configuration for pgmath, flang, flang-runtime
        flang_common_args = [
            "-DLLVM_ENABLE_ASSERTIONS=ON",
            "-DLLVM_CONFIG={0}/llvm-config".format(bin_dir),
            "-DCMAKE_CXX_COMPILER={0}/clang++".format(bin_dir),
            "-DCMAKE_C_COMPILER={0}/clang".format(bin_dir),
            "-DCMAKE_Fortran_COMPILER={0}/flang".format(bin_dir),
            "-DLLVM_TARGETS_TO_BUILD=AMDGPU;x86",
            # Spack thinks some warnings from the flang build are errors.
            # Disable those warnings in C and CXX flags.
            "-DCMAKE_CXX_FLAGS={0}".format(flang_warning) + " -I{0}{1}".format(src, libpgmath),
            "-DCMAKE_C_FLAGS={0}".format(flang_warning) + " -I{0}{1}".format(src, libpgmath),
        ]

        components["pgmath"] = ["../rocm-openmp-extras/flang/runtime/libpgmath"]

        components["pgmath"] += flang_common_args

        components["flang"] = [
            "../rocm-openmp-extras/flang",
            "-DFLANG_OPENMP_GPU_AMD=ON",
            "-DFLANG_OPENMP_GPU_NVIDIA=ON",
        ]

        components["flang"] += flang_common_args

        components["flang-runtime"] = [
            "../rocm-openmp-extras/flang",
            "-DLLVM_INSTALL_RUNTIME=ON",
            "-DFLANG_BUILD_RUNTIME=ON",
            "-DOPENMP_BUILD_DIR={0}/spack-build-openmp/runtime/src".format(src),
        ]
        components["flang-runtime"] += flang_common_args

        build_order = ["aomp-extras", "openmp", "openmp-debug", "pgmath", "flang", "flang-runtime"]

        # Override standard CMAKE_BUILD_TYPE
        for arg in std_cmake_args:
            found = re.search("CMAKE_BUILD_TYPE", arg)
            if found:
                std_cmake_args.remove(arg)
        for component in build_order:
            with working_dir("spack-build-{0}".format(component), create=True):
                cmake_args = components[component]
                cmake_args.extend(std_cmake_args)
                # OpenMP build needs to be run twice(Release, Debug)
                if component == "openmp-debug":
                    cmake_args.append("-DCMAKE_BUILD_TYPE=Debug")
                else:
                    cmake_args.append("-DCMAKE_BUILD_TYPE=Release")
                cmake(*cmake_args)
                make()
                make("install")
