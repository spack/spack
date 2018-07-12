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


class Sosflow(CMakePackage):
    """SOSflow provides a flexible, scalable, and programmable framework for
    observation, introspection, feedback, and control of HPC applications."""

    homepage = "https://github.com/cdwdirect/sos_flow/wiki"
    url      = "https://github.com/cdwdirect/sos_flow.git"

    version('1.17',      git='https://github.com/cdwdirect/sos_flow.git', tag='spack-build-v1.17', preferred=True)
    version('0.9901',    git='https://github.com/cdwdirect/sos_flow.git', tag='spack-build-v0.9901')
    version('chad_dev',  git='https://github.com/cdwdirect/sos_flow.git', branch='chad_dev')

    # Primary inter-daemon transport is EVPath for now.
    depends_on('libevpath',        type=('build', 'run'))
    depends_on('sqlite@3:',        type=('build', 'run'))
    # Python module is compiled with CFFI, requiring UCS4 support:
    depends_on('python@2: +ucs4',  type=('build', 'run'))
    # Python modules used for CFFI build and common ML usage:
    depends_on('py-cffi',          type=('build', 'run'))
    #depends_on('py-dateutil',      type=('build', 'run'))
    #depends_on('py-numexpr',       type=('build', 'run'))
    #depends_on('py-numpy',         type=('build', 'run'))
    #depends_on('py-packaging',     type=('build', 'run'))
    #depends_on('py-pandas',        type=('build', 'run'))
    #depends_on('py-pycparser',     type=('build', 'run'))
    #depends_on('py-pyparsing',     type=('build', 'run'))
    #depends_on('py-pytz',          type=('build', 'run'))
    #depends_on('py-scikit-learn',  type=('build', 'run'))
    #depends_on('py-scipy',         type=('build', 'run'))
    #depends_on('py-six',           type=('build', 'run'))

    parallel = False
    
    def setup_environment(self, spack_env, run_env):
        #
        # Build settings:
        spack_env.set('SOS_DIR', self.spec.prefix)
        #
        # Runtime defaults:
        run_env.set('SOS_DIR', self.spec.prefix)
        run_env.set('SOS_ROOT', self.spec.prefix)
        run_env.set('SOS_BUILD_DIR', self.spec.prefix)
        run_env.set('SOS_CMD_PORT', '22500')
        run_env.set('SOS_WORK', env['HOME'])
        run_env.set('SOS_EVPATH_MEETUP', env['HOME'])
        #
        run_env.set('SOS_DB_DISABLED', 'FALSE')
        run_env.set('SOS_UPDATE_LATEST_FRAME', 'TRUE')
        run_env.set('SOS_IN_MEMORY_DATABASE', 'FALSE')
        run_env.set('SOS_EXPORT_DB_AT_EXIT', 'FALSE')
        #
        run_env.set('SOS_OPTIONS_FILE', '')
        run_env.set('SOS_SYSTEM_MONITOR_ENABLED', 'FALSE')
        run_env.set('SOS_SYSTEM_MONITOR_FREQ_USEC', '0')
        run_env.set('SOS_SHUTDOWN', 'FALSE')
        run_env.set('SOS_ENV_SET', 'true')
