##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class PyGitReview(PythonPackage):
    """git-review is a tool that helps submitting git branches to gerrit"""

    homepage = "http://docs.openstack.org/infra/git-review"
    url = "https://pypi.io/packages/source/g/git-review/git-review-1.25.0.tar.gz"

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
        run_env.set('PBR_VERSION', self.spec.version)
