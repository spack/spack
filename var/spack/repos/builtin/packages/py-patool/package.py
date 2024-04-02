# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPatool(PythonPackage):
    """portable archive file manager"""

    homepage = "https://wummel.github.io/patool/"
    pypi = "patool/patool-1.12.tar.gz"

    license("GPL-3.0-or-later")

    version(
        "1.12",
        sha256="3f642549c9a78f5b8bef1af92df385b521d360520d1f34e4dba3fd1dee2a21bc",
        url="https://pypi.org/packages/43/94/52243ddff508780dd2d8110964320ab4851134a55ab102285b46e740f76a/patool-1.12-py2.py3-none-any.whl",
    )
