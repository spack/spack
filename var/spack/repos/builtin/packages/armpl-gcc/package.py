# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *

_os_map_before_23 = {
    "ubuntu18.04": "Ubuntu-18.04",
    "ubuntu20.04": "Ubuntu-20.04",
    "ubuntu22.04": "Ubuntu-20.04",
    "sles15": "SLES-15",
    "centos7": "RHEL-7",
    "centos8": "RHEL-8",
    "rhel7": "RHEL-7",
    "rhel8": "RHEL-8",
    "rocky8": "RHEL-8",
    "amzn2": "RHEL-7",
    "amzn2023": "RHEL-7",
}

_os_map = {
    "ubuntu20.04": "Ubuntu-20.04",
    "ubuntu22.04": "Ubuntu-22.04",
    "sles15": "SLES-15",
    "centos7": "RHEL-7",
    "centos8": "RHEL-8",
    "rhel7": "RHEL-7",
    "rhel8": "RHEL-8",
    "rhel9": "RHEL-9",
    "rocky8": "RHEL-8",
    "amzn2": "AmazonLinux-2",
    "amzn2023": "AmazonLinux-2023",
}

_versions = {
    "23.04_gcc-12.2": {
        "RHEL-7": ("e159f84f14d885aa5e47ca17c16ef3d95128f834a655827bf6b48fcf8d6ec459"),
        "RHEL-8": ("6ac1974ec9bd814d3a4eecf330cefd67cf2c878f026a8b04bc2928368948671a"),
        "RHEL-9": ("71fc8ac9e48ec531b24d5641481070daa8561a5c0373dfbd8915847c8b45641c"),
        "SLES-15": ("b26a22123294c161519dce398869626e6a793ce94b76648cce46b0111d17d215"),
        "Ubuntu-20.04": ("c410e1aebb1465f8ae7b264fa74f847137e3c1d9f28c1a9332bf69c59b6f9eec"),
        "Ubuntu-22.04": ("9f9179336d14ea253462701c96c13d0b01b7c8a09a3fb987c0b22ad647598410"),
        "AmazonLinux-2": ("3ef5556d7ac5a269af432eb24ed25d2504bcd0070f8b899231f2a45cea6f1a1d"),
        "AmazonLinux-2023": ("037c70ffdcbdf152ddcb7a4f9e1e1acb7c6cd7ea7337966a2b101e684493653d"),
    },
    "23.04_gcc-11.3": {
        "RHEL-7": ("75f53d160c2254db38f670e86b5381b6d4d778cb0325bfc6fed772c1a8f4c7d7"),
        "RHEL-8": ("3d10bd5d3b82a2affcea94fdb235eb046c622abf82306682aabdf3abd9e8fc4e"),
        "RHEL-9": ("df3a7c3571af2e6c3e071cf88afdc3352cd32428c22859d833e68afb3d39b4de"),
        "SLES-15": ("6dda1320be97d4e5bd2f192b8c6743a6975aab17499554d5506506a620f27e04"),
        "Ubuntu-20.04": ("57cc91b3b43fd663f827f5a2f3e2b3bddf76ea0f80d95e227a95d961fae64b5d"),
        "Ubuntu-22.04": ("aa56ea09ded38e17bf26ea449b5d45fb112b0feb34a5408c629fe030011c83a4"),
        "AmazonLinux-2": ("26494f69237eaf123356b41265f6531d8049dd7aa04898e7b3cd3e8d67d2f25a"),
        "AmazonLinux-2023": ("30a1a7d14b567c2e68b11cf40890d09899d4cb5fdc3605b9a0c271867ff0f4b9"),
    },
    "23.04_gcc-10.2": {
        "RHEL-7": ("08bb8a78dc27989e044f5154744355699e2896d60ae8838b0e6ce4318a9462ab"),
        "RHEL-8": ("29415b6d6bce9176aa372ac794769541775573f8302e801a4bf5cdfad5b07851"),
        "SLES-15": ("aa3ea267a4d02a9c01fa9ef9fd5ac9e0b8687bac8b19047b52ea57ca587ee838"),
        "Ubuntu-20.04": ("d68a66d85e4cd7e99b66308fe563a623b902e49cb01a2ba0342f575beb192a55"),
        "AmazonLinux-2": ("a9eded299ea08ba32c91b6e99e1fe24240fcbee0a60696d1dba6d20b2bb39d5c"),
    },
    "23.04_gcc-9.3": {
        "RHEL-7": ("0550fafeecfd8a23500f8fdd3cddf49ed574ae274894f2ca7935a69618dbd418"),
        "RHEL-8": ("d041b3b8ffd4752f0180999bdfc3c6764659097f0b042482bc1058d4c9a504cb"),
        "SLES-15": ("dcf8107423dc54068765a3e5f39bfed18df1c9662743f93c785554d0a223a727"),
        "Ubuntu-20.04": ("577dc2ceb34f1e0aaf3e28953ed406de02e3e245eeafd7f9d6666866509fb1a1"),
        "AmazonLinux-2": ("50df0ee6067c2d3b888545beaa34936bb3b8a8736d52535badf2ab48acc866e2"),
    },
    "23.04_gcc-8.2": {
        "RHEL-7": ("a579d3790c60ff05952cf4f778089843555413686037ab8b743c2756df8c4070"),
        "RHEL-8": ("6c90eb65cdd472a16eaebbcd7455840048814ced5986f31a0daaf10f9a2d33fd"),
        "SLES-15": ("9c3a8323f47db78128751ae74fb3dea11b6237d8433aae0c6e2c8e7951c3ea00"),
        "AmazonLinux-2": ("02819c958976530e6363d629c5b6d5097892eef5ee4904e27b25e18f52e08c17"),
    },
    "23.04_gcc-7.5": {
        "RHEL-7": ("2141340617d9a053ed03f9da5b1a787bc96bf065eceee3bf350184a4d3fd8a44"),
        "AmazonLinux-2": ("27dfc5f52e6c44a84d99b6d0841e526ea9ff5878262094760c3c82a6863eceb4"),
    },
    "22.1_gcc-11.2": {
        "RHEL-7": ("9ce7858525109cca8f4e1d533113b6410d55f10cc4db16c4742562da87a32f2b"),
        "RHEL-8": ("24f9f4496e41c2314d4ace25b6e3d63127bd586ff7bdd8a732471cbc65a8023e"),
        "SLES-15": ("5b2a88148157c2a6ac5fd5698e9cb5b8717fb5f7afeab156de253f53cef5ab71"),
        "Ubuntu-18.04": ("44315990a2bf9cca1f48cd873f97b4282c371b6894c96e58d890ba1ca9ed5b2a"),
        "Ubuntu-20.04": ("00c051e0176ac4354d6cf181d38ef5a6d41f5b1f4db0109f3abc5d877d8e0a1f"),
    },
    "22.1_gcc-10.2": {
        "RHEL-7": ("ca8bf196757b4755f817d97e289305893fbe9a195b6892c90f8414f438f42d83"),
        "RHEL-8": ("8a1b65b1086b7b9e0ccd7080f9ed1d411f98a775b61c1e05c000e584877a1e66"),
        "SLES-15": ("7d703d7a2954283f11b742e0bc8fee886135d5bc87fe3e700c05b8277de495c3"),
        "Ubuntu-18.04": ("fde39a1bad9d904f2b18445252245f30f31848fd4470b58b3124f92c4c641710"),
        "Ubuntu-20.04": ("f0dfde5e9f8ca29bb49ea4596cb56ca50c8fda51758a38281e191fb36def812a"),
    },
    "22.1_gcc-9.3": {
        "RHEL-7": ("76c8ab3687d421153f91cacd33047b65b3650b21e2094d34341a91e94c766425"),
        "RHEL-8": ("eebeedddab04a393f4afc499d8681dc531b6bba0312a583afde445efb29ab849"),
        "SLES-15": ("e33cc89582a98866aa5e1cf6573a0bbe71b98c1585bbe665173deeb561d9afc5"),
        "Ubuntu-18.04": ("453e524cb66c2525443ab09283baef1521c1389d9d967b24fa94539ceaa62088"),
        "Ubuntu-20.04": ("521b106652fd50dc23fa056f208b788a1e3e6f4dd6e162b8cd5d835d755cb3af"),
    },
    "22.1_gcc-8.2": {
        "RHEL-7": ("9a6caa9767367c16a5abc2a3c145f0fccd47052cd5e2b9e3fbf511009a85746c"),
        "RHEL-8": ("90009f854ab597ab3f4d6745d90460e01bbbe922bf4bdfd30a3e58e62352f6be"),
        "SLES-15": ("0b7a5a5631798cba794810983e6180dd57cb40d5e82a806fdbc8a00f50f01bd6"),
        "Ubuntu-18.04": ("7dddedcaf7ce56b10da4a8d21d253f5c6eec928d238233049462b4ce5fece1ae"),
    },
    "22.1_gcc-7.5": {
        "RHEL-7": ("33c66ed1aa78eec4a8bd9d9c77882e9275232f742dc7808789272dbded0032e0"),
        "Ubuntu-18.04": ("523b926595565af96cf8c4109517c30e248bb2336bdf55f626be4e7356c97b98"),
    },
    "22.0.2_gcc-11.2": {
        "RHEL-7": ("c8191f3a65762955714f020caf2a89e37ff7f9cb2326dc180c746acd8a018acd"),
        "RHEL-8": ("d69432a3148c9d2745c70859a0143285537e06920ecfdb4669ff364a9d24972c"),
        "SLES-15": ("dab5efa8cad15cc78212a085e7ed9125725fb51924cb79bd556229cde3c4f1a3"),
        "Ubuntu-18.04": ("38a9a2f8bf5101dd7a8b66b3eec7647730434b8ee5e4c5efd17a172e2ea1357e"),
        "Ubuntu-20.04": ("b7322d0e824615cd6fe784bfd4eeed359f11aa4eeb01a52cb61863844d79791f"),
    },
    "22.0.2_gcc-10.2": {
        "RHEL-7": ("1b728f7551db8b3d6a710151f24872d6ba8c97a7572581680161441268b9e500"),
        "RHEL-8": ("d0e2101db55f25a3ee5723c14c4209d5b082c6b737bad6121ae692e829b50038"),
        "SLES-15": ("4de686744937345bc7eeac06db2086535e0230813b87d6b4013f1336a54324a3"),
        "Ubuntu-18.04": ("ca08d6942352f4cdec634b5e8c3bfe46a05f04f19d957e6af56c25a433682e66"),
        "Ubuntu-20.04": ("25c5288c285fc08160a104dd2c36d2adab7f72b42b99771f93b0dfcb2b3e3230"),
    },
    "22.0.2_gcc-9.3": {
        "RHEL-7": ("2c2bc000d9819cae7785880b3bab00556fcc5eda3fb48356300048df28876e09"),
        "RHEL-8": ("1e992d603af0d1f80f05fffb0d57e3f66a5457fb82c56e38d5aec380f66b7bd9"),
        "SLES-15": ("e30b6d989b97f2065f981ce6061a00377455c84018c4639865c774994bab0c71"),
        "Ubuntu-18.04": ("fa0fa8367aa18169e045d9ba40f339629f14fdd6e7087b946b9bea9588213d5f"),
        "Ubuntu-20.04": ("7d3f6661304ecc7111e8b67b745d6d7fc15306e04e87dac4561e6040ac5f68b0"),
    },
    "22.0.2_gcc-8.2": {
        "RHEL-7": ("5a8cdbdfceb53252358842e505cfdc35c50af06d8d17d073bab41efdb78a38b5"),
        "RHEL-8": ("564f3e2fcdadc831d010aed0a938a419321a9ba8c18978bdad08f53924bd3986"),
        "SLES-15": ("c4d43e1ba84e2f09b6223ac148be3f7b4c7f83a4af77255dd1cb7ad0034c713a"),
        "Ubuntu-18.04": ("98c752dc997a3abe4ac4db16fd684bdd8aa8d4482bccf93948a593d523e477e0"),
    },
    "22.0.2_gcc-7.5": {
        "RHEL-7": ("adc76d9b1375330dd424dd85cd1aefa7bceaa3b25a353157d493d98850c0d8fa"),
        "Ubuntu-18.04": ("331846312e579e954dac54f69b1ffcda96ab51984050659f2314269e55b58b9e"),
    },
    "22.0.1_gcc-11.2": {
        "RHEL-7": ("32529fdc70c39084eafe746db6baa487815bb49dae1588ccf2f7bd7929c10f7c"),
        "RHEL-8": ("1abd0b1c47cae65ee74510cf6e25946c66f9f4244e4674d5e9f73c442901482c"),
        "SLES-15": ("631261d7b29e85e99d208bdd397bdb5fcb0b53fd834b4b5a9cf963789e29f96e"),
        "Ubuntu-18.04": ("2ec210ff3c33d94a7cbe0cd7ea92add0b954ab1b1dc438dffa1d5f516e80e3ec"),
        "Ubuntu-20.04": ("13e9b98afc01c5444799c7f2ef84716f8a7be11df93b71fe9cfdc7fc6162f6d5"),
    },
    "22.0.1_gcc-10.2": {
        "RHEL-7": ("d2d91f43872e072ccec0cfab61eccf531daf6f02997e29fef3d738178c023d7a"),
        "RHEL-8": ("d642f55937410d2d402589f09e985c05b577d1227063b8247dc5733199e124a4"),
        "SLES-15": ("6746de2db361a65edac2ff8dcd4fc84a314fd919df3758c9bad7027dcfadfea2"),
        "Ubuntu-18.04": ("f3a7a7cb1768046ef742110fa311c65504074f1a381d295d583848221e267bd9"),
        "Ubuntu-20.04": ("5da7450196d94b0aea613cf8e7c4083ae3eb2e905d049db3b300059a9fbf169b"),
    },
    "22.0.1_gcc-9.3": {
        "RHEL-7": ("8df55f83ccebf9c1de5291c701d7cbeb051ce194ffe2d1f1148b2a6be0d7ea1c"),
        "RHEL-8": ("b0e26004c40db3138939b7bddc4bbe54ec7de4e548b5dc697cce5c85a8acbb27"),
        "SLES-15": ("963278d35485ec28a8b17a89efcfe0f82d84edc4ff8af838d56648917ec7b547"),
        "Ubuntu-18.04": ("3c7d2f7d102954440539d5b541dd1f669d2ccb3daaa14de1f04d6790368d6794"),
        "Ubuntu-20.04": ("8e78bef6517f42efd878579aee2cae4e439e3cd5c8a28e3f3fa83254f7189a2f"),
    },
    "22.0.1_gcc-8.2": {
        "RHEL-7": ("1e682e319c3b07236acc3870bf291a1d0cba884112b447dad7e356fdc42bd06a"),
        "RHEL-8": ("1fad5a0de02cda0a23a7864cca653a04ceb4244e362073d2959ce7db4144bb20"),
        "SLES-15": ("fa6111264c3fbe29ec084e7322c794640a1b3c40b2f0e01f7637f3f0d87d03e2"),
        "Ubuntu-18.04": ("3d092ecd98620b31e813ad726244ff40fdcb012aa055b6695dff51bc1578039d"),
    },
    "22.0.1_gcc-7.5": {
        "RHEL-7": ("e23702a9fecfc64aa6bd56439a602f0c25b0febce059cb6c0192b575758c6f1a"),
        "Ubuntu-18.04": ("bf4e6327eedec656b696f98735aa988a75b0c60185f3c22af6b7e608abbdb305"),
    },
}


