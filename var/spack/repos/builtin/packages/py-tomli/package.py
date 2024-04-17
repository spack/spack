# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTomli(PythonPackage):
    """Tomli is a Python library for parsing TOML.

    Tomli is fully compatible with TOML v1.0.0."""

    homepage = "https://github.com/hukkin/tomli"
    pypi = "tomli/tomli-2.0.1.tar.gz"
    git = "https://github.com/hukkin/tomli.git"

    maintainers("charmoniumq")

    license("MIT")

    version(
        "2.0.1",
        sha256="939de3e7a6161af0c887ef91b7d41a53e7c5a1ca976325f429cb46ea9bc30ecc",
        url="https://pypi.org/packages/97/75/10a9ebee3fd790d20926a90a2547f0bf78f371b2f13aa822c759680ca7b9/tomli-2.0.1-py3-none-any.whl",
    )
    version(
        "1.2.2",
        sha256="f04066f68f5554911363063a30b108d2b5a5b1a010aa8b6132af78489fe3aade",
        url="https://pypi.org/packages/6d/6c/9908d4db66488217c665a9a5744319406e41f3c46fa5929a8886f2fe1090/tomli-1.2.2-py3-none-any.whl",
    )
    version(
        "1.2.1",
        sha256="8dd0e9524d6f386271a36b41dbf6c57d8e32fd96fd22b6584679dc569d20899f",
        url="https://pypi.org/packages/18/47/f7dab5b63b97efa7a715e389291d46246a5999c7b4705c2d147fc879e3b5/tomli-1.2.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@2:")
