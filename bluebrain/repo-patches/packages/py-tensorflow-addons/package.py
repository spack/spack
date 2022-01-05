# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTensorflowAddons(Package):
    """
    TensorFlow Addons is a repository of contributions that conform to
    well-established API patterns, but implement new functionality not
    available in core TensorFlow. TensorFlow natively supports a large number
    of operators, layers, metrics, losses, and optimizers. However, in a fast
    moving field like ML, there are many interesting new developments that
    cannot be integrated into core TensorFlow (because their broad
    applicability is not yet clear, or it is mostly used by a smaller subset
    of the community).
    """

    homepage = "https://pypi.org/project/tensorflow-addons/"
    url = "https://files.pythonhosted.org/packages/ac/08/6f02e247aeb0d93d04d8ddc435eb007b76e8991f415cb56ac568748e1530/tensorflow_addons-0.13.0-cp39-cp39-manylinux2010_x86_64.whl"

    # The version below just serves to trigger a rebuild!
    version('0.13.0', sha256='845bf0d87985cb4fe7d2011d5b79351e01f216e68910a6fe30ecf23ca135c5ad', expand=False)
    version('0.12.1', url="https://files.pythonhosted.org/packages/08/ac/c5a37833dd71acbb6ccc40847680f2882231acb6dca4c19a2b975f3a358d/tensorflow_addons-0.12.1-cp38-cp38-manylinux2010_x86_64.whl", sha256='288919ec1debf0bc56357fc1db6dccd27389d446b214042cd4de39d7edabdad6', expand=False)

    maintainers = ['pramodk']
    import_modules = ['tensorflow_addons']

    extends('python')
    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-pip', type='build')

    depends_on('py-setuptools', type='build')
    depends_on('py-tensorflow@2.5', type=('run'), when='@0.13:')
    depends_on('py-tensorflow@2.4.0:2.4.2', type=('run'), when='@0.12.1')
    depends_on('py-typeguard@2.7:', type=('run'))
    # no versions for Mac OS added
    conflicts('platform=darwin', msg='macOS is not supported')

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def import_module_test(self):
        with working_dir('spack-test', create=True):
            for module in self.import_modules:
                python('_c', 'import {0}'.format(module))
