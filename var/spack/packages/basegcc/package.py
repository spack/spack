from spack import *

# from contextlib import closing
# from glob import glob

class Basegcc(Package):
    """GCC, the GNU Compiler Collection"""
    homepage = "https://gcc.gnu.org"

    url = "http://ftp.gnu.org/gnu/gcc/gcc-5.2.0/gcc-5.2.0.tar.bz2"

    # version('5.3.0', 'c9616fd448f980259c31de613e575719')
    version('5.2.0', 'a51bcfeb3da7dd4c623e27207ed43467')

    # depends_on("wget")

    def install(self, spec, prefix):
        ln = which('ln')
        rm = which('rm')
        tar = which('tar')
        wget = which('wget')

        wget('-N', "https://gmplib.org/download/gmp/gmp-4.3.2.tar.bz2")
        # wget ('-N', "http://mpfr.loria.fr/mpfr-2.4.2/mpfr-2.4.2.tar.bz2")
        wget('-N', "ftp://gcc.gnu.org/pub/gcc/infrastructure/mpfr-2.4.2.tar.bz2")
        wget('-N', "http://www.multiprecision.org/mpc/download/mpc-0.8.1.tar.gz")
        wget('-N', "ftp://gcc.gnu.org/pub/gcc/infrastructure/isl-0.14.tar.bz2")

        rm('-rf', "gmp-4.3.2")
        rm('-rf', "mpfr-2.4.2")
        rm('-rf', "mpc-0.8.1")
        rm('-rf', "isl-0.14")

        tar('xjf', "gmp-4.3.2.tar.bz2")
        tar('xjf', "mpfr-2.4.2.tar.bz2")
        tar('xzf', "mpc-0.8.1.tar.gz")
        tar('xjf', "isl-0.14.tar.bz2")

        ln('-fns', "gmp-4.3.2", "gmp")
        ln('-fns', "mpfr-2.4.2", "mpfr")
        ln('-fns', "mpc-0.8.1", "mpc")
        ln('-fns', "isl-0.14", "isl")

        # unset("CPATH CPLUS_INCLUDE_PATH")
        # unset("C_INCLUDE_PATH")
        # unset("INCLUDE LIBRARY_PATH")
        # unset("PKG_CONFIG_PATH")

        configure("--prefix=%s" % prefix,
                  # "--libdir=%s/lib64" % prefix,
                  "--enable-languages=c,c++,fortran",
                  "--disable-multilib")
        make()
        make("install")

        # with working_dir('../spack-build', create=True):
        #     configure("--prefix=%s" % prefix,
        #               # "--libdir=%s/lib64" % prefix,
        #               "--enable-languages=c,c++,fortran",
        #               "--disable-multilib")
        #     make()
        #     make("install")

        # self.write_rpath_specs()

    # @property
    # def spec_dir(self):
    #     # e.g. lib64/gcc/x86_64-unknown-linux-gnu/4.9.2
    #     spec_dir = glob("%s/lib64/gcc/*/*" % self.prefix)
    #     return spec_dir[0] if spec_dir else None
    # 
    # 
    # def write_rpath_specs(self):
    #     """Generate a spec file so the linker adds a rpath to the libs
    #        the compiler used to build the executable."""
    #     if not self.spec_dir:
    #         tty.warn("Could not install specs for %s." % self.spec.format('$_$@'))
    #         return
    # 
    #     gcc = Executable(join_path(self.prefix.bin, 'gcc'))
    #     lines = gcc('-dumpspecs', return_output=True).strip().split("\n")
    #     specs_file = join_path(self.spec_dir, 'specs')
    #     with closing(open(specs_file, 'w')) as out:
    #         for line in lines:
    #             out.write(line + "\n")
    #             if line.startswith("*link:"):
    #                 out.write("-rpath %s/lib:%s/lib64 \\\n"% (self.prefix, self.prefix))
    #     set_install_permissions(specs_file)
