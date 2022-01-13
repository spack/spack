# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAtlalign(PythonPackage):
    """Blue Brain multi-modal registration and alignment toolbox."""

    homepage = "https://pypi.org/project/atlalign/"
    url = "https://files.pythonhosted.org/packages/74/b8/4382a758e4ccf5de26e35fb2b33863aea27b99e31e1ce9b4bc1e6bb593ef/atlalign-0.6.0.tar.gz"

    # The first version below just serves to trigger a rebuild!
    version('0.6.0.20210902', url=url, sha256='ecd74c89ecdca0a115252fa662e41b272dff2cdc3ea0d459daa5b7a672070b7c')
    version('0.6.0', sha256='ecd74c89ecdca0a115252fa662e41b272dff2cdc3ea0d459daa5b7a672070b7c')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-antspyx@0.2.7', type=('run'))
    depends_on('py-imgaug@:0.2', type=('run'))
    depends_on('py-matplotlib@3.0.3:', type=('run'))
    depends_on('py-mlflow', type=('run'))
    depends_on('py-nibabel@2.4.0:', type=('run'))
    depends_on('py-numpy', type=('run'))
    depends_on('py-seaborn', type=('run'))
    depends_on('py-scikit-image@0.16.0:', type=('run'))
    depends_on('py-scikit-learn@0.20.2:', type=('run'))
    depends_on('py-scipy', type=('run'))
    # Addons need to be in lockstep with TF
    depends_on('py-tensorflow@2.4:', type=('run'))
    depends_on('py-tensorflow-addons', type=('run'))

    patch('lpips.patch', when='@0.6.0')

    def patch(self):
        filter_file('"tensorflow>=[0-9.]+",', '', 'setup.py')
