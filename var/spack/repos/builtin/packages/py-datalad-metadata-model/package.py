# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDataladMetadataModel(PythonPackage):
    """This software implements the metadata model that datalad and
    datalad-metalad will use in the future (datalad-metalad>=0.3.0) to handle
    metadata."""

    homepage = "https://github.com/datalad/metadata-model"
    pypi = "datalad-metadata-model/datalad-metadata-model-0.3.5.tar.gz"

    version("0.3.5", sha256="992241adef6d36ad7f9a83d8c7762d887fbec7111e06a2bd12fd8816e6ee739a")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@42:", type=("build"))

    depends_on("py-appdirs", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-fasteners", type=("build", "run"))
