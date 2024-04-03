# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIgor2(PythonPackage):
    """igor2: interface for reading binary IGOR files."""

    # pypi only has no sdist
    homepage = "https://github.com/AFM-analysis/igor2"
    url = "https://pypi.io/packages/py3/i/igor2/igor2-0.5.3-py3-none-any.whl"

    license("LGPL-3.0-or-later")

    version(
        "0.5.3",
        sha256="bb7b54a5926ec640e0e9176f46e0dd88ad956fec2d17ba3b0a7687eba82cefee",
        url="https://pypi.org/packages/5c/b8/5c73c5c54804323c8b5b1a52b68ff5d34a22d52bbd9bc0dd6d63745e4f1e/igor2-0.5.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:3")
        depends_on("py-numpy@1.25.1:", when="@0.5.3:")
