# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCachetools(PythonPackage):
    """This module provides various memoizing collections and decorators,
    including variants of the Python 3 Standard Library @lru_cache function
    decorator."""

    homepage = "https://github.com/tkem/cachetools"
    pypi = "cachetools/cachetools-3.1.1.tar.gz"

    license("MIT")

    version(
        "5.2.0",
        sha256="f9f17d2aec496a9aa6b76f53e3b614c965223c061982d434d160f930c698a9db",
        url="https://pypi.org/packages/68/aa/5fc646cae6e997c3adf3b0a7e257cda75cff21fcba15354dffd67789b7bb/cachetools-5.2.0-py3-none-any.whl",
    )
    version(
        "4.2.4",
        sha256="92971d3cb7d2a97efff7c7bb1657f21a8f5fb309a37530537c71b1774189f2d1",
        url="https://pypi.org/packages/ea/c1/4740af52db75e6dbdd57fc7e9478439815bbac549c1c05881be27d19a17d/cachetools-4.2.4-py3-none-any.whl",
    )
    version(
        "4.2.2",
        sha256="2cc0b89715337ab6dbba85b5b50effe2b0c74e035d83ee8ed637cf52f12ae001",
        url="https://pypi.org/packages/bf/28/c4f5796c67ad06bb91d98d543a5e01805c1ff065e08871f78e52d2a331ad/cachetools-4.2.2-py3-none-any.whl",
    )
    version(
        "3.1.1",
        sha256="428266a1c0d36dc5aca63a2d7c5942e88c2c898d72139fca0e97fdd2380517ae",
        url="https://pypi.org/packages/2f/a6/30b0a0bef12283e83e58c1d6e7b5aabc7acfc4110df81a4471655d33e704/cachetools-3.1.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:3", when="@5:5.3.0")
        depends_on("python@:3", when="@4")
