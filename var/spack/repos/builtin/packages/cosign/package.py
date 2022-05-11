# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.util.package import *


class Cosign(Package):
    """
    Cosign is a go package for container Signing, verification and storage
    in an OCI registry.
    """

    homepage = "https://github.com/sigstore/cosign"
    url      = "https://github.com/sigstore/cosign/archive/refs/tags/v1.3.1.tar.gz"
    git      = "https://github.com/sigstore/cosign.git"

    version('main', branch='main')
    version('1.3.1', sha256='7f7e0af52ee8d795440e66dcc1a7a25783e22d30935f4f957779628b348f38af')

    depends_on("go", type='build')

    def setup_build_environment(self, env):
        # Point GOPATH at the top of the staging dir for the build step.
        env.prepend_path('GOPATH', self.stage.path)

    def install(self, spec, prefix):
        go = which("go")
        go("build", "-o", "cosign", os.path.join("cmd", "cosign", "main.go"))
        mkdirp(prefix.bin)
        install("cosign", prefix.bin)
