# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re

from spack.package import *


class Fzf(MakefilePackage):
    """fzf is a general-purpose command-line fuzzy finder."""

    homepage = "https://github.com/junegunn/fzf"
    url = "https://github.com/junegunn/fzf/archive/0.17.5.tar.gz"

    maintainers("alecbcs")

    executables = ["^fzf$"]

    version("0.44.1", sha256="295f3aec9519f0cf2dce67a14e94d8a743d82c19520e5671f39c71c9ea04f90c")
    version("0.42.0", sha256="743c1bfc7851b0796ab73c6da7db09d915c2b54c0dd3e8611308985af8ed3df2")
    version("0.41.1", sha256="982682eaac377c8a55ae8d7491fcd0e888d6c13915d01da9ebb6b7c434d7f4b5")
    version("0.40.0", sha256="9597f297a6811d300f619fff5aadab8003adbcc1566199a43886d2ea09109a65")

    depends_on("go@1.17:", type="build")

    variant("vim", default=False, description="Install vim plugins for fzf")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.match(r"(^[\d.]+)", output)
        return match.group(1) if match else None

    def setup_build_environment(self, env):
        # Point GOPATH at the top of the staging dir for the build step.
        env.prepend_path("GOPATH", self.stage.path)

        # Set required environment variables since we
        # are not using git to pull down the repository.
        env.set("FZF_VERSION", self.spec.version)
        env.set("FZF_REVISION", "tarball")

    def install(self, spec, prefix):
        make("install")

        mkdir(prefix.bin)
        install("bin/fzf", prefix.bin)

        mkdirp(prefix.share.fzf.shell)
        install_tree("shell", prefix.share.fzf.shell)

    @run_after("install")
    def post_install(self):
        if "+vim" in self.spec:
            mkdir(self.prefix.plugin)
            install("plugin/fzf.vim", self.prefix.plugin)
