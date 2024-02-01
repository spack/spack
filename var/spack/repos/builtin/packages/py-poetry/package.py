# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPoetry(PythonPackage):
    """Python dependency management and packaging made easy."""

    homepage = "https://python-poetry.org/"
    pypi = "poetry/poetry-1.1.12.tar.gz"

    version("1.2.1", sha256="2750bb2b636ef435d8beac51dde0b13d06199017a1d9b96cba899863d1e81024")
    version("1.2.0", sha256="17c527d5d5505a5a7c5c14348d87f077d643cf1f186321530cde68e530bba59f")
    version("1.1.13", sha256="b905ed610085f568aa61574e0e09260c02bff9eae12ff672af39e9f399357ac4")
    version("1.1.12", sha256="5c66e2357fe37b552462a88b7d31bfa2ed8e84172208becd666933c776252567")

    depends_on("python@2.7,3.5:3", type=("build", "run"))
    depends_on("python@3.7:3", when="@1.2.0:", type=("build", "run"))
    depends_on("py-poetry-core@1.0.7:1.0", when="@:1.1", type=("build", "run"))
    depends_on("py-poetry-core@1.1.0", when="@1.2.0", type=("build", "run"))
    depends_on("py-poetry-core@1.2.0", when="@1.2.1:", type=("build", "run"))
    depends_on("py-poetry-plugin-export@1.0.6:1", when="@1.2.0:", type=("build", "run"))
    depends_on("py-poetry-plugin-export@1.0.7:1", when="@1.2.1:", type=("build", "run"))
    depends_on(
        "py-backports-cached-property@1.0.2:1", when="@1.2.1: ^python@:3.7", type=("build", "run")
    )
    depends_on("py-cachecontrol@0.12.9:0.12+filecache", when="@1.2.1:", type=("build", "run"))
    depends_on(
        "py-cachecontrol@0.12.9:0.12+filecache", when="^python@3.6:3", type=("build", "run")
    )
    depends_on("py-cachy@0.3.0:0.3", type=("build", "run"))
    depends_on("py-cleo@0.8.1:0.8", when="@:1.1", type=("build", "run"))
    depends_on("py-cleo@1", type=("build", "run"), when="@1.2.0:")
    depends_on("py-clikit@0.6.2:0.6", when="@:1.1", type=("build", "run"))
    depends_on("py-crashtest@0.3.0:0.3", when="^python@3.6:3", type=("build", "run"))
    depends_on("py-html5lib@1.0:1", type=("build", "run"))
    depends_on("py-importlib-metadata@1.6:1", when="@:1.1 ^python@:3.7", type=("build", "run"))
    depends_on("py-importlib-metadata@4.4:", when="@1.2.0 ^python@:3.9", type=("build", "run"))
    depends_on("py-importlib-metadata@4.4:4", when="@1.2.1: ^python@:3.9", type=("build", "run"))
    depends_on("py-jsonschema@4.10.0:4", when="@1.2:", type=("build", "run"))
    depends_on("py-keyring@21.2.0:21", when="@1.1.12 ^python@3.6:3", type=("build", "run"))
    depends_on("py-keyring@21.2.0:", when="@1.1.13:", type=("build", "run"))
    depends_on("py-packaging@20.4:20", when="@:1.1", type=("build", "run"))
    depends_on("py-packaging@20.4:", when="@1.2:", type=("build", "run"))
    depends_on("py-pexpect@4.7:4", type=("build", "run"))
    depends_on("py-pkginfo@1.4:1", when="@:1.1", type=("build", "run"))
    depends_on("py-pkginfo@1.5:1", when="@1.2:", type=("build", "run"))
    depends_on("py-platformdirs@2.5.2:2", when="@1.2:", type=("build", "run"))
    depends_on("py-requests@2.18:2", type=("build", "run"))
    depends_on("py-requests-toolbelt@0.9.1:0.9", type=("build", "run"))
    depends_on("py-shellingham@1.1:1", when="@:1.1", type=("build", "run"))
    depends_on("py-shellingham@1.5:1", when="@1.2:", type=("build", "run"))
    depends_on("py-tomlkit@0.7:0", when="@:1.1", type=("build", "run"))
    depends_on("py-tomlkit@0.11.1,0.11.4:0", when="@1.2:", type=("build", "run"))
    depends_on("py-virtualenv@20.0.26:20", when="@:1.1", type=("build", "run"))
    depends_on("py-virtualenv@20.4.3:20.4.4,20.4.7:", when="@1.2:", type=("build", "run"))
    depends_on("py-xattr@0.9.7:0.9", when="platform=darwin @1.2:")
    depends_on("py-urllib3@1.26.0:1", when="@1.2:")
    depends_on("py-dulwich@0.20.44:0.20", when="@1.2.0")
    depends_on("py-dulwich@0.20.46:0.20", when="@1.2.1:")
