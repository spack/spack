# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGenerateds(PythonPackage):
    """Generate Python data structures and XML parser from Xschema."""

    homepage = "http://www.davekuhlman.org/generateDS.html"
    pypi = "generateDS/generateDS-2.41.4.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version(
        "2.43.2",
        sha256="63b5dbcb81746f66223c36853a2832dbf0f17dd8740654510377a0b9a50c0e27",
        url="https://pypi.org/packages/a6/9b/08221d09990dae613074865694d0eadb3ddab55ee7338126ddb650b0b129/generateDS-2.43.2-py3-none-any.whl",
    )
    version(
        "2.43.1",
        sha256="2c4c9f7cf0a9566075b48e635358c95b7635b8f349323f0802da3ae88aa45d57",
        url="https://pypi.org/packages/46/2f/facdb9d5217b821357ca410fc3c571f05383036a4fc8deea68a53b7c514a/generateDS-2.43.1-py3-none-any.whl",
    )
    version(
        "2.42.2",
        sha256="eef57580b97331b877efdeccbca5ff1153976fefb8cf68362b31e2504423998c",
        url="https://pypi.org/packages/44/1a/4665be43abf83759b805512190a59e8c7b401583b80c92fb59fa49a09223/generateDS-2.42.2-py3-none-any.whl",
    )
    version(
        "2.42.1",
        sha256="0a13bf2dae16db27268cd57febd3413448c577720f5729194746d0b73de1fa94",
        url="https://pypi.org/packages/40/29/6f7788177964ee69e8f660715d7230641a39fe9192e8f1bee0ccbdd2b58f/generateDS-2.42.1-py3-none-any.whl",
    )
    version(
        "2.41.5",
        sha256="4781e3685f09f53e7273f67eb8609177eb4bb586fef8a3d9054c6471462f8cb2",
        url="https://pypi.org/packages/b0/a0/9787633c3b80151c8b172c77875638041c93aac3af59f6d8c8f90c5361b6/generateDS-2.41.5-py3-none-any.whl",
    )
    version(
        "2.41.4",
        sha256="7417b2ad40d2ae96729ef2c46be8a27b94401f4fa3cd3f6ffed4db47644f7a94",
        url="https://pypi.org/packages/d2/45/0145a4beda2286eaa11afb6643a7e51e4633456dc738ad90fe2dd0defbe1/generateDS-2.41.4-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-lxml")
        depends_on("py-requests@2.21:")
        depends_on("py-six")
