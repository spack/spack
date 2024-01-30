# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *
from spack.util.environment import is_system_path


class Git(AutotoolsPackage):
    """Git is a free and open source distributed version control
    system designed to handle everything from small to very large
    projects with speed and efficiency.
    """

    homepage = "http://git-scm.com"
    url = "https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.12.0.tar.gz"
    maintainers("jennfshr")

    tags = ["build-tools"]

    executables = ["^git$"]

    license("GPL-2.0-only")

    # Every new git release comes with a corresponding manpage resource:
    # https://www.kernel.org/pub/software/scm/git/git-manpages-{version}.tar.gz
    # https://mirrors.edge.kernel.org/pub/software/scm/git/sha256sums.asc
    version("2.42.0", sha256="34aedd54210d7216a55d642bbb4cfb22695b7610719a106bf0ddef4c82a8beed")
    version("2.41.0", sha256="c4a6a3dd1827895a80cbd824e14d94811796ae54037549e0da93f7b84cb45b9f")
    version("2.40.1", sha256="55511f10f3b1cdf5db4e0e3dea61819dfb67661b0507a5a2b061c70e4f87e14c")
    version("2.39.3", sha256="2f9aa93c548941cc5aff641cedc24add15b912ad8c9b36ff5a41b1a9dcad783e")
    version("2.38.5", sha256="09392caf6ff296341022595a175d8b075bc98b6a82f6227d3bd21e36a2a812c3")
    version("2.37.7", sha256="2108fa57b74add4300b8960e9404e0ed3e5f0efda7470450c67c67e8ab7616d5")
    version("2.36.6", sha256="a8c09f46d5d16a8d8f19e8089aeb408d95d8097af03de297061e83a2c74890dd")
    version("2.35.8", sha256="3a675e0128a7153e1492bbe14d08195d44b5916e6b8879addf94b1f4add77dca")
    version("2.34.8", sha256="10a6c233471d7d4439cd4004961a3f4ff7e6de308645a1074ec3522b8ea52c83")
    version("2.33.8", sha256="eafd10da9fdf86be0a79beb67c3537eead114f91836c685d5b9c969c961516ae")
    version("2.32.7", sha256="f09904d13a9bfca5fcb228c3caba1d4c17426dec0000bf67672af257b8a73db4")
    version("2.31.8", sha256="d2443e368b1394858a1040bd74dacfba46bce2cf3410ef3bc5089a703fc91e9a")
    version("2.30.9", sha256="b14b5f4ce1fe23ed78839664c7ba888fb5cedba3dd98d9f5a499a36fa3a4a2d8")

    # Deprecated versions
    version(
        "2.40.0",
        sha256="ab37c343c0ad097282fd311ab9ca521ab3da836e5c4ed2093994f1b7f8575b09",
        deprecated=True,
    )
    version(
        "2.39.2",
        sha256="fb6807d1eb4094bb2349ab97d203fe1e6c3eb28af73ea391decfbd3a03c02e85",
        deprecated=True,
    )
    version(
        "2.39.1",
        sha256="ae8d3427e4ccd677abc931f16183c0ec953e3bfcd866493601351e04a2b97398",
        deprecated=True,
    )
    version(
        "2.38.3",
        sha256="ba8f1c56763cfde0433657b045629a4c55047c243eb3091d39dea6f281c8d8e1",
        deprecated=True,
    )
    version(
        "2.38.1",
        sha256="620ed3df572a34e782a2be4c7d958d443469b2665eac4ae33f27da554d88b270",
        deprecated=True,
    )
    version(
        "2.37.5",
        sha256="5c11f90652afee6c77ef7ddfc672facd4bc6f2596d9627df2f1780664b058b9a",
        deprecated=True,
    )
    version(
        "2.37.4",
        sha256="a638c9bf9e45e8d48592076266adaa9b7aa272a99ee2aee2e166a649a9ba8a03",
        deprecated=True,
    )
    version(
        "2.36.3",
        sha256="0c831b88b0534f08051d1287505dfe45c367108ee043de6f1c0502711a7aa3a6",
        deprecated=True,
    )
    version(
        "2.35.6",
        sha256="6bd51e0487028543ba40fe3d5b33bd124526a7f7109824aa7f022e79edf93bd1",
        deprecated=True,
    )
    version(
        "2.35.5",
        sha256="2cca63fe7bebb5b4bf8efea7b46b12bb89c16ff9711b6b6d845928501d00d0a3",
        deprecated=True,
    )
    version(
        "2.34.6",
        sha256="01c0ae4161a07ffeb89cfb8bda564eb2dcb83b45b678cf2930cdbdd8e81784d0",
        deprecated=True,
    )
    version(
        "2.34.5",
        sha256="26831c5e48a8c2bf6a4fede1b38e1e51ffd6dad85952cf69ac520ebd81a5ae82",
        deprecated=True,
    )
    version(
        "2.33.6",
        sha256="76f6a64a198bec38e83044f97fb5a2dfa8404091df5a905404615d2a4c5ebfb7",
        deprecated=True,
    )
    version(
        "2.33.5",
        sha256="d061ed97f890befaef18b4aad80a37b40db90bcf24113c42765fee157a69c7de",
        deprecated=True,
    )
    version(
        "2.32.5",
        sha256="9982e17209cf4a385ce4a6167863cdd29f68e425d4249aac186434dc3536fe5f",
        deprecated=True,
    )
    version(
        "2.32.4",
        sha256="4c791b8e1d96948c9772efc21373ab9b3187af42cdebc3bcbb1a06d794d4e494",
        deprecated=True,
    )
    version(
        "2.31.6",
        sha256="73971208dccdd6d87639abe50ee3405421ec4ba05dec9f8aa90b4e7f1985e15c",
        deprecated=True,
    )
    version(
        "2.31.5",
        sha256="2d4197660322937cc44cab5742deef727ba519ef7405455e33100912e3b019f2",
        deprecated=True,
    )
    version(
        "2.30.7",
        sha256="c98bf38a296f23ad5619a097df928044b31859df8f89b3ae5a8ea109d3ebd88e",
        deprecated=True,
    )
    version(
        "2.30.6",
        sha256="a6130b38843a5c80e80fb4f7ac4864d361cbf103d262b64e267264e49440d24a",
        deprecated=True,
    )

    for _version, _sha256_manpage in {
        "2.42.0": "51643c53d70ce15dde83b6da2bad76ba0c7bbcd4f944d7c378f03a15b9f2e1de",
        "2.41.0": "7b77c646b36d33c5c0f62677a147142011093270d6fd628ca38c42d5301f3888",
        "2.40.1": "6bbde434121bd0bf8aa574c60fd9a162388383679bd5ddd99921505149ffd4c2",
        "2.40.0": "fda16047e9c1dd07d9585cc26bbf4002ebf8462ada54cb72b97a0e48135fd435",
        "2.39.3": "c8377b5a3ff497d7e6377363c270931496e982509ff27a1e46956d6637671642",
        "2.39.2": "fd92e67fb750ceb2279dcee967a21303f2f8117834a21c1e0c9f312ebab6d254",
        "2.39.1": "b2d1b2c6cba2343934792c4409a370a8c684add1b3c0f9b757e71189b1a2e80e",
        "2.38.5": "648f2b89c9a173c3a687b99629208222170a398c7b14ed92de128656123c73cd",
        "2.38.3": "9e5c924f6f1c961e09d1a8926c2775a158a0375a3311205d7a6176a3ed522272",
        "2.38.1": "fcb27484406b64419a9f9890e95ef29af08e1f911d9d368546eddc59a18e245d",
        "2.37.7": "475a894584ecc8b278d592a2d99c5c4a4a863485f5126508bcef686cba4a4ac0",
        "2.37.5": "9fab559197891fc1b499cb57513effce7462383f861ac6a7791a46f5348dd7fe",
        "2.37.4": "06ed920949e717f3ab13c98327ee63cae5e3020ac657d14513ef8f843109b638",
        "2.36.6": "08bded34c0ff49b7e8d5d0778511a07f191751c6edb98aaf2cee4c96962cc94c",
        "2.36.3": "c5f5385c2b46270a8ce062a9c510bfa4288d9cca54efe0dff48a12ca969cfc6f",
        "2.35.8": "f85e549d37936df744fd78c1ce670c1682bdd2f35d1f072883b82babe66e484a",
        "2.35.6": "5e44e05a97f49d7a170a7303f795063b19bc78560acd7458274882f19b631187",
        "2.35.5": "6cbd4d2185c7a757db21f873973fa1efb81069d8b8b8cc350ca6735cb98f45c5",
        "2.34.8": "e43e75edb8d339ceed4990b5054eb2302efc857d0feab690598e14dbdb9bcccc",
        "2.34.6": "70c784ced9c5ccbd4137d676b032e2ccffeea8aef3094626c2b44d6c843547df",
        "2.34.5": "897941be5b223b9d32217adb64ea8747db2ba57be5f68be598c44d747d1061b2",
        "2.33.8": "9b49f931e58001d818b2cba7eb6d0242965cfb1eaa5194271b88fcc4529b4987",
        "2.33.6": "d7b9170dc7d6f461e00731cf5cf6e4b589e90c8d4eac440fd3e8b5e3d11f0b8f",
        "2.33.5": "34648ede9ac2869190083ee826065c36165e54d9e2906b10680261b243d89890",
        "2.32.7": "dcce6d701f99190e081f74b539389cdf4674ddbcd4af143631034354a5db39fc",
        "2.32.5": "99b236824f1677e15b21514e310d7a0954586d031ffc3a873a4e2138ed073f15",
        "2.32.4": "fa73d0eac384e594efdd4c21343545e407267ab64e970a6b395c7f1874ddb0bf",
        "2.31.8": "73722b9487456d7605beec65a9fa9415410faa8b9f8a5fd209d75be47bf1a968",
        "2.31.6": "2e2f921d8ef8a839e05ba3a1cea8f864a49b04648378bf0253213a5d4f1642fe",
        "2.31.5": "18850fc8f1c34e51a0a98b9f974b8356a5d63a53c96fb9fe3dc2880ee84746ab",
        "2.30.9": "a3f61fe08453dd88fdd84a28ee6d4c9fbd710a7b1ead7ce5c976146656714ece",
        "2.30.7": "4fc6063c229453de244a88c71f688a2508f30b80ebd47353cc68d730ea1b82aa",
        "2.30.6": "6c20ab10be233e8ff7838351fa5210e972c08005ec541a5241f626cfd4adebfe",
    }.items():
        resource(
            name="git-manpages",
            url="https://www.kernel.org/pub/software/scm/git/git-manpages-{0}.tar.gz".format(
                _version
            ),
            sha256=_sha256_manpage,
            placement="git-manpages",
            when="@{0} +man".format(_version),
        )

    variant("tcltk", default=False, description="Gitk: provide Tcl/Tk in the run environment")
    variant("svn", default=False, description="Provide SVN Perl dependency in run environment")
    variant("perl", default=True, description="Do not use Perl scripts or libraries at all")
    variant("nls", default=True, description="Enable native language support")
    variant("man", default=True, description="Install manual pages")
    variant("subtree", default=True, description="Add git-subtree command and capability")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("curl")
    depends_on("expat")
    depends_on("gettext", when="+nls")
    depends_on("iconv")
    depends_on("libidn2")
    depends_on("openssl")
    depends_on("pcre", when="@:2.13")
    depends_on("pcre2", when="@2.14:")
    depends_on("perl", when="+perl")
    depends_on("zlib-api")
    depends_on("openssh", type="run")
    depends_on("perl-alien-svn", type="run", when="+svn")
    depends_on("tk", type=("build", "link"), when="+tcltk")

    conflicts("+svn", when="~perl")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(spack.fetch_strategy.GitFetchStrategy.git_version_re, output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version_str):
        prefix = os.path.dirname(exes[0])
        variants = ""
        if "gitk" in os.listdir(prefix):
            variants += "+tcltk"
        else:
            variants += "~tcltk"
        return variants

    # See the comment in setup_build_environment re EXTLIBS.
    def patch(self):
        filter_file(r"^EXTLIBS =$", "#EXTLIBS =", "Makefile")

    def setup_build_environment(self, env):
        # We use EXTLIBS rather than LDFLAGS so that git's Makefile
        # inserts the information into the proper place in the link commands
        # (alongside the # other libraries/paths that configure discovers).
        # LDFLAGS is inserted *before* libgit.a, which requires libintl.
        # EXTFLAGS is inserted *after* libgit.a.
        # This depends on the patch method above, which keeps the Makefile
        # from stepping on the value that we pass in via the environment.
        #
        # The test avoids failures when git is an external package.
        # In that case the node in the DAG gets truncated and git DOES NOT
        # have a gettext dependency.
        spec = self.spec
        if "+nls" in spec:
            if "intl" in spec["gettext"].libs.names:
                extlib_bits = []
                if not is_system_path(spec["gettext"].prefix):
                    extlib_bits.append(spec["gettext"].libs.search_flags)
                extlib_bits.append("-lintl")
                env.append_flags("EXTLIBS", " ".join(extlib_bits))

        if not self.spec["curl"].satisfies("libs=shared"):
            curlconfig = which(os.path.join(self.spec["curl"].prefix.bin, "curl-config"))
            # For configure step:
            env.append_flags("LIBS", curlconfig("--static-libs", output=str).strip())
            # For build step:
            env.append_flags("EXTLIBS", curlconfig("--static-libs", output=str).strip())

        if "~perl" in self.spec:
            env.append_flags("NO_PERL", "1")

    def configure_args(self):
        spec = self.spec

        configure_args = [
            "--with-curl={0}".format(spec["curl"].prefix),
            "--with-expat={0}".format(spec["expat"].prefix),
            "--with-openssl={0}".format(spec["openssl"].prefix),
            "--with-zlib={0}".format(spec["zlib-api"].prefix),
        ]

        if not self.spec["iconv"].name == "libc":
            configure_args.append(
                "--with-iconv={0}".format(
                    "yes" if is_system_path(spec["iconv"].prefix) else spec["iconv"].prefix
                )
            )

        if "+perl" in self.spec:
            configure_args.append("--with-perl={0}".format(spec["perl"].command.path))

        if "^pcre" in self.spec:
            configure_args.append("--with-libpcre={0}".format(spec["pcre"].prefix))
        if "^pcre2" in self.spec:
            configure_args.append("--with-libpcre2={0}".format(spec["pcre2"].prefix))
        if "+tcltk" in self.spec:
            configure_args.append("--with-tcltk={0}".format(self.spec["tk"].prefix.bin.wish))
        else:
            configure_args.append("--without-tcltk")

        return configure_args

    @run_after("configure")
    def filter_rt(self):
        if self.spec.satisfies("platform=darwin"):
            # Don't link with -lrt; the system has no (and needs no) librt
            filter_file(r" -lrt$", "", "Makefile")

    def check(self):
        make("test")

    def build(self, spec, prefix):
        args = []
        if "~nls" in self.spec:
            args.append("NO_GETTEXT=1")
        make(*args)

        if spec.satisfies("platform=darwin"):
            with working_dir("contrib/credential/osxkeychain"):
                make()

    def install(self, spec, prefix):
        args = ["install"]
        if "~nls" in self.spec:
            args.append("NO_GETTEXT=1")
        make(*args)

        if spec.satisfies("platform=darwin"):
            install(
                "contrib/credential/osxkeychain/git-credential-osxkeychain",
                join_path(prefix, "libexec", "git-core"),
            )

    @run_after("install")
    def install_completions(self):
        install_tree("contrib/completion", self.prefix.share)

    @run_after("install")
    def install_manpages(self):
        if "~man" in self.spec:
            return

        prefix = self.prefix

        with working_dir("git-manpages"):
            install_tree("man1", prefix.share.man.man1)
            install_tree("man5", prefix.share.man.man5)
            install_tree("man7", prefix.share.man.man7)

    @run_after("install")
    def install_subtree(self):
        if "+subtree" in self.spec:
            with working_dir("contrib/subtree"):
                make_args = ["V=1", "prefix={}".format(self.prefix.bin)]
                make(" ".join(make_args))
                install_args = ["V=1", "prefix={}".format(self.prefix.bin), "install"]
                make(" ".join(install_args))
                install("git-subtree", self.prefix.bin)

    def setup_run_environment(self, env):
        # Setup run environment if using SVN extension
        # Libs from perl-alien-svn and apr-util are required in
        # LD_LIBRARY_PATH
        # TODO: extend to other platforms
        if "+svn platform=linux" in self.spec:
            perl_svn = self.spec["perl-alien-svn"]
            env.prepend_path(
                "LD_LIBRARY_PATH",
                join_path(
                    perl_svn.prefix, "lib", "perl5", "x86_64-linux-thread-multi", "Alien", "SVN"
                ),
            )
