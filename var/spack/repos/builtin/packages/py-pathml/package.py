# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPathml(PythonPackage):
    """An open-source toolkit for computational pathology and machine learning."""

    homepage = "https://github.com/Dana-Farber-AIOS/pathml"
    pypi = "pathml/pathml-2.1.0.tar.gz"

    license("GPL-2.0-or-later")

    version(
        "2.1.0",
        sha256="953848b9c56d01624e20a060cd0a78631304882e1401a11467524deb2cce8863",
        url="https://pypi.org/packages/3f/ae/01734cac44cdadda95d4cbd817dfd15667f23c8daec7aa892171c9a4b3d2/pathml-2.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-anndata@0.7.6:", when="@:1.0.dev,1.0.2:")
        depends_on("py-dask+distributed", when="@:1.0.dev,1.0.2:")
        depends_on("py-h5py", when="@:1.0.dev,1.0.2:")
        depends_on("py-loguru", when="@2.1:")
        depends_on("py-matplotlib", when="@:1.0.dev,1.0.2:")
        depends_on("py-numpy@1.16.4:", when="@:1.0.dev,1.0.2:")
        depends_on("py-opencv-contrib-python", when="@:1.0.dev,1.0.2:")
        depends_on("py-openslide-python", when="@:1.0.dev,1.0.2:")
        depends_on("py-pandas", when="@:1.0.dev,1.0.2:")
        depends_on("py-pip", when="@:1.0.dev,1.0.2:")
        depends_on("py-pydicom", when="@:1.0.dev,1.0.2:")
        depends_on("py-python-bioformats@4.0.0:", when="@2:")
        depends_on("py-scanpy", when="@:1.0.dev,1.0.2:")
        depends_on("py-scikit-image")
        depends_on("py-scikit-learn", when="@:1.0.dev,1.0.2:")
        depends_on("py-scipy", when="@:1.0.dev,1.0.2:")
        depends_on("py-statsmodels", when="@:1.0.dev,1.0.2:")
        depends_on("py-torch", when="@:1.0.dev,1.0.2:")
