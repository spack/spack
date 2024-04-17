# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List

from spack.package import *


class PySphinxcontribApplehelp(PythonPackage):
    """sphinxcontrib-applehelp is a sphinx extension which outputs Apple
    help books."""

    homepage = "http://sphinx-doc.org/"
    pypi = "sphinxcontrib-applehelp/sphinxcontrib-applehelp-1.0.1.tar.gz"
    git = "https://github.com/sphinx-doc/sphinxcontrib-applehelp.git"

    # 'sphinx' requires 'sphinxcontrib-applehelp' at build-time, but
    # 'sphinxcontrib-applehelp' requires 'sphinx' at run-time. Don't bother trying to
    # import any modules for this package.
    import_modules: List[str] = []

    license("BSD-2-Clause")

    version(
        "1.0.4",
        sha256="29d341f67fb0f6f586b23ad80e072c8e6ad0b48417db2bde114a4c9746feb228",
        url="https://pypi.org/packages/06/c1/5e2cafbd03105ce50d8500f9b4e8a6e8d02e22d0475b574c3b3e9451a15f/sphinxcontrib_applehelp-1.0.4-py3-none-any.whl",
    )
    version(
        "1.0.2",
        sha256="806111e5e962be97c29ec4c1e7fe277bfd19e9652fb1a4392105b43e01af885a",
        url="https://pypi.org/packages/dc/47/86022665a9433d89a66f5911b558ddff69861766807ba685de2e324bd6ed/sphinxcontrib_applehelp-1.0.2-py2.py3-none-any.whl",
    )
    version(
        "1.0.1",
        sha256="fb8dee85af95e5c30c91f10e7eb3c8967308518e0f7488a2828ef7bc191d0d5d",
        url="https://pypi.org/packages/13/9a/4428b3114d654cb1cd34d90d5e6fab938d5436f94a571155187ea1dd78b4/sphinxcontrib_applehelp-1.0.1-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@1.0.3:1.0.4")
