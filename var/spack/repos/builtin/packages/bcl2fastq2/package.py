##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
import os
import glob
import llnl.util.tty as tty


# This application uses cmake to build, but they wrap it with a
# configure script that performs dark magic.  This package does it
# their way.
class Bcl2fastq2(Package):
    """The bcl2fastq2 Conversion Software converts base
       call (BCL) files from a sequencing run into FASTQ
       files."""

    homepage = "https://support.illumina.com/downloads/bcl2fastq-conversion-software-v2-20.html"

    version('2.20.0.422', '4dc99f1af208498b7279b66556329488')
    version('2.19.1.403', 'baba7a02767fd868e87cb36781d2be26')
    version('2.18.0.12', 'fbe06492117f65609c41be0c27e3215c')
    # 2.17.1.14 is no longer distributed.  If you have a copy of the
    # source tarball, you can drop it into a local mirror w/ the name
    # mirror/bcl2fastq2/bcl2fastq2-2.17.1.14.zip and go from there.
    version('2.17.1.14', '7426226c6db095862e636b95c38608d3')

    depends_on('boost@1.54.0')
    depends_on('cmake@2.8.9:')
    depends_on('libxml2@2.7.8')
    depends_on('libxslt@1.1.26~crypto')
    depends_on('libgcrypt')
    depends_on('zlib')

    # Their cmake macros don't set the flag when they find a library
    # that makes them happy.
    patch('cmake-macros.patch')
    # After finding the libxslt bits, cmake still needs to wire in the
    # libexslt bits.
    patch('cxxConfigure-cmake.patch')

    root_cmakelists_dir = 'src'

    # v2.17.1.14 and v2.18.0.12 were available via HTTP.
    # v2.19.1.403 is only available via ftp.
    # who knows what the future will hold.
    def url_for_version(self, version):
        url = "ftp://webdata2:webdata2@ussd-ftp.illumina.com/downloads/software/bcl2fastq/bcl2fastq2-v{0}-tar.zip"
        if version.string == '2.19.1.403':
            return url.format(version.up_to(3).dotted)
        else:
            return url.format(version.up_to(3).dashed)

    # Illumina tucks the source inside a gzipped tarball inside a zip
    # file.  We let the normal Spack expansion bit unzip the zip file,
    # then follow it with a function untars the tarball after Spack's
    # done it's bit.
    def do_stage(self, mirror_only=False):
        # wrap (decorate) the standard expand_archive step with a
        # helper, then call the real do_stage().
        self.stage.expand_archive = self.unpack_it(self.stage.expand_archive)
        super(Bcl2fastq2, self).do_stage(mirror_only)

    def unpack_it(self, f):
        def wrap():
            f()                 # call the original expand_archive()
            with working_dir(self.stage.path):
                if os.path.isdir('bcl2fastq'):
                    tty.msg("The tarball has already been unpacked")
                else:
                    tty.msg("Unpacking bcl2fastq2 tarball")
                    tty.msg("cwd sez: {0}".format(os.getcwd()))
                    tarball = glob.glob(join_path('spack-expanded-archive',
                                        'bcl2fastq2*.tar.gz'))[0]
                    copy(tarball, '.')
                    os.rmdir('spack-expanded-archive')
                    tar = which('tar')
                    tarball = os.path.basename(tarball)
                    tar('-xf', tarball)
                    tty.msg("Finished unpacking bcl2fastq2 tarball")
        return wrap

    def install(self, spec, prefix):
        bash = which('bash')
        bash("src/configure", "--prefix={0}".format(prefix),
             "--with-cmake={0}".format(join_path(spec['cmake'].prefix.bin,
                                                 "cmake")))
        make()
        make("install")
