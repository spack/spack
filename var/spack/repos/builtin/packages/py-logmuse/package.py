# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLogmuse(PythonPackage):
    """A small logging setup package."""

    homepage = "https://github.com/databio/logmuse/"
    pypi = "logmuse/logmuse-0.2.7.tar.gz"

    license("BSD-2-Clause")

    version(
        "0.2.7",
        sha256="691fc43118feddeaf41b57cd8b8ed5c8e6071948e57a2b824b9c690712e858a8",
        url="https://pypi.org/packages/2e/6e/283626ed8c887809144942055e4c409e7a28627e95f6a8295e5606c6d913/logmuse-0.2.7-py3-none-any.whl",
    )
