# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGitReview(PythonPackage):
    """git-review is a tool that helps submitting git branches to gerrit"""

    homepage = "http://docs.openstack.org/infra/git-review"
    url = "https://pypi.io/packages/source/g/git-review/git-review-1.25.0.tar.gz"

    version('1.26.0', sha256='487c3c1d7cc81d02b303a1245e432579f683695c827ad454685b3953f70f0b94')
    version('1.25.0', sha256='087e0a7dc2415796a9f21c484a6f652c5410e6ba4562c36291c5399f9395a11d')
    version('1.24',   md5='145116fe58a3487c3ad1bf55538fd741')
    version('1.23',   md5='b0023ad8c037ab710da81412194c6a3a')
    version('1.22',   md5='e889df5838c059362e5e0d411bde9c48')
    version('1.21',   md5='eee88bdef1aa37a55cc8becd48c6aba9')

    extends('python')

    depends_on('py-setuptools',    type=('build'))
    depends_on('py-pbr',           type=('build', 'run'))
    depends_on('py-requests@1.1:', type=('build', 'run'))
    depends_on('git',              type=('run'))
    depends_on('tk',               type=('run'))

    def setup_environment(self, spack_env, run_env):
        run_env.set('PBR_VERSION', str(self.spec.version))
