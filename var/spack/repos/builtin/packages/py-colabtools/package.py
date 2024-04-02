# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColabtools(PythonPackage):
    """Tools to work with colab from google."""

    homepage = "https://github.com/zuuuhkrit/colabtools"
    pypi = "colabtools/colabtools-0.0.1.tar.gz"

    license("LGPL-3.0-only")

    version(
        "0.0.1",
        sha256="b80a6be1e4e5193af6c2d2b16f436fec6c67f1a77fabb222b82dcc3befcd516c",
        url="https://pypi.org/packages/bb/29/9088b67e938f38885c1035b36624ed6176c73845152c5ddd603facfa3e24/colabtools-0.0.1-py3-none-any.whl",
    )
