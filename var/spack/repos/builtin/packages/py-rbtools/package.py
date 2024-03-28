# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRbtools(PythonPackage):
    """RBTools is a set of command line tools and a rich Python API for
    use with Review Board."""

    homepage = "https://github.com/reviewboard/rbtools"
    url = "https://github.com/reviewboard/rbtools/archive/release-1.0.2.tar.gz"

    license("MIT")

    version(
        "1.0.2",
        sha256="1bb4f9a81bcb989f5cf7511261c0352b912e98d3f216f1f48fee12e031746edc",
        url="https://pypi.org/packages/1d/ad/870d7c7a258bd222d91c2ae264d28402b8bdfcae999967403ad42876b329/RBTools-1.0.2-py2.py3-none-any.whl",
    )
    version(
        "1.0.1",
        sha256="42c78c5a8555677a4d6b79300a4f0bedc3aabd4b4ef25374fac932447246d1fc",
        url="https://pypi.org/packages/6f/ce/d327fa8581585d72e1fbbe80f6fb288db454d070f0cedc0b9ed5e1570ea3/RBTools-1.0.1-py2.py3-none-any.whl",
    )
    version(
        "1.0",
        sha256="cf2f6d7dcabd023f420ede11d4db2b37bddb5a7f1482fc4f854dc71ea2d6db9b",
        url="https://pypi.org/packages/2e/28/c1205708d3092e556ea3d0a594442924c51bcee8767bd6bb8edec968d144/RBTools-1.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-backports-shutil-get-terminal-size", when="@1:1.0.1")
        depends_on("py-colorama", when="@1:")
        depends_on("py-six@1.8:", when="@0.7.7:0.7.8,0.7.10:4.0")
        depends_on("py-texttable", when="@1:")
        depends_on("py-tqdm", when="@0.7.7:0.7.8,0.7.10:")
