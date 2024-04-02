# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPy(PythonPackage):
    """Library with cross-python path, ini-parsing, io, code, log facilities"""

    homepage = "https://py.readthedocs.io/en/latest/"
    pypi = "py/py-1.8.0.tar.gz"

    license("MIT")

    version(
        "1.11.0",
        sha256="607c53218732647dff4acdfcd50cb62615cedf612e72d1724fb1a0cc6405b378",
        url="https://pypi.org/packages/f6/f0/10642828a8dfb741e5f3fbaac830550a518a775c7fff6f04a007259b0548/py-1.11.0-py2.py3-none-any.whl",
    )
    version(
        "1.9.0",
        sha256="366389d1db726cd2fcfc79732e75410e5fe4d31db13692115529d34069a043c2",
        url="https://pypi.org/packages/68/0f/41a43535b52a81e4f29e420a151032d26f08b62206840c48d14b70e53376/py-1.9.0-py2.py3-none-any.whl",
    )
    version(
        "1.8.2",
        sha256="a673fa23d7000440cc885c17dbd34fafcb7d7a6e230b29f6766400de36a33c44",
        url="https://pypi.org/packages/ae/12/76710702ccf77dab01246ecb55fbe43175131c0738d0be29f3de50d31071/py-1.8.2-py2.py3-none-any.whl",
    )
    version(
        "1.8.0",
        sha256="64f65755aee5b381cea27766a3a147c3f15b9b6b9ac88676de66ba2ae36793fa",
        url="https://pypi.org/packages/76/bc/394ad449851729244a97857ee14d7cba61ddb268dce3db538ba2f2ba1f0f/py-1.8.0-py2.py3-none-any.whl",
    )
    version(
        "1.5.4",
        sha256="e31fb2767eb657cbde86c454f02e99cb846d3cd9d61b318525140214fdc0e98e",
        url="https://pypi.org/packages/f3/bd/83369ff2dee18f22f27d16b78dd651e8939825af5f8b0b83c38729069962/py-1.5.4-py2.py3-none-any.whl",
    )
    version(
        "1.5.3",
        sha256="983f77f3331356039fdd792e9220b7b8ee1aa6bd2b25f567a963ff1de5a64f6a",
        url="https://pypi.org/packages/67/a5/f77982214dd4c8fd104b066f249adea2c49e25e8703d284382eb5e9ab35a/py-1.5.3-py2.py3-none-any.whl",
    )
    version(
        "1.4.33",
        sha256="81b5e37db3cc1052de438375605fb5d3b3e97f950f415f9143f04697c684d7eb",
        url="https://pypi.org/packages/92/8b/ac214296ed28a05efd36e8b55a7820eda62d7028ecf10e5a98afb1982e93/py-1.4.33-py2.py3-none-any.whl",
    )
    version(
        "1.4.31",
        sha256="4a3e4f3000c123835ac39cab5ccc510642153bc47bc1f13e2bbb53039540ae69",
        url="https://pypi.org/packages/19/f2/4b71181a49a4673a12c8f5075b8744c5feb0ed9eba352dd22512d2c04d47/py-1.4.31-py2.py3-none-any.whl",
    )
