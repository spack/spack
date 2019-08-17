# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMoltemplate(PythonPackage):
    """Moltemplate is a general cross-platform text-based molecule builder for
    LAMMPS."""

    homepage = "http://moltemplate.org"
    url      = "https://github.com/jewettaij/moltemplate/archive/v2.5.8.tar.gz"

    version('2.5.8', '9e127a254a206222e8a31684780f8dba')

    depends_on('python@2.7:',   type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
