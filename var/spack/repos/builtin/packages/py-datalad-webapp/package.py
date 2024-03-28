# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDataladWebapp(PythonPackage):
    """DataLad extension for exposing commands via a web request API"""

    homepage = "https://github.com/datalad/datalad-webapp"
    pypi = "datalad_webapp/datalad_webapp-0.3.tar.gz"

    version(
        "0.3",
        sha256="1ed74504c25a3ca87bddd2ba61399471e6e2614b034b09e601875672c4cd017f",
        url="https://pypi.org/packages/7e/0b/ec6d5e7b06d92c0c89b9547084c1e617950f138ddcd73d670b2b7b9fa978/datalad_webapp-0.3-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-datalad@0.12.5:", when="@0.3:")
        depends_on("py-flask@1:", when="@0.3:")
        depends_on("py-flask-restful")
        depends_on("py-pytest-cov")
