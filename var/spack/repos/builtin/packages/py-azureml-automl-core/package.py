# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzuremlAutomlCore(Package):
    """The azureml-automl-core package is a package containing functionality
    used by the azureml-train-automl package."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url      = "https://pypi.io/packages/py3/a/azureml_automl_core/azureml_automl_core-1.11.0-py3-none-any.whl"

    version('1.22.0', sha256='5d75d826eca8656a109092fb3abc34b82c5b08b692fb5577b3d30eb40cc2b2f5')
    version('1.21.0', sha256='9c7fface4f801dd3d4290306777101be89b8d350d32d67c817f12b9c57d63f1e')
    version('1.20.0', sha256='ef021531c9b4d0573c604d643c21e451fcdd82f83bf1bd04384e91fa2ab0a3f8')
    version('1.19.0', sha256='48bac9cc1a2e673fcff659313782dae2177fc77ea7bc237282ed37721895ab1e')
    version('1.18.0', sha256='bedc2a87b02e4db4080c185082e0c55167e2f1aec5a87b869a8b8f14a087765b')
    version('1.17.0', sha256='4448450fb9e2778cb2531c279f99dc72d66c0eed85c881f16a62e9aeb9079518')
    version('1.16.0', sha256='39941a9b39099e63dbcdde08b6cb96262f30b1cf88efea54641267b3a945f549')
    version('1.15.0', sha256='cc5612d05224df82e6c657dc41b194901881fa8b12f6fc9107472bcbdff4c9f3')
    version('1.14.0', sha256='ae736534fe660431bea3999d575ce2f2e81cf66e54d2e0a83ca5c4a8b3fca8d8')
    version('1.13.0', sha256='e4bd76f474362362d215216528ccdb7a4c5938cb2a80899c572673ffb16085f5')
    version('1.12.0', sha256='dfb67c03cb48f74f804a2d841670f53be3ff1e9400f5c9d136b7b44ec167e8b9')
    version('1.11.0', sha256='da1b9cef9aabbfaee69a19d5e15f5a911eefbd126546738343a78c032860b5a5', expand=False)
    version('1.8.0',  sha256='58ce54b01570996cda860c0c80693b8db19324785a356573f105afeaa31cae6c', expand=False)

    extends('python')
    depends_on('python@3.5:3.999', type=('build', 'run'))
    depends_on('py-pip', type='build')

    depends_on('py-azureml-dataset-runtime@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))
    depends_on('py-azureml-telemetry@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))

    depends_on('py-azureml-dataprep@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))
    depends_on('py-azureml-telemetry@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
