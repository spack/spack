# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOmegaconf(PythonPackage):
    """A hierarchical configuration system, with support for merging configurations from
    multiple sources (YAML config files, dataclasses/objects and CLI arguments)
    providing a consistent API regardless of how the configuration was created.
    """

    homepage = "https://github.com/omry/omegaconf"
    pypi = "omegaconf/omegaconf-2.3.0.tar.gz"

    maintainers("calebrob6")

    license("BSD-3-Clause")

    version(
        "2.3.0",
        sha256="7b4df175cdb08ba400f45cae3bdcae7ba8365db4d165fc65fd04b050ab63b46b",
        url="https://pypi.org/packages/e3/94/1843518e420fa3ed6919835845df698c7e27e183cb997394e4a670973a65/omegaconf-2.3.0-py3-none-any.whl",
    )
    version(
        "2.2.2",
        sha256="556917181487fb66fe832d3c7b324f51b2f4c8adc373dd5091be921501b7d420",
        url="https://pypi.org/packages/ce/56/ffc5a96c317f94aad1cdfa1e00307a9c18b4c79841663d8d6decb15afcf1/omegaconf-2.2.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-antlr4-python3-runtime@4.9", when="@2.2.0.dev3:2.4.0.dev0")
        depends_on("py-pyyaml@5.1:", when="@2.1:")
