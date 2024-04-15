# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTuswsgi(PythonPackage):
    """python wsgi filter for tus protocol 1.0.0"""

    homepage = "https://github.com/mvdbeek/tusfilter"
    url = "https://pypi.io/packages/py2.py3/t/tuswsgi/tuswsgi-0.5.4-py2.py3-none-any.whl"

    license("MIT")

    version(
        "0.5.4",
        sha256="f681a386254a161a97301a67c01ee7da77419c007d9bc43dbd48d5a987491a5e",
        url="https://pypi.org/packages/5a/82/cdfa7d9b8c90131a7f10e7fd85c6797a6ce36e255f3151b26778a025c386/tuswsgi-0.5.4-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-webob", when="@:0.5.5.0")
