# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySingledispatchmethod(PythonPackage):
    """Backport of functools.singledispatchmethod to Python 2.7-3.7."""

    homepage = "https://github.com/ikalnytskyi/singledispatchmethod"
    pypi = "singledispatchmethod/singledispatchmethod-1.0.tar.gz"

    license("MIT")

    version(
        "1.0",
        sha256="ed4a794e701cbe415f0df32b71dbdb96d3a415701795bcfb5ee694f8c12418db",
        url="https://pypi.org/packages/c4/ae/cb1b0901b332754245ce6ce900beef6e6c6a97b42e1e4eb78ab66379a6ba/singledispatchmethod-1.0-py2.py3-none-any.whl",
    )
