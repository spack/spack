# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPika(PythonPackage):
    """Pika is a RabbitMQ (AMQP 0-9-1) client library for Python."""

    homepage = "https://pika.readthedocs.io/"
    git = "https://github.com/pika/pika.git"
    pypi = "pika/pika-1.3.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.3.2",
        sha256="0779a7c1fafd805672796085560d290213a465e4f6f76a6fb19e378d8041a14f",
        url="https://pypi.org/packages/f9/f3/f412836ec714d36f0f4ab581b84c491e3f42c6b5b97a6c6ed1817f3c16d0/pika-1.3.2-py3-none-any.whl",
    )
    version(
        "1.3.1",
        sha256="89f5e606646caebe3c00cbdbc4c2c609834adde45d7507311807b5775edac8e0",
        url="https://pypi.org/packages/c9/4f/6abbb34a39352f40c66974e3ec4db7c79ef9b8bef06d7d3c9e0f3c6e039c/pika-1.3.1-py3-none-any.whl",
    )
    version(
        "1.3.0",
        sha256="9195f37aed089862b205fd8f8ce1cc6ea0a7ee3cd80f58e6eea6cb9d8411a647",
        url="https://pypi.org/packages/c8/d9/e44e4aa49f1bef15efc21147cbc032d07177ab300f947d915eafb3283af0/pika-1.3.0-py3-none-any.whl",
    )
    version(
        "1.2.1",
        sha256="fe89e95fb2d8d06fd713eeae2938299941e0ec329db37afca758f5f9458ce169",
        url="https://pypi.org/packages/15/95/274fbb38a153c129cffa394721e6e27b170069bd11d44c565defec73fcdf/pika-1.2.1-py2.py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="59da6701da1aeaf7e5e93bb521cc03129867f6e54b7dd352c4b3ecb2bd7ec624",
        url="https://pypi.org/packages/f5/56/2590c41852df1212426bec3e5e312cba50170e12d083a0fb1e544a52d215/pika-1.2.0-py2.py3-none-any.whl",
    )
    version(
        "1.1.0",
        sha256="4e1a1a6585a41b2341992ec32aadb7a919d649eb82904fd8e4a4e0871c8cf3af",
        url="https://pypi.org/packages/a1/ae/8bedf0e9f1c0c5d046db3a7428a4227fe36ec1b8e25607f3c38ac9bf513c/pika-1.1.0-py2.py3-none-any.whl",
    )
    version(
        "1.0.0",
        sha256="0b4c6cff9d156a3679eca6f71562535b172f54c69961be84d9bb704621319dc3",
        url="https://pypi.org/packages/53/a4/5aff2293e1cdcf5f77447ebdfeaac99b622aef7d1e723cf9a5fe317b077c/pika-1.0.0-py2.py3-none-any.whl",
    )
    version(
        "0.13.1",
        sha256="b785e0d5f74a94781bd7d020862eb137d2b56cef2a21475aadbe5bcc8ec4db15",
        url="https://pypi.org/packages/52/cd/452c69f5963ef6dbbe4286e774f3e2e3eae10efd0bb9816c886ebdef3070/pika-0.13.1-py2.py3-none-any.whl",
    )
    version(
        "0.13.0",
        sha256="847916ada527ee064025c1a0b981dc6856ea333734e695012006c24cab233bca",
        url="https://pypi.org/packages/5e/8a/1a805c24c024d7715b006d1089e3552559f6752fe5399151746b880fab69/pika-0.13.0-py2.py3-none-any.whl",
    )

    variant("gevent", default=False, description="Build with gevent support")
    variant("tornado", default=False, description="Build with tornado support")
    variant("twisted", default=False, description="Build with twisted support")

    with default_args(type="run"):
        depends_on("python@3.7:", when="@1.3.2:")
        depends_on("py-gevent", when="@1.2:+gevent")
        depends_on("py-tornado", when="@0.12:+tornado")
        depends_on("py-twisted", when="@0.12:+twisted")
