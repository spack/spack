# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SonamesConsumer(Package):
    """Package detected by its executables, which links to libraries of other packages"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/sonames-consumer-1.0.tar.gz"

    executables = ["^sonames-consumer$"]
    sonames = [r"^libsonames-consumer\.so\.\d+$"]

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    variant("owner", default=True, description="Link to sonames-owner")

    depends_on("sonames-owner", type=("build", "link"), when="+owner")
    depends_on("sonames-owner", type="build", when="~owner")
    depends_on("libraries-owner", type="link")

    @classmethod
    def determine_version(cls, exe):
        return "1.0"
