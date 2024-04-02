# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFlitScm(PythonPackage):
    """A PEP 518 build backend that uses setuptools_scm
    to generate a version file from your version control system,
    then flit to build the package.
    """

    homepage = "https://gitlab.com/WillDaSilva/flit_scm"
    pypi = "flit-scm/flit_scm-1.7.0.tar.gz"

    license("MIT")

    version(
        "1.7.0",
        sha256="9e864caa8a63f708f5bb2f1b5b53eedcd4da75ec2cc6221a64cea7aa5c9eae1a",
        url="https://pypi.org/packages/b8/c3/8d97318eeca2cf41e2a59e3af3e79d5fd23d56eed56ef1c34866d3b0a435/flit_scm-1.7.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-flit-core@3.5:", when="@1.2,1.6:")
        depends_on("py-setuptools-scm@6.4:", when="@1.7:")
        depends_on("py-tomli", when="@1.7: ^python@:3.10")
