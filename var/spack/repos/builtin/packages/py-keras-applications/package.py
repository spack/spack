# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyKerasApplications(PythonPackage):
    """
    Keras Applications is the applications module of the Keras deep learning
    library.  It provides model definitions and pre-trained weights for a
    number of popular archictures, such as VGG16, ResNet50, Xception,
    MobileNet, and more.
    """

    homepage = "https://github.com/keras-team/keras-applications"
    url      = "https://github.com/keras-team/keras-applications/archive/1.0.6.tar.gz"

    version('1.0.6', 'ae4926c3d973da42c68320372aa4b63c')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.9.1:', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
