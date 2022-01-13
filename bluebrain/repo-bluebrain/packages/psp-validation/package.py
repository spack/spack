# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PspValidation(PythonPackage):
    """PSP analysis tools"""

    homepage = "https://bbpgitlab.epfl.ch/nse/psp-validation/"
    git      = "git@bbpgitlab.epfl.ch:nse/psp-validation.git"

    version('develop', branch='master')
    version('0.4.0', tag='psp-validation-v0.4.0')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-attrs@20.3.0:', type='run')
    depends_on('py-click@7.0:7.999', type='run')
    depends_on('py-h5py@3:3.999', type='run')
    depends_on('py-joblib@0.16:', type='run')
    depends_on('py-numpy@1.10:', type='run')
    depends_on('py-tqdm@4.0:', type='run')
    depends_on('py-bglibpy@4.4.27:4.999', type='run')
    depends_on('py-bluepy@2.1:2.999', type='run')
    depends_on('py-efel@3.0.39:', type='run')
    depends_on('neuron+python@7.8:', type='run')
