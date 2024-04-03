# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPylint(PythonPackage):
    """python code static checker"""

    pypi = "pylint/pylint-1.6.5.tar.gz"

    import_modules = [
        "pylint",
        "pylint.lint",
        "pylint.extensions",
        "pylint.config",
        "pylint.checkers",
        "pylint.checkers.refactoring",
        "pylint.message",
        "pylint.utils",
        "pylint.pyreverse",
        "pylint.reporters",
        "pylint.reporters.ureports",
    ]

    license("GPL-2.0-or-later")

    version(
        "2.16.2",
        sha256="ff22dde9c2128cd257c145cfd51adeff0be7df4d80d669055f24a962b351bbe4",
        url="https://pypi.org/packages/e1/1b/b34a9c3485151db12402ab701f9cb836359cb95668870d071d5b2e327f67/pylint-2.16.2-py3-none-any.whl",
    )
    version(
        "2.15.0",
        sha256="4b124affc198b7f7c9b5f9ab690d85db48282a025ef9333f51d2d7281b92a6c3",
        url="https://pypi.org/packages/5e/1b/920b36e0db0fe3d4b583a934e1889153699bcccbca0a41b18202d2d2e1e9/pylint-2.15.0-py3-none-any.whl",
    )
    version(
        "2.14.4",
        sha256="89b61867db16eefb7b3c5b84afc94081edaf11544189e2b238154677529ad69f",
        url="https://pypi.org/packages/30/7a/db35d167413665b8cb82caa043d2931a45c4a05622367b1f19ceea65e415/pylint-2.14.4-py3-none-any.whl",
    )
    version(
        "2.13.5",
        sha256="c149694cfdeaee1aa2465e6eaab84c87a881a7d55e6e93e09466be7164764d1e",
        url="https://pypi.org/packages/9f/53/e1d8da0d381e4a303cc812238e733073abdd9099525c42cb100b20faf8b9/pylint-2.13.5-py3-none-any.whl",
    )
    version(
        "2.11.1",
        sha256="0f358e221c45cbd4dad2a1e4b883e75d28acdcccd29d40c76eb72b307269b126",
        url="https://pypi.org/packages/37/42/948d1486727806df2e0016f1cfc2d3beafe289f96d53dfc85d967f79afc5/pylint-2.11.1-py3-none-any.whl",
    )
    version(
        "2.8.2",
        sha256="f7e2072654a6b6afdf5e2fb38147d3e2d2d43c89f648637baab63e026481279b",
        url="https://pypi.org/packages/10/f0/9705d6ec002876bc20b6923cbdeeca82569a895fc214211562580e946079/pylint-2.8.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2.14:2,3.0.0-alpha5:3.0.0-alpha6")
        depends_on("python@:3", when="@:2.12.0,3:3.0.0-alpha4")
        depends_on("py-astroid@2.14.2:2", when="@2.16.2:2.16")
        depends_on("py-astroid@2.12.4:2.13", when="@2.15:2.15.0")
        depends_on("py-astroid@2.11.6:2.11", when="@2.14.2:2.14")
        depends_on("py-astroid@2.11.2:2.11", when="@2.13.2:2.13.5")
        depends_on("py-astroid@2.8", when="@2.11")
        depends_on("py-astroid@2.5.6:2.6", when="@2.8.1:2.8.1.0,2.8.2")
        depends_on("py-colorama@0.4.5:", when="@2.14.3:2,3.0.0-alpha6: platform=windows")
        depends_on("py-colorama", when="@:2.14.2,3:3.0.0-alpha5 platform=windows")
        depends_on("py-dill@0.3.6:", when="@2.15.9:2.16.0.0,2.16.1:2,3.0.0-alpha6: ^python@3.11:")
        depends_on("py-dill@0.2:", when="@2.15.9:2.16.0.0,2.16.1:2,3.0.0-alpha6: ^python@:3.10")
        depends_on("py-dill@0.2:", when="@2.13:2.15.8,2.16.0.dev:2.16.0,3.0.0-alpha5")
        depends_on("py-isort@4.2.5:5", when="@:3.0.2")
        depends_on("py-mccabe@0.6:", when="@2.13:2,3.0.0-alpha5:")
        depends_on("py-mccabe@0.6", when="@:2.12,3:3.0.0-alpha4")
        depends_on("py-platformdirs@2.2:", when="@2.10.2:2,3.0.0-alpha5:")
        depends_on("py-toml@0.7.1:", when="@:2.11,3:3.0.0-alpha4")
        depends_on("py-tomli@1.1:", when="@2.13:2,3.0.0-alpha5: ^python@:3.10")
        depends_on("py-tomlkit@0.10.1:", when="@2.14:2,3.0.0-alpha5:")
        depends_on("py-typing-extensions@3.10:", when="@2.11:2,3.0.0-alpha5: ^python@:3.9")

    # note there is no working version of astroid for this
