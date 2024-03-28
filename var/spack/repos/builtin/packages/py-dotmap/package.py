# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDotmap(PythonPackage):
    """`DotMap` is a dot-access `dict` subclass that allows dot access to items."""

    homepage = "https://github.com/drgrib/dotmap"
    pypi = "dotmap/dotmap-1.3.30.tar.gz"

    maintainers("jonas-eschle")
    license("MIT", checked_by="jonas-eschle")

    version(
        "1.3.30",
        sha256="bd9fa15286ea2ad899a4d1dc2445ed85a1ae884a42effb87c89a6ecce71243c6",
        url="https://pypi.org/packages/4d/f9/976d6813c160d6c89196d81e9466dca1503d20e609d8751f3536daf37ec6/dotmap-1.3.30-py3-none-any.whl",
    )
