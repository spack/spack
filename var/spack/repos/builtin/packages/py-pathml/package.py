# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

class PyPathml(PythonPackage):
    """An open-source toolkit for computational pathology and machine learning."""

    homepage = "https://github.com/Dana-Farber-AIOS/pathml"
    pypi     = "pathml/pathml-2.1.0.tar.gz"

    version('2.1.0', sha256='462bb2f16452dddad310c30f62678a1336ce492263355fd6722c07ee4840ea6a')

    depends_on('py-setuptools@42:', type='build')
    depends_on('py-numpy@1.16.4:')
    depends_on('py-pandas')
    depends_on('py-scipy')
    depends_on('py-pydicom')
    depends_on('py-statsmodels')
    depends_on('py-openslide-python')
    depends_on('py-matplotlib')
    depends_on('py-scikit-image')
    depends_on('py-scikit-learn')
    depends_on('py-dask +distributed')
    depends_on('py-anndata@0.7.6:')
    depends_on('py-scanpy')
    depends_on('py-torch')
    depends_on('py-opencv-contrib-python')
    depends_on('py-python-bioformats@4.0.0:')
    depends_on('py-loguru')
