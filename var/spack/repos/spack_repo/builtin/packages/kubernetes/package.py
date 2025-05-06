# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kubernetes(Package):
    """Kubernetes is an open source system for managing containerized
    applications across multiple hosts. It provides basic mechanisms
    for deployment, maintenance, and scaling of applications."""

    homepage = "https://kubernetes.io"
    url = "https://github.com/kubernetes/kubernetes/archive/refs/tags/v1.32.2.tar.gz"

    maintainers("alecbcs")

    license("Apache-2.0")

    version("1.32.3", sha256="b1ed5abe78a626804aadc49ecb8ade6fd33b27ab8c23d43cd59dc86f6462ac09")
    version("1.31.7", sha256="92005ebd010a8d4fe3a532444c4645840e0af486062611a4d9c8d862414c3f56")
    version("1.30.11", sha256="f30e4082b6a554d4a2bfedd8b2308a5e6012287e15bec94f72987f717bab4133")

    with default_args(deprecated=True):
        version(
            "1.32.0", sha256="3793859c53f09ebc92e013ea858b8916cc19d7fe288ec95882dada4e5a075d08"
        )
        version(
            "1.27.2", sha256="c6fcfddd38f877ce49c49318973496f9a16672e83a29874a921242950cd1c5d2"
        )
        version(
            "1.27.1", sha256="3a3f7c6b8cf1d9f03aa67ba2f04669772b1205b89826859f1636062d5f8bec3f"
        )
        version(
            "1.27.0", sha256="536025dba2714ee5e940bb0a6b1df9ca97c244fa5b00236e012776a69121c323"
        )

    depends_on("c", type="build")

    with default_args(type="build"):
        depends_on("bash")
        depends_on("gmake")

        depends_on("go@1.23:", when="@1.32:")
        depends_on("go@1.22:", when="@1.30:")
        depends_on("go@1.21:", when="@1.29:")
        depends_on("go@1.20:", when="@1.27:")

    phases = ["build", "install"]

    def build(self, spec, prefix):
        components = [
            "cmd/kubeadm",
            "cmd/kubelet",
            "cmd/kube-apiserver",
            "cmd/kube-controller-manager",
            "cmd/kube-proxy",
            "cmd/kube-scheduler",
        ]

        make(f"WHAT={' '.join(components)}")

    def install(self, spec, prefix):
        install_tree("_output/bin", prefix.bin)
