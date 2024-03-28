# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMergedeep(PythonPackage):
    """A deep merge function for Python."""

    homepage = "https://github.com/clarketm/mergedeep"
    pypi = "mergedeep/mergedeep-1.3.4.tar.gz"

    license("MIT")

    version(
        "1.3.4",
        sha256="70775750742b25c0d8f36c55aed03d24c3384d17c951b3175d898bd778ef0307",
        url="https://pypi.org/packages/2c/19/04f9b178c2d8a15b076c8b5140708fa6ffc5601fb6f1e975537072df5b2a/mergedeep-1.3.4-py3-none-any.whl",
    )
