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

<<<<<<< HEAD
    version(
        "68.0.0",
        sha256="11e52c67415a381d10d6b462ced9cfb97066179f0e871399e006c4ab101fc85f",
        expand=False,
    )
    version(
        "67.2.0",
        sha256="16ccf598aab3b506593c17378473978908a2734d7336755a8769b480906bec1c",
        expand=False,
    )
    version(
        "67.6.0",
        sha256="b78aaa36f6b90a074c1fa651168723acbf45d14cb1196b6f02c0fd07f17623b2",
        expand=False,
    )
    version(
        "65.5.0",
        sha256="f62ea9da9ed6289bfe868cd6845968a2c854d1427f8548d52cae02a42b4f0356",
        expand=False,
    )
    version(
        "65.0.0",
        sha256="fe9a97f68b064a6ddd4bacfb0b4b93a4c65a556d97ce906255540439d0c35cef",
        expand=False,
    )
    version(
        "64.0.0",
        sha256="63f463b90ff5e0a1422010100268fd688e15c44ae0798659013c8412963e15e4",
        expand=False,
    )
    version(
        "63.4.3",
        sha256="7f61f7e82647f77d4118eeaf43d64cbcd4d87e38af9611694d4866eb070cd10d",
        expand=False,
    )
    version(
        "63.0.0",
        sha256="045aec56a3eee5c82373a70e02db8b6da9a10f7faf61ff89a14ab66c738ed370",
        expand=False,
    )
    version(
        "62.6.0",
        sha256="c1848f654aea2e3526d17fc3ce6aeaa5e7e24e66e645b5be2171f3f6b4e5a178",
        expand=False,
    )
    version(
        "62.4.0",
        sha256="5a844ad6e190dccc67d6d7411d119c5152ce01f7c76be4d8a1eaa314501bba77",
        expand=False,
    )
    version(
        "62.3.2",
        sha256="68e45d17c9281ba25dc0104eadd2647172b3472d9e01f911efa57965e8d51a36",
        expand=False,
    )
    version(
        "59.4.0",
        sha256="feb5ff19b354cde9efd2344ef6d5e79880ce4be643037641b49508bbb850d060",
        expand=False,
    )
    version(
        "58.2.0",
        sha256="2551203ae6955b9876741a26ab3e767bb3242dafe86a32a749ea0d78b6792f11",
        expand=False,
    )
    version(
        "57.4.0",
        sha256="a49230977aa6cfb9d933614d2f7b79036e9945c4cdd7583163f4e920b83418d6",
        expand=False,
    )
    version(
        "57.1.0",
        sha256="ddae4c1b9220daf1e32ba9d4e3714df6019c5b583755559be84ff8199f7e1fe3",
        expand=False,
    )
    version(
        "51.0.0",
        sha256="8c177936215945c9a37ef809ada0fab365191952f7a123618432bbfac353c529",
        expand=False,
    )
    version(
        "50.3.2",
        sha256="2c242a0856fbad7efbe560df4a7add9324f340cf48df43651e9604924466794a",
        expand=False,
    )
    version(
        "50.1.0",
        sha256="4537c77e6e7dc170081f8547564551d4ff4e4999717434e1257600bbd3a23296",
        expand=False,
    )
    version(
        "49.6.0",
        sha256="4dd5bb0a0a0cff77b46ca5dd3a84857ee48c83e8223886b556613c724994073f",
        expand=False,
    )
    version(
        "49.2.0",
        sha256="272c7f48f5cddc5af5901f4265274c421c7eede5c8bc454ac2903d3f8fc365e9",
        expand=False,
    )
    version(
        "46.1.3",
        sha256="4fe404eec2738c20ab5841fa2d791902d2a645f32318a7850ef26f8d7215a8ee",
        expand=False,
    )
    version(
        "44.1.1",
        sha256="27a714c09253134e60a6fa68130f78c7037e5562c4f21f8f318f2ae900d152d5",
        expand=False,
    )
    version(
        "44.1.0",
        sha256="992728077ca19db6598072414fb83e0a284aca1253aaf2e24bb1e55ee6db1a30",
        expand=False,
    )
    version(
        "43.0.0",
        sha256="a67faa51519ef28cd8261aff0e221b6e4c370f8fb8bada8aa3e7ad8945199963",
        expand=False,
    )
    version(
        "41.4.0",
        sha256="8d01f7ee4191d9fdcd9cc5796f75199deccb25b154eba82d44d6a042cf873670",
        expand=False,
    )
    version(
        "41.3.0",
        sha256="e9832acd9be6f3174f4c34b40e7d913a146727920cbef6465c1c1bd2d21a4ec4",
        expand=False,
    )
    version(
        "41.0.1",
        sha256="c7769ce668c7a333d84e17fe8b524b1c45e7ee9f7908ad0a73e1eda7e6a5aebf",
        expand=False,
    )
    version(
        "41.0.0",
        sha256="e67486071cd5cdeba783bd0b64f5f30784ff855b35071c8670551fd7fc52d4a1",
        expand=False,
    )
    version(
        "40.8.0",
        sha256="e8496c0079f3ac30052ffe69b679bd876c5265686127a3159cfa415669b7f9ab",
        expand=False,
    )
    version(
        "40.4.3",
        sha256="ce4137d58b444bac11a31d4e0c1805c69d89e8ed4e91fde1999674ecc2f6f9ff",
        expand=False,
    )
    version(
        "40.2.0",
        sha256="ea3796a48a207b46ea36a9d26de4d0cc87c953a683a7b314ea65d666930ea8e6",
        expand=False,
    )
    version(
        "39.2.0",
        sha256="8fca9275c89964f13da985c3656cb00ba029d7f3916b37990927ffdf264e7926",
        expand=False,
    )
    version(
        "39.0.1",
        sha256="8010754433e3211b9cdbbf784b50f30e80bf40fc6b05eb5f865fab83300599b8",
        expand=False,
    )
    version(
        "25.2.0",
        sha256="2845247c359bb91097ccf8f6be8a69edfa44847f3d2d5def39aa43c3d7f615ca",
        expand=False,
    )
    version(
        "20.7.0",
        sha256="8917a52aa3a389893221b173a89dae0471022d32bff3ebc31a1072988aa8039d",
        expand=False,
    )
    version(
        "20.6.7",
        sha256="9982ee4d279a2541dc1a7efee994ff9c535cfc05315e121e09df7f93da48c442",
        expand=False,
    )
=======
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
>>>>>>> develop

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
