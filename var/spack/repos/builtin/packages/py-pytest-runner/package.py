# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestRunner(PythonPackage):
    """Invoke py.test as distutils command with dependency resolution."""

    homepage = "https://github.com/pytest-dev/pytest-runner"
    pypi = "pytest-runner/pytest-runner-5.1.tar.gz"

    license("MIT")

    version(
        "6.0.0",
        sha256="4c059cf11cf4306e369c0f8f703d1eaf8f32fad370f41deb5f007044656aca6b",
        url="https://pypi.org/packages/42/7b/1cec26caae4bf44bb9911e1119d5d1a35171571e100b728a2ccd8719a3b1/pytest_runner-6.0.0-py3-none-any.whl",
    )
    version(
        "5.3.1",
        sha256="85f93af814438ee322b4ea08fe3f5c2ad53b253577f3bd84b2ad451fee450ac5",
        url="https://pypi.org/packages/f4/f5/6605d73bf3f4c198915872111b10c4b3c2dccd8485f47b7290ceef037190/pytest_runner-5.3.1-py3-none-any.whl",
    )
    version(
        "5.1",
        sha256="d04243fbf29a3b574f18f1bcff2a07f505db5daede82f706f2e32728f77d3f4d",
        url="https://pypi.org/packages/f8/31/f291d04843523406f242e63b5b90f7b204a756169b4250ff213e10326deb/pytest_runner-5.1-py2.py3-none-any.whl",
    )
    version(
        "2.11.1",
        sha256="feca6166c9c3b535441a9818126c9030101417c057892f29ffd5d8ae56613f35",
        url="https://pypi.org/packages/26/d4/9e25eb226ddc6d395a72e3a6a6dcdfea197c21a2c7fbcd6f94545effb04d/pytest_runner-2.11.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@6:")

    # requirements from pyproject.toml are marked with *
