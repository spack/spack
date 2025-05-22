# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Fish(CMakePackage):
    """fish is a smart and user-friendly command line shell for OS X, Linux, and
    the rest of the family.
    """

    homepage = "https://fishshell.com/"
    url = "https://github.com/fish-shell/fish-shell/releases/download/3.6.1/fish-3.6.1.tar.xz"
    git = "https://github.com/fish-shell/fish-shell.git"
    list_url = homepage

    maintainers("funnell", "adamjstewart")

    license("GPL-2.0-only")

    version("master", branch="master")
    version("4.0.2", sha256="6e1ecdb164285fc057b2f35acbdc20815c1623099e7bb47bbfc011120adf7e83")
    version("4.0.1", sha256="4ed63a70207283e15cf21fc5f21db4230421e4f98d4826b5b1c8254d69c762b5")
    version("4.0.0", sha256="2fda5bd970357064d8d4c896e08285ba59965ca2a8c4829ca8a82bf3b89c69f3")
    version("3.7.1", sha256="614c9f5643cd0799df391395fa6bbc3649427bb839722ce3b114d3bbc1a3b250")
    version("3.7.0", sha256="df1b7378b714f0690b285ed9e4e58afe270ac98dbc9ca5839589c1afcca33ab1")
    version("3.6.4", sha256="0f3f610e580de092fbe882c8aa76623ecf91bb16fdf0543241e6e90d5d4bc393")
    version("3.6.3", sha256="55520128c8ef515908a3821423b430db9258527a6c6acb61c7cb95626b5a48d5")
    version("3.6.2", sha256="a21a6c986f1f80273895ba7e905fa80ad7e1a262ddb3d979efa443367eaf4863")
    version("3.6.1", sha256="55402bb47ca6739d8aba25e41780905b5ce1bce0a5e0dd17dca908b5bc0b49b2")
    version("3.6.0", sha256="97044d57773ee7ca15634f693d917ed1c3dc0fa7fde1017f1626d60b83ea6181")
    version("3.5.1", sha256="a6d45b3dc5a45dd31772e7f8dfdfecabc063986e8f67d60bd7ca60cc81db6928")
    version("3.4.1", sha256="b6f23b3843b04db6b0a90fea1f6f0d0e40cc027b4a732098200863f2864a94ea")
    version("3.3.1", sha256="b5b4ee1a5269762cbbe993a4bd6507e675e4100ce9bbe84214a5eeb2b19fae89")
    version("3.1.2", sha256="d5b927203b5ca95da16f514969e2a91a537b2f75bec9b21a584c4cd1c7aa74ed")
    version("3.1.0", sha256="e5db1e6839685c56f172e1000c138e290add4aa521f187df4cd79d4eab294368")
    version("3.0.0", sha256="ea9dd3614bb0346829ce7319437c6a93e3e1dfde3b7f6a469b543b0d2c68f2cf")

    variant("docs", default=False, description="Build documentation")

    # https://github.com/fish-shell/fish-shell#dependencies-1
    depends_on("rust@1.70:", when="@4:")
    depends_on("cmake@3.15:", when="@4:", type="build")
    depends_on("cmake@3.5:", when="@3.4:", type="build")
    depends_on("cmake@3.2:", type="build")
    depends_on("c", when="@4:", type="build")
    depends_on("pcre2@10.21:")
    depends_on("gettext")
    depends_on("py-sphinx", when="+docs", type="build")
    depends_on("python", type="test")
    depends_on("tmux", when="@4:", type="test")
    depends_on("py-pexpect", type="test")

    # Historical dependencies
    depends_on("cxx", when="@:3", type="build")
    depends_on("ncurses", when="@:3")

    # https://github.com/fish-shell/fish-shell/issues/7310
    patch("codesign.patch", when="@3.1.2 platform=darwin")

    executables = ["^fish$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"fish, version (\S+)", output)
        return match.group(1) if match else None

    def url_for_version(self, version):
        url = "https://github.com/fish-shell/fish-shell/releases/download/{0}/fish-{0}.tar.{1}"
        if version < Version("3.2.0"):
            ext = "gz"
        else:
            ext = "xz"
        return url.format(version, ext)

    def cmake_args(self):
        return [self.define_from_variant("BUILD_DOCS", "docs")]
