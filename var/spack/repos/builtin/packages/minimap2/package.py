# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Minimap2(PythonPackage):
    """Minimap2 is a versatile sequence alignment program that aligns DNA or
    mRNA sequences against a large reference database.
    Mappy provides a convenient interface to minimap2."""

    homepage = "https://github.com/lh3/minimap2"
    url = "https://github.com/lh3/minimap2/releases/download/v2.2/minimap2-2.2.tar.bz2"

    version("2.26", sha256="6a588efbd273bff4f4808d5190957c50272833d2daeb4407ccf4c1b78143624c")
    version("2.24", sha256="9dd4c31ff082182948944bcdad6d328f64f09295d10547d72eba24189880a615")
    version("2.23", sha256="a9ff45e3a5f5faf2b3837a28f228d7568baab60729c9d041f6e8b33ea25cf270")
    version("2.22", sha256="5a87a0c82a3bc159472280c9b9acaaabbb93befdf029aeede6d4049c4c1021e4")
    version("2.21", sha256="557d9c46a048eae0842fe111da787bd5348ba465702c3660369fea76f22f28ae")
    version("2.20", sha256="9590a693cb0a37811f736754831990fb62969d2e0bed56f09fde20e1043e54ad")
    version("2.19", sha256="2116ce7e517d8512e14c6e29a2a0ed951f53040ea530e7aa54382c7f66a4b0dc")
    version("2.18", sha256="71de93c501ad5b36eeea3bed0cbfa3c4d380d169ed4ab9e4b3face5e4e422cab")
    version("2.17", sha256="fe97310cf9abc165de2e17d41b68ee5a1003be3ff742179edef38fcf8a089a47")
    version("2.16", sha256="3367c918ec59ba420417487cd07f6673246be7a3d8d5f846b40cbb960f27a89d")
    version("2.15", sha256="8e9874e3d4efbaac07f50068efc5d1a206082c7314d996a717e2a75da51d2cf4")
    version("2.14", sha256="9088b785bb0c33488ca3a27c8994648ce21a8be54cb117f5ecee26343facd03b")
    version("2.10", sha256="52b36f726ec00bfca4a2ffc23036d1a2b5f96f0aae5a92fd826be6680c481c20")
    version("2.2", sha256="7e8683aa74c4454a8cfe3821f405c4439082e24c152b4b834fdb56a117ecaed9")

    variant(
        "js_engine",
        values=any_combination_of("node-js", "k8").prohibit_empty_set().with_default("k8"),
        description="List of javascript engines for which support is enabled",
    )

    conflicts("target=aarch64:", when="@:2.10")
    depends_on("zlib-api", type="link")
    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")

    conflicts("js_engine=k8", when="target=aarch64:")
    depends_on("k8", type="run", when="js_engine=k8")
    depends_on("node-js", type="run", when="js_engine=node-js")

    @run_after("install")
    def install_minimap2(self):
        make_arg = []
        if self.spec.target.family == "aarch64":
            make_arg.extend(["arm_neon=1", "aarch64=1"])
        make(*make_arg)
        mkdirp(prefix.bin)
        install("minimap2", prefix.bin)
        if self.spec.satisfies("js_engine=node"):
            filter_file(r"k8",  "node",  "./misc/paftools.js")
        install("./misc/paftools.js", prefix.bin)
