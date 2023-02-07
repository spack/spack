# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGssapi(PythonPackage):
    """Python-GSSAPI provides both low-level and high level wrappers
    around the GSSAPI C libraries."""

    homepage = "https://github.com/pythongssapi/python-gssapi"
    pypi = "gssapi/gssapi-1.8.2.tar.gz"

    maintainers("wdconinc")

    version("1.8.2", sha256="b78e0a021cc91158660e4c5cc9263e07c719346c35a9c0f66725e914b235c89a")

    depends_on("py-cython@0.29.29:2", type="build")
    depends_on("py-setuptools@40.6.0:", type="build")

    depends_on("py-decorator", type=("build", "run"))
