# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzuremlDataprep(Package):
    """Azure ML Data Preparation SDK."""

    homepage = "http://aka.ms/data-prep-sdk"
    url      = "https://pypi.io/packages/py3/a/azureml_dataprep/azureml_dataprep-1.8.2-py3-none-any.whl"

    version('1.8.2', sha256='e53f3206f0bd4af8d5e7de3a94c2c6e662902b86e94a7b9d930e36329fe5820f', expand=False)

    variant('fuse', default=False, description='Build with FUSE support')

    extends('python')
    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-pip', type='build')
    depends_on('py-dotnetcore2@2.1.14:', type=('build', 'run'))
    depends_on('py-azureml-dataprep-native@14.2.1:14.999', type=('build', 'run'))
    depends_on('py-cloudpickle@1.1.0:', type=('build', 'run'))
    depends_on('py-azure-identity@1.2.0:1.2.999', type=('build', 'run'))
    depends_on('py-fusepy@3.0.1:', when='+fuse', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