def get_os(ver):
    spack_os = spack.platforms.host().default_os
    if ver.startswith("22."):
        return _os_map_before_23.get(spack_os, "")
    else:
        return _os_map.get(spack_os, "RHEL-7")


def get_package_url(version):
    base_url = "https://developer.arm.com/-/media/Files/downloads/hpc/arm-performance-libraries/"
    armpl_version = version.split("_")[0]
    armpl_version_dashed = armpl_version.replace(".", "-")
    gcc_version = version.split("_")[1]
    os = get_os(armpl_version)
    filename = "arm-performance-libraries_" + armpl_version + "_" + os + "_" + gcc_version + ".tar"
    os_short = ""
    if armpl_version.startswith("22.0."):
        os_short = os.replace("-", "")
    else:
        os_short = os.split(".")[0].lower()
        if "amazonlinux" in os_short:
            os_short = os_short.replace("amazonlinux", "al")
    return base_url + armpl_version_dashed + "/" + os_short + "/" + filename


def get_armpl_prefix(spec):
    return os.path.join(spec.prefix, "armpl_" + spec.version.string)


class ArmplGcc(Package):
    """Arm Performance Libraries provides optimized standard core math libraries for
    high-performance computing applications on Arm processors."""

    homepage = "https://developer.arm.com/tools-and-software/server-and-hpc/downloads/arm-performance-libraries"
    url = "https://developer.arm.com/-/media/Files/downloads/hpc/arm-performance-libraries/22-1/ubuntu-20/arm-performance-libraries_22.1_Ubuntu-20.04_gcc-11.2.tar"

    maintainers("annop-w")

    for ver, packages in _versions.items():
        key = "{0}".format(get_os(ver))
        sha256sum = packages.get(key)
        url = get_package_url(ver)
        if sha256sum:
            version(ver, sha256=sha256sum, url=url)

    conflicts("target=x86:", msg="Only available on Aarch64")
    conflicts("target=ppc64:", msg="Only available on Aarch64")
    conflicts("target=ppc64le:", msg="Only available on Aarch64")

    conflicts("%gcc@:11", when="@23.04_gcc-12.2")
    conflicts("%gcc@:10", when="@23.04_gcc-11.3")
    conflicts("%gcc@:9", when="@23.04_gcc-10.2")
    conflicts("%gcc@:8", when="@23.04_gcc-9.3")
    conflicts("%gcc@:7", when="@23.04_gcc-8.2")
    conflicts("%gcc@:6", when="@23.04_gcc-7.5")

    conflicts("%gcc@:10", when="@22.1_gcc-11.2")
    conflicts("%gcc@:9", when="@22.1_gcc-10.2")
    conflicts("%gcc@:8", when="@22.1_gcc-9.3")
    conflicts("%gcc@:7", when="@22.1_gcc-8.2")
    conflicts("%gcc@:6", when="@22.1_gcc-7.5")

    conflicts("%gcc@:10", when="@22.0.2_gcc-11.2")
    conflicts("%gcc@:9", when="@22.0.2_gcc-10.2")
    conflicts("%gcc@:8", when="@22.0.2_gcc-9.3")
    conflicts("%gcc@:7", when="@22.0.2_gcc-8.2")
    conflicts("%gcc@:6", when="@22.0.2_gcc-7.5")

    conflicts("%gcc@:10", when="@22.0.1_gcc-11.2")
    conflicts("%gcc@:9", when="@22.0.1_gcc-10.2")
    conflicts("%gcc@:8", when="@22.0.1_gcc-9.3")
    conflicts("%gcc@:7", when="@22.0.1_gcc-8.2")
    conflicts("%gcc@:6", when="@22.0.1_gcc-7.5")

    variant("ilp64", default=False, description="use ilp64 specific Armpl library")
    variant("shared", default=True, description="enable shared libs")
    variant(
        "threads",
        default="none",
        description="Multithreading support",
        values=("openmp", "none"),
        multi=False,
    )

    provides("blas")
    provides("lapack")
    provides("fftw-api@3")

    # Run the installer with the desired install directory
    def install(self, spec, prefix):
        if self.compiler.name != "gcc":
            raise spack.error.SpackError(("Only compatible with GCC.\n"))

        with when("@:22"):
            armpl_version = "{}".format(spec.version.up_to(3)).split("_")[0]
        with when("@23:"):
            armpl_version = "{}".format(spec.version).split("_")[0]

        exe = Executable(
            "./arm-performance-libraries_{0}_{1}.sh".format(armpl_version, get_os(armpl_version))
        )
        exe("--accept", "--force", "--install-to", prefix)

    @property
    def lib_suffix(self):
        suffix = ""
        suffix += "_ilp64" if self.spec.satisfies("+ilp64") else ""
        suffix += "_mp" if self.spec.satisfies("threads=openmp") else ""
        return suffix

    @property
    def blas_libs(self):
        armpl_prefix = get_armpl_prefix(self.spec)

        libname = "libarmpl" + self.lib_suffix

        # Get ArmPL Lib
        armpl_libs = find_libraries(
            [libname, "libamath", "libastring"],
            root=armpl_prefix,
            shared=self.spec.satisfies("+shared"),
            recursive=True,
        )

        armpl_libs += find_system_libraries(["libm"])

        return armpl_libs

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def fftw_libs(self):
        return self.blas_libs

    @property
    def libs(self):
        return self.blas_libs

    @property
    def headers(self):
        armpl_dir = get_armpl_prefix(self.spec)

        suffix = "include" + self.lib_suffix

        incdir = join_path(armpl_dir, suffix)

        hlist = find_all_headers(incdir)
        hlist.directories = [incdir]
        return hlist

    def setup_run_environment(self, env):
        armpl_dir = get_armpl_prefix(self.spec)
        env.prepend_path("LD_LIBRARY_PATH", join_path(armpl_dir, "lib"))

    @run_after("install")
    def check_install(self):
        armpl_dir = get_armpl_prefix(self.spec)
        armpl_example_dir = join_path(armpl_dir, "examples")
        # run example makefile
        make("-C", armpl_example_dir, "ARMPL_DIR=" + armpl_dir)
        # clean up
        make("-C", armpl_example_dir, "ARMPL_DIR=" + armpl_dir, "clean")

    @run_after("install")
    def make_pkgconfig_files(self):
        if self.spec.satisfies("@:22"):
            # ArmPL pkgconfig files do not have .pc extension and are thus not found by pkg-config
            armpl_dir = get_armpl_prefix(self.spec)
            for f in find(join_path(armpl_dir, "pkgconfig"), "*"):
                symlink(f, f + ".pc")

    def setup_dependent_build_environment(self, env, dependent_spec):
        armpl_dir = get_armpl_prefix(self.spec)
        if self.spec.satisfies("@:22"):
            # pkgconfig directory is not in standard ("lib", "lib64", "share") location
            env.append_path("PKG_CONFIG_PATH", join_path(armpl_dir, "pkgconfig"))
        else:
            env.append_path("PKG_CONFIG_PATH", join_path(armpl_dir, "lib/pkgconfig"))
