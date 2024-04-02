# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFastai(PythonPackage):
    """You can use fastai without any installation by using
    Google Colab. In fact, every page of this documentation is
    also available as an interactive notebook - click "Open in
    colab" at the top of any page to open it (be sure to change
    the Colab runtime to "GPU" to have it run fast!) See the
    fast.ai documentation on Using Colab for more
    information."""

    homepage = "https://github.com/fastai/fastai/tree/master/"
    pypi = "fastai/fastai-2.5.3.tar.gz"

    license("Apache-2.0")

    version(
        "2.5.3",
        sha256="b6df7ae938a0fc587c89c350c1b3d8afba88f6ca7a722f7d367f95a3683cb5b0",
        url="https://pypi.org/packages/73/9a/661a804675d913535159d8de99e008d730382802dff12a3e990917aaebbb/fastai-2.5.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-fastcore@1.3.22:1.3", when="@2.5.3")
        depends_on("py-fastdownload@0.0.5:", when="@2.5.1:")
        depends_on("py-fastprogress@0.2.4:")
        depends_on("py-matplotlib")
        depends_on("py-packaging")
        depends_on("py-pandas")
        depends_on("py-pillow@6.1:", when="@:2.7.12")
        depends_on("py-pip")
        depends_on("py-pyyaml")
        depends_on("py-requests")
        depends_on("py-scikit-learn")
        depends_on("py-scipy")
        depends_on("py-spacy@:3", when="@2.3.1:")
        depends_on("py-torch@1.7:1.10", when="@2.5.3:2.5.5")
        depends_on("py-torchvision@0.8.2:", when="@2.3.1:2.7.12")
