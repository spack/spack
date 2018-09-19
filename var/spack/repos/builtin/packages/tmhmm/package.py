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


class Tmhmm(Package):
    """Transmembrane helices in proteins

       Note: A manual download is required for TMHMM.
       Spack will search your current directory for the download file.
       Alternatively, add this file to a mirror so that Spack can find it.
       For instructions on how to set up a mirror, see
       http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "http://www.cbs.dtu.dk/cgi-bin/nph-sw_request?tmhmm"
    url      = "file://{0}/tmhmm-2.0c.Linux.tar.gz".format(os.getcwd())

    version('2.0c', '359db0c4ecf84d1ade5786abe844d54e')

    depends_on('perl', type='run')

    def patch(self):
        with working_dir('bin'):
            tmhmm = FileFilter('tmhmmformat.pl')
            tmhmm.filter('#!/usr/local/bin/perl -w',
                         '#!/usr/bin/env perl')
            tmhmm = FileFilter('tmhmm')
            tmhmm.filter('#!/usr/local/bin/perl',
                         '#!/usr/bin/env perl')

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
