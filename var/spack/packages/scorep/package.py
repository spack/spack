##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *


class Scorep(Package):
    """
    The Score-P measurement infrastructure is a highly scalable and
       easy-to-use tool suite for profiling, event tracing, and online
       analysis of HPC applications."""

    homepage = "http://www.vi-hps.org/projects/score-p"
    url      = "http://www.vi-hps.org/upload/packages/scorep/scorep-1.2.3.tar.gz"

    version('1.4.2', '3b9a042b13bdd5836452354e6567f71e',
            url='http://www.vi-hps.org/upload/packages/scorep/scorep-1.4.2.tar.gz')
    version('1.3', '9db6f957b7f51fa01377a9537867a55c',
            url='http://www.vi-hps.org/upload/packages/scorep/scorep-1.3.tar.gz')

    ##########
    # Dependencies for SCORE-P are quite tight. See the homepage for more information.
    # SCOREP 1.4.2
    depends_on('otf2@1.5:1.6', when='@1.4.2')
    depends_on('opari2@1.1.4', when='@1.4.2')
    depends_on('cube@4.3:4.4', when='@1.4.2')
    # SCOREP 1.3
    depends_on("otf2@1.4", when='@1.3')
    depends_on("opari2@1.1.4", when='@1.3')
    depends_on("cube@4.2.3", when='@1.3')
    ##########

    depends_on("mpi")
    depends_on("papi")

    def get_compiler_config_line(self):
        backend_user_provided = ['CC=%s' % self.compiler.cc_names[0],
                                 'CXX=%s' % self.compiler.cxx_names[0],
                                 'F77=%s' % self.compiler.f77_names[0] if len(self.compiler.f77_names) else "",
                                 'FC=%s' % self.compiler.fc_names[0] if len(self.compiler.fc_names) else "",
                                 'CFLAGS=-fPIC %s' % self.rpath_args,
                                 'CXXFLAGS=-fPIC %s'% self.rpath_args]
        return backend_user_provided

    def install(self, spec, prefix):
        configure = Executable( join_path(self.stage.source_path, 'configure') )
        with working_dir('spack-build', create=True):
            configure_args = ["--prefix=%s" % prefix,
                              "--with-otf2=%s" % spec['otf2'].prefix.bin,
                              "--with-opari2=%s" % spec['opari2'].prefix.bin,
                              "--with-cube=%s" % spec['cube'].prefix.bin,
                              "--with-papi-header=%s" % spec['papi'].prefix.include,
                              "--with-papi-lib=%s" % spec['papi'].prefix.lib,
                              "--enable-shared"]
            configure_args.extend(self.get_compiler_config_line())
            configure(*configure_args)
            make()
            make("install")
