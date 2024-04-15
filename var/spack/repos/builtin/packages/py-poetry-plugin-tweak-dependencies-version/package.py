# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPoetryPluginTweakDependenciesVersion(PythonPackage):
    """Poetry plugin used to tweak dependency versions."""

    homepage = "https://github.com/sbrunner/poetry-plugin-tweak-dependencies-version"
    pypi = "poetry_plugin_tweak_dependencies_version/"
    pypi += "poetry_plugin_tweak_dependencies_version-1.5.1.tar.gz"

    maintainers("LydDeb")

    version(
        "1.5.1",
        sha256="50fe77909d61947572cf9d83916d5e87eb64f7a4744b4606b940b78d9ec53b83",
        url="https://pypi.org/packages/0b/58/4b821ef2eeaff4c3c7e4f5122d746fc074261ab06e4b630cb20cb1b8e120/poetry_plugin_tweak_dependencies_version-1.5.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.9:3.11", when="@1.5:1.5.1")
        depends_on("py-poetry@1.6", when="@1.5.1")
