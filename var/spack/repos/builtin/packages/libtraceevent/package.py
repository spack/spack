# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libtraceevent(MakefilePackage):
    """Library to parse raw trace event formats."""

    homepage = "https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git"
    url = "https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git/snapshot/libtraceevent-1.7.3.tar.gz"
    git = "https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git"

    maintainers("Jordan474")

    version("1.7.3", sha256="097b72e0d907f3107825fb2edf0188324bf70dc9da360f6efa68dc484ffde541")

    variant("doc", default=False, description="Build documentation")

    depends_on("asciidoc", when="+doc", type="build")
    depends_on("xmlto", when="+doc", type="build")

    def patch(self):
        set_executable("Documentation/install-docs.sh.in")

    @property
    def common_targets(self):
        return [
            "prefix=" + self.prefix,
            "pkgconfig_dir=" + join_path(self.prefix.lib, "pkgconfig"),
        ]

    @property
    def build_targets(self):
        result = self.common_targets + ["all"]
        if "+doc" in self.spec:
            result.append("doc")
        return result

    @property
    def install_targets(self):
        result = self.common_targets + ["install"]
        if "+doc" in self.spec:
            result.append("doc-install")
        return result
