# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlake8Polyfill(PythonPackage):
    """flake8-polyfill is a package that provides some compatibility helpers
    for Flake8 plugins that intend to support Flake8 2.x and 3.x
    simultaneously.
    """

    homepage = "https://gitlab.com/pycqa/flake8-polyfill"
    pypi = "flake8-polyfill/flake8-polyfill-1.0.2.tar.gz"

    license("MIT")

    version(
        "1.0.2",
        sha256="12be6a34ee3ab795b19ca73505e7b55826d5f6ad7230d31b18e106400169b9e9",
        url="https://pypi.org/packages/86/b5/a43fed6fd0193585d17d6faa7b85317d4461f694aaed546098c69f856579/flake8_polyfill-1.0.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-flake8")
