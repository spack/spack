# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBackportsWeakref(PythonPackage):
    """Backports of new features in Python's weakref module"""

    homepage = "https://github.com/PiDelport/backports.weakref"
    # Can't use pypi link as it doesn't have source files for the versions
    # indicated below.
    url      = "https://github.com/PiDelport/backports.weakref/archive/v1.0.tar.gz"

    version('1.0rc1', sha256='7826e249a0ccb382f1200e5f03c70a624537d4619f050e1c024ff18315550eed')
    version('1.0',    sha256='7e7457e61879db43b12b20d05acc3ef5bc6748adf37c6a4d9514316ba990a141')

    depends_on('py-setuptools', type='build')
