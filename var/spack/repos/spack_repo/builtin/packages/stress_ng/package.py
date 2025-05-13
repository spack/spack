# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class StressNg(MakefilePackage):
    """stress-ng will stress test a computer system in various
    selectable ways. It was designed to exercise various physical
    subsystems of a computer as well as the various operating system
    kernel interfaces."""

    homepage = "https://github.com/ColinIanKing/stress-ng"
    url = "https://github.com/ColinIanKing/stress-ng/archive/refs/tags/V0.19.00.tar.gz"

    license("GPL-2.0-or-later")

    version("0.19.00", sha256="7d0be69dcdad655145026f499863de01d317e87ff87acd48c3343d451540d172")

    depends_on("libaio")
    depends_on("libbsd")
    depends_on("judy")
    depends_on("libatomic-ops")
    depends_on("zlib-api")
    depends_on("keyutils")
    depends_on("libgcrypt")
    depends_on("libcap")

    conflicts("platform=darwin", msg="stress-ng is linux-only")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdirp(prefix.man.man1)
        mkdirp(join_path(prefix.share, "stress-ng", "example-jobs"))
        mkdirp(join_path(prefix.share, "bash-completion", "completions"))
        install("stress-ng", prefix.bin)
        install("stress-ng.1", prefix.man.man1)
        install_tree("example-jobs", join_path(prefix.share, "stress-ng"))
        install(
            "bash-completion/stress-ng", join_path(prefix.share, "bash-completion", "completions")
        )
