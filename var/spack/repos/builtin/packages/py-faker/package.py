# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFaker(PythonPackage):
    """Faker is a Python package that generates fake data for
    you. Whether you need to bootstrap your database, create
    good-looking XML documents, fill-in your persistence to
    stress test it, or anonymize data taken from a production
    service, Faker is for you."""

    homepage = "https://github.com/joke2k/faker"
    pypi = "Faker/Faker-9.8.2.tar.gz"

    license("MIT")

    version(
        "19.13.0",
        sha256="da880a76322db7a879c848a0771e129338e0a680a9f695fd9a3e7a6ac82b45e1",
        url="https://pypi.org/packages/18/d6/314868f573b09d9f0590a2c2f7dd7463153d3dab1049f0ba5e7008776d91/Faker-19.13.0-py3-none-any.whl",
    )
    version(
        "9.8.2",
        sha256="876ba213aaddd661a539ada2158917c1be17064b72792ee788b81c13528865d0",
        url="https://pypi.org/packages/0a/ec/97397fbb5f17c9bb571bab49f939b973ef79729e929449630b0ca771396a/Faker-9.8.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@19:")
        depends_on("py-python-dateutil@2.4:")
        depends_on("py-text-unidecode@1.3:", when="@:11")
        depends_on("py-typing-extensions@3.10.0.1:", when="@15.1.1: ^python@:3.7")
        depends_on("py-typing-extensions@3.10.0.2:", when="@9.5.2:14.1.0 ^python@:3.7")
