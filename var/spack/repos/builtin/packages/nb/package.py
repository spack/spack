# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nb(Package):
    """
    nb is a command line and local web note‑taking, bookmarking, archiving,
    and knowledge base application.
    """

    homepage = "https://xwmx.github.io/nb/"
    url = "https://github.com/xwmx/nb/archive/refs/tags/7.12.1.tar.gz"

    maintainers("taliaferro")

    license("AGPL-3.0", checked_by="taliaferro")

    version("7.12.1", sha256="c9b30448751dd726469ed3fde29e618c5747eb4a16ceaaf86d773989a6cf13f3")

    depends_on("bash")
    depends_on("git")

    def patch(self):
        shebang_regex = "^#!\s?.*bash"
        spack_bash_shebang = "#!{}".format(self.spec["bash"].command.path)
        filter_file(shebang_regex, spack_bash_shebang, "nb")
        filter_file(shebang_regex, spack_bash_shebang, "bin/bookmark")
        filter_file(shebang_regex, spack_bash_shebang, "bin/notes")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("nb", join_path(prefix, "bin/nb"))
        install("bin/notes", join_path(prefix, "bin/notes"))
        install("bin/bookmark", join_path(prefix, "bin/bookmark"))
