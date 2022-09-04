# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


# NOTE: This package uses a setup.py file, but does not use distutils/setuptools or any
# other known build system, so this is a custom package
class Kitty(Package):
    """
    fast, featureful, cross-platform, GPU-based terminal emulator
    """

    homepage = "https://sw.kovidgoyal.net/kitty/index.html"
    url = "https://github.com/kovidgoyal/kitty/archive/v0.12.3.tar.gz"
    git = "https://github.com/kovidgoyal/kitty.git"

    maintainers = ["JBlaschke"]

    version("0.25.2", sha256="0893f7c26045242919f8f2baafc5fdb427968a7dbc793771c0a04d4e86377990")
    version("0.25.1", sha256="935b7af0ac9c903f4328bcf26335930c7204fce7b2f8b386d7aef217795e8f29")
    version("0.25.0", sha256="be30160a905d26ddb2d07f52be40a56e6bf118162c447d3ea6f0e6f662b56676")
    version("0.24.4", sha256="e6619b635b5c9d6cebbba631a2175659698068ce1cd946732dc440b0f1c12ab3")
    version("0.24.3", sha256="48020cc09b4eedfd0e52431a2c18d0fc03eb58a57082b0d3e0732fa478931cc0")
    version("0.24.2", sha256="6edf5cb7f4f24afe4fef7d209cb7a2bb479438a90919610b0147f48d57b34fc0")
    version("0.24.1", sha256="a49b7ea7d36989fb17bd31935dc6a9a619338647c58ca1eb00400340b0d756ff")
    version("0.24.0", sha256="6272bed507de179cbe6aef571c100fe44596da1fd9eca41f31c43320b1ea6397")
    version("0.23.1", sha256="32d3344e357da7012227d49d5031bff254bb8735f3b9edabdb46cfd13cb0e44d")
    version("0.23.0", sha256="c71946f391c27056d3073c3b64ca1d3a5753a993eaa4462e69436e233a04ebe7")
    version("0.22.1", sha256="10fd149e3348a77702369f15c70765e11ce708ee29013089fba6ccabc5aa3aa7")
    version("0.22.0", sha256="e916eeb4e0a722ce3b71e1a5d1e50d2eb4a6996337d497ffadc8278487c46843")
    version("0.21.2", sha256="7f313beb63d8be0a35137f063cc2f6e929a6aa016607060c2ff45fad18379e6b")
    version("0.21.1", sha256="0b4b18788fa2bc0855078d6299139b12f61fa1d2311508a69e9936ca916d6c2d")
    version("0.21.0", sha256="24345ccdefca9bbd8e8ff13d242c335907701ff51dedaa5837d912c0622ab2ee")
    version("0.20.3", sha256="7048cc0e6c17fe5ef3fbac18125dbd5f05d6c628838f004b8e2ad3546fb77d85")
    version("0.20.2", sha256="531c4f5112c24189da9291ea7e2be4a60fdec63281866f4d17597d7e2ad3b293")
    version("0.20.1", sha256="b328beb51c75501f151305b09d5a37efcae270d6b54f72901ff12c8906274cd3")
    version("0.20.0", sha256="20a079cfc2ee4339970b06460f3dacb59c7c7810602821e1f2b731b7f2d83a4e")
    version("0.19.3", sha256="28fc5de9b8934174801aa7d95c5a6f4c878a7e93eea15cdf06d9c982e1cd2fec")
    version("0.19.2", sha256="7bad5787e05ebc9989b15c8759c09c5754c5c10dbd072fa777bca3e9ec2800d5")
    version("0.19.1", sha256="108d057d41b63d18b16c19e5a737124928961f40ccf5a009a9f9276ce443ad0e")
    version("0.19.0", sha256="f5e186c716ebaad2b8e625a42eff03420166e8083995b00e40cd8e07093e8547")
    version("0.18.3", sha256="efcd8972987f5a3085bb69670635e1f331b519bd5e41545c2a4c10a7ce6627ba")
    version("0.18.2", sha256="bace43ee651881c710197bdd28c57e4a37533daaf27ad1865c10c7ad0b55a091")
    version("0.18.1", sha256="326f5e8ef6b9c263fa26023c945c225d74b9c9674979d5d8864a6a33f01f0e22")
    version("0.18.0", sha256="e769c1b4f4ae87c817ad1ba8a14c22bb6a3a5a0a2669fa0dcc3eb6bd8cf36909")
    version("0.17.4", sha256="a33dc3b683fb6c762c66908c437c95b71a5b9c98d998f05496895304a27f82e9")
    version("0.17.3", sha256="0d78243025c45d4b018e475f249597e9d7d37166f53c46c97e75cc21a80509d9")
    version("0.17.2", sha256="1b0b98416b7c1343dba862c68943497ca6945c07cc9103043bece88a2b70bb7c")
    version("0.17.1", sha256="4ec1f25ba70ceab37814f0a21ca7ee3f3fb6d802e5fb9e058568c690cf81b94a")
    version("0.17.0", sha256="8ed9966dfd85b47a15272ad881df62149355b52d939082048931df9aab4044c9")
    version("0.16.0", sha256="01d4d7dcb8606577752f9d9009dd54dfd4607780a55c6f1caab9fa30d6651b41")
    version("0.15.1", sha256="4e3d669a658cc45a46089bb1040dd1c8a541ae391969a6b5bc783fa92660c8c5")
    version("0.15.0", sha256="7ea727dd9ff0bda844c4038c59ab4be56c4e00dc5725bef254272a1c939aecb3")
    version("0.14.6", sha256="9b79d6718cd2bd275888759a465eadd0c62814cbfb22d6362f2f21b0e00e146d")
    version("0.14.5", sha256="ddfa1dd4cd042f0b32cb8be3ecd4d024bba7092b08af8f7d59abcdbbcd9a8f5f")
    version("0.14.4", sha256="05d783ecec949bc863280476b57fca90e0124cb5dbc1e9671a53afd7970cd46a")
    version("0.14.3", sha256="67b58f02785222840ff93b972028a2555418f0e9f366d45e135d62fdc15be39e")
    version("0.14.2", sha256="f0fdf3760074afe3101ef7483506c6d15e852bddce38efd859c7214bcaa5034f")
    version("0.14.1", sha256="92b9e3555e33b3aa1e267a7bc9bc026233b87c01a6f36ddf4492c151ab68218b")
    version("0.14.0", sha256="9c56db4081bebaa3fc69bfb4e3896c014e7f477650c706c46ed4dc931f2d9b91")
    version("0.13.3", sha256="b6f48404349ca99049de40e7bb55511de9ea04a6b1567068997d3fddb2c20f08")
    version("0.13.2", sha256="59c5b17c0fedd7564933f61a4634ec051c13cbdf968815a7b4770611559de152")
    version("0.13.1", sha256="a305813a13bd4267da72fb22272343ef48cf97fe3ac7a939aa7c98750b5b259f")
    version("0.13.0", sha256="fe5460485c28553e3fe4abc8c2f050cc18502d3bd59d7c5792d0806f610d1870")
    version("0.12.3", sha256="8d8a1f9c48519e618ac53b614056cf4589edb02fd1d19aa26d5f478e7067887e")
    version("0.12.2", sha256="f1ffb3d10adb9532f9591fc0bbeca527dda50d6d2b6b3934f0799300fd4eefc2")
    version("0.12.1", sha256="a3bf33e3d014635c6951fe4e3f2a0681173a1f44a9fa7a8ed4b60d20de53534a")
    version("0.12.0", sha256="30db676c55cdee0bfe5ff9a30ba569941ba83376a4bb754c8894c1b59ad9ed19")
    version("0.11.3", sha256="f0e1f0972fcee141c05caac543ef017ee7c87ddddf5fde636c614a28e45021c3")
    version("0.11.2", sha256="20d5289732271c33fa4da52c841b8567a2a2b8f514675bb9a2ede9097adb3712")
    version("0.11.1", sha256="3bbc6b5465d424969b16c5ad7f2f67ffbfe33657fdcb443e1bcc11aa00726841")
    version("0.11.0", sha256="abba2b93795609810e4c9b5cefbbada57e370722cee8a00f94a78c0c96226432")
    version("0.10.1", sha256="ef22208497a76e2f88ebe56c176e4608f049b056252cf1bf122c9c1ec711cfa6")
    version("0.10.0", sha256="056563862c5759b740e95efff44b82c1a4efc370092f22f26aee0b774106bf4d")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("harfbuzz@1.5.0:")
    depends_on("libxkbcommon@0.5:")
    depends_on("zlib")
    depends_on("libpng")
    depends_on("gl", type=("build", "link", "run"))
    depends_on("pkgconfig", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-sphinx", type="build")
    depends_on("py-sphinx-copybutton", type="build")
    depends_on("py-sphinx-inline-tabs", type="build")
    depends_on("py-sphinxext-opengraph", type="build")
    depends_on("py-furo", type="build")
    depends_on("py-beautifulsoup4", type="build")
    depends_on("py-sphinx-basic-ng", type="build")
    depends_on("freetype", when=sys.platform != "darwin")
    depends_on("fontconfig", when=sys.platform != "darwin")
    depends_on("xrandr", when=sys.platform != "darwin")
    depends_on("libxinerama", when=sys.platform != "darwin")
    depends_on("xineramaproto", when=sys.platform != "darwin")
    depends_on("libxi", when=sys.platform != "darwin")
    depends_on("libxcursor", when=sys.platform != "darwin")
    depends_on("fixesproto", when=sys.platform != "darwin")
    depends_on("dbus", when=sys.platform != "darwin")
    depends_on("xkeyboard-config", when=sys.platform != "darwin")
    depends_on("librsync")
    depends_on("lcms2")

    def install(self, spec, prefix):
        with working_dir("."):
            python("-s", "setup.py", "linux-package", "--prefix={0}".format(prefix))
