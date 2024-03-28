# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGitReview(PythonPackage):
    """git-review is a tool that helps submitting git branches to gerrit"""

    homepage = "https://docs.openstack.org/infra/git-review"
    pypi = "git-review/git-review-1.25.0.tar.gz"

    license("Apache-2.0")

    version(
        "2.1.0",
        sha256="4ecbc01592a2cbfe5585a796fdfbbea16b44e1824621df32ef84ad1947dd8013",
        url="https://pypi.org/packages/d1/9c/3df750308dfbf520c01003cbb08fd5b947c2d0401265820e7b3c3ea1785a/git_review-2.1.0-py3-none-any.whl",
    )
    version(
        "2.0.0",
        sha256="484d1065375158396a431c47a99619cdf60c76968980776dad7b34f8c56896ff",
        url="https://pypi.org/packages/1c/fb/bcbfeca98d00f935bb484408ec199ab997781987ba5200cf8fc6a07ff466/git_review-2.0.0-py3-none-any.whl",
    )
    version(
        "1.28.0",
        sha256="922d556fd1ef405482bf6c45d7e7d69342ab80575b14d296aaba95c8dc459cb8",
        url="https://pypi.org/packages/d9/88/86360bc710b1485ca49c94481b92b5069f859354ec462d8793ec8ed4e45b/git_review-1.28.0-py2.py3-none-any.whl",
    )
    version(
        "1.27.0",
        sha256="a84555aee48197b6357edcff9a52d88c57761fa031a6527b684acfa379b65040",
        url="https://pypi.org/packages/0d/a3/ffb52b2f59904463cc3554456a25e5df66ec12aabcee538bb4b9e07b4333/git_review-1.27.0-py2.py3-none-any.whl",
    )
    version(
        "1.26.0",
        sha256="0856dac9196120cc69b5327a15a42b13af56c12cbab96bad6bc4d8784386846b",
        url="https://pypi.org/packages/f4/6f/acd3142c5aef1e7e7376fe3a55fd2789d439f8559d13a8c5cf4c4c8e5c2b/git_review-1.26.0-py2.py3-none-any.whl",
    )
    version(
        "1.25.0",
        sha256="6402b83f4f4b6966979809df7bb8b39f88881f821384672932fded78ae3a0635",
        url="https://pypi.org/packages/4d/1d/c6a3c01250329711f69d5ebba730e8910ec7e248fe92163fd809627e04a1/git_review-1.25.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-argparse", when="@1.25")
        depends_on("py-requests@1.1:", when="@1.25:")
        depends_on("py-six", when="@1.28:1")

    def setup_run_environment(self, env):
        env.set("PBR_VERSION", str(self.spec.version))
