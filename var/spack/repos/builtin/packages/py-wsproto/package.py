# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWsproto(PythonPackage):
    """This repository contains a pure-Python implementation of
    a WebSocket protocol stack. It's written from the ground up
    to be embeddable in whatever program you choose to use,
    ensuring that you can communicate via WebSockets, as
    defined in RFC6455, regardless of your programming
    paradigm."""

    homepage = "https://github.com/python-hyper/wsproto/"
    pypi = "wsproto/wsproto-1.0.0.tar.gz"

    license("MIT")

    version(
        "1.0.0",
        sha256="d8345d1808dd599b5ffb352c25a367adb6157e664e140dbecba3f9bc007edb9f",
        url="https://pypi.org/packages/ea/25/0934b1d00f404d75335b144d4396e01998f25db8953bf54b4d6fe65b80ab/wsproto-1.0.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-dataclasses", when="@0.15:1.0 ^python@:3.6")
        depends_on("py-h11@0.9:", when="@1:")
