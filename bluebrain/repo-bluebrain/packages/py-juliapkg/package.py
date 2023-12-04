# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJuliapkg(PythonPackage):
    """Manage your Julia dependencies from Python"""

    homepage = "https://github.com/JuliaPy/pyjuliapkg"
    pypi = "juliapkg/juliapkg-0.1.10.tar.gz"

    maintainers("tristan0x")

    version("0.1.10", sha256="70507318d51ac8663e856f56048764e49f5a0c4c90d81a3712d039a316369505")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-semantic-version", type=("build", "run"))
