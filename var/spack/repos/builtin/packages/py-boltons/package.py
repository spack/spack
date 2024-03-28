# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBoltons(PythonPackage):
    """When they're not builtins, they're boltons.

    Functionality that should be in the standard library. Like builtins,
    but Boltons.

    Otherwise known as, "everyone's util.py," but cleaned up and tested.
    """

    homepage = "https://boltons.readthedocs.io/"
    pypi = "boltons/boltons-16.5.1.tar.gz"

    version(
        "23.0.0",
        sha256="f716a1b57698a5b19062f3146cb5ce3549904028a2f267c2c0cf584eea3ad75b",
        url="https://pypi.org/packages/22/f0/d81d7f6688d25cfb8b8fce60504c3cbf5d5890b9a1d71911047aa89707c2/boltons-23.0.0-py2.py3-none-any.whl",
    )
    version(
        "16.5.1",
        sha256="78a06ba22b79afb8fdb34e92ea2bad79de09657a9d95a28cbda40946330ecb6e",
        url="https://pypi.org/packages/da/98/7aea4ba3e21df0f23244ded8b8c8ff367f7b2d5bcc3f026f5ae267212b8f/boltons-16.5.1-py2.py3-none-any.whl",
    )
