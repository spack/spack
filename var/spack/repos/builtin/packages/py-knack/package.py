# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyKnack(PythonPackage):
    """A Command-Line Interface framework."""

    homepage = "https://github.com/microsoft/knack"
    pypi = "knack/knack-0.7.1.tar.gz"

    license("MIT")

    version(
        "0.7.1",
        sha256="1c4c1aa16df842caa862ce39c5f83aab79c0fcb4e992e1043f68add87250e9fd",
        url="https://pypi.org/packages/31/df/b891050d92244449eb8a28aa312ad0cca7d71cebe6d9705b65a90bb784ba/knack-0.7.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-argcomplete")
        depends_on("py-colorama", when="@:0.8.2")
        depends_on("py-jmespath")
        depends_on("py-pygments")
        depends_on("py-pyyaml")
        depends_on("py-six", when="@:0.8.0-rc2")
        depends_on("py-tabulate")
