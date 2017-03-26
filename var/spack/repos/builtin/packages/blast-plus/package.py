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
#
# This is a based largely on the Homebrew science formula:
# https://github.com/Homebrew/homebrew-science/blob/master/blast.rb
#
from spack import *


class BlastPlus(AutotoolsPackage):
    """Basic Local Alignment Search Tool."""


    homepage = "http://blast.ncbi.nlm.nih.gov/"
    url      = "https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.6.0/ncbi-blast-2.6.0+-src.tar.gz"

    def url_for_version(self, version):
        url = "https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/{0}/ncbi-blast-{0}+-src.tar.gz"
        return url.format(version)

    version('2.6.0', 'c8ce8055b10c4d774d995f88c7cc6225')

    # homebrew sez: Fixed upstream in future version > 2.6
    patch('blast-make-fix2.5.0.diff', when="@:2.6.0")

    # No...
    # depends_on :mysql => :optional

    variant('static', default=False,
            description='Build with static linkage')
    variant('jpeg', default=True,
            description='Build with jpeg support')
    variant('png', default=True,
            description='Build with png support')
    variant('freetype', default=True,
            description='Build with freetype support')
    # variant('hdf5', default=True,
    #        description='Build with hdf5 support')
    variant('lzo', default=True,
            description='Build with lzo support')
    variant('pcre', default=True,
            description='Build with pcre support')

    depends_on('jpeg', when='+jpeg')
    depends_on('libpng', when='+png')
    depends_on('freetype', when='+freetype')
    # depends_on('hdf5', when='+hdf5')
    depends_on('lzo', when='+lzo')
    depends_on('pcre', when='+pcre')

    depends_on('python')

    configure_directory = 'c++'

    def configure_args(self):
        spec   = self.spec
        prefix = self.prefix

        config_args = [
            '--prefix={0}'.format(prefix),
            '--without-debug',
            '--with-mt',
            '--without-boost',
        ]

        if '+static' in spec:
            config_args.append('--with-static')
            # FIXME
            # args << "--with-static-exe" unless OS.linux?
            # args << "--with-dll" if build.with? "dll"
        else:
            config_args.extend([
                '--with-dll',
                '--without-static',
                '--without-static-exe'
            ])

        if '+jpeg' in spec:
            config_args.append('--with-jpeg')
        else:
            config_args.append('--without-jpeg')

        if '+png' in spec:
            config_args.append('--with-png')
        else:
            config_args.append('--without-png')

        if '+freetype' in spec:
            config_args.append('--with-freetype')
        else:
            config_args.append('--without-freetype')

        config_args.append('--without-hdf5')
        # if '+hdf5' in spec:
        #     # FIXME
        #     config_args.append('--with-hdf5={0}'.format(self.spec['hdf5'].prefix))
        # else:
        #     config_args.append('--without-hdf5')

        if '+lzo' in spec:
            config_args.append('--with-lzo')
        else:
            config_args.append('--without-lzo')

        if '+pcre' in spec:
            config_args.append('--with-pcre')
        else:
            config_args.append('--without-pcre')

        return config_args
