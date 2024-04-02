# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyWasabi(PythonPackage):
    """wasabi: A lightweight console printing and formatting toolkit."""

    homepage = "https://github.com/explosion/wasabi"
    pypi = "wasabi/wasabi-0.6.0.tar.gz"

    license("MIT")

    version(
        "1.1.2",
        sha256="0a3f933c4bf0ed3f93071132c1b87549733256d6c8de6473c5f7ed2e171b5cf9",
        url="https://pypi.org/packages/8f/69/26cbf0bad11703241cb84d5324d868097f7a8faf2f1888354dac8883f3fc/wasabi-1.1.2-py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="da1f100e0025fe1e50fd67fa5b0b05df902187d5c65c86dc110974ab856d1f05",
        url="https://pypi.org/packages/21/e1/e4e7b754e6be3a79c400eb766fb34924a6d278c43bb828f94233e0124a21/wasabi-0.6.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-colorama@0.4.6:", when="@1: platform=windows ^python@3.7:")
        depends_on("py-typing-extensions@3.7.4.1:4.4", when="@1.1.1: ^python@:3.7")
