# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBluepy(PythonPackage):
    """Pythonic Blue Brain data access API"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/bluepy"
    git      = "ssh://bbpcode.epfl.ch/nse/bluepy"

    version('develop', branch='master')
    version('0.13.0', tag='bluepy-v0.13.0', preferred=True)
    version('0.12.7', tag='bluepy-v0.12.7')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-enum34@1.0:', type='run', when='^python@:3.3.99')
    depends_on('py-h5py~mpi@2.3:', type='run')
    depends_on('py-lazy@1.0:', type='run')
    depends_on('py-lxml@3.3:', type='run')
    depends_on('py-neurom@1.3:', type='run')
    depends_on('py-numpy@1.8:', type='run')
    depends_on('py-pandas@0.17:', type='run')
    depends_on('py-pylru@1.0:', type='run')
    depends_on('py-pyyaml@3.10:', type='run')
    depends_on('py-six@1.0:', type='run')
    depends_on('py-sqlalchemy@1.0:', type='run')

    depends_on('py-bluepy-configfile@0.1:', type='run')

    # TODO: remove once legacy dependencies are removed from BluePy
    def patch(self):
        filter_file("'jsonschema>=2.3.0',", "", "setup.py")
        filter_file("'progressbar2>=3.18',", "", "setup.py")
        filter_file("'shapely>=1.3.2',", "", "setup.py")
