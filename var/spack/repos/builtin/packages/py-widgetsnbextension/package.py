# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWidgetsnbextension(PythonPackage):
    """IPython HTML widgets for Jupyter"""

    pypi = "widgetsnbextension/widgetsnbextension-1.2.6.tar.gz"

    license("BSD-3-Clause")

    version(
        "4.0.3",
        sha256="7f3b0de8fda692d31ef03743b598620e31c2668b835edbd3962d080ccecf31eb",
        url="https://pypi.org/packages/d7/ae/ee70b20dc836d935a9a6483339854c09d8752e55a8104668e2426cf3baf3/widgetsnbextension-4.0.3-py3-none-any.whl",
    )
    version(
        "3.6.0",
        sha256="4fd321cad39fdcf8a8e248a657202d42917ada8e8ed5dd3f60f073e0d54ceabd",
        url="https://pypi.org/packages/4e/69/273f584c28805939c6cb45717638cb8edbd78147f02c564b8c7763e1872e/widgetsnbextension-3.6.0-py2.py3-none-any.whl",
    )
    version(
        "3.5.1",
        sha256="bd314f8ceb488571a5ffea6cc5b9fc6cba0adaf88a9d2386b93a489751938bcd",
        url="https://pypi.org/packages/6c/7b/7ac231c20d2d33c445eaacf8a433f4e22c60677eb9776c7c5262d7ddee2d/widgetsnbextension-3.5.1-py2.py3-none-any.whl",
    )
    version(
        "3.4.2",
        sha256="14b2c65f9940c9a7d3b70adbe713dbd38b5ec69724eebaba034d1036cf3d4740",
        url="https://pypi.org/packages/8a/81/35789a3952afb48238289171728072d26d6e76649ddc8b3588657a2d78c1/widgetsnbextension-3.4.2-py2.py3-none-any.whl",
    )
    version(
        "3.4.0",
        sha256="7e8fc9688d4fb68c96537ce00604cf8d3bbf48bd348f2c4dfb91174c308b1e10",
        url="https://pypi.org/packages/83/03/ed063ec3ecf499d5491734822d8cadfc80f531a41ae1604277b25fbed795/widgetsnbextension-3.4.0-py2.py3-none-any.whl",
    )
    version(
        "3.3.0",
        sha256="af7412053b646a5372278bf772714543acdd6e0ad87f18171ba6a0c9009e3114",
        url="https://pypi.org/packages/b9/43/f6ff09448f7b961e102fd75b7e46a5d44b68b9746bb1ab5c4be64c3e236d/widgetsnbextension-3.3.0-py2.py3-none-any.whl",
    )
    version(
        "1.2.6",
        sha256="d177773d363c643430c7b10c46d655e0eac2615aec653cd99d92330ea0d4505c",
        url="https://pypi.org/packages/42/20/24730ef6a6f52117562e893e829f546fdbff300fd50203fc2d4449c70635/widgetsnbextension-1.2.6-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@4.0.0-beta1:")
        depends_on("py-notebook@4.4.1:", when="@2.0.0-beta18:3.0.0-alpha2,3.0.0-alpha4:3")
