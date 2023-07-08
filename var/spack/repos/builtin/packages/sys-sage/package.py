# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class SysSage(CMakePackage):
    """A library for capturing hadrware topology and attributes of compute systems."""

    homepage = "https://github.com/stepanvanecek/sys-sage"
    url = "https://github.com/stepanvanecek/sys-sage/archive/refs/tags/v0.1.1-alpha.2.tar.gz"
    git = "https://github.com/stepanvanecek/sys-sage.git"

    maintainers("stepanvanecek")

    version("master", branch="master")
    version(
        "0.1.1-alpha.2", sha256="991a77cf37b061a911c8566fd4486f914de4f4c8cdf39112ec8a32903450c178"
    )

    depends_on("cmake@3.21:", type="build")
    depends_on("libxml2@2.9.13:")
