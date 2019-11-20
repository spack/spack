# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGriddataformats(PythonPackage):
    """The gridDataFormats package provides classes to unify reading
    and writing n-dimensional datasets. One can read grid data from
    files, make them available as a Grid object, and write out the
    data again."""

    homepage = "http://www.mdanalysis.org/GridDataFormats"
    url      = "https://pypi.io/packages/source/G/GridDataFormats/GridDataFormats-0.3.3.tar.gz"

    version('0.3.3', sha256='938f0efcb3bc2f58ec85048b933942da8a52c134170acc97cb095f09d3698fbd')

    depends_on('python@2.7:')
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.0.3:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
