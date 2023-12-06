# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xcdf(CMakePackage):
    """Binary data format designed to store data fields with user-specified accuracy."""

    homepage = "https://github.com/jimbraun/XCDF"
    url = "https://github.com/jimbraun/XCDF/archive/refs/tags/v3.00.03.tar.gz"

    license("BSD-2-Clause")

    version("3.00.03", sha256="4e445a2fea947ba14505d08177c8d5b55856f8411f28de1fe4d4c00f6824b711")

    patch("remove_python_support.patch")
