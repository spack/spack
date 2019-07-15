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
    version('0.1.12', tag='psp-validation-v0.1.12', preferred=True)

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@7.0:7.999', type='run')
    depends_on('py-future@0.16:', type='run')
    depends_on('py-h5py~mpi@2.7:', type='run')
    depends_on('py-joblib@0.13:', type='run')
    depends_on('py-numpy@1.10:', type='run')
    depends_on('py-tqdm@4.0:', type='run')

    depends_on('py-bglibpy@4.0.17', type='run')
    depends_on('py-bluepy@0.13.3:', type='run')
