# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDecorator(PythonPackage):
    """The aim of the decorator module it to simplify the usage of decorators
    for the average programmer, and to popularize decorators by showing
    various non-trivial examples."""

    homepage = "https://github.com/micheles/decorator"
    pypi = "decorator/decorator-5.1.0.tar.gz"

    license("BSD-2-Clause")

    version(
        "5.1.1",
        sha256="b8c3f85900b9dc423225913c5aace94729fe1fa9763b38939a95226f02d37186",
        url="https://pypi.org/packages/d5/50/83c593b07763e1161326b3b8c6686f0f4b0f24d5526546bee538c89837d6/decorator-5.1.1-py3-none-any.whl",
    )
    version(
        "5.1.0",
        sha256="7b12e7c3c6ab203a29e157335e9122cb03de9ab7264b137594103fd4a683b374",
        url="https://pypi.org/packages/3d/cc/d7b758e54779f7e465179427de7e78c601d3330d6c411ea7ba9ae2f38102/decorator-5.1.0-py3-none-any.whl",
    )
    version(
        "5.0.9",
        sha256="6e5c199c16f7a9f0e3a61a4a54b3d27e7dad0dbdde92b944426cb20914376323",
        url="https://pypi.org/packages/6a/36/b1b9bfdf28690ae01d9ca0aa5b0d07cb4448ac65fb91dc7e2d094e3d992f/decorator-5.0.9-py3-none-any.whl",
    )
    version(
        "4.4.2",
        sha256="41fa54c2a0cc4ba648be4fd43cff00aedf5b9465c9bf18d64325bc225f08f760",
        url="https://pypi.org/packages/ed/1b/72a1821152d07cf1d8b6fce298aeb06a7eb90f4d6d41acec9861e7cc6df0/decorator-4.4.2-py2.py3-none-any.whl",
    )
    version(
        "4.4.0",
        sha256="f069f3a01830ca754ba5258fde2278454a0b5b79e0d7f5c13b3b97e57d4acff6",
        url="https://pypi.org/packages/5f/88/0075e461560a1e750a0dcbf77f1d9de775028c37a19a346a6c565a257399/decorator-4.4.0-py2.py3-none-any.whl",
    )
    version(
        "4.3.2",
        sha256="cabb249f4710888a2fc0e13e9a16c343d932033718ff62e1e9bc93a9d3a9122b",
        url="https://pypi.org/packages/f1/cd/7c8240007e9716b14679bc217a1baefa4432aa30394f7e2ec40a52b1a708/decorator-4.3.2-py2.py3-none-any.whl",
    )
    version(
        "4.3.0",
        sha256="2c51dff8ef3c447388fe5e4453d24a2bf128d3a4c32af3fabef1f01c6851ab82",
        url="https://pypi.org/packages/bc/bb/a24838832ba35baf52f32ab1a49b906b5f82fb7c76b2f6a7e35e140bac30/decorator-4.3.0-py2.py3-none-any.whl",
    )
    version(
        "4.0.9",
        sha256="f4718552326c99544a6ec602d96b7d03ef61180cf4a492c515ecb2438dd14ccc",
        url="https://pypi.org/packages/7d/ca/493b2377bf42d57bdd985c31975be3d2b500ad9079199cecb7633e8e2cde/decorator-4.0.9-py2.py3-none-any.whl",
    )
