# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHepdataConverter(PythonPackage):
    """This Python 3 library provides support for converting
    Old HepData input format (sample) to YAML as well as
    YAML to ROOT, YODA and CSV."""

    homepage = "https://github.com/HEPData/hepdata-converter"
    pypi = "hepdata-converter/hepdata-converter-0.2.3.tar.gz"

    maintainers("haralmha")

    version(
        "0.2.3",
        sha256="52d810011971993341908628a00591f912a3365cad675dd655b140ee3b19c331",
        url="https://pypi.org/packages/61/76/ed28e00180c2ff4368d30e7fc79c8b1a7316ec7eb3523fb3ce8d420fb544/hepdata_converter-0.2.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-hepdata-validator@0.2.2:", when="@0.2")
        depends_on("py-pyyaml@5.3:", when="@0.1.35:0.2")
