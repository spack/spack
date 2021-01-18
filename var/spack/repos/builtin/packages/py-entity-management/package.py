# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEntityManagement(PythonPackage):
    '''Pythonic Blue Brain Nexus access library.'''

    homepage = 'https://bbpcode.epfl.ch/code/#/admin/projects/nse/entity-management'
    git      = 'ssh://bbpcode.epfl.ch/nse/entity-management'

    version('1.2.10', tag='entity-management-v1.2.10')

    depends_on('py-setuptools', type=('build'))

    depends_on('py-requests', type='run')
    depends_on('py-attrs', type='run')
    depends_on('py-dateutil', type='run')
    depends_on('py-sparqlwrapper', type='run')
    depends_on('py-rdflib-jsonld', type='run')
    depends_on('py-pyjwt', type='run')
    depends_on('py-python-keycloak', type='run')
    depends_on('py-devtools+pygments', type='run')
