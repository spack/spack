# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.autotools import AutotoolsPackage

from spack.package import *


class GitRefCommitDep(AutotoolsPackage):
    """
    tests dependency using commit
    """

    homepage = "https://github.com/dummy/dummy"
    git = "https://github.com/dummy/dummy.git"
    url = git

    version("develop", branch="develop")
    version("main", branch="main")
    version("1.0.0", sha256="a5d504c0d52e2e2721e7e7d86988dec2e290d723ced2307145dedd06aeb6fef2")

    variant("commit-selector", default=False, description="test grabbing a specific commit")

    depends_on(f"git-ref-package commit={'a' * 40}", when="@1.0.0")
    depends_on(f"git-ref-package commit={'b' * 40}", when="@develop")
    depends_on(f"git-ref-package commit={'c' * 40}", when="+commit-selector")
