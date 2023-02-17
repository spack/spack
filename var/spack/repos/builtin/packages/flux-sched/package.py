# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.util.executable
from spack.package import *


class FluxSched(AutotoolsPackage):
    """A scheduler for flux-core (pre-alpha)"""

    homepage = "https://github.com/flux-framework/flux-sched"
    url = "https://github.com/flux-framework/flux-sched/releases/download/v0.5.0/flux-sched-0.5.0.tar.gz"
    git = "https://github.com/flux-framework/flux-sched.git"
    tags = ["radiuss", "e4s"]

    maintainers("grondo")

    version("master", branch="master")
    version("0.26.0", sha256="184faec800cf45952ef79bda113f710bf91a05be584034d36a3234627d4a54c7")
    version("0.25.0", sha256="a984b238d8b6968ef51f1948a550bf57887bf3da8002dcd1734ce26afc4bff07")
    version("0.24.0", sha256="e104eb740e94f26a6a690f1c299bbe643f88751cc14a2596f0779a19cfeb5e6f")
    version("0.23.0", sha256="159b62cc4d25ef3d5da5338511ff38449a893d8adca13383cda7b322295acc1c")
    version("0.22.0", sha256="33cab21b667eeccd5665c5f139293b7b3e17cd3847e5fb2633c0dbacb33c611f")
    version("0.21.1", sha256="4dbe8a2e06a816535ef43f34cec960c1e4108932438cd6dbb1d0040423f4477d")
    version("0.21.0", sha256="156fe5b078a7c0b2075a1f1925ec9303a608c846c93187272f52c23eea24e06d")
    version("0.20.0", sha256="1d2074e1458ba1e7a1d4c33341b9f09769559cd1b8c68edc32097e220c4240b8")
    version("0.19.0", sha256="8dffa8eaec95a81286f621639ef851c52dc4c562d365971233bbd91100c31ed2")
    version("0.18.0", sha256="a4d8a6444fdb7b857b26f47fdea57992b486c9522f4ff92d5a6f547d95b586ae")
    version("0.17.0", sha256="5acfcb757e2294a92eaa91be58ba9b42736b88b42d2937de4a78f4642b1c4933")
    version("0.16.0", sha256="08313976161c141b9b34e2d44d5a08d1b11302e22d60aeaf878eef84d4bd2884")
    version("0.15.0", sha256="ff24d26997f91af415f98734b8117291f5a5001e86dac865b56b3d72980c80c8")
    version("0.14.0", sha256="2808f42032b917823d69cd26103c9238694416e2f30c6d39c11c670927ed232a")
    version("0.13.0", sha256="ba17fc0451239fe31a1524b6a270741873f59a5057514d2524fd3e9215c47a82")
    version("0.12.0", sha256="b41ecaebba254abfb5a7995fd9100bd45a59d4ad0a79bdca8b3db02785d97b1d")
    version("0.11.0", sha256="6a0e3c0678f85da8724e5399b02be9686311c835617f6036235ef54b489cc336")
    version("0.10.0", sha256="5944927774709b5f52ddf64a0e825d9b0f24c9dea890b5504b87a8576d217cf6")
    version("0.9.0", sha256="0e1eb408a937c2843bdaaed915d4d7e2ea763b98c31e7b849a96a74758d66a21")
    version("0.8.0", sha256="45bc3cefb453d19c0cb289f03692fba600a39045846568d258e4b896ca19ca0d")

    # Avoid the infinite symlink issue
    # This workaround is documented in PR #3543
    build_directory = "spack-build"

    variant("cuda", default=False, description="Build dependencies with support for CUDA")

    # Needs to be seen if tis is needed once we remove the default variants
    depends_on(
        "boost+exception+filesystem+system+serialization+graph+container+regex@1.53.0,1.59.0: "
    )
    depends_on("py-pyyaml@3.10:", type=("build", "run"))
    depends_on("py-jsonschema@2.3:", type=("build", "run"))
    depends_on("libedit")
    depends_on("libxml2@2.9.1:")
    # pin yaml-cpp to 0.6.3 due to issue #886
    # https://github.com/flux-framework/flux-sched/issues/886
    depends_on("yaml-cpp@0.6.3")
    depends_on("uuid")
    depends_on("pkgconfig")

    depends_on("flux-core", type=("build", "link", "run"))
    depends_on("flux-core+cuda", when="+cuda", type=("build", "run", "link"))
    depends_on("flux-core@0.16.0:0.16", when="@0.8.0", type=("build", "run", "link"))
    depends_on("flux-core@0.22.0", when="@0.14.0", type=("build", "run", "link"))
    depends_on("flux-core@0.23.0:0.25", when="@0.15.0", type=("build", "run", "link"))
    depends_on("flux-core@0.26.0:", when="@0.16.0", type=("build", "run", "link"))
    depends_on("flux-core@0.28.0:", when="@0.17.0", type=("build", "run", "link"))
    depends_on("flux-core@0.29.0:", when="@0.18.0", type=("build", "run", "link"))
    depends_on("flux-core@0.30.0:", when="@0.19.0", type=("build", "run", "link"))
    depends_on("flux-core@0.31.0:", when="@0.19.0", type=("build", "run", "link"))
    depends_on("flux-core@0.38.0:", when="@0.21.0", type=("build", "run", "link"))
    depends_on("flux-core@master", when="@master", type=("build", "run", "link"))

    # Need autotools when building on master:
    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@master")

    # Disable t5000-valgrind.t by default due to false positives not yet
    # in the suppressions file. (This patch will be in v0.21.0)
    patch("no-valgrind.patch", when="@:0.20.0")
    patch("jobid-sign-compare-fix.patch", when="@:0.22.0")

    def url_for_version(self, version):
        """
        Flux uses a fork of ZeroMQ's Collective Code Construction Contract
        (https://github.com/flux-framework/rfc/blob/master/spec_1.adoc).
        This model requires a repository fork for every stable release that has
        patch releases.  For example, 0.8.0 and 0.9.0 are both tags within the
        main repository, but 0.8.1 and 0.9.5 would be releases on the v0.8 and
        v0.9 forks, respectively.

        Rather than provide an explicit URL for each patch release, make Spack
        aware of this repo structure.
        """
        if version[-1] == 0:
            url = "https://github.com/flux-framework/flux-sched/releases/download/v{0}/flux-sched-{0}.tar.gz"
        else:
            url = "https://github.com/flux-framework/flux-sched-v{1}/releases/download/v{0}/flux-sched-{0}.tar.gz"
        return url.format(version.up_to(3), version.up_to(2))

    def setup(self):
        pass

    @when("@master")
    def setup(self):
        with working_dir(self.stage.source_path):
            # Allow git-describe to get last tag so flux-version works:
            git = which("git")
            # When using spack develop, this will already be unshallow
            try:
                git("fetch", "--unshallow")
                git("config", "remote.origin.fetch", "+refs/heads/*:refs/remotes/origin/*")
                git("fetch", "origin")
            except spack.util.executable.ProcessError:
                git("fetch")

    def autoreconf(self, spec, prefix):
        self.setup()
        if os.path.exists(self.configure_abs_path):
            return
        # make sure configure doesn't get confused by the staging symlink
        with working_dir(self.configure_directory):
            # Bootstrap with autotools
            bash = which("bash")
            bash("./autogen.sh")

    @when("@:0.20")
    def patch(self):
        """Fix build with clang@13 and gcc@11"""
        filter_file("NULL", "nullptr", "resource/schema/sched_data.hpp")
        filter_file("size_t", "std::size_t", "resource/planner/planner.h")

    def configure_args(self):
        args = []
        if self.spec.satisfies("@0.9.0:"):
            args.append("CXXFLAGS=-Wno-uninitialized")
        if self.spec.satisfies("%clang@12:"):
            args.append("CXXFLAGS=-Wno-defaulted-function-deleted")
        if self.spec.satisfies("%oneapi"):
            args.append("CXXFLAGS=-Wno-tautological-constant-compare")
        # flux-sched's ax_boost is sometimes weird about non-system locations
        # explicitly setting the path guarantees success
        args.append("--with-boost={0}".format(self.spec["boost"].prefix))
        return args

    @property
    def lua_version(self):
        return self.spec["lua"].version.up_to(2)

    @property
    def lua_share_dir(self):
        return os.path.join("share", "lua", str(self.lua_version))

    @property
    def lua_lib_dir(self):
        return os.path.join("lib", "lua", str(self.lua_version))

    def setup_run_environment(self, env):
        env.prepend_path(
            "LUA_PATH", os.path.join(self.spec.prefix, self.lua_share_dir, "?.lua"), separator=";"
        )
        env.prepend_path(
            "LUA_CPATH", os.path.join(self.spec.prefix, self.lua_lib_dir, "?.so"), separator=";"
        )

        env.prepend_path("FLUX_MODULE_PATH", self.prefix.lib.flux.modules)
        env.prepend_path("FLUX_MODULE_PATH", self.prefix.lib.flux.modules.sched)
        env.prepend_path("FLUX_EXEC_PATH", self.prefix.libexec.flux.cmd)
        env.prepend_path("FLUX_RC_EXTRA", self.prefix.etc.flux)
