# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMultiqc(PythonPackage):
    """MultiQC is a tool to aggregate bioinformatics results across many
    samples into a single report. It is written in Python and contains modules
    for a large number of common bioinformatics tools."""

    homepage = "https://multiqc.info"
    url      = "https://pypi.io/packages/source/m/multiqc/multiqc-1.0.tar.gz"

    version('1.5', 'c9fc5f54a75b1d0c3e119e0db7f5fe72')
    version('1.3', '78fef8a89c0bd40d559b10c1f736bbcd')
    version('1.0', '0b7310b3f75595e5be8099fbed2d2515')

    depends_on('python@2.7:')
    depends_on('py-setuptools', type='build')
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-jinja2@2.9:', type=('build', 'run'))
    depends_on('py-lzstring', type=('build', 'run'))
    depends_on('py-future@0.14.1:', type=('build', 'run'))
    depends_on('py-spectra@0.0.10:', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-simplejson', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'), when='@1.5:')
    depends_on('py-enum34', type=('build', 'run'), when='@1.5:')
    depends_on('py-markdown', type=('build', 'run'), when='@1.5:')
