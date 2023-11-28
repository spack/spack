# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import platform

from spack.package import *


class Pmix(AutotoolsPackage):
    """The Process Management Interface (PMI) has been used for quite some
    time as a means of exchanging wireup information needed for
    interprocess communication. However, meeting the significant
    orchestration challenges presented by exascale systems requires
    that the process-to-system interface evolve to permit a tighter
    integration between the different components of the parallel
    application and existing and future SMS solutions.

    PMI Exascale (PMIx) addresses these needs by providing an extended
    version of the PMI definitions specifically designed to support
    exascale and beyond environments by: (a) adding flexibility to the
    functionality expressed in the existing APIs, (b) augmenting the
    interfaces with new APIs that provide extended capabilities, (c)
    forging a collaboration between subsystem providers including
    resource manager, fabric, file system, and programming library
    developers, (d) establishing a standards-like body for maintaining
    the definitions, and (e) providing a reference implementation of the
    PMIx standard that demonstrates the desired level of scalability
    while maintaining strict separation between it and the standard
    itself."""

    homepage = "https://pmix.org"
    url = "https://github.com/pmix/pmix/releases/download/v3.1.3/pmix-3.1.3.tar.bz2"
    git = "https://github.com/openpmix/openpmix.git"
    maintainers("rhc54")

    # Branches 4.2 & 5.0 will also need submodules
    version("master", branch="master", submodules=True)
    version("5.0.1", sha256="d4371792d4ba4c791e1010100b4bf9a65500ababaf5ff25d681f938527a67d4a")
    version("5.0.0", sha256="92a85c4946346816c297ac244fbaf4f723bba87fb7e4424a057c2dabd569928d")
    version("4.2.6", sha256="10b0d5a7fca70272e9427c677557578ac452cea02aeb00e30dec2116d20c3cd0")
    version("4.2.5", sha256="a89c2c5dc69715a4df1e76fdc4318299386c184623a1d0d5eb1fb062e14b0d2b")
    version("4.2.4", sha256="c4699543f2278d3a78bdac72b4b2da9cd92d11d18478d66522b8991764b021c8")
    version("4.2.3", sha256="c3d9d6885ae39c15627a86dc4718e050baf604acda71b8b9e2ee3b12ad5c2d2a")
    version("4.2.2", sha256="935b2f492e4bc409017f1425a83366aa72a7039605ea187c9fac7bb1371cd73c")
    version("4.2.1", sha256="3c992fa0d653b56e0e409bbaec9de8fc1b82c948364dbb28545442315ed2a179")
    version("4.1.2", sha256="670d3a02b39fb2126fe8084174cf03c484e027b5921b5c98a851108134e2597a")
    version("4.1.1", sha256="0527a15d616637b95975d238bbc100b244894518fbba822cd8f46589ca61ccec")
    version("4.1.0", sha256="145f05a6c621bfb3fc434776b615d7e6d53260cc9ba340a01f55b383e07c842e")
    version("3.2.3", sha256="9b835f23c2f94a193c14012ee68b3657a61c568598cdd1212a3716b32d41a135")
    version("3.2.2", sha256="7e7fafe2b338dab42a94002d99330a5bb0ebbdd06381ec65953a87c94db3dd23")
    version("3.2.1", sha256="7e5db8ada5828cf85c12f70db6bfcf777d13e5c4c73b2206bb5e394d47066a2b")
    version("3.1.6", sha256="3df0e0cb0cae67b59edba1d90f55d73467be8404874fe89056690739e039a840")
    version("3.1.5", sha256="88934195174455df478b996313095df25b51d0caf5a5cce01b22f0ccdc6c5cf7")
    version("3.1.3", sha256="118acb9c4e10c4e481406dcffdfa762f314af50db75336bf8460e53b56dc439d")
    version("3.1.2", sha256="28aed0392d4ca2cdfbdd721e6210c94dadc9830677fea37a0abe9d592c00f9c3")
    version("3.0.2", sha256="df68f35a3ed9517eeade80b13855cebad8fde2772b36a3f6be87559b6d430670")
    version("3.0.1", sha256="b81055d2c0d61ef5a451b63debc39c820bcd530490e2e4dcb4cdbacb618c157c")
    version("3.0.0", sha256="ee8f68107c24b706237a53333d832445315ae37de6773c5413d7fda415a6e2ee")
    version("2.2.3", sha256="6fa5d45eb089e29101190c645e986342a24a03a4ea3a936db0b120aafa45b1f0")
    version("2.2.2", sha256="cd951dbda623fadc5b32ae149d8cc41f9462eac4d718d089340911b1a7c20714")
    version("2.1.4", sha256="eb72d292e76e200f02cf162a477eecea2559ef3ac2edf50ee95b3fe3983d033e")
    version("2.1.3", sha256="281283133498e7e5999ed5c6557542c22408bc9eb51ecbcf7696160616782a41")
    version("2.1.2", sha256="94bb9c801c51a6caa1b8cef2b85ecf67703a5dfa4d79262e6668c37c744bb643")
    version("2.0.1", sha256="ba6e0f32936b1859741adb221e18b2c1ee7dc53a6b374b9f7831adf1692b15fd")
    version("1.2.5", sha256="a2b02d489ee730c06ee40e7f9ffcebb6c35bcb4f95153fab7c4276a3add6ae31")

    variant(
        "pmi_backwards_compatibility",
        default=True,
        description="Toggle pmi backwards compatibility",
    )

    variant(
        "restful",
        default=False,
        when="@4:",
        description="allow a PMIx server to request services from " "a system-level REST server",
    )

    variant("python", default=False, when="@4.1.2:", description="Enable python bindigs")

    variant("docs", default=False, description="Build manpages")

    depends_on("m4", type="build", when="@master")
    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@master")
    depends_on("perl", type="build", when="@master")
    depends_on("pandoc", type="build", when="+docs")
    depends_on("pkgconfig", type="build")

    depends_on("libevent@2.0.20:")
    depends_on("hwloc@1.0:1", when="@:2")
    depends_on("hwloc@1.11:1,2:", when="@3:")
    depends_on("curl", when="+restful")
    depends_on("jansson@2.11:", when="+restful")
    depends_on("python", when="+python")
    depends_on("py-cython", when="+python")

    def autoreconf(self, spec, prefix):
        """Only needed when building from git checkout"""
        # If configure exists nothing needs to be done
        if os.path.exists(self.configure_abs_path):
            return
        # Else bootstrap with autotools
        perl = which("perl")
        perl("./autogen.pl")

    def find_external_lib_path(self, pkg_name, path_match_str=""):
        spec = self.spec
        tgt_libpath = ""
        dir_list = spec[pkg_name].libs
        for entry in dir_list:
            if path_match_str == "" or (path_match_str != "" and path_match_str in entry):
                tgt_libpath = entry
                break
        path_list = tgt_libpath.split(os.sep)
        del path_list[-1]
        return (os.sep).join(path_list)

    def configure_args(self):
        spec = self.spec

        config_args = ["--enable-shared", "--enable-static", "--disable-sphinx", "--without-munge"]

        config_args.append("--with-libevent=" + spec["libevent"].prefix)
        config_args.append("--with-hwloc=" + spec["hwloc"].prefix)

        # As of 09/22/22 pmix build does not detect the hwloc version
        # for 32-bit architecture correctly. Since, we have only been
        # able to test on 64-bit architecture, we are keeping this
        # check for "64" in place. We will need to re-visit this when we
        # have the fix in Pmix for 32-bit library version detection
        if "64" in platform.machine():
            if spec["libevent"].external_path:
                dep_libpath = self.find_external_lib_path("libevent", "64")
                config_args.append("--with-libevent-libdir=" + dep_libpath)
            if spec["hwloc"].external_path:
                dep_libpath = self.find_external_lib_path("hwloc", "64")
                config_args.append("--with-hwloc-libdir=" + dep_libpath)

        config_args.extend(self.enable_or_disable("python-bindings", variant="python"))

        config_args.extend(
            self.enable_or_disable(
                "pmi-backward-compatibility", variant="pmi_backwards_compatibility"
            )
        )

        if "~docs" in self.spec:
            config_args.append("--disable-man-pages")

        # Versions < 2.1.1 have a bug in the test code that *sometimes*
        # causes problems on strict alignment architectures such as
        # aarch64.  Work-around is to just not build the test code.
        if spec.satisfies("@:2.1.0 target=aarch64:"):
            config_args.append("--without-tests-examples")

        return config_args
