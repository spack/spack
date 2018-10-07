# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGitReview(PythonPackage):
    """git-review is a tool that helps submitting git branches to gerrit"""

    homepage = "http://docs.openstack.org/infra/git-review"
    url = "https://pypi.io/packages/source/g/git-review/git-review-1.25.0.tar.gz"

    version('1.26.0', 'dec20e8a259c03fe19c9dd2362c4ec3f')
    version('1.25.0', '0a061d0e23ee9b93c6212a3fe68fb7ab')
    version('1.24',   '145116fe58a3487c3ad1bf55538fd741')
    version('1.23',   'b0023ad8c037ab710da81412194c6a3a')
    version('1.22',   'e889df5838c059362e5e0d411bde9c48')
    version('1.21',   'eee88bdef1aa37a55cc8becd48c6aba9')

    extends('python')

    depends_on('py-setuptools',    type=('build'))
    depends_on('py-pbr',           type=('build', 'run'))
    depends_on('py-requests@1.1:', type=('build', 'run'))
    depends_on('git',              type=('run'))
    depends_on('tk',               type=('run'))

    def setup_environment(self, spack_env, run_env):
        run_env.set('PBR_VERSION', str(self.spec.version))
