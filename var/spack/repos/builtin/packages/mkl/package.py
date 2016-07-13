from spack import *
import os

from spack.pkg.builtin.intel import IntelInstaller


class Mkl(IntelInstaller):
    """Intel Math Kernel Library.

    Note: You will have to add the download file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://software.llnl.gov/spack/mirrors.html"""

    homepage = "https://software.intel.com/en-us/intel-mkl"

    version('11.3.2.181', '536dbd82896d6facc16de8f961d17d65',
            url="file://%s/l_mkl_11.3.2.181.tgz" % os.getcwd())
    version('11.3.3.210', 'f72546df27f5ebb0941b5d21fd804e34',
            url="file://%s/l_mkl_11.3.3.210.tgz" % os.getcwd())

    # virtual dependency
    provides('blas')
    provides('lapack')
    # TODO: MKL also provides implementation of Scalapack.

    def install(self, spec, prefix):

        self.intel_prefix = os.path.join(prefix, "pkg")
        IntelInstaller.install(self, spec, prefix)

        mkl_dir = os.path.join(self.intel_prefix, "mkl")
        for f in os.listdir(mkl_dir):
            os.symlink(os.path.join(mkl_dir, f), os.path.join(self.prefix, f))

    def setup_dependent_package(self, module, dspec):
        # For now use Single Dynamic Library:
        # To set the threading layer at run time, use the
        # mkl_set_threading_layer function or set MKL_THREADING_LAYER
        # variable to one of the following values: INTEL, SEQUENTIAL, PGI.
        # To set interface layer at run time, use the mkl_set_interface_layer
        # function or set the MKL_INTERFACE_LAYER variable to LP64 or ILP64.

        # Otherwise one would need to specify several libraries
        # (e.g. mkl_intel_lp64;mkl_sequential;mkl_core), which reflect
        # different interface and threading layers.

        name = 'libmkl_rt.%s' % dso_suffix
        libdir = find_library_path(name, self.prefix.lib64, self.prefix.lib)

        self.spec.blas_shared_lib   = join_path(libdir, name)
        self.spec.lapack_shared_lib = self.spec.blas_shared_lib

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # set up MKLROOT for everyone using MKL package
        spack_env.set('MKLROOT', self.prefix)

    def setup_environment(self, spack_env, env):
        env.set('MKLROOT', self.prefix)
