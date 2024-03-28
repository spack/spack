# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMultipledispatch(PythonPackage):
    """A relatively sane approach to multiple dispatch in Python."""

    homepage = "https://multiple-dispatch.readthedocs.io/"
    url = "https://github.com/mrocklin/multipledispatch/archive/0.6.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.6.0",
        sha256="407e6d8c5fa27075968ba07c4db3ef5f02bea4e871e959570eeb69ee39a6565b",
        url="https://pypi.org/packages/3d/a3/3638c2232eb513a9f876bb96e2e400f18d2f5bdc2e7abe84194c8bd38c2d/multipledispatch-0.6.0-py2-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-six", when="@0.6:0")
