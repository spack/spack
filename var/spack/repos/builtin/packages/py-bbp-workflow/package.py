# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBbpWorkflow(PythonPackage):
    '''Blue Brain Workflow.'''

    homepage = 'https://bbpcode.epfl.ch/code/#/admin/projects/nse/bbp-workflow'
    git      = 'ssh://bbpcode.epfl.ch/nse/bbp-workflow'

    version('2.0.6', tag='bbp-workflow-v2.0.6')

    depends_on('py-setuptools', type=('build'))

    depends_on('py-luigi', type='run')
    depends_on('py-entity-management', type='run')
    depends_on('py-requests-unixsocket', type='run')
    depends_on('py-sh', type='run')
    depends_on('py-matplotlib', type='run')
    depends_on('py-dask', type='run')
    depends_on('py-distributed', type='run')
    depends_on('py-xarray', type='run')
    depends_on('py-notebook', type='run')

    depends_on('py-bluepy', type='run')
    depends_on('py-bluepy-configfile', type='run')
    depends_on('py-simwriter', type='run')
