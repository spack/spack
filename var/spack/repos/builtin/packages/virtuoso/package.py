# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Virtuoso(AutotoolsPackage):
    """Virtuoso is a high-performance and scalable Multi-Model RDBMS, 
    Data Integration Middleware, Linked Data Deployment, and HTTP 
    Application Server Platform"""

    homepage = "https://github.com/openlink/virtuoso-opensource"
    url      = "https://github.com/openlink/virtuoso-opensource/archive/v7.2.5.1.tar.gz"

    version('7.2.5.1', sha256='3e4807e94098b8265f8cf00867d1215bb1e9d0d274878e59a420742d2de471c2')

    variant('dbpedia-vad', default=False, description='DBpedia vad package')
    variant('demo-vad', default=False, description='Demo vad package')
    variant('fct-vad', default=True, description='Facet Browser vad package')
    variant('ods-vad', default=True, description='ODS vad package')
    variant('sparqldemo-vad', default=False, description='Sparql Demo vad package')
    variant('tutorial-vad', default=False, description='Tutorial vad package')
    variant('isparql-vad', default=True, description='iSPARQL vad package')
    variant('rdfmappers-vad', default=True, description='RDF Mappers vad package')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('gperf')
    depends_on('readline')
    depends_on('openssl@0.9.8:1.1.99')

    # Fix fail to include <rpc/types.h> problem
    # https://github.com/openlink/virtuoso-opensource/commit/52b6f8ebe108c1ed86fb840305c5f5a9677228f5
    patch('virt_rpc.patch')

    # support openssl@1.1.1
    # https://github.com/openlink/virtuoso-opensource/commit/713fa25b14457aa5127fac071830a2d20f4f968c
    # https://github.com/openlink/virtuoso-opensource/commit/713fa25b14457aa5127fac071830a2d20f4f968c
    # https://github.com/openlink/virtuoso-opensource/commit/713fa25b14457aa5127fac071830a2d20f4f968c
    patch('virt_openssl.patch')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')

    def configure_args(self):
        readlinep = self.spec['readline'].prefix.lib
        args = ['--with-layout=opt',
                '--program-transform-name=s/isql/isql-v/',
                '--with-readline={0}'.format(readlinep)
                ]
        args.extend(self.enable_or_disable('dbpedia-vad'))
        args.extend(self.enable_or_disable('demo-vad'))
        args.extend(self.enable_or_disable('fct-vad'))
        args.extend(self.enable_or_disable('ods-vad'))
        args.extend(self.enable_or_disable('sparqldemo-vad'))
        args.extend(self.enable_or_disable('tutorial-vad'))
        args.extend(self.enable_or_disable('isparql-vad'))
        args.extend(self.enable_or_disable('rdfmappers-vad'))
        return args
