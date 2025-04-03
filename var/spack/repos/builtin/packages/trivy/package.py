# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Trivy(GoPackage):
    """Trivy is a comprehensive and versatile security scanner."""

    homepage = "https://trivy.dev/"
    url = "https://github.com/aquasecurity/trivy/archive/refs/tags/v0.61.0.tar.gz"

    maintainers("RobertMaaskant")

    license("Apache-2.0", checked_by="RobertMaaskant")

    version("0.61.0", sha256="1e97b1b67a4c3aee9c567534e60355033a58ce43a3705bdf198d7449d53b6979")

    depends_on("go@1.24:", type="build")

    build_directory = "cmd/trivy"

    # Required to correctly set the version
    # https://github.com/aquasecurity/trivy/blob/v0.61.0/goreleaser.yml#L11
    @property
    def build_args(self):
        extra_ldflags = [f"-X 'github.com/aquasecurity/trivy/pkg/version/app.ver=v{self.version}'"]

        args = super().build_args

        if "-ldflags" in args:
            ldflags_index = args.index("-ldflags") + 1
            args[ldflags_index] = args[ldflags_index] + " " + " ".join(extra_ldflags)
        else:
            args.extend(["-ldflags", " ".join(extra_ldflags)])

        return args
