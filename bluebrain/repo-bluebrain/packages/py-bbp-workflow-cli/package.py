# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBbpWorkflowCli(PythonPackage):
    '''Blue Brain Workflow command line tool.'''

    homepage = 'https://bbpgitlab.epfl.ch/nse/bbp-workflow-cli'
    git = 'ssh://git@bbpgitlab.epfl.ch/nse/bbp-workflow-cli.git'

    version('3.1.0.dev1', tag='bbp-workflow-cli-v3.1.0.dev1')

    depends_on('py-setuptools', type=('build'))

    depends_on('py-requests', type='run')
    depends_on('py-click', type='run')
    depends_on('py-sh', type='run')
    depends_on('py-python-keycloak', type='run')
    depends_on('py-kubernetes', type='run')
    depends_on('py-pyjwt', type='run')
