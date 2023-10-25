# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Emacs(AutotoolsPackage, GNUMirrorPackage):
    """The Emacs programmable text editor."""

    homepage = "https://www.gnu.org/software/emacs"
    git = "https://git.savannah.gnu.org/git/emacs.git"
    gnu_mirror_path = "emacs/emacs-24.5.tar.gz"

    maintainers("alecbcs", "cosmicexplorer")

    version("master", branch="master")
    version("29.1", sha256="5b80e0475b0e619d2ad395ef5bc481b7cb9f13894ed23c301210572040e4b5b1")
    version("28.2", sha256="a6912b14ef4abb1edab7f88191bfd61c3edd7085e084de960a4f86485cb7cad8")
    version("28.1", sha256="1439bf7f24e5769f35601dbf332e74dfc07634da6b1e9500af67188a92340a28")
    version("27.2", sha256="80ff6118fb730a6d8c704dccd6915a6c0e0a166ab1daeef9fe68afa9073ddb73")
    version("27.1", sha256="ffbfa61dc951b92cf31ebe3efc86c5a9d4411a1222b8a4ae6716cfd0e2a584db")
    version("26.3", sha256="09c747e048137c99ed35747b012910b704e0974dde4db6696fde7054ce387591")
    version("26.2", sha256="4f99e52a38a737556932cc57479e85c305a37a8038aaceb5156625caf102b4eb")
    version("26.1", sha256="760382d5e8cdc5d0d079e8f754bce1136fbe1473be24bb885669b0e38fc56aa3")
    version("25.3", sha256="f72c6a1b48b6fbaca2b991eed801964a208a2f8686c70940013db26cd37983c9")
    version("25.2", sha256="505bbd6ea6c197947001d0f80bfccb6b30e1add584d6376f54d4fd6e4de72d2d")
    version("25.1", sha256="763344b90db4d40e9fe90c5d14748a9dbd201ce544e2cf0835ab48a0aa4a1c67")
    version("24.5", sha256="2737a6622fb2d9982e9c47fb6f2fb297bda42674e09db40fc9bcc0db4297c3b6")

    variant("X", default=False, description="Enable an X toolkit")
    variant(
        "toolkit",
        default="gtk",
        values=("gtk", "athena"),
        when="+X",
        description="Select an X toolkit (gtk, athena)",
    )
    variant("tls", default=True, description="Build Emacs with gnutls")
    variant("native", default=False, when="@28:", description="enable native compilation of elisp")
    variant("treesitter", default=False, when="@29:", description="Build with tree-sitter support")
    variant(
        "deterministic_build",
        default=False,
        description="Make the build more deterministic by omitting names, time stamps, etc. from the output.",  # noqa: E501
    )
    variant(
        "link_time_optimization",
        default=False,
        description="build with link-time optimization (experimental)",
    )
    variant("mailutils", default=False, description="build with GNU mailutils")
    variant("kerberos5", default=False, description="support Kerberos version 5 authenticated POP")
    variant(
        "json",
        default=False,
        when="@27:",
        description="use the native json library for json parsing",
    )
    variant("imagemagick", default=False, description="build with imagemagick")
    variant("sound", default="alsa", values=("alsa", "no"), description="Build with sound support")

    depends_on("pkgconfig", type="build")
    depends_on("gzip", type="build")

    depends_on("ncurses")
    depends_on("pcre")
    depends_on("zlib-api")
    depends_on("libxml2")

    # Window system deps.
    with when("+X"):
        depends_on("libx11")

        depends_on("libxaw", when="toolkit=athena")
        depends_on("gtkplus", when="toolkit=gtk")

    depends_on("gnutls", when="+tls")

    # Image processing.
    depends_on("libtiff")
    depends_on("libpng")
    depends_on("libxpm")
    depends_on("giflib")
    depends_on("jpeg")

    depends_on("tree-sitter", when="+treesitter")

    # TODO: this should really be checking for a version from any git ref, but we don't
    # currently have the ability to select for that in a `when` clause.
    with when("@master:"):
        depends_on("m4", type="build")
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")
        depends_on("texinfo", type="build")

    # Native compilation depends on libgccjit, which will work regardless of the
    # compiler that emacs is compiled with.
    depends_on("gcc@11: languages=jit", when="+native")

    depends_on("mailutils", when="+mailutils")
    depends_on("krb5", when="+kerberos5")
    depends_on("gmp")

    depends_on("acl")
    depends_on("imagemagick", when="+imagemagick")
    depends_on("alsa-lib", when="sound=alsa")

    depends_on("jansson", when="+json")

    conflicts("+native", when="@:27", msg="native compilation requires emacs 28 or later")

    # TODO: explain what was fixed in 26.3 on catalina in msg=?
    conflicts("@:26.3", when="platform=darwin os=catalina")

    @when("platform=darwin")
    def setup_build_environment(self, env):
        # On macOS, emacs's config doesn't search hard enough for ncurses's
        # termlib `-ltinfo` lib, which results in linker errors.
        if "+termlib" in self.spec["ncurses"]:
            env.append_flags("LDFLAGS", "-ltinfo")

    def configure_args(self):
        spec = self.spec

        args = []
        args += self.with_or_without("x", variant="X")
        if "+X" in spec:
            toolkit = spec.variants["toolkit"].value
            # TODO: make this use case (a `values=` variant gated on another variant
            # with `when="+X"`) work with self.with_or_without()!
            args.append("--with-x-toolkit={0}".format(toolkit))

        # On OS X/macOS, do not build "nextstep/Emacs.app", because
        # doing so throws an error at build-time.
        if "platform=darwin" in spec:
            # TODO: make selecting by platform/os/architecture work with
            # self.with_or_without() instead of just by variant!
            args.append("--without-ns")

        # Register dependencies to provide to the configure script.
        args += self.with_or_without("native-compilation", variant="native")
        args += self.with_or_without("gnutls", variant="tls")
        args += self.with_or_without("tree-sitter", variant="treesitter")
        args += self.with_or_without("mailutils")
        args += self.with_or_without("imagemagick")
        args += self.with_or_without("kerberos5")
        args += self.with_or_without("json")

        args += self.enable_or_disable("link-time-optimization", variant="link_time_optimization")

        if "+deterministic_build" in spec:
            # TODO: allow negating a boolean variant with self.enable_or_disable() so
            # that a build option can be *dis*abled when the variant is *en*abled!
            args.append("--disable-build-details")

        if self.spec.variants["sound"].value == "alsa":
            # TODO: figure out how self.with_or_without() is supposed to work with
            # a `values=` variant at all; it seems to produce "--with-*=..." for *all*
            # values of the specified variant, not just the *selected* value!
            args.append("--with-sound=alsa")

        return args

    def run_version_check(self, bin):
        """Runs and checks output of the installed binary."""
        exe_path = join_path(self.prefix.bin, bin)
        if not os.path.exists(exe_path):
            raise SkipTest(f"{exe_path} is not installed")

        exe = which(exe_path)
        out = exe("--version", output=str.split, error=str.split)
        assert str(self.spec.version) in out

    def test_ctags(self):
        """check ctags version"""
        self.run_version_check("ctags")

    def test_ebrowse(self):
        """check ebrowse version"""
        self.run_version_check("ebrowse")

    def test_emacs(self):
        """check emacs version"""
        self.run_version_check("emacs")

    def test_emacsclient(self):
        """check emacsclient version"""
        self.run_version_check("emacsclient")

    def test_etags(self):
        """check etags version"""
        self.run_version_check("etags")
