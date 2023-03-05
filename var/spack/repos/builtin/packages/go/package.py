# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

import llnl.util.tty as tty

from spack.package import *

# - vanilla CentOS 7, and possibly other systems, fail a test:
#   TestCloneNEWUSERAndRemapRootDisableSetgroups
#
#   The Fix, discussed here: https://github.com/golang/go/issues/16283
#   is to enable "user_namespace".
#
#   On a Digital Ocean image, this can be achieved by updating
#   `/etc/default/grub` so that the `GRUB_CMDLINE_LINUX` variable
#   includes `user_namespace.enable=1`, re-cooking the grub
#   configuration with `sudo grub2-mkconfig -o /boot/grub2/grub.cfg`,
#   and then rebooting.
#
# - on CentOS 7 systems (and possibly others) you need to have the
#   glibc package installed or various static cgo tests fail.
#


class Go(Package):
    """The golang compiler and build environment"""

    homepage = "https://golang.org"
    url = "https://dl.google.com/go/go1.16.6.src.tar.gz"
    git = "https://go.googlesource.com/go.git"

    extendable = True
    executables = ["^go$"]

    maintainers("alecbcs")

    version("1.20.1", sha256="b5c1a3af52c385a6d1c76aed5361cf26459023980d0320de7658bae3915831a2")
    version("1.20", sha256="3a29ff0421beaf6329292b8a46311c9fbf06c800077ceddef5fb7f8d5b1ace33")

    version("1.19.6", sha256="d7f0013f82e6d7f862cc6cb5c8cdb48eef5f2e239b35baa97e2f1a7466043767")
    version("1.19.5", sha256="8e486e8e85a281fc5ce3f0bedc5b9d2dbf6276d7db0b25d3ec034f313da0375f")
    version("1.19.4", sha256="eda74db4ac494800a3e66ee784e495bfbb9b8e535df924a8b01b1a8028b7f368")

    version("1.18.10", sha256="9cedcca58845df0c9474ae00274c44a95c9dfaefb132fc59921c28c7c106f8e6")
    version("1.18.9", sha256="fbe7f09b96aca3db6faeaf180da8bb632868ec049731e355ff61695197c0e3ea")

    provides("golang")

    depends_on("git", type=("build", "link", "run"))
    depends_on("go-or-gccgo-bootstrap", type="build")
    depends_on("go-or-gccgo-bootstrap@1.17.13:", type="build", when="@1.20:")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("version", output=str, error=str)
        match = re.search(r"go version go(\S+)", output)
        return match.group(1) if match else None

    def install(self, spec, prefix):
        bash = which("bash")

        with working_dir("src"):
            bash("{0}.bash".format("all" if self.run_tests else "make"))

        install_tree(".", prefix)

    def setup_build_environment(self, env):
        env.set("GOROOT_FINAL", self.spec.prefix)
        # We need to set CC/CXX_FOR_TARGET, otherwise cgo will use the
        # internal Spack wrappers and fail.
        env.set("CC_FOR_TARGET", self.compiler.cc)
        env.set("CXX_FOR_TARGET", self.compiler.cxx)
        env.set("GOMAXPROCS", make_jobs)

    def setup_dependent_package(self, module, dependent_spec):
        """Called before go modules' install() methods.

        In most cases, extensions will only need to set GOPATH and use go::

        env['GOPATH'] = self.source_path + ':' + env['GOPATH']
        go('get', '<package>', env=env)
        install_tree('bin', prefix.bin)
        """
        #  Add a go command/compiler for extensions
        module.go = self.spec["go"].command

    def generate_path_components(self, dependent_spec):
        if os.environ.get("GOROOT", False):
            tty.warn("GOROOT is set, this is not recommended")

        # Set to include paths of dependencies
        path_components = [dependent_spec.prefix]
        for d in dependent_spec.traverse():
            if d.package.extends(self.spec):
                path_components.append(d.prefix)
        return ":".join(path_components)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # This *MUST* be first, this is where new code is installed
        env.prepend_path("GOPATH", self.generate_path_components(dependent_spec))

    def setup_dependent_run_environment(self, env, dependent_spec):
        # Allow packages to find this when using module files
        env.prepend_path("GOPATH", self.generate_path_components(dependent_spec))
