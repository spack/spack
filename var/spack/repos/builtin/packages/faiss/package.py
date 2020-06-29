# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
from spack import *


class Faiss(AutotoolsPackage, PythonPackage):
    """Faiss is a library for efficient similarity search and clustering of
       dense vectors.

      Faiss contains algorithms that search in sets of vectors of any size, up
      to ones that possibly do not fit in RAM. It also contains supporting code
      for evaluation and parameter tuning. Faiss is written in C++ with complete
      wrappers for Python/numpy. Some of the most useful algorithms are
      implemented on the GPU. It is developed by Facebook AI Research.
    """

    homepage = "https://github.com/facebookresearch/faiss"
    url      = "https://github.com/facebookresearch/faiss/archive/v1.6.3.tar.gz"

    # putting the creator's name for now
    #  hopefully, FAISS developers will take over
    maintainers = ['bhatiaharsh']

    version('1.6.3', sha256='e1a41c159f0b896975fbb133e0240a233af5c9286c09a28fde6aefff5336e542')
    version('1.5.3', sha256='b24d347b0285d01c2ed663ccc7596cd0ea95071f3dd5ebb573ccfc28f15f043b')

    variant('cuda',   default=False, description='Build with CUDA')
    variant('python', default=False, description='Build Python bindings')
    variant('tests',  default=False, description='Build Tests')

    #TODO: figure out how to do these --
    # +tests cannot work with ~python
    # tested only 1.5.3 and 1.6.3 (other versions likely have other issues)

    depends_on('blas')
    depends_on('cuda',          when='+cuda')

    # we dont't want "extend" because we don't want to symlink to python prefix
    depends_on('python',        when='+python', type=('build', 'run'))
    depends_on('py-numpy',      when='+python', type=('build', 'run'))
    depends_on('py-setuptools', when='+python', type=('build', 'run'))
    depends_on('swig',          when='+python', type='build')
    depends_on('py-scipy',      when='+tests',  type=('build', 'run'))

    # --- patch for v1.5.3 -----------------------------------------------
    # faiss assumes that the "source directory" will always
    # be called "faiss" (not spack-src or faiss-1.5.3)
    # so, we will have to create a symlink to self (faiss did that in 1.6.3)
    # and add an include path
    patch('fixes-in-v1.5.3.patch', when='@1.5.3')

    # --- patch for v1.6.3 -----------------------------------------------
    # for v1.6.3, GPU build has a bug (two files need to be deleted)
    # https://github.com/facebookresearch/faiss/issues/1159
    # also, some include paths in gpu/tests/Makefile are missing
    patch('fixes-in-v1.6.3.patch', when='@1.6.3')

    # --------------------------------------------------------------------------
    phases = ['configure', 'build', 'install']

    def configure_args(self):

        #TODO: ask spack team about the correct way to force this
        if '+tests' in self.spec and '~python' in self.spec:
            raise InstallError('Incorrect variants: +tests must be accompanied by +python')

        args = []
        if '+cuda' in self.spec:
            args.append('--with-cuda={}'.format(self.spec['cuda'].prefix))
        else:
            args.append('--without-cuda')
        return args

    # --------------------------------------------------------------------------
    def build(self, spec, prefix):

        make()
        if '+python' in self.spec:
            make('-C', 'python')

        # CPU tests
        if '+tests' in self.spec:
            os.chdir(os.path.join(self.stage.source_path, 'tests'))
            make('tests', parallel=False)

        # GPU tests
        if '+tests' in self.spec and '+cuda' in self.spec:
            os.chdir(os.path.join(self.stage.source_path, 'gpu', 'test'))
            make('build', parallel=False)   # this target is added by the patch
            make('demo_ivfpq_indexing_gpu', parallel=False)

        os.chdir(self.stage.source_path)

    # --------------------------------------------------------------------------
    def install(self, spec, prefix):

        make('install')

        if '+python' in self.spec:

            # faiss's suggested installation (using makefile) puts the
            # python bindings in python prefix
            # but, instead, we want to keep these files in the faiss prefix
            # TODO: replace with make install once the PR is accepted
            # https://github.com/facebookresearch/faiss/pull/1271
            cmd = '{} setup.py install --prefix={}'
            os.chdir(os.path.join(self.stage.source_path, 'python'))
            os.system(cmd.format(self.spec['python'].command, self.prefix))

        def _prefix_and_install(file):
            os.system('mv {} faiss_{}'.format(file, file))
            install('faiss_{}'.format(file), self.prefix.bin)

        # CPU tests
        if '+tests' in self.spec:
            os.chdir(os.path.join(self.stage.source_path, 'tests'))
            _prefix_and_install('tests')

        # GPU tests
        if '+tests' in self.spec and '+cuda' in self.spec:
            os.chdir(os.path.join(self.stage.source_path, 'gpu', 'test'))
            _prefix_and_install('TestGpuIndexFlat')
            _prefix_and_install('TestGpuIndexBinaryFlat')
            _prefix_and_install('TestGpuIndexIVFFlat')
            _prefix_and_install('TestGpuIndexIVFPQ')
            _prefix_and_install('TestGpuMemoryException')
            _prefix_and_install('TestGpuSelect')
            _prefix_and_install('demo_ivfpq_indexing_gpu')

        os.chdir(self.stage.source_path)

    # --------------------------------------------------------------------------
    @run_after('configure')
    def _fix_makefile(self):

        # for v1.5.3, the makefile contains x86-specific flags
        # so, we need to remove them for powerpc
        # for v1.6.0 and forward, this seems to have been fixed

        # TODO: didn't check < 1.5.3 (but, do we care about the older versions)
        # TODO: should this be removed for other architectures as well?
        #       i.e., change the condition to target != 'x86' ?

        if self.version <= Version('1.5.3') and self.spec.architecture.target == 'power9le':
            makefile = FileFilter('makefile.inc')
            makefile.filter( 'CPUFLAGS     = -mavx2 -mf16c',
                            '#CPUFLAGS     = -mavx2 -mf16c')

    # --------------------------------------------------------------------------
    @run_after('install')
    def _fix_install(self):

        # for some reason, the egg gets installed as the archive
        # so, let's inflate it manually
        if '+python' in self.spec:

            fversion = self.version.string
            pversion = self.spec['python'].version.up_to(2).string

            fname = 'faiss-{}-py{}.egg'.format(fversion, pversion)
            lpath = 'lib/python{}/site-packages'.format(pversion)

            os.chdir(os.path.join(self.prefix, lpath))

            # if this is a file, not a directory
            if os.path.isfile(fname):
                bname = '{}.zip'.format(fname)
                os.system('mv {} {}'.format(fname, bname))
                os.system('unzip {} -d {}'.format(bname, fname))

            os.chdir(self.stage.source_path)
    # --------------------------------------------------------------------------
