# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTuswsgi(PythonPackage):
    """python wsgi filter for tus protocol 1.0.0"""

    homepage = "https://github.com/mvdbeek/tusfilter"

    version(
        "0.5.4",
        url="https://files.pythonhosted.org/packages/5a/82/cdfa7d9b8c90131a7f10e7fd85c6797a6ce36e255f3151b26778a025c386/tuswsgi-0.5.4-py2.py3-none-any.whl",
        sha256="f681a386254a161a97301a67c01ee7da77419c007d9bc43dbd48d5a987491a5e",
        expand=False,
    )

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-webob", type=("build", "run"))

