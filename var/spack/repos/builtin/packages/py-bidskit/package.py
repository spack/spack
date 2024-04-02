# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBidskit(PythonPackage):
    """Tools for DICOM to BIDS conversion."""

    homepage = "https://github.com/jmtyszka/bidskit"
    pypi = "bidskit/bidskit-2022.10.13.tar.gz"

    license("MIT")

    version(
        "2023.9.7",
        sha256="26b5ff686cdfb93d78175b962ec6cb7514373161a86d387c39ebd1643f64ab8b",
        url="https://pypi.org/packages/42/36/7fdcfb83024809edf8f2e7240a7e0306c0a44bbbe478bd3eb971da1c1839/bidskit-2023.9.7-py3-none-any.whl",
    )
    version(
        "2023.2.16",
        sha256="10929d293c8f70cf2e6667d54748b73ce1bd61292745a22739c51a4fdce75fec",
        url="https://pypi.org/packages/64/92/72a69f7242b5aeec7e2b035caea123a7e7587a5e4cf8402d37a546f04ccd/bidskit-2023.2.16-py3-none-any.whl",
    )
    version(
        "2022.10.13",
        sha256="42a977c12e2f26b9a329c7dd673603f096776281d8574a24f249f489cf2663ad",
        url="https://pypi.org/packages/8f/36/1d04ee996bae57fc95ac4eab13a4ce96c1135677b4e67d64529646593bee/bidskit-2022.10.13-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:3", when="@:2023")
        depends_on("py-numpy@1.21.0:")
        depends_on("py-pybids@0.15:")
        depends_on("py-pydicom@2.2.0:")

    # version requirement comes from error message when using bidskit
