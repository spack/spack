# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyShtab(PythonPackage):
    """Automatically generate shell tab completion scripts for python CLI apps."""

    homepage = "https://github.com/iterative/shtab"
    pypi = "shtab/shtab-1.3.3.tar.gz"

    license("Apache-2.0")

    version(
        "1.3.4",
        sha256="aa392d1cdfa9dfd047887bed1be0bd0c99cba77851848a36bc175093e582a462",
        url="https://pypi.org/packages/e4/10/54846a1cd8c2291d2afd1f4c56ddcf090e36a9e014387ec655577f669983/shtab-1.3.4-py2.py3-none-any.whl",
    )
    version(
        "1.3.3",
        sha256="bfc0dbeccf1106af25e01a366ada3b8c4005da0c62130fafc7da24dfa4c54914",
        url="https://pypi.org/packages/7a/b2/6a1669b94868e9b0856000d3daa8e60eba544668611e61a015799330b76a/shtab-1.3.3-py2.py3-none-any.whl",
    )

    # setuptools and setuptools_scm imported in shtab/__init__.py
