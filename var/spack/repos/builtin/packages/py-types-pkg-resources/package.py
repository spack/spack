# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTypesPkgResources(PythonPackage):
    """Typing stubs for pkg_resources"""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-pkg-resources/types-pkg_resources-0.1.3.tar.gz"

    version(
        "0.1.3",
        sha256="0cb9972cee992249f93fff1a491bf2dc3ce674e5a1926e27d4f0866f7d9b6d9c",
        url="https://pypi.org/packages/e9/97/a24ffd614ac2962dabbd599afbed00adf6464604a53b96b5f48301518a5f/types_pkg_resources-0.1.3-py2.py3-none-any.whl",
    )
