# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzuremlTrainCore(Package):
    """The azureml-train-core contains functionality used by azureml-train
    metapackage."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url      = "https://pypi.io/packages/py3/a/azureml_train_core/azureml_train_core-1.11.0-py3-none-any.whl"

    version('1.22.0', sha256='bf8ad81d31a6a94158de98f577175a17ee59009965c262fc5edd88a1b9d34ff8')
    version('1.21.0', sha256='93284b78d99f84eca598c1378dae83dcd3b5f31aea7fb21b898ac313457cb0fc')
    version('1.20.0', sha256='7755ada5c7e09a39a40a6799ee5aeb9bf05430d7cca5bd158214e7dcf3dea8e0')
    version('1.19.0', sha256='3f4d573cc36154eaa0abe1af2edb9ecf674936ed62a71c8b272ca994caae45d1')
    version('1.18.0', sha256='a8f34b907a3a30558ffb0c0e3608407c1c4513fc99425779e5ff8046ae57fe86')
    version('1.17.0', sha256='6d5f0feaa566d40b8d49d071a774e638bb0da5db31825ba2adbd0ea7d8f5f686')
    version('1.16.0', sha256='550f0daf1635be01e470b2adade60013da11a30dccbf3eab7a6733ad70c941c4')
    version('1.15.0', sha256='be98b6a1b5cf5fce70bc6fc58d7e15b0fb82bb13d292a9db91e57d65bacb7e58')
    version('1.14.0', sha256='2c3b9542acd6a780100ec5d933e3449fc99404a55f68b9e3d88236c4af5567b3')
    version('1.13.0', sha256='62e1b3afeb11eee0005aeefbd23dd5e5a13b11a97499bc6e213ef8dea2e9b678')
    version('1.12.0', sha256='445969a41e8c219843a8055950f3b75e8f86e1349b97739e5e59f8a1ad167326')
    version('1.11.0', sha256='1b5fd813d21e75cd522d3a078eba779333980a309bcff6fc72b74ddc8e7a26f1', expand=False)
    version('1.8.0',  sha256='5a8d90a08d4477527049d793feb40d07dc32fafc0e4e57b4f0729d3c50b408a2', expand=False)

    extends('python')
    depends_on('python@3.5:3.999', type=('build', 'run'))
    depends_on('py-pip', type='build')

    depends_on('py-azureml-train-restclients-hyperdrive@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))
    depends_on('py-azureml-core@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))
    depends_on('py-azureml-telemetry@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))

    depends_on('py-azureml-train-restclients-hyperdrive@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))
    depends_on('py-azureml-core@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))
    depends_on('py-azureml-telemetry@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))
    depends_on('py-flake8@3.1.0:3.7.9', when='@1.8.0 ^python@3.6:', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
