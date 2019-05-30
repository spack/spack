# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Eman2(CMakePackage):
    """EMAN2 is a broadly based greyscale scientific image processing suite
       with a primary focus on processing data from transmission electron 
       microscopes."""

    homepage = "https://blake.bcm.edu/emanwiki/EMAN2"
    url      = "https://github.com/cryoem/eman2/archive/v2.3.tar.gz"

    version('2.3', sha256='e64b8c5d87dba8a77ac0ff7cb4441d39dd0786f6cc91498fd49b96585ce99001')

    depends_on('boost+python@1.32:1.64')
    depends_on('fftw@3:')
    depends_on('ftgl')
    depends_on('gl@3:')
    depends_on('gsl')
    depends_on('hdf5')
    depends_on('libpng')
    depends_on('libtiff')
    depends_on('mpi')
    depends_on('python@2.7.1:2.7.99', type=('build', 'run'))
    depends_on('py-future', type=('build', 'run'))
    depends_on('py-ipython@:6.9', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))

    def patch(self):
        # remove conda test
        filter_file('find_package(Conda REQUIRED)',
                    'set(EMAN_PREFIX %s)' % self.prefix,
                    'CMakeLists.txt', string=True)

        # fix bad git command call
        filter_file('${GIT_EXECUTABLE} describe --always --dirty',
                    'echo nohash', 'programs/CMakeLists.txt', string=True)

    def setup_environment(self, spack_env, run_env):
        sp_dir = join_path(self.prefix, 'lib/python2.7/site-packages')
        spack_env.set('SP_DIR', sp_dir)

    def cmake_args(self):
        def fftw_path(p):
            return join_path(self.spec['fftw'].prefix, p)

        def ftgl_path(p):
            return join_path(self.spec['ftgl'].prefix, p)

        def hdf5_path(p):
            return join_path(self.spec['hdf5'].prefix, p)

        # need to initialize a directory for python libraries
        sp_dir = join_path(self.prefix, 'lib/python2.7/site-packages')
        mkdirp(sp_dir)

        args = []

        return [
            '-DFFTW3F_INCLUDE_PATH=%s' % fftw_path('include'),
            '-DFFTW3F_LIBRARY=%s' % fftw_path('lib/libfftw3f.so'),
            '-DFFTW3D_INCLUDE_PATH=%s' % fftw_path('include'),
            '-DFFTW3D_LIBRARY=%s' % fftw_path('lib/libfftw3.so'),
            '-DFFTW3F_THREADS_INCLUDE_PATH=%s' % fftw_path('include'),
            '-DFFTW3F_THREADS_LIBRARY=%s' % fftw_path('lib/libfftw3f_threads.so'),
            '-DFFTW3D_THREADS_INCLUDE_PATH=%s' % fftw_path('include'),
            '-DFFTW3D_THREADS_LIBRARY=%s' % fftw_path('lib/libfftw3_threads.so'),
            '-DFTGL_INCLUDE_PATH=%s' % ftgl_path('include'),
            '-DFTGL_LIBRARY=%s' % ftgl_path('lib/libftgl.so'),
            '-DHDF5_LIBRARY=%s' % hdf5_path('lib/libhdf5.so'),
            '-DHDF5_INCLUDE_PATH=%s' % hdf5_path('include'),
        ]
