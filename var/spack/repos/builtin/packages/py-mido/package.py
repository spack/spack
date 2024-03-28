# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMido(PythonPackage):
    """Mido is a library for working with MIDI messages and ports. It's
    designed to be as straight forward and Pythonic as possible."""

    homepage = "https://mido.readthedocs.io/"
    url = "https://github.com/mido/mido/archive/1.2.9.tar.gz"

    license("MIT")

    version(
        "1.2.9",
        sha256="fc6364efa028c8405166f63e6a83cbc6c17aaeac2c28680abe64ae48703a89dd",
        url="https://pypi.org/packages/20/0a/81beb587b1ae832ea6a1901dc7c6faa380e8dd154e0a862f0a9f3d2afab9/mido-1.2.9-py2.py3-none-any.whl",
    )
    version(
        "1.2.8",
        sha256="64b9d1595da8f319bff2eb866f9181257d3670a7803f7e38415f22c03a577560",
        url="https://pypi.org/packages/70/37/96da8908dd6b04fec9b3d3931fa38c43d36b6942f206d9586efede105e7d/mido-1.2.8-py2.py3-none-any.whl",
    )
    version(
        "1.2.7",
        sha256="b119c26852417f49656790998e7bf091b29c7d5e2e44fcf6c64eda3a13ebbc40",
        url="https://pypi.org/packages/4e/20/2a94d7d31178d20011ef096ac8cd49b16b02b076663185c260594f96443e/mido-1.2.7-py2.py3-none-any.whl",
    )
    version(
        "1.2.6",
        sha256="6aeb89c7360ae6e0dcb4c9b1b209691e4423c2a81dbcc833949ecd9723a25cdf",
        url="https://pypi.org/packages/10/51/447066f537e05996a4579829b93390a4d85b0e3da90c5fbc34c1e70a37d5/mido-1.2.6-py2.py3-none-any.whl",
    )
