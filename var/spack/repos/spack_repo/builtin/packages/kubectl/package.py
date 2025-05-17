# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.go import GoPackage

from spack.package import *


class Kubectl(GoPackage):
    """
    Kubectl is a command-line interface for Kubernetes clusters.
    """

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
            "1.31.1", sha256="83094915698a9c24f93d1ffda3f17804a4024d3b65eabf681e77a62b35137208"
        )
        version(
            "1.31.0", sha256="6679eb90815cc4c3bef6c1b93f7a8451bf3f40d003f45ab57fdc9f8c4e8d4b4f"
        )
        version(
            "1.27.1", sha256="3a3f7c6b8cf1d9f03aa67ba2f04669772b1205b89826859f1636062d5f8bec3f"
        )
        version(
            "1.27.0", sha256="536025dba2714ee5e940bb0a6b1df9ca97c244fa5b00236e012776a69121c323"
        )

    with default_args(type="build"):
        depends_on("bash")

        depends_on("go@1.23:", when="@1.32:")
        depends_on("go@1.22:", when="@1.30:")
        depends_on("go@1.21:", when="@1.29:")
        depends_on("go@1.20:", when="@1.27:")

    build_directory = "cmd/kubectl"

    # Required to correctly set the version
    # Method discovered by following the trail below
    #
    # 1. https://github.com/kubernetes/kubernetes/blob/v1.32.2/Makefile#L1
    # 2. https://github.com/kubernetes/kubernetes/blob/v1.32.2/build/root/Makefile#L97
    # 3. https://github.com/kubernetes/kubernetes/blob/v1.32.2/hack/make-rules/build.sh#L25
    # 4. https://github.com/kubernetes/kubernetes/blob/v1.32.2/hack/lib/init.sh#L61
    # 5. https://github.com/kubernetes/kubernetes/blob/v1.32.2/hack/lib/version.sh#L151-L183
    @property
    def build_args(self):
        kube_ldflags = [
            f"-X 'k8s.io/client-go/pkg/version.gitVersion=v{self.version}'",
            f"-X 'k8s.io/client-go/pkg/version.gitMajor={self.version.up_to(1)}'",
            f"-X 'k8s.io/client-go/pkg/version.gitMinor={str(self.version).split('.')[1]}'",
            f"-X 'k8s.io/component-base/version.gitVersion=v{self.version}'",
            f"-X 'k8s.io/component-base/version.gitMajor={self.version.up_to(1)}'",
            f"-X 'k8s.io/component-base/version.gitMinor={str(self.version).split('.')[1]}'",
        ]

        args = super().build_args

        if "-ldflags" in args:
            ldflags_index = args.index("-ldflags") + 1
            args[ldflags_index] = args[ldflags_index] + " " + " ".join(kube_ldflags)
        else:
            args.extend(["-ldflags", " ".join(kube_ldflags)])

        return args
