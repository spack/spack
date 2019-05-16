# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyKerasPreprocessing(PythonPackage):
    """
    Keras Preprocessing is the data preprocessing and data augmentation module
    of the Keras deep learning library. It provides utilities for working with
    image data, text data, and sequence data.
    """

    homepage = "https://github.com/keras-team/keras-preprocessing"
    url      = "https://github.com/keras-team/keras-preprocessing/archive/1.0.5.tar.gz"

    version('1.0.5', '471738fb1be380b6cc747b39214b66b9')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.9.1:', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
