# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCtgan(PythonPackage):
    """CTGAN is a collection of Deep Learning based Synthetic
    Data Generators for single table data, which are able to
    learn from real data and generate synthetic clones with
    high fidelity."""

    homepage = "https://github.com/sdv-dev/CTGAN"
    pypi = "ctgan/ctgan-0.5.0.tar.gz"

    license("MIT")

    version(
        "0.5.2",
        sha256="d4001e15d07b43de2bbd78fff2ba0e7f6903686c92888cab3fb19be9f2560d06",
        url="https://pypi.org/packages/53/1d/5e4f6796428a32375eed14b230a07c9f6b26316341a376fd90f2c4bc8fad/ctgan-0.5.2-py2.py3-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="aa53689bb16e1f64cde349d3151d11d8dadf1042d35365c307c89afc88458c7a",
        url="https://pypi.org/packages/b4/ea/fba41f2b0ce20902257daa7263f3deed3c4e03a6c3e7b9f8018dd0574e4c/ctgan-0.5.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3.9", when="@0.5:0.6")
        depends_on("py-numpy@1.20.0:1", when="@0.5:0.6 ^python@3.7:")
        depends_on("py-numpy@1.18.0:1.19", when="@0.5:0.6 ^python@:3.6")
        depends_on("py-packaging@20:21", when="@0.5:0.7.3")
        depends_on("py-pandas@1.1.3:1", when="@0.5:0.6")
        depends_on("py-rdt@1.2:1.2.0.0,1.2.1:", when="@0.5.2:0.6")
        depends_on("py-rdt@0.6.1:0.6.1.0,0.6.2:0", when="@0.5:0.5.0")
        depends_on("py-scikit-learn@0.24.0:", when="@0.5:0.6")
        depends_on("py-torch@1.8:1", when="@0.5:0.6")
        depends_on("py-torchvision@0.9:", when="@0.5:0.6")
