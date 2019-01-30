# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyStevedore(PythonPackage):
    """Manage Dynamic Plugins for Python Applications."""

    homepage = "https://docs.openstack.org/stevedore/latest/"
    url      = "https://pypi.io/packages/source/s/stevedore/stevedore-1.28.0.tar.gz"

    version('1.28.0', 'b736a71431a2ff5831bbff4a6ccec0c1')

    depends_on('python@2.6:')

    depends_on('py-six@1.10.0:', type=('build', 'run'))
    depends_on('py-pbr@2.0.0:2.1.0', type=('build', 'run'))
