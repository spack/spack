# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Badfs(Package):
    """Experimental Rust distributed file system with a CXL-oriented data path."""

    homepage = "https://github.com/vickiegpt/badfs"
    git = "https://github.com/vickiegpt/badfs.git"

    license("MIT")

    version("main", branch="main")
    version("2026-05-17", commit="86e99cd6804404d6bef74892ef0c6db3b71b1f5d")

    variant("server", default=True, description="Build and install the badfs-server binary")
    variant("bench", default=False, description="Build and install the badfs-bench binary")
    variant(
        "intercept",
        default=False,
        description="Build and install the BadFS LD_PRELOAD library",
    )

    depends_on("rust@1.70:", type="build")
    depends_on("syscall-intercept", when="+intercept platform=linux target=x86_64:")

    conflicts("~server~bench~intercept", msg="Select at least one BadFS build target.")
    conflicts("+bench", when="platform=darwin", msg="badfs-bench pulls Linux syscall ABI code.")
    conflicts(
        "+intercept",
        when="platform=darwin",
        msg="badfs-intercept is a Linux LD_PRELOAD library.",
    )

    phases = ("build", "install")

    def patch(self):
        filter_file(
            "self.mode & libc::S_IFREG != 0",
            "self.mode & (libc::S_IFREG as u32) != 0",
            "badfs-common/src/metadata/metadata.rs",
            string=True,
        )

    def setup_build_environment(self, env):
        if self.spec.satisfies("+intercept ^syscall-intercept"):
            syscall_intercept_lib = self.spec["syscall-intercept"].prefix.lib
            env.prepend_path("LIBRARY_PATH", syscall_intercept_lib)
            env.append_flags("RUSTFLAGS", "-L native={0}".format(syscall_intercept_lib))
            env.append_flags(
                "RUSTFLAGS",
                "-C link-arg=-Wl,-rpath,{0}".format(syscall_intercept_lib),
            )

    @property
    def selected_cargo_packages(self):
        packages = []
        if "+server" in self.spec:
            packages.append("badfs-server")
        if "+bench" in self.spec:
            packages.append("badfs-bench")
        if "+intercept" in self.spec:
            packages.append("badfs-intercept")
        return packages

    def build(self, spec, prefix):
        cargo = which("cargo")
        cargo_args = ["build", "--release", "--locked"]
        for package in self.selected_cargo_packages:
            cargo_args.extend(["-p", package])
        cargo(*cargo_args)

    def install(self, spec, prefix):
        if "+server" in spec:
            mkdirp(prefix.bin)
            install("target/release/badfs-server", prefix.bin)

        if "+bench" in spec:
            mkdirp(prefix.bin)
            install("target/release/badfs-bench", prefix.bin)

        if "+intercept" in spec:
            mkdirp(prefix.lib)
            self._install_intercept_library(prefix)

        doc_dir = prefix.share.doc.badfs
        mkdirp(doc_dir)
        install("README.md", doc_dir)
        install("LICENSE", doc_dir)

        if os.path.isdir("scripts"):
            install_tree("scripts", prefix.share.badfs.scripts)

    def _install_intercept_library(self, prefix):
        installed = False
        for library in ("libbadfs_intercept.so", "libbadfs_intercept.dylib"):
            path = join_path("target", "release", library)
            if os.path.exists(path):
                install(path, prefix.lib)
                installed = True

        if not installed:
            raise InstallError("badfs-intercept was selected, but no preload library was built.")
