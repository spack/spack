# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZipp(PythonPackage):
    """Backport of pathlib-compatible object wrapper for zip files."""

    homepage = "https://github.com/jaraco/zipp"
    pypi = "zipp/zipp-0.6.0.tar.gz"

    license("MIT")

    version(
        "3.17.0",
        sha256="0e923e726174922dce09c53c59ad483ff7bbb8e572e00c7f7c46b88556409f31",
        url="https://pypi.org/packages/d9/66/48866fc6b158c81cc2bfecc04c480f105c6040e8b077bc54c634b4a67926/zipp-3.17.0-py3-none-any.whl",
    )
    version(
        "3.8.1",
        sha256="47c40d7fe183a6f21403a199b3e4192cca5774656965b0a4988ad2f8feb5f009",
        url="https://pypi.org/packages/f0/36/639d6742bcc3ffdce8b85c31d79fcfae7bb04b95f0e5c4c6f8b206a038cc/zipp-3.8.1-py3-none-any.whl",
    )
    version(
        "3.6.0",
        sha256="9fe5ea21568a0a70e50f273397638d39b03353731e6cbbb3fd8502a33fec40bc",
        url="https://pypi.org/packages/bd/df/d4a4974a3e3957fd1c1fa3082366d7fff6e428ddb55f074bf64876f8e8ad/zipp-3.6.0-py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="f06903e9f1f43b12d371004b4ac7b06ab39a44adc747266928ae6debfa7b3335",
        url="https://pypi.org/packages/74/3d/1ee25a26411ba0401b43c6376d2316a71addcc72ef8690b101b4ea56d76a/zipp-0.6.0-py2.py3-none-any.whl",
    )
    version(
        "0.5.1",
        sha256="8c1019c6aad13642199fbe458275ad6a84907634cc9f0989877ccc4a2840139d",
        url="https://pypi.org/packages/a0/0f/9bf71d438d2e9d5fd0e4569ea4d1a2b6f5a524c234c6d221b494298bb4d1/zipp-0.5.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@3.16:")
        depends_on("python@3.7:", when="@3.7:3.15")
        depends_on("py-more-itertools", when="@0.6:1.0,2:2.0")

    # needed for spack bootstrap as spack itself supports python 3.6

    # Historical dependencies
