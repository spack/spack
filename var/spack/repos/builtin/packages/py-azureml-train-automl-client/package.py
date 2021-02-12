# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzuremlTrainAutomlClient(Package):
    """The azureml-train-automl-client package contains functionality for
    automatically finding the best machine learning model and its parameters,
    given training and test data."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url      = "https://pypi.io/packages/py3/a/azureml_train_automl_client/azureml_train_automl_client-1.11.0-py3-none-any.whl"

    version('1.22.0', sha256='bfccb2e7ef388478e8327e8616a9bca19273d7093998be97273cb12bc2f1c0d8')
    version('1.21.0', sha256='bb2a8fcf1da82b7f6c27ad6a3cdbc48ee9cd66f4638a90b04bad6af2dc134117')
    version('1.20.0', sha256='883f539b2db7d720e4b5bb1910f40db7914f334982d9b54b10e74c9ec462ba2a')
    version('1.19.0', sha256='4042718e2d6618f3d0ff4582498daed52e533bb8f48059b15e993fac1a953500')
    version('1.18.0', sha256='21e0c23e88aafd6b5166c58766bf3c2d83f9a6e211cc18638bf384b7c779029c')
    version('1.17.0', sha256='68c2b5b300166aa614fb90d600567718b54a286c9f3a7bfbda3c3d5eed07be3c')
    version('1.16.0', sha256='7c890bf3d3a736902566d1d6dccc2c296ceb2a61d054152d9e186d7f3dde422a')
    version('1.15.0', sha256='a8d0ff327525643f448ce9f41ddefd74812fff9b40be9bb1f040a2084808e967')
    version('1.14.0', sha256='0e670fd25737dea2e12e51eab87e584a7b9965061208422ee5ebdc2eb7b6d57b')
    version('1.13.0', sha256='55bc3ad8e0802403ac50fedf76974a1666b6ad6578ca8f7a92df1961d562702b')
    version('1.12.0', sha256='80ebb165acff92fe02688a58ccc0a0e2dafb5d44d4be22eac8667932c65d33b6')
    version('1.11.0', sha256='3184df60a46917e92140a299aecb54591b19df490a3f4f571ff1f92c5e70a715', expand=False)
    version('1.8.0',  sha256='562300095db6c4dea7b052e255c53dd95c4c3d0589a828b545497fe1ca7e9677', expand=False)

    extends('python')
    depends_on('python@3.5:3.999', type=('build', 'run'))
    depends_on('py-pip', type='build')

    depends_on('py-azureml-automl-core@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))
    depends_on('py-azureml-core@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))
    depends_on('py-azureml-dataset-runtime@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))
    depends_on('py-azureml-telemetry@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))

    depends_on('py-azureml-dataprep@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))
    depends_on('py-azureml-automl-core@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))
    depends_on('py-azureml-core@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))
    depends_on('py-azureml-telemetry@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
