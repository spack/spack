# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nb(Package):
    """
    CLI and local web plain text note‑taking, bookmarking, and archiving with
    linking, tagging, filtering, search, Git versioning & syncing, Pandoc
    conversion, + more, in a single portable script.
    """

    homepage = "https://xwmx.github.io/nb/"
    url = "https://github.com/xwmx/nb/archive/refs/tags/7.12.1.tar.gz"

    maintainers("taliaferro")

    license("AGPL-3.0", checked_by="taliaferro")

    version("7.12.1", sha256="c9b30448751dd726469ed3fde29e618c5747eb4a16ceaaf86d773989a6cf13f3")

    depends_on("bash")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("nb", prefix.bin)
