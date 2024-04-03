# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribWebsupport(PythonPackage):
    """sphinxcontrib-webuspport provides a Python API to easily integrate
    Sphinx documentation into your Web application."""

    homepage = "http://sphinx-doc.org/"
    pypi = "sphinxcontrib-websupport/sphinxcontrib-websupport-1.1.2.tar.gz"

    license("BSD-2-Clause")

    version(
        "1.1.2",
        sha256="e02f717baf02d0b6c3dd62cf81232ffca4c9d5c331e03766982e3ff9f1d2bc3f",
        url="https://pypi.org/packages/2a/59/d64bda9b7480a84a3569be4dde267c0f6675b255ba63b4c8e84469940457/sphinxcontrib_websupport-1.1.2-py2.py3-none-any.whl",
    )
    version(
        "1.1.0",
        sha256="68ca7ff70785cbe1e7bccc71a48b5b6d965d79ca50629606c7861a21b206d9dd",
        url="https://pypi.org/packages/52/69/3c2fbdc3702358c5b34ee25e387b24838597ef099761fc9a42c166796e8f/sphinxcontrib_websupport-1.1.0-py2.py3-none-any.whl",
    )
    version(
        "1.0.1",
        sha256="f4932e95869599b89bf4f80fc3989132d83c9faa5bf633e7b5e0c25dffb75da2",
        url="https://pypi.org/packages/56/0f/3ee19ca5e5a1d9751cf4bbeb372d40a46421c4321fe55a4703ba66d0bafb/sphinxcontrib_websupport-1.0.1-py2.py3-none-any.whl",
    )
