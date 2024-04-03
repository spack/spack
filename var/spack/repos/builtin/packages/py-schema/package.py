# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySchema(PythonPackage):
    """Simple data validation library"""

    homepage = "https://github.com/keleshev/schema"
    pypi = "schema/schema-0.7.5.tar.gz"

    license("MIT")

    version(
        "0.7.5",
        sha256="f3ffdeeada09ec34bf40d7d79996d9f7175db93b7a5065de0faa7f41083c1e6c",
        url="https://pypi.org/packages/0d/93/ca8aa5a772efd69043d0a745172d92bee027caa7565c7f774a2f44b91207/schema-0.7.5-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-contextlib2@0.5.5:", when="@0.7.2:0.7.3,0.7.5:")
