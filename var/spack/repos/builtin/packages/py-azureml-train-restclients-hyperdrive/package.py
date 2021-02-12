# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzuremlTrainRestclientsHyperdrive(Package):
    """The azureml-train-restclients-hyperdrive contains functionality for
    azureml-train metapackage."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url      = "https://pypi.io/packages/py3/a/azureml_train_restclients_hyperdrive/azureml_train_restclients_hyperdrive-1.11.0-py3-none-any.whl"

    version('1.22.0', sha256='f07686c3590f7c75bd55c50ad7390243a5873a1d345bbded6750f7675b7f8e91')
    version('1.21.0', sha256='8c71c2b4bc9876039e14865fee2303d2067311fc19cd8d54fe86e71721fa5110')
    version('1.20.0', sha256='054f6705389419e4f3a96d92e926923f3d9f3b728947f1ef78e58bc11a45230c')
    version('1.19.0', sha256='36b685fcdd90cea13b348e64c71b58300da10d9b08272d2c3cd4214c2c4e2aaa')
    version('1.18.0', sha256='d5db56701de878fc6d92514e80a28d8c180fb8c5933a2a0c3aba92f680fbc751')
    version('1.17.0', sha256='478b6fb5828e8baa4c865f0056a48a38e1916c17e6fb07bbd89e87802815be61')
    version('1.16.0', sha256='17d9cdee85defb49a2057ea7d353b91839c38d8efdc97d717bf28005c833c99c')
    version('1.15.0', sha256='333800be9216ea0a8c113ce355dbd66983dee935b48200eab8a2c01a72a421a9')
    version('1.14.0', sha256='4b793da0a25dbaccfe9113a06e219bd0e70d84afe206b970fc8eb6ae808f9670')
    version('1.13.0', sha256='4cd1eaf3c61e21a665a30f4e5e713b2cd28272638b7221ccea28eacbb5d983d2')
    version('1.12.0', sha256='d280c2a465074ce0ced3e8b69132db39eeff3addb535dc937c40ea5238f474c4')
    version('1.11.0', sha256='8bc6f9676a9f75e6ee06d201c418ea904c24e854f26cf799b08c259c3ac92d13', expand=False)
    version('1.8.0',  sha256='1633c7eb0fd96714f54f72072ccf1c5ee1ef0a8ba52680793f20d27e0fd43c87', expand=False)

    extends('python')
    depends_on('python@3.5:3.999', type=('build', 'run'))
    depends_on('py-pip', type='build')
    depends_on('py-requests@2.19.1:', type=('build', 'run'))
    depends_on('py-msrest@0.5.1:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.33:', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
