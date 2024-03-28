# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribNapoleon(PythonPackage):
    """Sphinx "napoleon" extension."""

    homepage = "https://github.com/sphinx-contrib/napoleon"
    pypi = "sphinxcontrib-napoleon/sphinxcontrib-napoleon-0.7.tar.gz"

    license("BSD-2-Clause")

    version(
        "0.7",
        sha256="711e41a3974bdf110a484aec4c1a556799eb0b3f3b897521a018ad7e2db13fef",
        url="https://pypi.org/packages/75/f2/6b7627dfe7b4e418e295e254bb15c3a6455f11f8c0ad0d43113f678049c3/sphinxcontrib_napoleon-0.7-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pockets@0.3:", when="@0.4.4:")
        depends_on("py-six@1.5.2:", when="@0.4.4:")
