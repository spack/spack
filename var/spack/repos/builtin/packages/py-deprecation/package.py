# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDeprecation(PythonPackage):
    """The deprecation library provides a deprecated decorator and a
    fail_if_not_removed decorator for your tests."""

    homepage = "https://deprecation.readthedocs.io/"
    pypi = "deprecation/deprecation-2.0.7.tar.gz"

    license("Apache-2.0")

    version(
        "2.1.0",
        sha256="a10811591210e1fb0e768a8c25517cabeabcba6f0bf96564f8ff45189f90b14a",
        url="https://pypi.org/packages/02/c3/253a89ee03fc9b9682f1541728eb66db7db22148cd94f89ab22528cd1e1b/deprecation-2.1.0-py2.py3-none-any.whl",
    )
    version(
        "2.0.7",
        sha256="dc9b4f252b7aca8165ce2764a71da92a653b5ffbf7a389461d7a640f6536ecb2",
        url="https://pypi.org/packages/b9/2a/d5084a8781398cea745c01237b95d9762c382697c63760a95cc6a814ad3a/deprecation-2.0.7-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-packaging", when="@2.0.1:")
