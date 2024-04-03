# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKerasApplications(PythonPackage):
    """Sample Deep Learning application in Keras.
    Keras depends on this package to run properly."""

    homepage = "https://keras.io"
    url = "https://github.com/keras-team/keras-applications/archive/1.0.4.tar.gz"

    license("MIT")

    version(
        "1.0.8",
        sha256="df4323692b8c1174af821bf906f1e442e63fa7589bf0f1230a0b6bdc5a810c95",
        url="https://pypi.org/packages/71/e3/19762fdfc62877ae9102edf6342d71b28fbfd9dea3d2f96a882ce099b03f/Keras_Applications-1.0.8-py3-none-any.whl",
    )
    version(
        "1.0.7",
        sha256="94b8acc84fb8b1e3d752e20ed4cafa8377c9ecf6e6c1aa09942d959dc02e439a",
        url="https://pypi.org/packages/90/85/64c82949765cfb246bbdaf5aca2d55f400f792655927a017710a78445def/Keras_Applications-1.0.7-py2.py3-none-any.whl",
    )
    version(
        "1.0.6",
        sha256="721dda4fa4e043e5bbd6f52a2996885c4639a7130ae478059b3798d0706f5ae7",
        url="https://pypi.org/packages/3f/c4/2ff40221029f7098d58f8d7fb99b97e8100f3293f9856f0fb5834bef100b/Keras_Applications-1.0.6-py2.py3-none-any.whl",
    )
    version(
        "1.0.4",
        sha256="0ee155e0e07b8a614c92a72bba081264b69ecd91d74c742488054dc89e24b05e",
        url="https://pypi.org/packages/54/90/8f327deaa37a71caddb59b7b4aaa9d4b3e90c0e76f8c2d1572005278ddc5/Keras_Applications-1.0.4-py2.py3-none-any.whl",
    )
    version(
        "1.0.2",
        sha256="9924be748e5d180806d133c714d22895b997ed722757491dd99538851145d3bf",
        url="https://pypi.org/packages/e2/60/c557075e586e968d7a9c314aa38c236b37cb3ee6b37e8d57152b1a5e0b47/Keras_Applications-1.0.2-py2.py3-none-any.whl",
    )
    version(
        "1.0.1",
        sha256="b0e82871d03d82a08648b4f03104c89fe70ffd09563b6a08fbba3ac99e6995df",
        url="https://pypi.org/packages/a6/97/a72fe350476ccc383a8161353520f5d854729ac01c11e2d52980eeaed87a/Keras_Applications-1.0.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-h5py")
        depends_on("py-keras@2.1.6:", when="@:1.0.5")
        depends_on("py-numpy@1.9.1:")
