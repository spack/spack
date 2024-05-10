# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEntityManagement(PythonPackage):
    """Pythonic Blue Brain Nexus access library."""

    homepage = "https://github.com/BlueBrain/entity-management"
    git = "https://github.com/BlueBrain/entity-management.git"
    pypi = "entity-management/entity_management-1.2.46.tar.gz"

    version("1.2.46", sha256="0c3a3c1c0c9d47b47a2804746eefdbb26d5e707ac24f707ba8d42395c14eaa10")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-requests", type=("build", "run"))
    depends_on("py-attrs", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-sparqlwrapper", type=("build", "run"))
    depends_on("py-rdflib", type=("build", "run"))
    depends_on("py-pyjwt", type=("build", "run"))
    depends_on("py-python-keycloak", type=("build", "run"))
    depends_on("py-devtools+pygments", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
