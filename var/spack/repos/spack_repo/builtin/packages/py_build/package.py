# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyBuild(PythonPackage):
    """A simple, correct PEP517 package builder."""

    homepage = "https://github.com/pypa/build"
    pypi = "build/build-0.7.0.tar.gz"

    license("MIT")

    version("1.2.2", sha256="119b2fb462adef986483438377a13b2f42064a2a3a4161f24a0cca698a07ac8c")
    version("1.2.1", sha256="526263f4870c26f26c433545579475377b2b7588b6f1eac76a001e873ae3e19d")
    version("1.1.1", sha256="8eea65bb45b1aac2e734ba2cc8dad3a6d97d97901a395bd0ed3e7b46953d2a31")
    version("1.1.0", sha256="f8da3eebb19668bb338b6eb256b1896ef4e87a5398bbdda97ee29ec474569f16")
    version("1.0.3", sha256="538aab1b64f9828977f84bc63ae570b060a8ed1be419e7870b8b4fc5e6ea553b")
    version("1.0.0", sha256="49a60f212df4d9925727c2118e1cbe3abf30b393eff7d0e7287d2170eb36844d")
    version("0.10.0", sha256="d5b71264afdb5951d6704482aac78de887c80691c52b88a9ad195983ca2c9269")
    version("0.9.0", sha256="1a07724e891cbd898923145eb7752ee7653674c511378eb9c7691aab1612bc3c")
    version("0.8.0", sha256="887a6d471c901b1a6e6574ebaeeebb45e5269a79d095fe9a8f88d6614ed2e5f0")
    version("0.7.0", sha256="1aaadcd69338252ade4f7ec1265e1a19184bf916d84c9b7df095f423948cb89f")

    variant("virtualenv", default=False, description="Install optional virtualenv dependency")

    with default_args(type="build"):
        depends_on("py-flit-core@3.8:", when="@1:")
        depends_on("py-flit-core@3.4:", when="@0.10:")

        # Historical dependencies
        depends_on("py-setuptools", when="@:0.9")

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@1.2:")
        depends_on("python@3.7:", when="@0.10:")
        depends_on("python@3.6:", when="@0.6:")

        depends_on("py-packaging@19.1:", when="@1.2:")
        depends_on("py-packaging@19:")

        depends_on("py-pyproject-hooks", when="@0.10.0:")

        depends_on("py-colorama", when="platform=windows")

        depends_on("py-importlib-metadata@4.6:", when="@1.1.0: ^python@:3.10.1")
        depends_on("py-importlib-metadata@4.6:", when="@1: ^python@:3.9")
        depends_on("py-importlib-metadata@0.22:", when="@0 ^python@:3.7")

        depends_on("py-tomli@1.1:", when="@0.10: ^python@:3.10")
        depends_on("py-tomli@1:", when="@:0.9")

        # Historical dependencies
        depends_on("py-pep517@0.9.1:", when="@:0.9")
        depends_on("py-virtualenv@20.0.35:", when="+virtualenv")

    # https://github.com/pypa/build/issues/266
    # https://github.com/pypa/build/issues/406
    def patch(self):
        filter_file(
            r"^(\s*)(venv\.EnvBuilder.*)$",
            r"\1os.environ.pop('PYTHONPATH', None)" + "\n" + r"\1\2",
            "src/build/env.py",
        )
