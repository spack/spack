# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Virtuoso(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/openlink/virtuoso-opensource"
    url      = "https://github.com/openlink/virtuoso-opensource/archive/v7.2.5.1.tar.gz"

    version('7.2.5.1', sha256='3e4807e94098b8265f8cf00867d1215bb1e9d0d274878e59a420742d2de471c2')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('gperf')
    depends_on('readline')
    depends_on('openssl@0.9.8:1.1.99')

    patch('virt_rpc.patch')
    patch('virt_openssl.patch')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')

    def configure_args(self):
        args = []
        args.append('--with-layout=opt')
        args.append('--with-readline=/usr')
        args.append('--program-transform-name=s/isql/isql-v/')
        args.append('--disable-dbpedia-vad')
        args.append('--disable-demo-vad')
        args.append('--enable-fct-vad')
        args.append('--enable-ods-vad')
        args.append('--disable-sparqldemo-vad')
        args.append('--disable-tutorial-vad')
        args.append('--enable-isparql-vad')
        args.append('--enable-rdfmappers-vad')
        return args
