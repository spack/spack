# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyCheapRepr(PythonPackage):
    """This library provides short, fast, configurable string representations,
    and an easy API for registering your own. It's an improvement of the
    standard library module reprlib (repr in Python 2)."""

    pypi = "cheap-repr/cheap_repr-0.5.1.tar.gz"

    license("MIT", checked_by="jmlapre")

    version(
        "0.5.1",
        sha256="30096998aeb49367a4a153988d7a99dce9dc59bbdd4b19740da6b4f3f97cf2ff",
        url="https://pypi.org/packages/9c/77/0e46ad222a3f32f7b84583ea38ec2de117367c91b90e050858ee49c2935a/cheap_repr-0.5.1-py2.py3-none-any.whl",
    )
