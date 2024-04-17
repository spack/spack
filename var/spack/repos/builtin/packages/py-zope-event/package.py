# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZopeEvent(PythonPackage):
    """Very basic event publishing system."""

    homepage = "https://github.com/zopefoundation/zope.event"
    pypi = "zope.event/zope.event-4.3.0.tar.gz"

    license("ZPL-2.1")

    version(
        "4.6",
        sha256="73d9e3ef750cca14816a9c322c7250b0d7c9dbc337df5d1b807ff8d3d0b9e97c",
        url="https://pypi.org/packages/8b/a8/3ab9648dc08d2ab7543145ec174a2d982d08fb996d50d9a4d3e057da7132/zope.event-4.6-py2.py3-none-any.whl",
    )
    version(
        "4.5.0",
        sha256="2666401939cdaa5f4e0c08cf7f20c9b21423b95e88f4675b1443973bdb080c42",
        url="https://pypi.org/packages/9e/85/b45408c64f3b888976f1d5b37eed8d746b8d5729a66a49ec846fda27d371/zope.event-4.5.0-py2.py3-none-any.whl",
    )
    version(
        "4.3.0",
        sha256="57b5fefd1d92774a7c26d7307b7ad9d0eac2181fd320b2061e69216e2a3b3a07",
        url="https://pypi.org/packages/03/62/bb2d843b59f62bac43d071e2d3543ffc63d35fcc515a5796c759b62de49b/zope.event-4.3.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-setuptools", when="@4.3:")
