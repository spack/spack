# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Unison(MakefilePackage):
    """Unison is a file-synchronization tool for OSX, Unix, and
    Windows. It allows two replicas of a collection of files and
    directories to be stored on different hosts (or different disks
    on the same host), modified separately, and then brought up to
    date by propagating the changes in each replica to the
    other."""

    homepage = "https://www.cis.upenn.edu/~bcpierce/unison/"
    url = "https://github.com/bcpierce00/unison/archive/v2.51.2.tar.gz"
    maintainers("hseara")

    license("GPL-3.0-or-later")

    version("2.53.3", sha256="aaea04fc5bc76dcfe8627683c9659ee4c194d4f992cc8aaa15bbb2820fc8de46")

    depends_on("ocaml@4.10.0:~force-safe-string", type=("build", "link"))

    parallel = False

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("src/unison", prefix.bin)
