# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libvterm(MakefilePackage):
    """An abstract library implementation of a terminal emulator"""

    homepage = "http://www.leonerd.org.uk/code/libvterm/"
    url = "http://www.leonerd.org.uk/code/libvterm/libvterm-0.1.3.tar.gz"

    version("0.3", sha256="61eb0d6628c52bdf02900dfd4468aa86a1a7125228bab8a67328981887483358")
    version("0.2", sha256="4c5150655438cfb8c57e7bd133041140857eb04defd0e544521c0e469258e105")
    version("0.1.4", sha256="bc70349e95559c667672fc8c55b9527d9db9ada0fb80a3beda533418d782d3dd")
    version("0.1.3", sha256="e41724466a4658e0f095e8fc5aeae26026c0726dce98ee71d6920d06f7d78e2b")
    version(
        "0.0.0",
        sha256="6344eca01c02e2270348b79e033c1e0957028dbcd76bc784e8106bea9ec3029d",
        url="http://www.leonerd.org.uk/code/libvterm/libvterm-0+bzr726.tar.gz",
    )

    depends_on("libtool", type="build")

    def setup_build_environment(self, env):
        env.set("LIBTOOL", self.spec["libtool"].prefix.bin.join("libtool"))

    def build(self, spec, prefix):
        make("PREFIX=" + prefix)

    def install(self, spec, prefix):
        make("install", "PREFIX=" + prefix)
