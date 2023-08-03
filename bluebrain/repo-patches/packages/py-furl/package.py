# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFurl(PythonPackage):
    """furl is a small Python library that makes parsing and
    manipulating URLs easy"""

    homepage = "https://github.com/gruns/furl"
    pypi = "furl/furl-2.1.3.tar.gz"

    version("2.1.3", sha256="5a6188fe2666c484a12159c18be97a1977a71d632ef5bb867ef15f54af39cc4e")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
    depends_on("py-six@1.8.0", type=("run"))
    depends_on("py-orderedmultidict@1.0.1", type=("run"))
