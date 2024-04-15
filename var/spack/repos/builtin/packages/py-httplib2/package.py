# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHttplib2(PythonPackage):
    """A comprehensive HTTP client library."""

    homepage = "https://github.com/httplib2/httplib2"
    pypi = "httplib2/httplib2-0.13.1.tar.gz"

    license("MIT")

    version(
        "0.22.0",
        sha256="14ae0a53c1ba8f3d37e9e27cf37eabb0fb9980f435ba405d546948b009dd64dc",
        url="https://pypi.org/packages/a8/6c/d2fbdaaa5959339d53ba38e94c123e4e84b8fbc4b84beb0e70d7c1608486/httplib2-0.22.0-py3-none-any.whl",
    )
    version(
        "0.20.4",
        sha256="8b6a905cb1c79eefd03f8669fd993c36dc341f7c558f056cb5a33b5c2f458543",
        url="https://pypi.org/packages/59/0f/29725a9caf4b2618f524e0f28e2bda91aca8f880123ec77426ede6ea1ea4/httplib2-0.20.4-py3-none-any.whl",
    )
    version(
        "0.18.0",
        sha256="4f6988e6399a2546b525a037d56da34aed4d149bbdc0e78523018d5606c26e74",
        url="https://pypi.org/packages/cc/f9/2a2c5be40e3d664cc3de70f72a9299fbe4fda5011e6ef1c008cfaef2d302/httplib2-0.18.0-py3-none-any.whl",
    )
    version(
        "0.13.1",
        sha256="cf6f9d5876d796539ec922a2c9b9a7cad9bfd90f04badcdc3bcfa537168052c3",
        url="https://pypi.org/packages/60/55/3902b9f33ad9c15abf447ad91b86ef2d0835a1ae78530f1410c115cf8fe3/httplib2-0.13.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-pyparsing@2.4.2:3.0.0-rc2,3.0.4:", when="@0.20.2:")

    conflicts("^py-pyparsing@3.0.1:3.0.3", when="@0.19:")
