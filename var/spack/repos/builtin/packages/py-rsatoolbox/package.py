# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRsatoolbox(PythonPackage):
    """Representational Similarity Analysis (RSA) in Python."""

    homepage = "https://github.com/rsagroup/rsatoolbox"
    pypi     = "rsatoolbox/rsatoolbox-0.0.3.tar.gz"

    version('0.0.3', sha256='9bf6e16d9feadc081f9daaaaab7ef38fc1cd64dd8ef0ccd9f74adb5fe6166649')

    depends_on('py-setuptools', type='build')
    depends_on('py-coverage', type=('build', 'run'))
    depends_on('py-numpy@1.21.2:', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-scikit-learn', type=('build', 'run'))
    depends_on('py-scikit-image', type=('build', 'run'))
    depends_on('py-tqdm', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-joblib', type=('build', 'run'))

    def patch(self):
        # tests are looking for a not existing requirements.txt file
        with working_dir('tests'):
            open('requirements.txt', 'a').close()
