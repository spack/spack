# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVlConvertPython(PythonPackage):
    """Declarative statistical visualization library for Python"""

    pypi = "vl_convert_python/vl_convert_python-1.1.0.tar.gz"

    version("1.1.0", sha256="cc2bf58e019a5b4796b2903af8eb952555a7701603e0752e9f9fe66627af5c2e")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@40.6:", type="build")
    depends_on("py-entrypoints", type=("build", "run"))
    depends_on("py-jsonschema@3:", type=("build", "run"))
