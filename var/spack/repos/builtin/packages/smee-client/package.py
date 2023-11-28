# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.util.executable import ProcessError


class SmeeClient(Package):
    """
    Client and CLI for smee.io, a service that delivers webhooks to your
    local development environment.
    """

    homepage = "https://smee.io"
    url = "https://github.com/probot/smee-client/archive/refs/tags/v1.2.5.tar.gz"

    maintainers("alecbcs")

    license("ISC")

    version("1.2.3", sha256="b9afff843fc7a3c2b5d6659acf45357b5db7a739243b99f6d18a9b110981a328")

    depends_on("node-js", type=("build", "link", "run"))
    depends_on("npm", type="build")
    depends_on("typescript", type="build")

    phases = ["build", "install"]

    def build(self, spec, prefix):
        npm = which("npm", required=True)

        # Allow tsc to fail with typing "errors" which don't affect results
        output = npm("run", "build", output=str, error=str, fail_on_error=False)
        if npm.returncode not in (0, 2):
            raise ProcessError(output)

    def install(self, spec, prefix):
        npm = which("npm", required=True)
        npm("install", "--global", f"--prefix={prefix}")
