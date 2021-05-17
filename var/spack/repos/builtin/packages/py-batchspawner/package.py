# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBatchspawner(PythonPackage):
    """This is a custom spawner for Jupyterhub that is designed for
    installations on clusters using batch scheduling software."""

    homepage = "https://github.com/jupyterhub/batchspawner"
    url      = "https://pypi.io/packages/source/b/batchspawner/batchspawner-1.0.1.tar.gz"

    version('1.0.1', sha256='b96ab7e1eb3b69e0863ebf045b960a4d074935a8a8fbfd0369b5d1af5b1bab8d')

    depends_on('py-setuptools',           type='build')
    depends_on('py-async-generator@1.8:', type=('build', 'run'))
    depends_on('py-jinja2',               type=('build', 'run'))
    depends_on('py-jupyterhub@0.5:',      type=('build', 'run'))
