# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Hyperqueue(Package):
    """Scheduler for sub-node tasks for HPC systems with batch scheduling"""

    homepage = "https://it4innovations.github.io/hyperqueue"
    url = "https://github.com/It4innovations/hyperqueue/archive/refs/tags/v0.11.0.tar.gz"
    git = "https://github.com/It4innovations/hyperqueue"

    maintainers = ["Nortamo", "samiilvonen"]

    version("main", branch="main")
    version(
        "0.12.0-rc1", sha256="0c7b5d567bb6cb8dd4e7bafdf784b0379cef74b3aecb958c7f20248f8fedfbc1"
    )
    version("0.11.0", sha256="07fa7eda3a8a5278e058a526fee92e1e524370813b362aaa1a5dfc49d1f3fc28")
    version("0.10.0", sha256="53983b6382123ecd480884b9872a27296739db59e1bb9813b82225841f924790")
    version("0.9.0", sha256="96e743ffac0512a278de9ca3277183536ee8b691a46ff200ec27e28108fef783")

    depends_on("rust@1.59:")

    def install(self, spec, prefix):
        cargo = which("cargo")
        cargo("install", "--root", prefix, "--path", "crates/hyperqueue")
