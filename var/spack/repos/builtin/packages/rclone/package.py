# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rclone(Package):
    """Rclone is a command line program to sync files and directories
    to and from various cloud storage providers"""

    homepage = "https://rclone.org"
    url = "https://github.com/rclone/rclone/releases/download/v1.57.0/rclone-v1.57.0.tar.gz"

    maintainers("alecbcs")

    version("1.61.1", sha256="34b5f52047741c7bbf54572c02cc9998489c4736a753af3c99255296b1af125d")
    version("1.59.1", sha256="db3860e4549af28d87aa83f2035a57c5d081b179e40d4c828db19c3c3545831e")
    version("1.58.1", sha256="4d1d50a5b4888aa8eca10624073759ab8376c8b1acb38a238831d40074792524")
    version("1.58.0", sha256="8e0c49fad69525d1219415d2f0651fd243ddf02291fd95e91d2b074d4858c31f")
    version("1.57.0", sha256="3a762c02c202a9142c2d5c1a3927563a556d1683abadd25d2f695e237e4ea693")
    version("1.56.2", sha256="a8813d25c4640e52495fee83e525e76283c63f01d1cce8fbb58d8486b0c20c8a")
    version("1.56.1", sha256="090b4b082caa554812f341ae26ea6758b40338836122595d6283c60c39eb5a97")
    version("1.56.0", sha256="81d2eda23ebaad0a355aab6ff030712470a42505b94c01c9bb5a9ead9168cedb")
    version("1.55.1", sha256="25da7fc5c9269b3897f27b0d946919df595c6dda1b127085fda0fe32aa59d29d")
    version("1.55.0", sha256="75accdaedad3b82edc185dc8824a19a59c30dc6392de7074b6cd98d1dc2c9040")

    # https://nvd.nist.gov/vuln/detail/CVE-2020-28924
    version(
        "1.51.0",
        sha256="3eb5b7ffce17e56fadb29bf854666723a14c93fedc02046c7f34c792dbd227ee",
        deprecated=True,
    )
    version(
        "1.50.2",
        sha256="6dd8998a72514d3820d241ae46dc609c0305b742aee3db6aaf6017b46c996091",
        deprecated=True,
    )
    version(
        "1.50.1",
        sha256="48d6c80883427469682b4d97099d7631cf3b67aa85e652c254423bd1422ce216",
        deprecated=True,
    )
    version(
        "1.50.0",
        sha256="f901fd1752aae6116d94fd08d010a70d94535257c2d23caa505e631cce1e802a",
        deprecated=True,
    )
    version(
        "1.49.5",
        sha256="abd2c83d71c63a4b0a30b1980b942868e707d05e14ae76ad39abf5cc5a5fde63",
        deprecated=True,
    )
    version(
        "1.49.4",
        sha256="070afc85e4e9921151d7cb67247db8f0ff2f06fcf2652c43a42fa6e1e35847af",
        deprecated=True,
    )
    version(
        "1.43",
        sha256="d30527b00cecb4e5e7188dddb78e5cec62d67cf2422dab82190db58512b5a4e3",
        deprecated=True,
    )

    depends_on("go@1.15:", type="build")

    def setup_build_environment(self, env):
        # Point GOPATH at the top of the staging dir for the build step.
        env.prepend_path("GOPATH", self.stage.path)

    def install(self, spec, prefix):
        go("build")
        mkdirp(prefix.bin)
        install("rclone", prefix.bin)
