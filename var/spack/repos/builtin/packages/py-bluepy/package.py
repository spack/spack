# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBluepy(PythonPackage):
    """Pythonic Blue Brain data access API"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/bluepy"
    git      = "ssh://bbpcode.epfl.ch/nse/bluepy"

    version('2.4.1', tag='bluepy-v2.4.1')
    version('2.3.0', tag='bluepy-v2.3.0')
    version('2.2.0', tag='bluepy-v2.2.0')
    version('2.1.0', tag='bluepy-v2.1.0')
    version('2.0.0', tag='bluepy-v2.0.0')
    version('0.16.0', tag='bluepy-v0.16.0')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-libsonata@0.1.7:', type='run')
    depends_on('py-pandas@1.0.0:', type='run', when='@2.0.0:')
    depends_on('py-bluepy-configfile@0.1.11:', type='run')
    depends_on('py-numpy@1.8:', type='run')

    # the version of bluepy <2 needed multiple dependencies compatible
    # with h5py < 3.0.0 and bluepy > 2 needs h5py > 3.0.0. Hence the
    # following switches :
    # h5py
    depends_on('py-h5py@3.0.0:', type='run', when='@2.0.0:')
    depends_on('py-h5py@2.3:2.99', type='run', when='@:1.0.0')

    # neurom
    depends_on('py-neurom@1.6.0:1.99.99', type='run', when='@2.0.0:2.2.0')
    depends_on('py-neurom@1.4.18:1.5.99', type='run', when='@:1.0.0')

    # py-lru
    depends_on('py-pylru@1.2:', type='run', when='@:2.2.9')

    # morph-tool
    depends_on('py-morph-tool@2.5.1:2.999', type='run', when='@2.3.0:')

    # morphio
    depends_on('py-morphio@3.0.1:3.999', type='run', when='@2.3.0:')

    # voxcell
    depends_on('py-voxcell@3.0.0:', type='run', when='@2.0.0:')
    depends_on('py-voxcell@2.7.4:2.99', type='run', when='@0.14.16:0.16.0')

    # bluepysnap
    depends_on('py-bluepysnap@0.12.0:0.999', type='run', when='@2.3.0:')
    depends_on('py-bluepysnap@0.10.0:0.999', type='run', when='@2.2.0:')
    depends_on('py-bluepysnap@0.8.0:0.999', type='run', when='@2.0.0:')
    depends_on('py-bluepysnap@0.4.1:0.7.1', type='run', when='@:1.0.0')

    # lazy / cached properties (change of backend for caching)
    depends_on('py-cached-property@1.0:', type='run', when='@2.0.0:')
    depends_on('py-lazy@1.0:', type='run', when='@:1.0.0')

    # brion changed package name in 3.3.0 and brion bump in bluepy==2.1.0
    depends_on('brion+python@3.1.0:3.2.0', type='run', when='@:2.0.9')
    depends_on('brion+python@3.3.0:', type='run', when='@2.1.0:')

    @property
    def import_modules(self):
        if self.version < Version('2.0.0'):
            # don't run import tests on older versions
            return []
        # bluepy.index requires libFLATIndex, unavailable on spack
        modules = super(PyBluepy, self).import_modules
        return [m for m in modules if m != 'bluepy.index']
