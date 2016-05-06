from spack import *

class Kripke(Package):
    """Kripke is a simple, scalable, 3D Sn deterministic particle transport code."""

    homepage = "https://codesign.llnl.gov/kripke.php"
    url      = ""
    #version('master', git='https://lc.llnl.gov/stash/scm/kripke/kripke.git')
    version('master', git='https://lc.llnl.gov/stash/scm/~islam3/kripke.git')

    def install(self, spec, prefix):
      with working_dir('build', create=True):
        cmake('-DCMAKE_INSTALL_PREFIX:PATH=.', '-DCMAKE_TOOLCHAIN_FILE=../cmake/Toolchain/chaos_5_x86_64_ib-ic15.cmake', '-DENABLE_OPENMP=1', '..', *std_cmake_args)
        make()
        make("install")

