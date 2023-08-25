# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypesSetuptools(PythonPackage):
    """Typing stubs for setuptools."""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-setuptools/types-setuptools-65.5.0.3.tar.gz"

    version("65.5.0.3", sha256="17769171f5f2a2dc69b25c0d3106552a5cda767bbf6b36cb6212b26dae5aa9fc")

    depends_on("py-setuptools", type="build")
