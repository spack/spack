# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *  # noqa: E402

sys.path.append(os.path.dirname(__file__))
import boostorg.bjam as bjam  # noqa: E402
import boostorg.bootstrap as bootstrap  # noqa: E402
import boostorg.patches as boostpatches  # noqa: E402
import boostorg.toolset  # noqa: E402
import boostorg.variants as boostvariants  # noqa: E402


class Boost(Package):
    """Boost provides free peer-reviewed portable C++ source
    libraries, emphasizing libraries that work well with the C++
    Standard Library.

    Boost libraries are intended to be widely useful, and usable
    across a broad spectrum of applications. The Boost license
    encourages both commercial and non-commercial use.
    """

    homepage = "https://www.boost.org"
    url = "https://archives.boost.io/release/1.87.0/source/boost_1_87_0.tar.bz2"
    git = "https://github.com/boostorg/boost.git"
    list_url = "https://sourceforge.net/projects/boost/files/boost/"
    list_depth = 1
    maintainers("hainest")

    license("BSL-1.0")

    version("develop", branch="develop", submodules=True)
    version("1.88.0", sha256="46d9d2c06637b219270877c9e16155cbd015b6dc84349af064c088e9b5b12f7b")
    version("1.87.0", sha256="af57be25cb4c4f4b413ed692fe378affb4352ea50fbe294a11ef548f4d527d89")
    version("1.86.0", sha256="1bed88e40401b2cb7a1f76d4bab499e352fa4d0c5f31c0dbae64e24d34d7513b")
    version("1.85.0", sha256="7009fe1faa1697476bdc7027703a2badb84e849b7b0baad5086b087b971f8617")
    version("1.84.0", sha256="cc4b893acf645c9d4b698e9a0f08ca8846aa5d6c68275c14c3e7949c24109454")
    version("1.83.0", sha256="6478edfe2f3305127cffe8caf73ea0176c53769f4bf1585be237eb30798c3b8e")
    version("1.82.0", sha256="a6e1ab9b0860e6a2881dd7b21fe9f737a095e5f33a3a874afc6a345228597ee6")
    version("1.81.0", sha256="71feeed900fbccca04a3b4f2f84a7c217186f28a940ed8b7ed4725986baf99fa")
    version("1.80.0", sha256="1e19565d82e43bc59209a168f5ac899d3ba471d55c7610c677d4ccf2c9c500c0")
    version("1.79.0", sha256="475d589d51a7f8b3ba2ba4eda022b170e562ca3b760ee922c146b6c65856ef39")
    version("1.78.0", sha256="8681f175d4bdb26c52222665793eef08490d7758529330f98d3b29dd0735bccc")
    version("1.77.0", sha256="fc9f85fc030e233142908241af7a846e60630aa7388de9a5fafb1f3a26840854")
    version("1.76.0", sha256="f0397ba6e982c4450f27bf32a2a83292aba035b827a5623a14636ea583318c41")
    version("1.75.0", sha256="953db31e016db7bb207f11432bef7df100516eeb746843fa0486a222e3fd49cb")
    version("1.74.0", sha256="83bfc1507731a0906e387fc28b7ef5417d591429e51e788417fe9ff025e116b1")
    version("1.73.0", sha256="4eb3b8d442b426dc35346235c8733b5ae35ba431690e38c6a8263dce9fcbb402")
    version("1.72.0", sha256="59c9b274bc451cf91a9ba1dd2c7fdcaf5d60b1b3aa83f2c9fa143417cc660722")
    version("1.71.0", sha256="d73a8da01e8bf8c7eda40b4c84915071a8c8a0df4a6734537ddde4a8580524ee")
    version("1.70.0", sha256="430ae8354789de4fd19ee52f3b1f739e1fba576f0aded0897c3c2bc00fb38778")
    version("1.69.0", sha256="8f32d4617390d1c2d16f26a27ab60d97807b35440d45891fa340fc2648b04406")
    version("1.68.0", sha256="7f6130bc3cf65f56a618888ce9d5ea704fa10b462be126ad053e80e553d6d8b7")
    version("1.67.0", sha256="2684c972994ee57fc5632e03bf044746f6eb45d4920c343937a465fd67a5adba")
    version("1.66.0", sha256="5721818253e6a0989583192f96782c4a98eb6204965316df9f5ad75819225ca9")
    version("1.65.1", sha256="9807a5d16566c57fd74fb522764e0b134a8bbe6b6e8967b83afefd30dcd3be81")
    version("1.65.0", sha256="ea26712742e2fb079c2a566a31f3266973b76e38222b9f88b387e3c8b2f9902c")
    version("1.64.0", sha256="7bcc5caace97baa948931d712ea5f37038dbb1c5d89b43ad4def4ed7cb683332")
    version("1.63.0", sha256="beae2529f759f6b3bf3f4969a19c2e9d6f0c503edcb2de4a61d1428519fcb3b0")
    version("1.62.0", sha256="36c96b0f6155c98404091d8ceb48319a28279ca0333fba1ad8611eb90afb2ca0")
    version("1.61.0", sha256="a547bd06c2fd9a71ba1d169d9cf0339da7ebf4753849a8f7d6fdb8feee99b640")
    version("1.60.0", sha256="686affff989ac2488f79a97b9479efb9f2abae035b5ed4d8226de6857933fd3b")
    version("1.59.0", sha256="727a932322d94287b62abb1bd2d41723eec4356a7728909e38adb65ca25241ca")
    version("1.58.0", sha256="fdfc204fc33ec79c99b9a74944c3e54bd78be4f7f15e260c0e2700a36dc7d3e5")
    version("1.57.0", sha256="910c8c022a33ccec7f088bd65d4f14b466588dda94ba2124e78b8c57db264967")
    version("1.56.0", sha256="134732acaf3a6e7eba85988118d943f0fa6b7f0850f65131fff89823ad30ff1d")
    version("1.55.0", sha256="fff00023dd79486d444c8e29922f4072e1d451fc5a4d2b6075852ead7f2b7b52")
    version("1.54.0", sha256="047e927de336af106a24bceba30069980c191529fd76b8dff8eb9a328b48ae1d")
    version("1.53.0", sha256="f88a041b01882b0c9c5c05b39603ec8383fb881f772f6f9e6e6fd0e0cddb9196")
    version("1.52.0", sha256="222b6afd7723f396f5682c20130314a10196d3999feab5ba920d2a6bf53bac92")
    version("1.51.0", sha256="fb2d2335a29ee7fe040a197292bfce982af84a645c81688a915c84c925b69696")
    version("1.50.0", sha256="c9ace2b8c81fa6703d1d17c7e478de3bc51101c5adbdeb3f6cb72cf3045a8529")
    version("1.49.0", sha256="dd748a7f5507a7e7af74f452e1c52a64e651ed1f7263fce438a06641d2180d3c")
    version("1.48.0", sha256="1bf254b2d69393ccd57a3cdd30a2f80318a005de8883a0792ed2f5e2598e5ada")
    version("1.47.0", sha256="815a5d9faac4dbd523fbcf3fe1065e443c0bbf43427c44aa423422c6ec4c2e31")
    version("1.46.1", sha256="e1dfbf42b16e5015c46b98e9899c423ca4d04469cbeee05e43ea19236416d883")
    version("1.46.0", sha256="2f90f60792fdc25e674b8a857a0bcbb8d01199651719c90d5c4f8c61c08eba59")
    version("1.45.0", sha256="55ed3ec51d5687e8224c988e22bef215dacce04e037d9f689569a80c4377a6d5")
    version("1.44.0", sha256="45c328029d97d1f1dc7ff8c9527cd0c5cc356636084a800bca2ee4bfab1978db")
    version("1.43.0", sha256="344f100b1aa410e812cabf0e4130728a80be042bf346135516b9187853806120")
    version("1.42.0", sha256="4b1eb95bd250ce15ac66435d6167f225b072b0d3a7eb72477a31847a9ca9e609")
    version("1.41.0", sha256="1ef94e6749eaf13318284b4f629be063544c7015b45e38113b975ac1945cc726")
    version("1.40.0", sha256="36cf4a239b587067a4923fdf6e290525a14c3af29829524fa73f3dec6841530c")
    version("1.39.0", sha256="44785eae8c6cce61a29a8a51f9b737e57b34d66baa7c0bcd4af188832b8018fd")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    boost_variants = boostvariants.load()
    boostpatches.load()

    @property
    def libs(self):
        query = self.spec.last_query.extra_parameters
        shared = self.spec.satisfies("+shared")

        libnames = query if query else self.boost_variants.libraries_to_build(self.spec)
        libnames += ["monitor"]
        libraries = ["libboost_*%s*" % lib for lib in libnames]

        return find_libraries(libraries, root=self.prefix, shared=shared, recursive=True)

    # C++98/03 support was removed in 1.84.0
    conflicts("cxxstd=98", when="@1.84.0:", msg="This version of Boost requires C++11 or newer")
    conflicts("cxxstd=03", when="@1.84.0:", msg="This version of Boost requires C++11 or newer")

    # Boost 1.80 does not build with the Intel oneapi compiler
    # https://github.com/spack/spack/pull/32879#issuecomment-1265933265
    conflicts("%oneapi", when="@1.80")

    with when("+icu"):
        depends_on("icu4c")

        # icu4c currently only supports c++11,14,17
        #   when cxxstd > 17, icu4c defaults to c++11.
        #   This is not ideal, but nothing we can do about it here.
        for std in ["11", "14", "17"]:
            depends_on(f"icu4c cxxstd={std}", when=f"cxxstd={std}")

    with when("+python"):
        depends_on("python")

        # https://github.com/boostorg/python/commit/cbd2d9f033c61d29d0a1df14951f4ec91e7d05cd
        depends_on("python@:3.9", when="@:1.75")

    with when("+iostreams"):
        depends_on("bzip2")
        depends_on("zlib-api")
        depends_on("zstd")
        depends_on("xz")

    with when("+numpy"):
        depends_on("py-numpy", type=("build", "run"))

    with when("+mpi"):
        depends_on("mpi")

    def patch(self):
        boostpatches.apply(self.spec)

    def url_for_version(self, version):
        url = "https://archives.boost.io/release/{0}/source/boost_{1}.tar.bz2"
        return url.format(version.dotted, version.underscored)

    def flag_handler(self, name, flags):
        if name == "cxxflags":
            if self.spec.satisfies("@1.79.0 %oneapi"):
                flags.append("-Wno-error=enum-constexpr-conversion")
        return (flags, None, None)

    def _bootstrap(self, spec, with_libs, toolset):
        opts = [f"--prefix={prefix}"]

        if spec.satisfies("platform=windows"):
            version = self.compiler.platform_toolset_ver
            opts.extend(bootstrap.options_windows(spec, version))
            Executable("cmd.exe")("/c", ".\\bootstrap.bat", *opts)
        else:
            # to make Boost find the user-config.jam
            env["BOOST_BUILD_PATH"] = self.stage.source_path
            opts.extend(bootstrap.options(spec, toolset, with_libs))
            Executable("./bootstrap.sh")(*opts)

    def _b2_options(self, spec, toolset):
        opts = []

        if spec.satisfies("platform=windows"):
            is_64bit = "64" in str(spec.target.family)
            opts.append(f"address-model={64 if is_64bit else 32}")
            if not spec.satisfies("+python"):
                opts.append("--without-python")

            # The runtime link must either be shared or static, not both.
            if spec.satisfies("+shared"):
                opts.append("runtime-link=shared")
            else:
                opts.append("runtime-link=static")

            # Any library that could be passed to `--with-libraries` but is not
            # an active variant needs to be passed to `--without-<NAME>`.
            buildable = set(boost_variants.libraries_to_build(spec))
            all_libs = set(self.boost_variants.all_libraries())
            for lib in all_libs - buildable:
                opts.append(f"--without-{lib}")
        else:
            jobs = make_jobs
            # in 1.59 max jobs became dynamic
            if jobs > 64 and spec.satisfies("@:1.58"):
                jobs = 64

            opts.append(f"-j {jobs}")

            if not spec.satisfies("@:1.75 %intel"):
                # When building any version >= 1.76, the toolset must be specified.
                # Earlier versions could not specify Intel as the toolset
                # as that was considered to be redundant/conflicting with
                # --with-toolset in bootstrap.
                # (although it is not currently known if 1.76 is the earliest
                # version that requires specifying the toolset for Intel)
                opts.append(f"toolset={toolset}")

        opts.extend(bjam.b2_options(spec))
        return opts

    def install(self, spec, prefix):
        # On Darwin, Boost expects the Darwin libtool. However, one of the
        # dependencies may have pulled in Spack's GNU libtool, and these two
        # are not compatible. We thus create a symlink to Darwin's libtool
        # and add it at the beginning of PATH.
        if sys.platform == "darwin":
            newdir = os.path.abspath("darwin-libtool")
            mkdirp(newdir)
            force_symlink("/usr/bin/libtool", join_path(newdir, "libtool"))
            env["PATH"] = newdir + ":" + env["PATH"]

        # Library names that need to be passed to `--with-libraries`
        with_libs = self.boost_variants.libraries_to_build(spec)

        # Compiler/toolset to use
        toolset = boostorg.toolset.config(spec)

        # Create the user-level jam file
        user_jam_file = os.path.join(self.stage.source_path, "user-config.jam")
        bjam.write_user_jam_file(user_jam_file, spec, spack_cxx, toolset)

        # Run the bootstrap script
        self._bootstrap(spec, with_libs, toolset)

        # strip the toolchain to avoid double include errors (intel) or
        # user-config being overwritten (again intel, but different boost version)
        filter_file(
            r"^\s*using {0}.*".format(toolset),
            "",
            os.path.join(self.stage.source_path, "project-config.jam"),
        )

        # fmt: off
        # Gather the options for `b2`
        b2_options = [
            f"--prefix={self.prefix}",
            f"--user-config={user_jam_file}"
        ]
        # fmt: on

        b2_options.extend(self._b2_options(spec, toolset))

        # Run b2
        b2 = Executable(bjam.b2_name(spec))

        # Create headers if building from a git checkout
        if spec.satisfies("@develop"):
            b2("headers", *b2_options)

        # Remove any previously-built targets (in case this is a rebuild)
        b2("--clean", *b2_options)

        threading_opts = bjam.threading_options(spec)

        if spec.satisfies("platform=windows"):
            # Windows doesn't use the the threading option
            b2("install", *b2_options)
        elif spec.satisfies("+mpi"):
            # Boost.MPI fails if the threading options aren't separated
            for o in threading_opts:
                b2("install", f"threading={o}", *b2_options)
        else:
            threading = ",".join(threading_opts)
            b2("install", f"threading={threading}", *b2_options)

        if spec.satisfies("+multithreaded") and spec.satisfies("~taggedlayout"):
            self.add_buildopt_symlinks(prefix)

        # The shared libraries are not installed correctly
        # on Darwin; correct this
        if (sys.platform == "darwin") and spec.satisfies("+shared"):
            fix_darwin_install_name(prefix.lib)

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        env.set("BOOST_ROOT", self.prefix)

    def setup_dependent_build_environment(
        self, env: EnvironmentModifications, dependent_spec: Spec
    ) -> None:
        if self.spec.satisfies("+context"):
            context_impl = self.spec.variants["context-impl"].value
            # fcontext, as the default, has no corresponding macro
            if context_impl == "ucontext":
                env.append_flags("CXXFLAGS", "-DBOOST_USE_UCONTEXT")
            elif context_impl == "winfib":
                env.append_flags("CXXFLAGS", "-DBOOST_USE_WINFIB")

    def add_buildopt_symlinks(self, prefix):
        with working_dir(prefix.lib, create=True):
            for lib in os.listdir(os.curdir):
                if os.path.isfile(lib):
                    prefix, remainder = lib.split(".", 1)
                    symlink(lib, "%s-mt.%s" % (prefix, remainder))
