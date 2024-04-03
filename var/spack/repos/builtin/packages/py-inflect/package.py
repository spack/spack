# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyInflect(PythonPackage):
    """inflect.py - Correctly generate plurals, singular nouns, ordinals,
    indefinite articles; convert numbers to words."""

    homepage = "https://github.com/jaraco/inflect"
    pypi = "inflect/inflect-5.0.2.tar.gz"

    license("MIT")

    version(
        "6.0.2",
        sha256="182741ec7e9e4c8f7f55b01fa6d80bcd3c4a183d349dfa6d9abbff0a1279e98f",
        url="https://pypi.org/packages/67/e2/bcd7099b31d6a1f7be358f7ef7cf6fc97cc5a66353784fdfa4867e4243fb/inflect-6.0.2-py3-none-any.whl",
    )
    version(
        "5.0.2",
        sha256="f125f678288f4830f0ee4a4f51e088ff869ac44451a5717627a4ed38d734144c",
        url="https://pypi.org/packages/a8/d7/9ee314763935ce36e3023103ea2c689e6026147230037503a7772cdad6c1/inflect-5.0.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@5.4:6.0")
        depends_on("py-pydantic@1.9.1:", when="@6.0.2:6.0.4,6.2:7.0")
