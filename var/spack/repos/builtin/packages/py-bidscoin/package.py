# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBidscoin(PythonPackage):
    """Converts and organises raw MRI data-sets according to the Brain Imaging
    Data Structure (BIDS)."""

    homepage = "https://github.com/Donders-Institute/bidscoin"
    pypi = "bidscoin/bidscoin-3.7.4.tar.gz"

    license("GPL-3.0-or-later")

    version(
        "4.1.1",
        sha256="ec536dbbf75c2e88a41d15cc22314b674099bdd108c69cab0f7d1036cc0ec9d7",
        url="https://pypi.org/packages/dc/42/1c82fc605b2289f3d1d014c1031010396b1fcc7a6bae373f48fb403cfefb/bidscoin-4.1.1-py3-none-any.whl",
    )
    version(
        "4.0.0",
        sha256="1a4574e13a8dd093c271be8b2158fad6bc32410e4844c6ec6dac6f5e25e7059f",
        url="https://pypi.org/packages/74/dd/5c154e4431e18be016a6971d8a42987572df33c885e7d0298cb2d45dbb88/bidscoin-4.0.0-py3-none-any.whl",
    )
    version(
        "3.7.4",
        sha256="f223493e9752cfed54b66bff811a74906f5069453fb24367e104ed1f22b25187",
        url="https://pypi.org/packages/d0/e6/92e073cf7e02790bcf7634de651ccb376baced68b2501e2a96cf5f314720/bidscoin-3.7.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@3.5:")
        depends_on("py-bids-validator", when="@4:")
        depends_on("py-coloredlogs")
        depends_on("py-matplotlib", when="@3.5:")
        depends_on("py-multiecho@0.25:", when="@3.5:")
        depends_on("py-nibabel")
        depends_on("py-numpy", when="@3.5:")
        depends_on("py-pandas")
        depends_on("py-pydeface", when="@:3.6,4:4.0")
        depends_on("py-pydicom@2.0.0:", when="@3.5:")
        depends_on("py-pyqt5@5.12.1:", when="@:4.0")
        depends_on("py-pyqt6", when="@4.1:")
        depends_on("py-pytest", when="@4:4.0")
        depends_on("py-python-dateutil")
        depends_on("py-ruamel-yaml@0.15.35:", when="@:4.2")
        depends_on("py-tomli@1.1:", when="@4.1: ^python@:3.10")
        depends_on("py-tqdm@4.60:", when="@4:")
        depends_on("py-tqdm", when="@3.7:3")

    # Historical dependencies
