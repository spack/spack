# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFindDuplicateFiles(PythonPackage):
    """A tool to find duplicate stuff."""

    pypi = "find-duplicate-files/find-duplicate-files-2.1.0.tar.gz"

    version("2.1.0", "11a4c742720e49883901a5be4447225d4a67a9e1e67f9446127f90ffda96a339")

    depends_on("py-setuptools", type="build")
    depends_on("py-mock", type="build")
