# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mosquitto(CMakePackage):
    """Mosquitto is an open source implementation of a server
       for version 5.0, 3.1.1, and 3.1 of the MQTT protocol."""

    homepage = 'https://mosquitto.org/N'
    git      = 'https://github.com/eclipse/mosquitto'
    url      = 'https://github.com/eclipse/mosquitto/archive/refs/tags/v2.0.14.zip'

    version('2.0.14', sha256='8efe7b24a1ca185a0de4f1d82b89fb6ec6715fba28a3b38d40306f398394ae4d')
    version('2.0.13', sha256='c3b01b7844bce6e8e5ead519503631302d15572cccada88402a423fc8fc51d2b')
    version('2.0.12', sha256='b8747b7c6e76f7aa89600df66c7eebda0eaf959d5efeed887ac6fe4a1fcd63d6')
    version('2.0.11', sha256='4265bac617c9352c9150b74726e52d63934c9b3421350b1ae4958ddda9cd8828')
    version('2.0.10', sha256='f92800163a87861f0e432aac490e37b31a0f96a5f23bb6442a50041345ac8cbd')
    version('2.0.9',  sha256='a88cf7e6cb3892a507750a8de3c88fea65e300b6e9cb7231f0fb3be2a877eb57')
    version('2.0.8',  sha256='a4946f139c20ef4cfdc14d8976a18506cfd6d2a4525c07e0945bc91e9d4c1d12')
    version('2.0.7',  sha256='11fd8307ba8552bd78532cb185dd1abf9293fb9536fe9979b1a22c174142ec98')
    version('2.0.6',  sha256='0c8d14e549c3fcd12f0ad0797f2cb8a10cb5508eb60bfa5671004420af8cbd4b')
    version('2.0.5',  sha256='3a91b737d6ccfa298e52ba751dad7cb3b3c0ac1907d2bdd6a1b0e02fae716525')
    version('2.0.4',  sha256='80fff5efb39bd4b4e600449de9e8dfc034a8f134f2be4a4a3cdb6f58c52446f4')
    version('2.0.3',  sha256='e12bcd86432f0477c5cc8f5a88cfeabdb96b2dcb4a989d060ca2298d81d19db2')
    version('2.0.2',  sha256='6a3f221524c273b025065175a8ad55963f767d311237847b4b6b1870fb4d43fd')
    version('2.0.1',  sha256='c653506eaeff6a2226aa4c8292c0d9fdc031ee49fec9d2429399e6e31dd119c5')
    version('2.0.0',  sha256='7d0de70968f243ac84ed73518cb09aecc922651f6bc0670852ffade1362e7ace')
    version('1.6.15', sha256='e67d456013470c8aac2271767127b47ed316b2980f8ef4e0ca9a1c6234d15fa3')
    version('1.6.14', sha256='fcb4730ef0d2e6d7c3e888a6915c33f42881d3e367a109e78b4e41a59df3749c')
    version('1.6.13', sha256='1dab17d68d908b2b520c0847b59f413649e11b773348b645821f77bc53687cbf')
    version('1.6.12', sha256='d1db1be18eddf87d813b73cdd84bc59a9a9d2ec169d3ada12c5e250678f8f980')
    version('1.6.11', sha256='6a9e23ad191298221fc975a3ae7d851a7e93c2b3c10b5a0d7b7ba8d7e89a5591')
    version('1.6.10', sha256='799929cdb886e4a300ea448b2d7c5cb4879b976805b488506fb142e7196b986a')
    version('1.6.9',  sha256='2dc1360828e05ea16c254e2af845f6620b42bada0bec895cc5b6d947c470664a')
    version('1.6.8',  sha256='1a5a245b68b3a8c5b96eda079bae96ecf983241c329a60731a7f77a9b562c289')
    version('1.6.7',  sha256='69e302cc30bacdbf1d5b769ed47ac4304073e40abd8b5cad3869e86af0f97d4c')
    version('1.6.6',  sha256='f5b174f5de50ebaf5819a0cc9ccc956069c06340e86971f0ba6880e51580f082')
    version('1.6.5',  sha256='377eb3295929cb73816987f895d5a21a643a2c1dbf3e8f3209ecf46c59ec7435')
    version('1.6.4',  sha256='053a535081d61ac54727adf27d373432c8fe2fe6db31276d5b702fca019d704e')
    version('1.6.3',  sha256='c4b7a97568f329395d9411e393c58e4016bebe3b10fef52d08e46af365f3a441')
    version('1.6.2',  sha256='e9d59c9049f2da0915591e692a3fdef7fb5fa6704d67a49c63f6b0e6ddf79eb1')
    version('1.6.1',  sha256='d2db7d44a271d865bc8af833ade6e841e579dd96d79cad2f398ce798e7737795')

    variant('cjson',     default=True,  description='Build with cJSON support')
    variant('tls',       default=True,  description='Build with TLS support')
    variant('static',    default=False, description='Build with static libraries')
    variant('websocket', default=False, description='Build with websocket support')

    depends_on('openssl',       when='+tls')
    depends_on('cjson',         when='+cjson')
    depends_on('libwebsockets', when='+websocket')

    def cmake_args(self):
        args = [
            self.define('DOCUMENTATION', 'no'),
            self.define_from_variant('WITH_CJSON', 'cjson'),
            self.define_from_variant('WITH_TLS', 'tls'),
            self.define_from_variant('WITH_STATIC_LIBRARIES', 'static'),
            self.define_from_variant('WITH_WEBSOCKETS', 'websocket')
        ]
        return args
