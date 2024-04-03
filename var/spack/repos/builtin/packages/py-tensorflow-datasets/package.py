# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTensorflowDatasets(PythonPackage):
    """tensorflow/datasets is a library of datasets ready to use with
    TensorFlow."""

    homepage = "https://github.com/tensorflow/datasets"
    pypi = "tensorflow-datasets/tensorflow-datasets-4.4.0.tar.gz"

    license("Apache-2.0")

    version(
        "4.4.0",
        sha256="b373e7b724a357637d15f29a11bb7bef3dc62bd144defffe5fec1b8b4f6cf580",
        url="https://pypi.org/packages/93/83/85f14bcf27df5ae23502803502f8506eefec18a285fea909aa67dc9b736e/tensorflow_datasets-4.4.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-absl-py")
        depends_on("py-attrs@18:", when="@:4.4")
        depends_on("py-dataclasses", when="@4:4.8.2 ^python@:3.6")
        depends_on("py-dill", when="@:4.8.2")
        depends_on("py-future", when="@:4.4")
        depends_on("py-importlib-resources", when="@4: ^python@:3.8")
        depends_on("py-numpy")
        depends_on("py-promise")
        depends_on("py-protobuf@3.12.2:", when="@4.2:4.8")
        depends_on("py-requests@2.19:")
        depends_on("py-six", when="@:4.8.1")
        depends_on("py-tensorflow-metadata")
        depends_on("py-termcolor")
        depends_on("py-tqdm")
        depends_on("py-typing-extensions", when="@4.1:4.8.2 ^python@:3.7")
