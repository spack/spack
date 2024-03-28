# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPureEval(PythonPackage):
    """Safely evaluate AST nodes without side effects."""

    homepage = "https://github.com/alexmojaki/pure_eval"
    git = "https://github.com/alexmojaki/pure_eval.git"
    pypi = "pure_eval/pure_eval-0.2.2.tar.gz"

    license("MIT")

    version(
        "0.2.2",
        sha256="01eaab343580944bc56080ebe0a674b39ec44a945e6d09ba7db3cb8cec289350",
        url="https://pypi.org/packages/2b/27/77f9d5684e6bce929f5cfe18d6cfbe5133013c06cb2fbf5933670e60761d/pure_eval-0.2.2-py3-none-any.whl",
    )
