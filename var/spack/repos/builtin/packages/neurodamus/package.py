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
from spack.pkg.builtin.neurodamus_base import NeurodamusBase
import llnl.util.tty as tty
import os


class Neurodamus(NeurodamusBase):

    """Package used for building special from NeurodamusBase package"""

    variant('coreneuron', default=True, description="Enable CoreNEURON Support")
    variant('profile', default=False, description="Enable profiling using Tau")

    depends_on("hdf5")
    depends_on("mpi")
    depends_on("neuron")
    depends_on('reportinglib')
    depends_on("zlib")

    depends_on('coreneuron', when='+coreneuron')
    depends_on('coreneuron+profile', when='+profile')
    depends_on('coreneuron@plasticity', when='@plasicity')
    depends_on('coreneuron@hippocampus', when='@hippocampus')

    depends_on('neurodamus-base@master', when='@master')
    depends_on('neurodamus-base@hippocampus', when='@hippocampus')
    depends_on('neurodamus-base@plasticity', when='@plasicity')

    depends_on("neuron+profile", when='+profile')
    depends_on('reportinglib+profile', when='+profile')
    depends_on('tau', when='+profile')

    # coreneuron support is available for plasticity model
    # and requires python support in neuron
    conflicts('@hippocampus', when='+coreneuron')
    conflicts('@master', when='+coreneuron')
    conflicts('^neuron~python', when='+coreneuron')

    @run_before('install')
    def profiling_wrapper_on(self):
        os.environ["USE_PROFILER_WRAPPER"] = "1"

    @run_after('install')
    def profiling_wrapper_off(self):
        del os.environ["USE_PROFILER_WRAPPER"]

    def install(self, spec, prefix):
        with working_dir(prefix):
            modlib = os.path.relpath(self.spec['neurodamus-base'].prefix.lib.modlib)
            profile_flag = '-DENABLE_TAU_PROFILER' if '+profile' in spec else ''
            include_flag = ''
            link_flag = ''

            if '+coreneuron' in spec:
                include_flag += ' -DENABLE_CORENEURON -I%s' % (spec['coreneuron'].prefix.include)
                link_flag += ' %s' % (spec['coreneuron'].libs.ld_flags)

            include_flag += ' -I%s -I%s %s' % (spec['reportinglib'].prefix.include,
                                              spec['hdf5'].prefix.include,
                                              profile_flag)
            link_flag += ' %s -L%s -lhdf5 -L%s -lz' % (
                         spec['reportinglib'].libs.ld_flags,
                         spec['hdf5'].prefix.lib,
                         spec['zlib'].prefix.lib)

            nrnivmodl = which('nrnivmodl')
            nrnivmodl('-incflags', include_flag,
                      '-loadflags', link_flag,
                      modlib)

    @run_after('install')
    def check_install(self):
        special = '%s/special' % join_path(self.prefix, os.path.basename(self.neuron_archdir))
        if not os.path.isfile(special):
            raise RuntimeError("Neurodamus installion check failed, %s not created!" % special)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', join_path(self.prefix, os.path.basename(self.neuron_archdir)))
        run_env.set('HOC_LIBRARY_PATH', self.spec['neurodamus-base'].prefix.lib.hoclib)
