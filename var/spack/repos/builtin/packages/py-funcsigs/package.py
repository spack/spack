# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFuncsigs(PythonPackage):
    """Python function signatures from PEP362 for Python 2.6, 2.7 and 3.2+"""

    homepage = "https://funcsigs.readthedocs.io"
    pypi = "funcsigs/funcsigs-1.0.2.tar.gz"

    version("1.0.2", sha256="a7bb0f2cf3a3fd1ab2732cb49eba4252c2af4240442415b4abce3b87022a8f50")

    depends_on("python@:3.5", type=("build", "run"))
    depends_on("py-setuptools", type="build")
