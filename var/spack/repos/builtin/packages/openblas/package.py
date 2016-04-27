from spack import *
import sys
import os
import shutil

class Openblas(Package):
    """OpenBLAS: An optimized BLAS library"""
    homepage = "http://www.openblas.net"
    url      = "http://github.com/xianyi/OpenBLAS/archive/v0.2.15.tar.gz"

    version('0.2.17', '664a12807f2a2a7cda4781e3ab2ae0e1')
    version('0.2.16', 'fef46ab92463bdbb1479dcec594ef6dc')
    version('0.2.15', 'b1190f3d3471685f17cfd1ec1d252ac9')

    variant('shared', default=True, description="Build shared libraries as well as static libs.")
    variant('openmp', default=True, description="Enable OpenMP support.")

    # virtual dependency
    provides('blas')
    provides('lapack')


    def install(self, spec, prefix):
        # Openblas is picky about compilers. Configure fails with
        # FC=/abs/path/to/f77, whereas FC=f77 works fine.
        # To circumvent this, provide basename only:
        make_defs = ['CC=%s' % os.path.basename(spack_cc),
                     'FC=%s' % os.path.basename(spack_f77)]

        make_targets = ['libs', 'netlib']

        # Build shared if variant is set.
        if '+shared' in spec:
            make_targets += ['shared']
        else:
            make_defs += ['NO_SHARED=1']

        # fix missing _dggsvd_ and _sggsvd_
        if spec.satisfies('@0.2.16'):
            make_defs += ['BUILD_LAPACK_DEPRECATED=1']

        # Add support for OpenMP
        # Note: Make sure your compiler supports OpenMP
        if '+openmp' in spec:
            make_defs += ['USE_OPENMP=1']

        make_args = make_defs + make_targets
        make(*make_args)

        make("tests", *make_defs)

        # no quotes around prefix (spack doesn't use a shell)
        make('install', "PREFIX=%s" % prefix, *make_defs)

        # Blas virtual package should provide blas.a and libblas.a
        with working_dir(prefix.lib):
            symlink('libopenblas.a', 'blas.a')
            symlink('libopenblas.a', 'libblas.a')
            if '+shared' in spec:
                symlink('libopenblas.%s' % dso_suffix, 'libblas.%s' % dso_suffix)

        # Lapack virtual package should provide liblapack.a
        with working_dir(prefix.lib):
            symlink('libopenblas.a', 'liblapack.a')
            if '+shared' in spec:
                symlink('libopenblas.%s' % dso_suffix, 'liblapack.%s' % dso_suffix)

        # Openblas may pass its own test but still fail to compile Lapack
        # symbols. To make sure we get working Blas and Lapack, do a small test.
        self.check_install(spec)


    def setup_dependent_package(self, module, dspec):
        # This is WIP for a prototype interface for virtual packages.
        # We can update this as more builds start depending on BLAS/LAPACK.
        libdir = find_library_path('libopenblas.a', self.prefix.lib64, self.prefix.lib)

        self.spec.blas_static_lib   = join_path(libdir, 'libopenblas.a')
        self.spec.lapack_static_lib = self.spec.blas_static_lib

        if '+shared' in self.spec:
            self.spec.blas_shared_lib   = join_path(libdir, 'libopenblas.%s' % dso_suffix)
            self.spec.lapack_shared_lib = self.spec.blas_shared_lib

    def check_install(self, spec):
        "Build and run a small program to test that we have Lapack symbols"
        print "Checking Openblas installation..."
        checkdir = "spack-check"
        with working_dir(checkdir, create=True):
            source = r"""
#include <cblas.h>
#include <stdio.h>
int main(void) {
int i=0;
double A[6] = {1.0, 2.0, 1.0, -3.0, 4.0, -1.0};
double B[6] = {1.0, 2.0, 1.0, -3.0, 4.0, -1.0};
double C[9] = {.5, .5, .5, .5, .5, .5, .5, .5, .5};
cblas_dgemm(CblasColMajor, CblasNoTrans, CblasTrans,
            3, 3, 2, 1, A, 3, B, 3, 2, C, 3);
for (i = 0; i < 9; i++)
  printf("%f\n", C[i]);
return 0;
}
"""
            expected = """\
11.000000
-9.000000
5.000000
-9.000000
21.000000
-1.000000
5.000000
-1.000000
3.000000
"""
            with open("check.c", 'w') as f:
                f.write(source)
            cc = which('cc')
            # TODO: Automate these path and library settings
            cc('-c', "-I%s" % join_path(spec.prefix, "include"), "check.c")
            cc('-o', "check", "check.o",
               "-L%s" % join_path(spec.prefix, "lib"), "-llapack", "-lblas")
            try:
                check = Executable('./check')
                output = check(return_output=True)
            except:
                output = ""
            success = output == expected
            if not success:
                print "Produced output does not match expected output."
                print "Expected output:"
                print '-'*80
                print expected
                print '-'*80
                print "Produced output:"
                print '-'*80
                print output
                print '-'*80
                raise RuntimeError("Openblas install check failed")
        shutil.rmtree(checkdir)
