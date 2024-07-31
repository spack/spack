# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from shutil import copy2

class Linux(MakefilePackage):
# class Linux(Package):
    """Linux is a clone of the operating system Unix and aims towards POSIX and 
    Single UNIX Specification compliance. It has all the features you would expect 
    in a modern fully-fledged Unix, including true multitasking, virtual memory, 
    shared libraries, demand loading, shared copy-on-write executables, proper memory 
    management, and multistack networking including IPv4 and IPv6."""

    homepage = "https://github.com/torvalds/linux"
    url = "https://github.com/fleshling/linux/archive/refs/heads/master.zip"

    maintainers("fleshling", "rountree", "rountree-alt")

    license("GPL-2.0-only", checked_by="fleshling")

    version("6.9.9", sha256="19e8dd54db1e338d59c17102d81edba7a988f9e1c7224c69165a9d442df8aac3")

    # FIXME: Add dependencies if required.
    # depends_on("foo")

    def setup_build_environment(self, env):
        env.set("KBUILD_OUTPUT", self.prefix)

    @run_before("build")
    def copy_kconfig(self):
        name = "kconfig_allconfig"
        try:
            copy2(f"{self.package_dir}/{name}", f"{self.build_directory}/{name}")
        except Exception as e:
            print("exception occured: ", e)

    def build(self, spec, prefix):
        import llnl.util.filesystem as fs
        import inspect
        import sys
        stage_dir = "~"
        #print("word!", file=sys.stdout)
#       self.stage.expand_archive
        print("Staged DIR is:", self.stage.archive_file)
        try:
            import subprocess
            print(f"Self.stage.path: {self.stage.path}")
            subprocess.run(f"cp -rf {self.stage.path} {stage_dir}")
            print("copied")
        except Exception as e:
            print(f"Exception: {e}")
            
        with fs.working_dir(self.build_directory):
            make("KCONFIG_ALLCONFIG=kconfig_allconfig", "allnoconfig")
            make("modules")

    def install(self, spec, prefix):
        install_tree(self.build_directory, self.prefix)
        print("Got to install")
