# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySimpleeval(PythonPackage):
    """A quick single file library for easily adding evaluatable expressions into python
    projects."""

    homepage = "https://github.com/danthedeckie/simpleeval"
    pypi = "simpleeval/simpleeval-0.9.12.tar.gz"

    version("0.9.12", sha256="3e0be507486d4e21cf9d08847c7e57dd61a1603950399985f7c5a0be7fd33e36")

    depends_on("py-setuptools@30.3.0:", type="build")
    depends_on("py-build", type="build")
