# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyYapf(PythonPackage):
    """Yet Another Python Formatter"""

    homepage = "https://github.com/google/yapf"
    # base https://pypi.python.org/pypi/cffi
    url = "https://github.com/google/yapf/archive/v0.2.1.tar.gz"

    license("Apache-2.0")

    version(
        "0.30.0",
        sha256="3abf61ba67cf603069710d30acbc88cfe565d907e16ad81429ae90ce9651e0c9",
        url="https://pypi.org/packages/c1/5d/d84677fe852bc5e091739acda444a9b6700ffc6b11a21b00dd244c8caef0/yapf-0.30.0-py2.py3-none-any.whl",
    )
    version(
        "0.29.0",
        sha256="cad8a272c6001b3401de3278238fdc54997b6c2e56baa751788915f879a52fca",
        url="https://pypi.org/packages/7c/21/534d143afd3df9cae9b21674fcc32207cb80cfb3de56b89ef7a37c746cca/yapf-0.29.0-py2.py3-none-any.whl",
    )
    version(
        "0.2.1",
        sha256="6bbc0b79c1e80963345984a4fce6ecb032c94351d03f0c0017855e15dad9be97",
        url="https://pypi.org/packages/4f/b8/05762d7d74de7841dfe1f4d6078d7d10f581c7b0589f247671c16aa3ef8d/yapf-0.2.1-py2.py3-none-any.whl",
    )
