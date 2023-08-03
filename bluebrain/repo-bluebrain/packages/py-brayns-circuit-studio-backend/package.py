# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBraynsCircuitStudioBackend(PythonPackage):
    """Services for Brayns Circuit Studio software."""

    homepage = "https://bbpgitlab.epfl.ch/viz/brayns/braynscircuitstudiobackend"
    git = "ssh://git@bbpgitlab.epfl.ch/viz/brayns/braynscircuitstudiobackend.git"

    version("develop", branch="develop")
    version("1.0.1", commit="13389b219a11665c856af813e205d4225ffe062a")
    version("1.0.0", tag="v1.0.0")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-aiohttp@3.8.3", type=("run"))
    depends_on("py-aiosignal@1.2.0", type=("run"))
    depends_on("py-async-timeout@4.0.2", type=("run"))
    depends_on("py-attrs@21.4.0", type=("run"))
    depends_on("py-charset-normalizer@2.0.12", type=("run"))
    depends_on("py-click@8.1.3", type=("run"))
    depends_on("py-frozenlist@1.3.0", type=("run"))
    depends_on("py-idna@3.3", type=("run"))
    depends_on("py-libsonata@0.1.14:", type=("run"))
    depends_on("py-marshmallow@3.19.0", type=("run"))
    depends_on("py-multidict@6.0.2", type=("run"))
    depends_on("py-mypy-extensions@0.4.3", type=("run"))
    depends_on("py-pathspec@0.9.0", type=("run"))
    depends_on("py-platformdirs@2.5.2", type=("run"))
    depends_on("py-tomli@2.0.1", type=("run"))
    depends_on("py-typing-extensions@4.2.0", type=("run"))
    depends_on("py-yarl@1.7.2", type=("run"))
    depends_on("py-psutil@5.9.4:", type=("run"))
    depends_on("py-pydash@5.1.0:", type=("run"))
    depends_on("py-furl@2.1.3:", type=("run"))
    depends_on("py-pytz@2022.7.1", type=("run"))
    depends_on("py-sentry-sdk@1.15.0", type=("run"))
    depends_on("py-bluepy@2.5.1", type=("run"))
