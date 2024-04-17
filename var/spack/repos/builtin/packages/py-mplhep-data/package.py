# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMplhepData(PythonPackage):
    """Font (Data) sub-package for mplhep"""

    homepage = "https://github.com/Scikit-HEP/mplhep_data"
    pypi = "mplhep_data/mplhep_data-0.0.3.tar.gz"

    license("MIT")

    version(
        "0.0.3",
        sha256="a1eba7727fab31902e6fcd113c8f4b12ff3fb0666781e7514f8b79093cdc1c65",
        url="https://pypi.org/packages/b9/f2/97faf68c79fc135061190092e8e6db9a024de4249a7e82acc83d9443db2b/mplhep_data-0.0.3-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:")
