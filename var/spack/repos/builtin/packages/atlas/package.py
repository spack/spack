from spack import *
from spack.util.executable import Executable
import os.path

class Atlas(Package):
    """
    Automatically Tuned Linear Algebra Software, generic shared ATLAS is an approach for the automatic generation and
    optimization of numerical software. Currently ATLAS supplies optimized versions for the complete set of linear
    algebra kernels known as the Basic Linear Algebra Subroutines (BLAS), and a subset of the linear algebra routines
    in the LAPACK library.
    """
    homepage = "http://math-atlas.sourceforge.net/"

    version('3.10.2', 'a4e21f343dec8f22e7415e339f09f6da',
            url='http://downloads.sourceforge.net/project/math-atlas/Stable/3.10.2/atlas3.10.2.tar.bz2', preferred=True)
    resource(name='lapack',
             url='http://www.netlib.org/lapack/lapack-3.5.0.tgz',
             md5='b1d3e3e425b2e44a06760ff173104bdf',
             destination='spack-resource-lapack',
             when='@3:')

    version('3.11.34', '0b6c5389c095c4c8785fd0f724ec6825',
            url='http://sourceforge.net/projects/math-atlas/files/Developer%20%28unstable%29/3.11.34/atlas3.11.34.tar.bz2/download')

    variant('shared', default=True, description='Builds shared library')

    provides('blas')
    provides('lapack')

    parallel = False

    def patch(self):
        # Disable thread check.  LLNL's environment does not allow
        # disabling of CPU throttling in a way that ATLAS actually
        # understands.
        filter_file(r'^\s+if \(thrchk\) exit\(1\);', 'if (0) exit(1);',
                    'CONFIG/src/config.c')
        # TODO: investigate a better way to add the check back in
        # TODO: using, say, MSRs.  Or move this to a variant.

    def install(self, spec, prefix):

        options = []
        if '+shared' in spec:
            options.append('--shared')

        # Lapack resource
        lapack_stage = self.stage[1]
        lapack_tarfile = os.path.basename(lapack_stage.fetcher.url)
        lapack_tarfile_path = join_path(lapack_stage.path, lapack_tarfile)
        options.append('--with-netlib-lapack-tarfile=%s' % lapack_tarfile_path)

        with working_dir('spack-build', create=True):
            configure = Executable('../configure')
            configure('--prefix=%s' % prefix, *options)
            make()
            make('check')
            make('ptcheck')
            make('time')
            make("install")
