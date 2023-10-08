# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySetuptools(PythonPackage):
    """A Python utility that aids in the process of downloading, building,
    upgrading, installing, and uninstalling Python packages."""

    homepage = "https://github.com/pypa/setuptools"
    pypi = "setuptools/setuptools-62.3.2.tar.gz"

    tags = ["build-tools"]

    version("68.0.0", sha256="baf1fdb41c6da4cd2eae722e135500da913332ab3f2f5c7d33af9b492acb5235")
    version("67.6.0", sha256="2ee892cd5f29f3373097f5a814697e397cf3ce313616df0af11231e2ad118077")
    version("65.5.0", sha256="512e5536220e38146176efb833d4a62aa726b7bbff82cfbc8ba9eaa3996e0b17")
    version("65.0.0", sha256="d73f8cd714a1a6691f5eb5abeeacbf313242b7aa2f5eba93776542c1aad90c6f")
    version("64.0.0", sha256="9b5d2cb8df48f005825654e0cb17217418317e4d996c035f0bca7cbaeb8acf51")
    version("63.4.3", sha256="521c833d1e5e1ef0869940e7f486a83de7773b9f029010ad0c2fe35453a9dad9")
    version("63.0.0", sha256="7388e17e72f5c0c7279f59da950a7925910e35bc1a84e19d3affbb40da248d1d")
    version("62.6.0", sha256="990a4f7861b31532871ab72331e755b5f14efbe52d336ea7f6118144dd478741")
    version("62.4.0", sha256="bf8a748ac98b09d32c9a64a995a6b25921c96cc5743c1efa82763ba80ff54e91")
    version("62.3.2", sha256="a43bdedf853c670e5fed28e5623403bad2f73cf02f9a2774e91def6bda8265a7")
    version("59.4.0", sha256="b4c634615a0cf5b02cf83c7bedffc8da0ca439f00e79452699454da6fbd4153d")
    version("58.2.0", sha256="2c55bdb85d5bb460bd2e3b12052b677879cffcf46c0c688f2e5bf51d36001145")
    version("57.4.0", sha256="6bac238ffdf24e8806c61440e755192470352850f3419a52f26ffe0a1a64f465")
    version("57.1.0", sha256="cfca9c97e7eebbc8abe18d5e5e962a08dcad55bb63afddd82d681de4d22a597b")
    version("51.0.0", sha256="029c49fd713e9230f6a41c0298e6e1f5839f2cde7104c0ad5e053a37777e7688")
    version("50.3.2", sha256="ed0519d27a243843b05d82a5e9d01b0b083d9934eaa3d02779a23da18077bd3c")
    version("50.1.0", sha256="4a7708dafd2d360ce5e2ac7577374da9fb65fc867bc4cdaf461f9f834dfa6ac3")
    version("49.6.0", sha256="46bd862894ed22c2edff033c758c2dc026324788d758e96788e8f7c11f4e9707")
    version("49.2.0", sha256="afe9e81fee0270d3f60d52608549cc8ec4c46dada8c95640c1a00160f577acf2")
    version("46.1.3", sha256="795e0475ba6cd7fa082b1ee6e90d552209995627a2a227a47c6ea93282f4bfb1")
    version("44.1.1", sha256="c67aa55db532a0dadc4d2e20ba9961cbd3ccc84d544e9029699822542b5a476b")
    version("44.1.0", sha256="794a96b0c1dc6f182c36b72ab70d7e90f1d59f7a132e6919bb37b4fd4d424aca")
    version("43.0.0", sha256="db45ebb4a4b3b95ff0aca3ce5fe1e820ce17be393caf8902c78aa36240e8c378")
    version("41.4.0", sha256="7eae782ccf36b790c21bde7d86a4f303a441cd77036b25c559a602cf5186ce4d")
    version("41.3.0", sha256="9f5c54b529b2156c6f288e837e625581bb31ff94d4cfd116b8f271c589749556")
    version("41.0.1", sha256="a222d126f5471598053c9a77f4b5d4f26eaa1f150ad6e01dcf1a42e185d05613")
    version("41.0.0", sha256="79d30254b6fe7a8e672e43cd85f13a9f3f2a50080bc81d851143e2219ef0dcb1")
    version("40.8.0", sha256="6e4eec90337e849ade7103723b9a99631c1f0d19990d6e8412dc42f5ae8b304d")
    version("40.4.3", sha256="acbc5740dd63f243f46c2b4b8e2c7fd92259c2ddb55a4115b16418a2ed371b15")
    version("40.2.0", sha256="47881d54ede4da9c15273bac65f9340f8929d4f0213193fa7894be384f2dcfa6")
    version("39.2.0", sha256="f7cddbb5f5c640311eb00eab6e849f7701fa70bf6a183fc8a2c33dd1d1672fb2")
    version("39.0.1", sha256="bec7badf0f60e7fc8153fac47836edc41b74e5d541d7692e614e635720d6a7c7")
    version("25.2.0", sha256="b2757ddac2c41173140b111e246d200768f6dd314110e1e40661d0ecf9b4d6a6")
    version("20.7.0", sha256="505cdf282c5f6e3a056e79f0244b8945f3632257bba8469386c6b9b396400233")
    version("20.6.7", sha256="d20152ee6337323d3b6d95cd733fb719d6b4f3fbc40f61f7a48e5a1bb96478b2")

    def url_for_version(self, version):
        url = self.url.rsplit("/", 1)[0]
        if version.satisfies(ver("32.1.2:51.0.0")):
            url += "/setuptools-{}.zip"
        else:
            url += "/setuptools-{}.tar.gz"
        return url.format(version)

    patch("rpath-compiler-flag.patch", when="@48:58.2")

    extends("python")

    depends_on("python@3.7:", when="@59.7:", type=("build", "run"))
    depends_on("python@3.6:", when="@51:", type=("build", "run"))
    depends_on("python@3.5:", when="@45:50", type=("build", "run"))
    depends_on("python@2.7:2.8,3.5:", when="@44", type=("build", "run"))
    depends_on("python@2.7:2.8,3.4:", when="@:43", type=("build", "run"))

    # Newer pip requires setuptools to be installed, before building
    # setuptools. This issue was fixed or worked around in setuptools 54+
    depends_on("py-pip@:18", when="@:53", type="build")

    # Uses HTMLParser.unescape
    depends_on("python@:3.8", when="@:41.0", type=("build", "run"))

    # Uses collections.MutableMapping
    depends_on("python@:3.9", when="@:40.4.2", type=("build", "run"))

    # https://github.com/pypa/setuptools/issues/3661
    depends_on("python@:3.11", when="@:67", type=("build", "run"))
