# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kubectl(Package):
    """
    Kubectl is a command-line interface for Kubernetes clusters.
    """

    homepage = "https://kubernetes.io"
    url = "https://github.com/kubernetes/kubernetes/archive/refs/tags/v1.26.3.tar.gz"

    maintainers("alecbcs")

    version("1.26.3", sha256="e9db7e0a2e8cb40e478564de22530c5e582ae7136558994130b3ae7d8828ab31")

    depends_on("bash", type="build")
    depends_on("go", type="build")

    phases = ["build", "install"]

    def build(self, spec, prefix):
        make("WHAT=cmd/kubectl")

    def install(self, spec, prefix):
        install_tree("_output/bin", prefix.bin)
