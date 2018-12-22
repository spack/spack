# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os.path
import glob


class Express(CMakePackage):
    """eXpress is a streaming tool for quantifying the abundances of a set of
       target sequences from sampled subsequences."""

    homepage = "http://bio.math.berkeley.edu/eXpress/"
    git      = "https://github.com/adarob/eXpress.git"

    version('2015-11-29', commit='f845cab2c7f2d9247b35143e4aa05869cfb10e79')

    depends_on('boost')
    depends_on('bamtools')
    depends_on('zlib')

    conflicts('%gcc@6.0.0:', when='@2015-11-29')

    def patch(self):
        with working_dir('src'):
            files = glob.iglob('*.*')
            for file in files:
                if os.path.isfile(file):
                    edit = FileFilter(file)
                    edit.filter('#include <api', '#include <%s' % self.spec[
                                'bamtools'].prefix.include.bamtools.api)
            edit = FileFilter('CMakeLists.txt')
            edit.filter('\${CMAKE_CURRENT_SOURCE_DIR}/../bamtools/lib/'
                        'libbamtools.a', '%s' % self.spec['bamtools'].libs)

    def setup_environment(self, spack_env, run_env):
        spack_env.prepend_path('CPATH', self.spec[
                               'bamtools'].prefix.include.bamtools)
