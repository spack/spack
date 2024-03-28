# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTensorboardx(PythonPackage):
    """The purpose of this package is to let researchers use
    a simple interface to log events within PyTorch (and
    then show visualization in tensorboard). This package
    currently supports logging scalar, image, audio,
    histogram, text, embedding, and the route of back-propagation."""

    homepage = "https://github.com/lanpa/tensorboardX"
    pypi = "tensorboardx/tensorboardX-1.8.tar.gz"

    license("MIT")

    version(
        "2.6.2.2",
        sha256="160025acbf759ede23fd3526ae9d9bfbfd8b68eb16c38a010ebe326dc6395db8",
        url="https://pypi.org/packages/44/71/f3e7c9b2ab67e28c572ab4e9d5fa3499e0d252650f96d8a3a03e26677f53/tensorboardX-2.6.2.2-py2.py3-none-any.whl",
    )
    version(
        "2.5.1",
        sha256="8808133ccca673cd04076f6f2a85cf2d39bb2d0393a0f20d0f9cbb06d472b57e",
        url="https://pypi.org/packages/96/47/9004f6b182920e921b6937a345019c9317fda4cbfcbeeb2af618b3b7a53e/tensorboardX-2.5.1-py2.py3-none-any.whl",
    )
    version(
        "2.1",
        sha256="2d81c10d9e3225dcd9bb5fb277588610bdf45317603e7682f6953d83b5b38f6a",
        url="https://pypi.org/packages/af/0c/4f41bcd45db376e6fe5c619c01100e9b7531c55791b7244815bac6eac32c/tensorboardX-2.1-py2.py3-none-any.whl",
    )
    version(
        "2.0",
        sha256="8e336103a66b1b97a663057cc13d1db4419f7a12f332b8364386dbf8635031d9",
        url="https://pypi.org/packages/35/f1/5843425495765c8c2dd0784a851a93ef204d314fc87bcc2bbb9f662a3ad1/tensorboardX-2.0-py2.py3-none-any.whl",
    )
    version(
        "1.9",
        sha256="3d6706fc0d0b2d4afbb9ec8bfc2aa9b7c2abff7d4dc3e1cb92cf180c9cfaf1d6",
        url="https://pypi.org/packages/a6/5c/e918d9f190baab8d55bad52840d8091dd5114cc99f03eaa6d72d404503cc/tensorboardX-1.9-py2.py3-none-any.whl",
    )
    version(
        "1.8",
        sha256="f52e59b38b4cdf83384f3fce067bcaf2d2847619f9f533394df0de3b5a71ab8e",
        url="https://pypi.org/packages/c3/12/dcaf67e1312475b26db9e45e7bb6f32b540671a9ee120b3a72d9e09bc517/tensorboardX-1.8-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy", when="@1:")
        depends_on("py-packaging", when="@2.6:")
        depends_on("py-protobuf@3.20.0:", when="@2.6.2.2:")
        depends_on("py-protobuf@3.8.0:3.20.1", when="@2.5.1:2.5")
        depends_on("py-protobuf@3.8.0:", when="@1.9:2.5.0")
        depends_on("py-protobuf@3.2.0:", when="@1.4:1.8")
        depends_on("py-six", when="@1:2.1,2.5:2.5.0")
