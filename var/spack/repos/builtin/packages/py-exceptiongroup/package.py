# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyExceptiongroup(PythonPackage):
    """A backport of the BaseExceptionGroup and ExceptionGroup classes from Python 3.11."""

    homepage = "https://github.com/agronholm/exceptiongroup"
    pypi = "exceptiongroup/exceptiongroup-1.0.4.tar.gz"

    version("1.0.4", sha256="bd14967b79cd9bdb54d97323216f8fdf533e278df937aa2a90089e7d6e06e5ec")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-flit-scm", type="build")
