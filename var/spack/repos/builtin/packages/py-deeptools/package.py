# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDeeptools(PythonPackage):
    """deepTools addresses the challenge of handling the large amounts of data
       that are now routinely generated from DNA sequencing centers."""

    homepage = "https://pypi.io/packages/source/d/deepTools"
    # The test suite and associated test data is missing in the pypi tarball.
    url      = "https://files.pythonhosted.org/packages/f6/f3/789edda975fcca4736fab2007d82cab2e86739901c88bb0528db5c338d1f/deepTools-3.5.0.tar.gz"

    version('3.5.0', sha256='1a14a29e60be13eac11bd204dab9aef73cd72fe56a94c587333f21087584c0d8')
    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.9.0:', type=('build', 'run'))
    depends_on('py-scipy@0.17.0:', type=('build', 'run'))
    depends_on('py-matplotlib@3.1.0:', type=('build', 'run'))
    depends_on('py-pysam@0.14.0:', type=('build', 'run'))
    depends_on('py-numpydoc@0.5:', type=('build', 'run'))
    depends_on('py-pybigwig@0.2.1:', type=('build', 'run'))
    depends_on('py-py2bit@0.2.0:', type=('build', 'run'))
    depends_on('py-plotly@2.0.0:', type=('build', 'run'))
    depends_on('py-deeptoolsintervals@0.1.8:', type=('build', 'run'))
