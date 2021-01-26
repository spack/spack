# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDeeplabcut(PythonPackage):
    """DeepLabCut is an efficient method for 3D markerless pose
    estimation based on transfer learning with deep neural
    networks that achieves excellent results (i.e. you can
    match human labeling accuracy) with minimal training data
    (typically 50-200 frames)."""

    homepage = "http://www.mousemotorlab.org/deeplabcut"
    url      = "https://github.com/DeepLabCut/DeepLabCut/archive/v2.2b8.tar.gz"

    version('2.2b8',   sha256='eb6180741bb7eab173e09118bad60551b3c9ab2c8d4ed68460979105137fe72e')

    depends_on('py-setuptools', type='build')
    depends_on("py-bayesian-optimization", type=('build', 'run'))
    depends_on("py-certifi", type=('build', 'run'))
    depends_on("py-chardet", type=('build', 'run'))
    depends_on("py-click", type=('build', 'run'))
    depends_on("py-cython", type=('build', 'run'))
    depends_on("py-easydict", type=('build', 'run'))
    depends_on("py-filterpy", type=('build', 'run'))
    depends_on("py-h5py", type=('build', 'run'))
    depends_on("py-intel-openmp", type=('build', 'run'))
    depends_on("py-imgaug", type=('build', 'run'))
    depends_on("py-ipython", type=('build', 'run'))
    depends_on("py-ipython-genutils", type=('build', 'run'))
    depends_on("py-numba@0.51.1", type=('build', 'run'))
    depends_on("py-matplotlib@3.1.3", type=('build', 'run'))
    depends_on("py-moviepy@:1.0.1", type=('build', 'run'))
    depends_on("py-numpy@1.16.4:1.999", type=('build', 'run'))
    # depends_on("py-opencv-python-headless", type=('build', 'run'))
    depends_on("opencv+python", type=('build', 'run'))
    depends_on("py-pandas@1.0.1:", type=('build', 'run'))
    depends_on("py-patsy", type=('build', 'run'))
    depends_on("py-python-dateutil", type=('build', 'run'))
    depends_on("py-pyyaml", type=('build', 'run'))
    depends_on("py-requests", type=('build', 'run'))
    depends_on("py-ruamel-yaml@0.15.0:", type=('build', 'run'))
    depends_on("py-setuptools", type=('build', 'run'))
    depends_on("py-scikit-image", type=('build', 'run'))
    depends_on("py-scikit-learn", type=('build', 'run'))
    depends_on("py-scipy@1.4:", type=('build', 'run'))
    depends_on("py-six", type=('build', 'run'))
    depends_on("py-statsmodels@0.11:", type=('build', 'run'))
    depends_on("py-tables", type=('build', 'run'))
    depends_on("py-tensorpack@0.9.8", type=('build', 'run'))
    depends_on("py-tqdm", type=('build', 'run'))
    depends_on("py-wheel", type=('build', 'run'))
