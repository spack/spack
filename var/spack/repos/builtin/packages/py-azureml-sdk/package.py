# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzuremlSdk(Package):
    """Microsoft Azure Machine Learning Python SDK."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url      = "https://pypi.io/packages/py3/a/azureml_sdk/azureml_sdk-1.8.0-py3-none-any.whl"

    maintainers = ['adamjstewart']

    version('1.8.0', sha256='61107db1403ce2c1a12064eb0fa31a1d075debbf32dd17cb93b7639b615b7839', expand=False)

    extends('python')
    depends_on('python@3.5:3.999', type=('build', 'run'))
    depends_on('py-pip', type='build')

    # For version 1.8.0, dependencies are locked to ~= 1.8.0
    for ver in ['1.8.0']:
        ver = Version(ver)
        for dep in [
            'core', 'train', 'train-automl-client', 'pipeline',
            'dataprep+fuse'
        ]:
            depends_on('py-azureml-{0}@{1}:{2}.999'.format(
                dep, ver, ver.up_to(2)
            ), when='@{0}'.format(ver), type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
