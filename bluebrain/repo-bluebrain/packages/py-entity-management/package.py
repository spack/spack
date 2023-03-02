# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEntityManagement(PythonPackage):
    """Pythonic Blue Brain Nexus access library."""

    homepage = "https://bbpgitlab.epfl.ch/nse/entity-management"
    git = "ssh://git@bbpgitlab.epfl.ch/nse/entity-management.git"

    version("1.2.19", tag="entity-management-v1.2.19")
    version("0.1.12", tag="entity-management-v0.1.12")

    depends_on("py-setuptools", type=("build"))

    depends_on("py-requests", type="run")
    depends_on("py-attrs", type="run")
    depends_on("py-python-dateutil", type="run")
    depends_on("py-sparqlwrapper", type="run")
    depends_on("py-rdflib", type="run")
    depends_on("py-pyjwt", type="run")
    depends_on("py-python-keycloak", type="run")
    depends_on("py-devtools+pygments", type="run")
