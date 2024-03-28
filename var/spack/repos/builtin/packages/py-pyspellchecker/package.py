# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyspellchecker(PythonPackage):
    """Pure python spell checker based on work by Peter Norvig"""

    homepage = "https://github.com/barrust/pyspellchecker"
    pypi = "pyspellchecker/pyspellchecker-0.6.2.tar.gz"

    license("MIT")

    version(
        "0.6.2",
        sha256="218759d4166fd49dee5c0473da99792d9274aca495ded0d9594a0bd75e2831ca",
        url="https://pypi.org/packages/64/c7/435f49c0ac6bec031d1aba4daf94dc21dc08a9db329692cdb77faac51cea/pyspellchecker-0.6.2-py3-none-any.whl",
    )
