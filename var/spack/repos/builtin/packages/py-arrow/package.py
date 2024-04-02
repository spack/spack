# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArrow(PythonPackage):
    """Arrow is a Python library that offers a sensible and human-friendly
    approach to creating, manipulating, formatting and converting dates,
    times and timestamps. It implements and updates the datetime type,
    plugging gaps in functionality and providing an intelligent module API
    that supports many common creation scenarios. Simply put, it helps you
    work with dates and times with fewer imports and a lot less code."""

    homepage = "https://arrow.readthedocs.io/en/latest/"
    pypi = "arrow/arrow-0.16.0.tar.gz"

    license("Apache-2.0")

    version(
        "1.2.3",
        sha256="5a49ab92e3b7b71d96cd6bfcc4df14efefc9dfa96ea19045815914a6ab6b1fe2",
        url="https://pypi.org/packages/67/67/4bca5a595e2f89bff271724ddb1098e6c9e16f7f3d018d120255e3c30313/arrow-1.2.3-py3-none-any.whl",
    )
    version(
        "1.2.2",
        sha256="d622c46ca681b5b3e3574fcb60a04e5cc81b9625112d5fb2b44220c36c892177",
        url="https://pypi.org/packages/36/e7/3043959c8e3e3d6e346b69417e85daa591f9c018b99c383cc3f316bbf269/arrow-1.2.2-py3-none-any.whl",
    )
    version(
        "1.2.1",
        sha256="6b2914ef3997d1fd7b37a71ce9dd61a6e329d09e1c7b44f4d3099ca4a5c0933e",
        url="https://pypi.org/packages/f4/97/a6b394b0ee6c9a7f645308f3a205c6cfe4fc804aac1bf29e4aebb5cd5a16/arrow-1.2.1-py3-none-any.whl",
    )
    version(
        "0.16.0",
        sha256="98184d8dd3e5d30b96c2df4596526f7de679ccb467f358b82b0f686436f3a6b8",
        url="https://pypi.org/packages/ed/d2/aa994f2d8dd442113c753041761dc0732a35def05538de48f61adb28642a/arrow-0.16.0-py2.py3-none-any.whl",
    )
    version(
        "0.14.7",
        sha256="4bfacea734ead51495dc47df00421ecfd4ca1f2c0fbe58b9a26eaeddedc31caf",
        url="https://pypi.org/packages/b9/26/aff20e20eb4fc8f9cbe60434494b53b8cc327062585517461bfdff76125f/arrow-0.14.7-py2.py3-none-any.whl",
    )
    version(
        "0.14.1",
        sha256="e4c4157d9f5eb7f850ffdcedd0cc1454ff677881deee03434a5705dc19192042",
        url="https://pypi.org/packages/51/4d/e0728a800636654fb9edc1ffde6ff505eec56bf87fdc3a861d8060b64193/arrow-0.14.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-python-dateutil@2.7:", when="@0.16:")
        depends_on("py-python-dateutil", when="@0.14.3:0.15")
        depends_on("py-typing-extensions", when="@1:1.2 ^python@:3.7")
