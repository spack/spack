##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class NcbiToolkit(AutotoolsPackage):
    """NCBI C++ Toolkit"""

    homepage = "https://www.ncbi.nlm.nih.gov/IEB/ToolBox/CPP_DOC/"
    url      = "ftp://ftp.ncbi.nih.gov/toolbox/ncbi_tools++/CURRENT/ncbi_cxx--21_0_0.tar.gz"

    version('21_0_0', '14e021e08b1a78ac9cde98d0cab92098')

    depends_on('boost@1.35.0:')
    depends_on('bzip2')
    depends_on('libjpeg')
    depends_on('libpng')
    depends_on('libtiff')
    depends_on('libxml2')
    depends_on('libxslt@1.1.14:')
    depends_on('lzo')
    depends_on('pcre')
    depends_on('giflib')
    depends_on('sqlite@3.6.6:')
    depends_on('zlib')
    depends_on('samtools')
    depends_on('bamtools')

    def configure_args(self):
        return ['--without-sybase', '--without-fastcgi']

    def patch(self):
        with working_dir(join_path('src', 'util', 'image')):
            filter_file(r'jpeg_start_compress(&cinfo, true)',
                        'jpeg_start_compress(&cinfo, TRUE)',
                        'image_io_jpeg.cpp', string=True)

    def build(self, spec, prefix):
        compiler_version = self.compiler.version.joined

        with working_dir(join_path(
                'GCC{0}-DebugMT64'.format(compiler_version), 'build')):
            make('all_r')
