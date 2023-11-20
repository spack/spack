# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEntityManagement(PythonPackage):
    """Pythonic Blue Brain Nexus access library."""

    homepage = "https://bbpgitlab.epfl.ch/nse/entity-management"
    git = "ssh://git@bbpgitlab.epfl.ch/nse/entity-management.git"

    version("1.2.34", tag="entity-management-v1.2.34")
    version("1.2.27", tag="entity-management-v1.2.27")
    version("1.2.26", tag="entity-management-v1.2.26")
    version("1.2.25", tag="entity-management-v1.2.25")
    version("1.2.19", tag="entity-management-v1.2.19")

    depends_on("py-setuptools", type="build")

    depends_on("py-requests", type=("build", "run"))
    depends_on("py-attrs", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-sparqlwrapper", type=("build", "run"))
    depends_on("py-rdflib", type=("build", "run"))
    depends_on("py-pyjwt", type=("build", "run"))
    depends_on("py-python-keycloak", type=("build", "run"))
    depends_on("py-devtools+pygments", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
