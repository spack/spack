# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class LinuxHeaders(Package):
    """The Linux kernel headers."""

    homepage = "https://www.kernel.org/"
    url = "https://www.kernel.org/pub/linux/kernel/v4.x/linux-4.9.10.tar.xz"
    list_url = "https://www.kernel.org/pub/linux/kernel"
    list_depth = 2

    version("6.5.2", sha256="2027e14057d568ad3ddc100dadf4c8853a49b031270478a61d88f6011572650f")
    version("6.2.8", sha256="fed0ad87d42f83a70ce019ff2800bc30a855e672e72bf6d54a014d98d344f665")
    version("4.9.10", sha256="bd6e05476fd8d9ea4945e11598d87bc97806bbc8d03556abbaaf809707661525")

    def url_for_version(self, version):
        url = "https://www.kernel.org/pub/linux/kernel/v{0}.x/linux-{1}.tar.xz"
        return url.format(version.up_to(1), version)

    def setup_build_environment(self, env):
        # This variable is used in the Makefile. If it is defined on the
        # system, it can break the build if there is no build recipe for
        # that specific ARCH
        env.unset("ARCH")

    def install(self, spec, prefix):
        make("headers")

        src, dst = join_path("usr", "include"), join_path(prefix, "include")

        # This copy_tree + ignore is really poor API design, but the it avoids
        # running make install_headers which depends on rsync.
        copy_tree(
            src, dst, ignore=lambda f: os.path.isfile(join_path(src, f)) and not f.endswith(".h")
        )
