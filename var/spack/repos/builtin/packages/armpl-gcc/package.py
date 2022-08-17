# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *

_os_map = {
    "ubuntu18.04": "Ubuntu-18.04",
    "ubuntu20.04": "Ubuntu-20.04",
    "sles15": "SLES-15",
    "centos7": "RHEL-7",
    "centos8": "RHEL-8",
    "amzn2": "RHEL-7",
}


_versions = {
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


def get_os():
    spack_os = spack.platforms.host().default_os
    return _os_map.get(spack_os, "RHEL-7")


def get_package_url(version):
    os = get_os()
    os_no_dash = get_os().replace("-", "")
    base_url = "https://developer.arm.com/-/media/Files/downloads/hpc/arm-performance-libraries/"
    armpl_version = version.split("_")[0]
    armpl_version_dashed = armpl_version.replace(".", "-")
    gcc_version = version.split("_")[1]
    filename = "arm-performance-libraries_" + armpl_version + "_" + os + "_" + gcc_version + ".tar"
    return base_url + armpl_version_dashed + "/" + os_no_dash + "/" + filename


def get_armpl_prefix(spec):
    return os.path.join(spec.prefix, "armpl_" + spec.version.string)


class ArmplGcc(Package):
    """Arm Performance Libraries provides optimized standard core math libraries for
    high-performance computing applications on Arm processors."""

    homepage = "https://developer.arm.com/tools-and-software/server-and-hpc/downloads/arm-performance-libraries"
    url = "https://developer.arm.com/-/media/Files/downloads/hpc/arm-performance-libraries/22-0-2/RHEL7/arm-performance-libraries_22.0.2_RHEL-7_gcc-11.2.tar"

    maintainers = ["annop-w"]

    for ver, packages in _versions.items():
        key = "{0}".format(get_os())
        sha256sum = packages.get(key)
        url = get_package_url(ver)
        if sha256sum:
            version(ver, sha256=sha256sum, url=url)

    conflicts("target=x86:", msg="Only available on Aarch64")
    conflicts("target=ppc64:", msg="Only available on Aarch64")
    conflicts("target=ppc64le:", msg="Only available on Aarch64")

    conflicts("%gcc@:11.0", when="@22.0.2_gcc-11.2")
    conflicts("%gcc@:10.0", when="@22.0.2_gcc-10.2")
    conflicts("%gcc@:9.0", when="@22.0.2_gcc-9.3")
    conflicts("%gcc@:8.0", when="@22.0.2_gcc-8.2")
    conflicts("%gcc@:7.0", when="@22.0.2_gcc-7.5")

    conflicts("%gcc@:11.0", when="@22.0.1_gcc-11.2")
    conflicts("%gcc@:10.0", when="@22.0.1_gcc-10.2")
    conflicts("%gcc@:9.0", when="@22.0.1_gcc-9.3")
    conflicts("%gcc@:8.0", when="@22.0.1_gcc-8.2")
    conflicts("%gcc@:7.0", when="@22.0.1_gcc-7.5")

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

        exe = Executable(
            "./arm-performance-libraries_{0}_{1}.sh".format(spec.version.up_to(3), get_os())
        )
        exe("--accept", "--force", "--install-to", prefix)

    @property
    def blas_libs(self):

        armpl_prefix = get_armpl_prefix(self.spec)

        shared = True if "+shared" in self.spec else False
        if "+ilp64" in self.spec and self.spec.satisfies("threads=openmp"):
            libname = "libarmpl_ilp64_mp"
        elif "+ilp64" in self.spec:
            libname = "libarmpl_ilp64"
        elif self.spec.satisfies("threads=openmp"):
            libname = "libarmpl_mp"
        else:
            libname = "libarmpl"

        # Get ArmPL Lib
        armpl_libs = find_libraries(
            [libname, "libamath", "libastring"], root=armpl_prefix, shared=shared, recursive=True
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
        suffix = "include"
        if self.spec.satisfies("+ilp64"):
            suffix += "_ilp64"
        if self.spec.satisfies("threads=openmp"):
            suffix += "_mp"
        incdir = join_path(armpl_dir, suffix)

        hlist = find_all_headers(incdir)
        hlist.directories = [incdir]
        return hlist

    def setup_run_environment(self, env):
        armpl_dir = get_armpl_prefix(self.spec)
        env.prepend_path("LD_LIBRARY_PATH", join_path(armpl_dir, "lib"))
