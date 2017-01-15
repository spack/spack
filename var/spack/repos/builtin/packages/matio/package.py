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
from spack import architecture
import subprocess



class Matio(Package):
    """matio is an C library for reading and writing Matlab MAT files"""
    homepage = "http://sourceforge.net/projects/matio/"
    url = "http://downloads.sourceforge.net/project/matio/matio/1.5.2/matio-1.5.2.tar.gz"

    version('1.5.2', '85b007b99916c63791f28398f6a4c6f1')

    def get_arch(self):
        arch = architecture.Arch()
        arch.platform = architecture.platform()
        return str(arch.platform.target('default_target'))

    def install(self, spec, prefix):
        ## update the config.sub/guess files if on ppc64le
        if self.get_arch() == 'ppc64le':
            with working_dir("config"):
                # get new config.guess and config.sub files
                print 'Backing up existing config.[sub|guess] files\n'
                subprocess.call("mv config.sub config.sub.orig", shell=True)
                subprocess.call("mv config.guess config.guess.orig", shell=True)
                print 'Downloading lastest config.[sub|guess] files\n'
                subprocess.call("wget -O config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'", shell=True)
                subprocess.call("wget -O config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'", shell=True)
        configure('--prefix=%s' % prefix)

        make()
        make("install")
