# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJprops(PythonPackage):
    """Java properties file parser for Python"""

    homepage = "https://github.com/mgood/jprops/"
    pypi = "jprops/jprops-2.0.2.tar.gz"

    version(
        "2.0.2",
        sha256="f6be13f0bbc3ca6f7175d74ec8f9f17a4f33a6874473733591c6551d272186a0",
        url="https://pypi.org/packages/d0/57/cb7364a3c3140091de3fffc6b91f7a638c7aeccabeef9b3f6e418a545d5b/jprops-2.0.2-py2.py3-none-any.whl",
    )
