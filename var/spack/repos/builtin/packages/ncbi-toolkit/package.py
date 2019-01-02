# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
