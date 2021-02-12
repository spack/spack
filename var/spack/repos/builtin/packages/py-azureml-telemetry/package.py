# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzuremlTelemetry(Package):
    """Machine learning (ML) telemetry package is used to collect telemetry
    data."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url      = "https://pypi.io/packages/py3/a/azureml_telemetry/azureml_telemetry-1.11.0-py3-none-any.whl"

    version('1.22.0', sha256='f0f741144b0a1d7ec32ceda3239fc93f377b94c0f7946883b469e806fcf3f0e0')
    version('1.21.0', sha256='6b08989748d18128cf87c1db3deb10bd9b3a4d9697b9f3d62381acf2473a1cb5')
    version('1.20.0', sha256='14243df255b6a17cb643352ca66207955a7cea38cff5f0c2cb2e0b326dd22f5b')
    version('1.19.0', sha256='07114bf812f9f200eb4c5733c2213141cf0c94f9e85ea84607617a68609e25f9')
    version('1.18.0', sha256='f4d7c18d4a0036bc7491032a4d3a144d9c090bc1ee308d174a5d3fe35a438f22')
    version('1.17.0', sha256='83d6f378aaaadce8b9ac56c8024435242baea78352b33b3b07a3d3ad8c4b9fa6')
    version('1.16.0', sha256='741187370c36722cdcca946a92672dc5daa6ddac4e906dee990d620d18a04f66')
    version('1.15.0', sha256='f5a720043b462ee66d2f4719f2a38908f493e46010eaafe9dd326818fc501bbf')
    version('1.14.0', sha256='866b649a9db3c27ea2ec7ce5f246002cfdb1c2610d3b4f6d1da65797f525900d')
    version('1.13.0', sha256='c3565a9868689b7804479244a0ef179a5144d647baeddbe7cc54a3178d683c64')
    version('1.12.0', sha256='0cb6fbdb037d99d99bb7f1b34132b136c56b64047e21af856ee8df41a29129aa')
    version('1.11.0', sha256='0d46c4a7bb8c0b188f1503504a6029384bc2237d82a131e7d1e9e89c3491b1fc', expand=False)
    version('1.8.0',  sha256='de657efe9773bea0de76c432cbab34501ac28606fe1b380d6883562ebda3d804', expand=False)

    extends('python')
    depends_on('python@3.5:3.999', type=('build', 'run'))
    depends_on('py-pip', type='build')
    depends_on('py-applicationinsights', type=('build', 'run'))

    depends_on('py-azureml-core@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))

    depends_on('py-azureml-core@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
