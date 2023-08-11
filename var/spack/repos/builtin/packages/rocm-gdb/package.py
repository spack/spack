# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RocmGdb(AutotoolsPackage):
    """This is ROCmgdb, the ROCm source-level debugger for Linux,
    based on GDB, the GNU source-level debugger."""

    homepage = "https://github.com/ROCm-Developer-Tools/ROCgdb/"
    url = "https://github.com/ROCm-Developer-Tools/ROCgdb/archive/rocm-5.5.0.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    version("5.5.1", sha256="359258548bc7e6abff16bb13c301339fb96560b2b961433c9e0712e4aaf2d9e1")
    version("5.5.0", sha256="d3b100e332facd9635e328f5efd9f0565250edbe05be986baa2e0470a19bcd79")
    version("5.4.3", sha256="28c1ce39fb1fabe61f86f6e3c6940c10f9a8b8de77f7bb4fdd73b04e172f85f6")
    version("5.4.0", sha256="7ee984d99818da04733030b140c1f0929639bc719a5e418d53cc2c2a8cbc9a79")
    version("5.3.3", sha256="9fc3ccd9378ad40f2f0c9577bc400cc9a202d0ae4656378813b67653b9023c46")
    version("5.3.0", sha256="402537baf0779cae586d608505e81173ba85f976fe993f1633e3afe81669350f")
    version("5.2.3", sha256="c2df5cccd8bb07ea331b45091fb3141999a37a67696d273f3888b48f6d4281aa")
    version("5.2.1", sha256="77169d88f24e6ccb6aef3945448b179edffe806a51a3e996236b08fb510f3979")
    version("5.2.0", sha256="70c5b443292b9bb114844eb63b72cfab1b65f083511ee39d55db7a633c63bf5a")
    version("5.1.3", sha256="81f5e368facdcc424a37cb5809f0b436bedb9a6d9af4d17785b3c446ab0a7821")
    version("5.1.0", sha256="cf638149b269f838aaec59c5801098b9c0fc42f6c86a39309a8995b56978b424")
    version(
        "5.0.2",
        sha256="0eced8cd5a2996cb4bcf254f2bd9defe24112d21c2f750e98f784ecdf94ba5c9",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="aa311fb557bd95e35c6e4dfd245188f35c294a93bacb77fe4d3b178b1d0097e8",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="e278abf50f1758ce396b26a6719d0af09a6053c195516a44ec9b2be925d79203",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="dd37c8b1ea6bb41b1263183637575d7bf4746cabc573dbff888e23b0379877b0",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="995756a24b1e1510647dac1476a3a9a8e3af8e9fd9f4af1d00dd2db28e7a4ef2",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="8ee0667ab2cd91b2cc41d3a7af046d36a6b4e2007f050265aa65e0aedec83fd7",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="4bc579584a1f8614111e7e44d8aa1c6d5d06be3f5db055aba2cf1abc140122ac",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="28dc806e48695d654d52fb1a634df6d4c1243f00846ae90161e7a5e9f4d88b24",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="b90291b0a8409fe66d8a65d2731dcb87b9f5a22bac9ce3ffbab726eb129ba13d",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="05455cb47dd42404ee8bba047def6a6846a7e877e7a7db8dcffc7100d5ba16f0",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="0765c96439c0efa145418d210d865b9faed463466d7522274959cc4476a37097",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="a7c11dc30c952587c616bf7769bad603c3bf80522afc8b73ccda5b78d27bed41",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="7a29ef584fd7b6c66bb03aaf8ec2f5a8c758370672a28a4d0d95066e5f6fbdc1",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="cf36d956e84c7a5711b71f281a44b0a9708e13e941d8fca0247d01567e7ee7d1",
        deprecated=True,
    )

    depends_on("cmake@3:", type="build")
    depends_on("texinfo", type="build")
    depends_on("bison", type="build")
    depends_on("flex@2.6.4:", type="build")
    depends_on("libunwind", type="build")
    depends_on("expat", type=("build", "link"))
    depends_on("python", type=("build", "link"))
    depends_on("zlib-api", type="link")
    depends_on("babeltrace@1.2.4", type="link")
    depends_on("gmp", type=("build", "link"), when="@4.5.0:")

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
    ]:
        depends_on("rocm-dbgapi@" + ver, type="link", when="@" + ver)
        depends_on("comgr@" + ver, type="link", when="@" + ver)

    for ver in ["5.5.0", "5.5.1"]:
        depends_on("rocm-core@" + ver, when="@" + ver)

    build_directory = "spack-build"

    def configure_args(self):
        # Generic options to compile GCC
        options = [
            # Distributor options
            "--program-prefix=roc",
            "--enable-64-bit-bfd",
            "--with-bugurl=https://github.com/ROCm-Developer-Tools/ROCgdb/issues",
            "--with-pkgversion=-ROCm",
            "--enable-targets=x86_64-linux-gnu,amdgcn-amd-amdhsa",
            "--disable-ld",
            "--disable-gas",
            "--disable-gdbserver",
            "--disable-sim",
            "--enable-tui",
            "--disable-gdbtk",
            "--disable-shared",
            "--with-expat",
            "--with-system-zlib" "--without-guile",
            "--with-babeltrace",
            "--with-lzma",
            "--with-python",
            "--with-rocm-dbgapi={0}".format(self.spec["rocm-dbgapi"].prefix),
        ]
        if self.spec.satisfies("@5.2.0:"):
            options.append("--disable-gprofng")
        return options
