# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzuremlPipelineSteps(Package):
    """Represents a unit of computation in azureml-pipeline."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url      = "https://pypi.io/packages/py3/a/azureml_pipeline_steps/azureml_pipeline_steps-1.8.0-py3-none-any.whl"

    version('1.8.0', sha256='3310674207ed457a26fb978e7168e400306c695f7f854f354dee9d5c7c81304c', expand=False)

    extends('python')
    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-pip', type='build')
    depends_on('py-azureml-train-core@1.8.0:1.8.999', type=('build', 'run'))
    depends_on('py-azureml-train-automl-client@1.8.0:1.8.999', type=('build', 'run'))
    depends_on('py-azureml-pipeline-core@1.8.0:1.8.999', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
