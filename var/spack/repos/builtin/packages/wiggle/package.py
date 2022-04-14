# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Wiggle(MakefilePackage):
    """Word-wise heuristic diff and merge tool to apply rejected patches and perform
    word-wise diffs
    """

    homepage = "http://neil.brown.name/wiggle"
    url = "https://github.com/neilbrown/wiggle/archive/refs/tags/v1.3.tar.gz"

    maintainers = ["trws"]

    version(
        "1.3", sha256="ff92cf0133c1f4dce33563e263cb30e7ddb6f4abdf86d427b1ec1490bec25afa"
    )
    depends_on("groff")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter(r"^\s*PREFIX\s*=.*", 'PREFIX = "{}"'.format(spec.prefix))
