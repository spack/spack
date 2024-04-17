# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJavaproperties(PythonPackage):
    """Read & write Java .properties files."""

    homepage = "https://github.com/jwodder/javaproperties"
    pypi = "javaproperties/javaproperties-0.7.0.tar.gz"

    license("MIT")

    version(
        "0.7.0",
        sha256="2de84a64579abccc201e56ef4449bd27a9b2c644874f7738e7d04ebeadc75bec",
        url="https://pypi.org/packages/d9/e1/2c9ba71d740c953996aca3d2899649805db2f3b5fdbd3b570570d7d52bbf/javaproperties-0.7.0-py2.py3-none-any.whl",
    )
    version(
        "0.5.1",
        sha256="8bfb757116ed0589d88b4e13ecdc7d05a22c647a4645abf43ec27059430b1468",
        url="https://pypi.org/packages/ee/c3/1e42437893a99717da1eda415c4b7353e8aaba395cc0ef387a47f4ac1c60/javaproperties-0.5.1-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@:3", when="@0.5:")
        depends_on("py-six@1.4:", when="@0.5:0.7")
