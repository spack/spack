# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kubectl(Package):
    """
    Kubectl is a command-line interface for Kubernetes clusters.
    """

    homepage = "https://kubernetes.io"
    url = "https://github.com/kubernetes/kubernetes/archive/refs/tags/v1.27.0.tar.gz"

    maintainers("alecbcs")

    license("Apache-2.0")

    version("1.27.1", sha256="3a3f7c6b8cf1d9f03aa67ba2f04669772b1205b89826859f1636062d5f8bec3f")
    version("1.27.0", sha256="536025dba2714ee5e940bb0a6b1df9ca97c244fa5b00236e012776a69121c323")

    depends_on("bash", type="build")
    depends_on("go", type="build")

    phases = ["build", "install"]

    def build(self, spec, prefix):
        make("-f", "build/root/Makefile", "WHAT=cmd/kubectl")

    def install(self, spec, prefix):
        install_tree("_output/bin", prefix.bin)
