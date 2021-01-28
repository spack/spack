# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PspValidation(PythonPackage):
    """PSP analysis tools"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/psp-validation"
    git      = "ssh://bbpcode.epfl.ch/nse/psp-validation"

    version('develop', branch='master')
    version('0.3.3', tag='psp-validation-v0.3.3')
    version('0.3.1', tag='psp-validation-v0.3.1')
    version('0.3.0', tag='psp-validation-v0.3.0')
    version('0.2.1', tag='psp-validation-v0.2.1')
    version('0.2.0', tag='psp-validation-v0.2.0')
    version('0.1.19', tag='psp-validation-v0.1.19')
    version('0.1.14', tag='psp-validation-v0.1.14')
    version('0.1.12', tag='psp-validation-v0.1.12')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-attrs', type='run')
    depends_on('py-click@7.0:7.999', type='run')
    depends_on('py-future@0.16:', when='@:0.2.1', type='run')
    depends_on('py-h5py~mpi@2.7:2.999', type='run')
    depends_on('py-joblib@0.13:', type='run')
    depends_on('py-numpy@1.10:', type='run')
    depends_on('py-tqdm@4.0:', type='run')
    depends_on('py-bglibpy@4.3.15:4.999', type='run')
    depends_on('py-bluepy@0.16.0:1.999', type='run')
    depends_on('py-efel@3.0.39:', type='run')
    depends_on('neuron+python@7.8:', when='@0.2.2:', type='run')

    depends_on('py-mock@3.0.5', when='@:0.3.1', type='build')  # remove in 2020
