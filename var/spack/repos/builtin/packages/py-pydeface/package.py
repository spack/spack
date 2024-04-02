# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydeface(PythonPackage):
    """A script to remove facial structure from MRI images."""

    homepage = "http://poldracklab.org/"
    pypi = "pydeface/pydeface-2.0.2.tar.gz"
    git = "https://github.com/poldracklab/pydeface"

    license("MIT")

    version(
        "2.0.2",
        sha256="beb838c4246b8c5798fdc3a331f3064d4aac1bcd1ac9c26b991c9f28207d059e",
        url="https://pypi.org/packages/81/78/257fe9f0715883bbecc2a68e3d965272956c292d0981d717665da69f4efd/pydeface-2.0.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-nibabel", when="@2.0.2:")
        depends_on("py-nipype", when="@2.0.2:")
        depends_on("py-numpy", when="@2.0.2:")
        depends_on("py-setuptools", when="@2.0.2:")
