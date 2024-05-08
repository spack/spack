# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAnnotatedTypes(PythonPackage):
    """Reusable constraint types to use with typing.Annotated"""

    homepage = "https://pypi.org/project/annotated-types/"
    pypi = "annotated-types/annotated_types-0.6.0.tar.gz"

    version("0.6.0", sha256="563339e807e53ffd9c267e99fc6d9ea23eb8443c08f112651963e24e22f84a5d")

    depends_on("py-hatchling@0.15.0:", type="build")
