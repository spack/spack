# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyHandyArchives(PythonPackage):
    """Some handy archive helpers for Python."""

    homepage = "https://github.com/domdfcoding/handy-archives"
    pypi = "handy_archives/handy_archives-0.2.0.tar.gz"

    license("MIT")

    version(
        "0.2.0",
        sha256="8495e08f3cd1c452fe65570db1869db07f709149f85c7e9cd8f3f461df436318",
        url="https://pypi.org/packages/f9/e5/23451e1cee169259fbc98d2b2ed7b1c3711b707355896c9c3761325ddb01/handy_archives-0.2.0-py3-none-any.whl",
    )
