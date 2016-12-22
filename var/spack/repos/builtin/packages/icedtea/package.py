##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Icedtea(AutotoolsPackage):
    """The IcedTea project provides a harness to build the source code from
       http://openjdk.java.net using Free Software build tools and adds a number
       of key features to the upstream OpenJDK codebase."""

    homepage = "http://icedtea.classpath.org"
    url = "http://icedtea.wildebeest.org/download/source/icedtea-3.2.0.tar.xz"

    version('3.2.0', 'f2a197734cc1f820f14a6ba0aef0f198c24c77e9f026d14ddf185b684b178f80')

    resource(name='corba', placement='spack-resource/corba',
             md5='19a12dc608da61a6878f4614a91156af',
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.2.0/corba.tar.xz')
    resource(name='hotspot', placement='spack-resource/hotspot',
             md5='cc5f423ed2949ee8a7e25d43f0cb425f',
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.2.0/hotspot.tar.xz')
    resource(name='jaxp', placement='spack-resource/jaxp',
             md5='8b1171ec1060517fc1c4eee162c78b33',
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.2.0/jaxp.tar.xz')
    resource(name='jaxws', placement='spack-resource/jaxws',
             md5='ca6bbcdb0f87399bd0a5481ad55939c8',
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.2.0/jaxws.tar.xz')
    resource(name='jdk', placement='spack-resource/jdk',
             md5='5f5d90b7036f1e8561f6943308528e80',
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.2.0/jdk.tar.xz')
    resource(name='langtools', placement='spack-resource/langtools',
             md5='9d105ca8e4de3936fe1a4916ec30ad7f',
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.2.0/langtools.tar.xz')
    resource(name='nashorn', placement='spack-resource/nashorn',
             md5='05fa4f0110a5c9c18828a3e359b1adde',
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.2.0/nashorn.tar.xz')
    resource(name='openjdk', placement='spack-resource/openjdk',
             md5='c7a7681fff0afda6a897b135820a1440',
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.2.0/openjdk.tar.xz')

    depends_on('libx11')
    depends_on('freetype')
    depends_on('libxp')
    depends_on('libxtst')
    depends_on('libxinerama')
    depends_on('jpeg')
    depends_on('libpng')
    depends_on('zlib')

    depends_on('fastjar', type='build')
    depends_on('wget', type='build')
    depends_on('gawk', type='build')
    depends_on('pkg-config@0.9.0:', type='build')

    def configure_args(self):
        return [
            '--with-corba-src-zip=%s'      % self.stage[1].archive_file,
            '--with-corba-checksum=no',
            '--with-hotspot-src-zip=%s'    % self.stage[2].archive_file,
            '--with-hotspot-checksum=no',
            '--with-jaxp-src-zip=%s'       % self.stage[3].archive_file,
            '--with-jaxp-checksum=no',
            '--with-jaxws-src-zip=%s'      % self.stage[4].archive_file,
            '--with-jaxws-checksum=no',
            '--with-jdk-src-zip=%s'        % self.stage[5].archive_file,
            '--with-jdk-checksum=no',
            '--with-langtools-src-zip=%s'  % self.stage[6].archive_file,
            '--with-langtools-checksum=no',
            '--with-nashorn-src-zip=%s'    % self.stage[7].archive_file,
            '--with-nashorn-checksum=no',
            '--with-openjdk-src-zip=%s'    % self.stage[8].archive_file,
            '--with-openjdk-checksum=no'
        ]
