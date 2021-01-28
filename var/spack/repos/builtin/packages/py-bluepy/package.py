# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBluepy(PythonPackage):
    """Pythonic Blue Brain data access API"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/bluepy"
    git      = "ssh://bbpcode.epfl.ch/nse/bluepy"

    version('2.0.0', tag='bluepy-v2.0.0')
    version('0.16.0', tag='bluepy-v0.16.0')
    version('0.14.15', tag='bluepy-v0.14.15')
    version('0.14.14', tag='bluepy-v0.14.14')
    version('0.14.13', tag='bluepy-v0.14.13')
    version('0.14.12', tag='bluepy-v0.14.12')
    version('0.14.8', tag='bluepy-v0.14.8')
    version('0.14.7', tag='bluepy-v0.14.7')
    version('0.14.6', tag='bluepy-v0.14.6')
    version('0.14.5', tag='bluepy-v0.14.5')
    version('0.14.3', tag='bluepy-v0.14.3')
    version('0.14.1', tag='bluepy-v0.14.1')
    version('0.13.5', tag='bluepy-v0.13.5')
    version('0.12.7', tag='bluepy-v0.12.7')

    depends_on('py-setuptools', type=('build', 'run'))

    # the version of bluepy <2 needed multiple dependencies compatible
    # with h5py < 3.0.0 and bluepy > 2 needs h5py > 3.0.0. Hence the
    # following switches :

    # h5py
    depends_on('py-h5py~mpi@3.0.0:', type='run', when='@2.0.0:')
    depends_on('py-h5py~mpi@2.3:2.99', type='run', when='@:1.0.0')

    # neurom
    depends_on('py-neurom@1.6.0:', type='run', when='@2.0.0:')
    depends_on('py-neurom@1.4.18:', type='run', when='@:1.0.0')

    # voxcell
    depends_on('py-voxcell@3.0.0', type='run', when='@2.0.0:')
    depends_on('py-voxcell@2.7.4:2.99', type='run', when='@0.14.16:0.16.0')
    depends_on('py-voxcell@:2.7.3', type='run', when='@:0.14.15')

    # bluepysnap
    depends_on('py-bluepysnap@0.9.0:', type='run', when='@2.0.0:')
    depends_on('py-bluepysnap@0.4.1:0.7.1', type='run', when='@:1.0.0')

    # pandas
    depends_on('py-pandas@1.0.0:', type='run', when='@2.0.0:')
    depends_on('py-pandas@0.17:', type='run', when='@:1.0.0')

    # lazy / cached properties (change of backend for caching)
    depends_on('py-cached-property@1.0:', type='run', when='@2.0.0:')
    depends_on('py-lazy@1.0:', type='run', when='@:1.0.0')

    # common to bluepy <2 and >2 versions
    depends_on('py-libsonata@0.1.6:', type='run', when='^python@3.6:')
    depends_on('py-libsonata@0.1.3:0.1.4', type='run', when='^python@:3.5.99')

    depends_on('brion+python@3.1.0:', type='run')
    depends_on('py-bluepy-configfile@0.1.11:', type='run')
    depends_on('py-numpy@1.8:', type='run')
    depends_on('py-pylru@1.2:', type='run')

    # for old versions of bluepy <2.0.0
    depends_on('py-enum34@1.0:', type='run', when='^python@:3.3.99')
    depends_on('py-lxml@3.3:', type='run', when='@:1.0.0')
    depends_on('py-pyyaml@3.10:', type='run', when='@:1.0.0')
    depends_on('py-six@1.0:', type='run', when='@:1.0.0')
    depends_on('py-sqlalchemy@1.0:', type='run', when='@:1.0.0')
    depends_on('py-pyrsistent@:0.17', type='run', when='@:1.0.0')

    # TODO: remove once legacy dependencies are removed from BluePy
    def patch(self):
        filter_file("'jsonschema>=2.3.0',", "", "setup.py")
        filter_file("'progressbar2>=3.18',", "", "setup.py")
        filter_file("'shapely>=1.3.2',", "", "setup.py")
