# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCloudpickle(PythonPackage):
    """Extended pickling support for Python objects."""

    homepage = "https://github.com/cloudpipe/cloudpickle"
    pypi = "cloudpickle/cloudpickle-0.5.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "2.2.0",
        sha256="7428798d5926d8fcbfd092d18d01a2a03daf8237d8fcdc8095d256b8490796f0",
        url="https://pypi.org/packages/cf/26/cd6c4177273ee35f7a31245893489c68bc340988f12ca315b392f1f18a93/cloudpickle-2.2.0-py3-none-any.whl",
    )
    version(
        "1.6.0",
        sha256="3a32d0eb0bc6f4d0c57fbc4f3e3780f7a81e6fee0fa935072884d58ae8e1cc7c",
        url="https://pypi.org/packages/e7/e3/898487e5dbeb612054cf2e0c188463acb358167fef749c53c8bb8918cea1/cloudpickle-1.6.0-py3-none-any.whl",
    )
    version(
        "1.2.1",
        sha256="b8ba7e322f2394b9bbbdc1c976e6442c2c02acc784cb9e553cee9186166a6890",
        url="https://pypi.org/packages/09/f4/4a080c349c1680a2086196fcf0286a65931708156f39568ed7051e42ff6a/cloudpickle-1.2.1-py2.py3-none-any.whl",
    )
    version(
        "1.1.1",
        sha256="d119fb6627e65d43541bdf927975a0f2a5d40074a30d691c8585f761d721bf49",
        url="https://pypi.org/packages/24/fb/4f92f8c0f40a0d728b4f3d5ec5ff84353e705d8ff5e3e447620ea98b06bd/cloudpickle-1.1.1-py2.py3-none-any.whl",
    )
    version(
        "0.5.2",
        sha256="604c1cb39c2043ba44f017444dd89b7f82541701dfa8a64f5ae72e6346755c0b",
        url="https://pypi.org/packages/aa/18/514b557c4d8d4ada1f0454ad06c845454ad438fd5c5e0039ba51d6b032fe/cloudpickle-0.5.2-py2.py3-none-any.whl",
    )
