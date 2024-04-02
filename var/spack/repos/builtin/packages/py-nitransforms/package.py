# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNitransforms(PythonPackage):
    """NiTransforms -- Neuroimaging spatial transforms in Python."""

    homepage = "https://github.com/poldracklab/nitransforms"
    pypi = "nitransforms/nitransforms-21.0.0.tar.gz"

    license("MIT")

    version(
        "21.0.0",
        sha256="3341a3ac73b46d358c8ff0b9e241142e4b360b6a4750d718ccad024dfe8be3a6",
        url="https://pypi.org/packages/75/b6/385af347514e7f8d6a21b49ed04b86fb1fe744ccf5d745648ab2555a0ce1/nitransforms-21.0.0-py3-none-any.whl",
    )
    version(
        "20.0.0-rc5",
        sha256="a4c27dabe1e9a5ef19462142dfbfe4354c234492b90f41a32e3a9aa762e1c940",
        url="https://pypi.org/packages/81/6b/f95acf8c69b6b6b5a470bf2c1c80571696b4f81cba65eb5df3bbf6931691/nitransforms-20.0.0rc5-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@20.0.0-rc4:")
        depends_on("py-h5py")
        depends_on("py-nibabel@3.0.0:")
        depends_on("py-numpy", when="@:21.0.0")
        depends_on("py-scipy", when="@:21.0.0")
