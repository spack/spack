# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBackportsTempfile(PythonPackage):
    """This package provides backports of new features in Python's tempfile
    module under the backports namespace
    """

    homepage = "https://github.com/PiDelport/backports.tempfile"
    pypi = "backports.tempfile/backports.tempfile-1.0.tar.gz"

    license("PSF-2.0")

    version(
        "1.0",
        sha256="05aa50940946f05759696156a8c39be118169a0e0f94a49d0bb106503891ff54",
        url="https://pypi.org/packages/b4/5c/077f910632476281428fe254807952eb47ca78e720d059a46178c541e669/backports.tempfile-1.0-py2.py3-none-any.whl",
    )
