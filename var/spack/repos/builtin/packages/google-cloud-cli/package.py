# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *


class GoogleCloudCli(Package):
    """Create and manage Google Cloud resources and services directly on the command line
    or via scripts using the Google Cloud CLI."""

    homepage = "https://cloud.google.com/cli"

    # https://cloud.google.com/sdk/docs/downloads-versioned-archives
    system = platform.system().lower()
    machine = platform.machine().lower().replace("arm64", "arm").replace("aarch64", "arm")
    ext = "zip" if system == "windows" else "tar.gz"
    if system == "linux":
        if machine == "arm":
            version("426.0.0", sha256="8409b8cc00f0ae8089be97d8a565f4072eada890776345bccb988bcd4d4bb27f")
        elif machine == "x86_64":
            version("426.0.0", sha256="c653a8ac1e48889005fd00e2de580a27be5a3cb46ceccc570146982c4ddf4245")
        elif machine == "x86":
            version("426.0.0", sha256="13e8b75a3ba352bda58e9974ed5779c16a6631e2957ea6e43cf3b11d5da49ae7")
    elif system == "darwin":
        if machine == "arm":
            version("426.0.0", sha256="5228c93f04af2e3eda3cf03c18bcc75a5440c62170fcdcd46e77e4e97452786a")
        elif machine == "x86_64":
            version("426.0.0", sha256="1ac867378e8e6d59aacadfa0a5282b549146cd8bcd971341d047006c6f702c63")
        elif machine == "x86":
            version("426.0.0", sha256="dd95eb5f3ef82825f3e930f538c3964c5ae37e3bf35492e21f5fed3916b980c0")
    elif system == "windows":
        if machine == "arm":
            version("426.0.0", sha256="d45bdb6808ca737b6c14d6ac85f3380ab1037eeb3c641164d5d4fad032d382af")
        elif machine == "x86_64":
            version("426.0.0", sha256="2a5199f04414df36e483c892d0e89cdc9e962266414ce7990cf2b59058b94e9b")
        elif machine == "x86":
            version("426.0.0", sha256="c04c39b6a7c82365f3c4a0d79ed60dbc6c5ce672970a87a70478bb7c55926852")

    depends_on("python", type=("build", "run"))

    def url_for_version(self, version):
        return f"https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-{version}-{self.system}-{self.machine}.{self.ext}"

    def setup_build_environment(self, env):
        # https://cloud.google.com/sdk/gcloud/reference/topic/startup
        env.set("CLOUDSDK_PYTHON", self.spec["python"].command.path)
        # ~70 dependencies with no hints as to what versions are supported, just use bundled deps
        env.set("CLOUDSDK_PYTHON_SITEPACKAGES", 0)

    def setup_run_environment(self, env):
        self.setup_build_environment(env)

    def install(self, spec, prefix):
        # https://cloud.google.com/sdk/docs/install
        installer = Executable(r".\install.bat" if self.system == "windows" else "./install.sh")
        installer(
            "--usage-reporting=false",
            "--screen-reader=false",
            "--command-completion=false",
            "--path-update=false",
            "--quiet",
            "--install-python=false",
            "--no-compile-python",
        )

        install_tree("bin", prefix.bin)
        install_tree("lib", prefix.lib)
