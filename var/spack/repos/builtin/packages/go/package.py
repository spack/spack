# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from llnl.util import tty

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

    homepage = "https://go.dev"
    url = "https://go.dev/dl/go1.20.2.src.tar.gz"
    git = "https://go.googlesource.com/go.git"

    extendable = True
    executables = ["^go$"]

    maintainers("alecbcs")

    license("BSD-3-Clause")

    version("1.22.1", sha256="79c9b91d7f109515a25fc3ecdaad125d67e6bdb54f6d4d98580f46799caea321")
    version("1.22.0", sha256="4d196c3d41a0d6c1dfc64d04e3cc1f608b0c436bd87b7060ce3e23234e1f4d5c")
    version("1.21.6", sha256="124926a62e45f78daabbaedb9c011d97633186a33c238ffc1e25320c02046248")
    version("1.21.5", sha256="285cbbdf4b6e6e62ed58f370f3f6d8c30825d6e56c5853c66d3c23bcdb09db19")

    # Deprecated Versions
    # https://nvd.nist.gov/vuln/detail/CVE-2023-44487
    version(
        "1.21.3",
        sha256="186f2b6f8c8b704e696821b09ab2041a5c1ee13dcbc3156a13adcf75931ee488",
        deprecated=True,
    )
    # https://nvd.nist.gov/vuln/detail/CVE-2023-39533
    version(
        "1.20.6",
        sha256="62ee5bc6fb55b8bae8f705e0cb8df86d6453626b4ecf93279e2867092e0b7f70",
        deprecated=True,
    )
    # https://nvd.nist.gov/vuln/detail/CVE-2023-29405
    version(
        "1.20.4",
        sha256="9f34ace128764b7a3a4b238b805856cc1b2184304df9e5690825b0710f4202d6",
        deprecated=True,
    )
    version(
        "1.20.3",
        sha256="e447b498cde50215c4f7619e5124b0fc4e25fb5d16ea47271c47f278e7aa763a",
        deprecated=True,
    )
    version(
        "1.19.11",
        sha256="e25c9ab72d811142b7f41ff6da5165fec2d1be5feec3ef2c66bc0bdecb431489",
        deprecated=True,
    )
    version(
        "1.19.9",
        sha256="131190a4697a70c5b1d232df5d3f55a3f9ec0e78e40516196ffb3f09ae6a5744",
        deprecated=True,
    )
    version(
        "1.19.8",
        sha256="1d7a67929dccafeaf8a29e55985bc2b789e0499cb1a17100039f084e3238da2f",
        deprecated=True,
    )
    # https://nvd.nist.gov/vuln/detail/CVE-2023-24538
    version(
        "1.20.2",
        sha256="4d0e2850d197b4ddad3bdb0196300179d095bb3aefd4dfbc3b36702c3728f8ab",
        deprecated=True,
    )
    version(
        "1.19.7",
        sha256="775bdf285ceaba940da8a2fe20122500efd7a0b65dbcee85247854a8d7402633",
        deprecated=True,
    )

    provides("golang")

    depends_on("git", type="run")
    depends_on("go-or-gccgo-bootstrap", type="build")
    depends_on("go-or-gccgo-bootstrap@1.17.13:", type="build", when="@1.20:")
    depends_on("go-or-gccgo-bootstrap@1.20.6:", type="build", when="@1.22:")

    phases = ["build", "install"]

    def url_for_version(self, version):
        return f"https://go.dev/dl/go{version}.src.tar.gz"

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("version", output=str, error=str)
        match = re.search(r"go version go(\S+)", output)
        return match.group(1) if match else None

    def setup_build_environment(self, env):
        env.set("GOROOT_FINAL", self.spec.prefix)
        # We need to set CC/CXX_FOR_TARGET, otherwise cgo will use the
        # internal Spack wrappers and fail.
        env.set("CC_FOR_TARGET", self.compiler.cc)
        env.set("CXX_FOR_TARGET", self.compiler.cxx)
        env.set("GOMAXPROCS", make_jobs)

    def build(self, spec, prefix):
        bash = which("bash")

        with working_dir("src"):
            bash(f"{'all' if self.run_tests else 'make'}.bash")

    def install(self, spec, prefix):
        install_tree(".", prefix)

    def setup_dependent_package(self, module, dependent_spec):
        """Called before go modules' build(), install() methods.

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
