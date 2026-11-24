# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SbomGit(Package):
    """Has only git versions, and a url_for_version that fails on non-numeric versions."""

    homepage = "https://example.com/sbom-git"
    git = "https://github.com/example/sbom-git.git"

    version("main", branch="main")
    version("1.0", commit="cccccccccccccccccccccccccccccccccccccccc")

    def url_for_version(self, version):
        return "https://example.com/v%02d-%02d.tar.gz" % (version[0], version[-1])
