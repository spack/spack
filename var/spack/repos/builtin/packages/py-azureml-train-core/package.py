# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzuremlTrainCore(Package):
    """The azureml-train-core contains functionality used by azureml-train
    metapackage."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url      = "https://pypi.io/packages/py3/a/azureml_train_core/azureml_train_core-1.8.0-py3-none-any.whl"

    version('1.8.0', sha256='5a8d90a08d4477527049d793feb40d07dc32fafc0e4e57b4f0729d3c50b408a2', expand=False)

    extends('python')
    depends_on('python@3.5:3.999', type=('build', 'run'))
    depends_on('py-pip', type='build')
    depends_on('py-azureml-train-restclients-hyperdrive@1.8.0:1.8.999', type=('build', 'run'))
    depends_on('py-azureml-core@1.8.0:1.8.999', type=('build', 'run'))
    depends_on('py-azureml-telemetry@1.8.0:1.8.999', type=('build', 'run'))
    depends_on('py-flake8@3.1.0:3.7.9', when='^python@3.6:', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
