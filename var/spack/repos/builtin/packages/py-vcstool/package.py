# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyVcstool(PythonPackage):
    """vcstool enables batch commands on multiple different vcs repositories.

    Currently it supports git, hg, svn and bzr."""

    homepage = "https://github.com/dirk-thomas/vcstool"
    pypi = "vcstool/vcstool-0.2.15.tar.gz"

    version(
        "0.2.15",
        sha256="1bbdb817fd45da6ca67480a08fbfc8e791ec6c95b1de5f6ac126d84129648e13",
        url="https://pypi.org/packages/86/ad/01fcd69b32933321858fc5c7cf6ec1fa29daa8942d37849637a8c87c7def/vcstool-0.2.15-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pyyaml")
        depends_on("py-setuptools")
