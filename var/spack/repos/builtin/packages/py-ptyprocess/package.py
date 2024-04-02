# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPtyprocess(PythonPackage):
    """Run a subprocess in a pseudo terminal"""

    pypi = "ptyprocess/ptyprocess-0.5.1.tar.gz"

    license("ISC")

    version(
        "0.7.0",
        sha256="4b41f3967fce3af57cc7e94b888626c18bf37a083e3651ca8feeb66d492fef35",
        url="https://pypi.org/packages/22/a6/858897256d0deac81a172289110f31629fc4cee19b6f01283303e18c8db3/ptyprocess-0.7.0-py2.py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="d7cc528d76e76342423ca640335bd3633420dc1366f258cb31d05e865ef5ca1f",
        url="https://pypi.org/packages/d1/29/605c2cc68a9992d18dada28206eeada56ea4bd07a239669da41674648b6f/ptyprocess-0.6.0-py2.py3-none-any.whl",
    )
    version(
        "0.5.1",
        sha256="464cb76f7a7122743dd25507650db89cd447c51f38e4671602b3eaa2e38e05ae",
        url="https://pypi.org/packages/40/a5/184b46a3c986000196abd077166b2536acb2500009bec95feb9b8fc19828/ptyprocess-0.5.1-py2.py3-none-any.whl",
    )
