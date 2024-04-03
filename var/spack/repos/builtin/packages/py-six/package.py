# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySix(PythonPackage):
    """Python 2 and 3 compatibility utilities."""

    pypi = "six/six-1.11.0.tar.gz"

    license("MIT")

    version(
        "1.16.0",
        sha256="8abb2f1d86890a2dfb989f9a77cfcfd3e47c2a354b01111771326f8aa26e0254",
        url="https://pypi.org/packages/d9/5a/e7c31adbe875f2abbb91bd84cf2dc52d792b5a01506781dbcf25c91daf11/six-1.16.0-py2.py3-none-any.whl",
    )
    version(
        "1.15.0",
        sha256="8b74bedcbbbaca38ff6d7491d76f2b06b3592611af620f8426e82dddb04a5ced",
        url="https://pypi.org/packages/ee/ff/48bde5c0f013094d729fe4b0316ba2a24774b3ff1c52d924a8a4cb04078a/six-1.15.0-py2.py3-none-any.whl",
    )
    version(
        "1.14.0",
        sha256="8f3cd2e254d8f793e7f3d6d9df77b92252b52637291d0f0da013c76ea2724b6c",
        url="https://pypi.org/packages/65/eb/1f97cb97bfc2390a276969c6fae16075da282f5058082d4cb10c6c5c1dba/six-1.14.0-py2.py3-none-any.whl",
    )
    version(
        "1.12.0",
        sha256="3350809f0555b11f552448330d0b52d5f24c91a322ea4a15ef22629740f3761c",
        url="https://pypi.org/packages/73/fb/00a976f728d0d1fecfe898238ce23f502a721c0ac0ecfedb80e0d88c64e9/six-1.12.0-py2.py3-none-any.whl",
    )
    version(
        "1.11.0",
        sha256="832dc0e10feb1aa2c68dcc57dbb658f1c7e65b9b61af69048abc87a2db00a0eb",
        url="https://pypi.org/packages/67/4b/141a581104b1f6397bfa78ac9d43d8ad29a7ca43ea90a2d863fe3056e86a/six-1.11.0-py2.py3-none-any.whl",
    )
    version(
        "1.10.0",
        sha256="0ff78c403d9bccf5a425a6d31a12aa6b47f1c21ca4dc2573a7e2f32a97335eb1",
        url="https://pypi.org/packages/c8/0a/b6723e1bc4c516cb687841499455a8505b44607ab535be01091c0f24f079/six-1.10.0-py2.py3-none-any.whl",
    )
    version(
        "1.9.0",
        sha256="418a93c397a7edab23e5588dbc067ac74a723edb3d541bd4936f79476e7645da",
        url="https://pypi.org/packages/10/e3/a7f8eea80a9fa8358c1cd89ef489bc03675e69e54ed2982cd6f2a28d8295/six-1.9.0-py2.py3-none-any.whl",
    )
    version(
        "1.8.0",
        sha256="facfe0c7cceafd49e8f7e472111294566605fdfddc23011da06cc3a4601c9f7d",
        url="https://pypi.org/packages/a2/4b/2b4532b4eba116a02fc0b5e0b3540a073a61c003b7b6293b7b884afa8ff1/six-1.8.0-py2.py3-none-any.whl",
    )
