# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUproot3Methods(PythonPackage):
    """Pythonic mix-ins for ROOT classes.

    This package is typically used as a dependency for uproot 3.x, to define
    methods on the classes that are automatically generated from ROOT files.
    This includes histograms (TH*) and physics objects like TLorentzVectors.
    The reason it's a separate library is so that we can add physics-specific
    functionality on a shorter timescale than we can update Uproot 3 itself,
    which is purely an I/O package."""

    homepage = "https://github.com/scikit-hep/uproot3-methods"
    pypi = "uproot3-methods/uproot3-methods-0.10.1.tar.gz"

    version(
        "0.10.1",
        sha256="10e4be8dbcabdf3efb5cce185b0b8ede2ed8390e875750649c6f1c277c26d28c",
        url="https://pypi.org/packages/3f/57/598207abeb64bf3e0af3fdc19217e56936b6bebabaac6ee270fb151790ce/uproot3_methods-0.10.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-awkward0")
        depends_on("py-numpy@1.13.1:")
