# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPfzy(PythonPackage):
    """Python port of the fzy fuzzy string matching algorithm."""

    homepage = "https://github.com/kazhala/pfzy"
    pypi = "pfzy/pfzy-0.3.4.tar.gz"

    license("MIT")

    version(
        "0.3.4",
        sha256="5f50d5b2b3207fa72e7ec0ef08372ef652685470974a107d0d4999fc5a903a96",
        url="https://pypi.org/packages/8c/d7/8ff98376b1acc4503253b685ea09981697385ce344d4e3935c2af49e044d/pfzy-0.3.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:3")
