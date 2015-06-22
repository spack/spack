from spack import *
import subprocess
import os

class Starpu(Package):
    """offers support for heterogeneous multicore architecture"""
    homepage = "http://starpu.gforge.inria.fr/"
    url      = "http://starpu.gforge.inria.fr/files/starpu-1.1.4.tar.gz"

    # Install from sources
    if os.environ.has_key("MORSE_STARPU_TAR") and os.environ.has_key("MORSE_STARPU_TAR_MD5"):
        version('1.1.4', '%s' % os.environ['MORSE_STARPU_TAR_MD5'],
                url = "file://%s" % os.environ['MORSE_STARPU_TAR'])
        version('1.2.0rc2', 'a2f3e37c64dbdfddedfc265eff74601f',
                url = "file:///home/pruvost/work/archives/starpu-1.2.0rc2.tar.gz")
        version('nakov', '8ac25f2c7c92d576ed25da01e7be2b61',
                url = "file:///home/pruvost/work/archives/starpu_nakov.tar.gz")
    else:
        version('1.2.0rc2', 'a2f3e37c64dbdfddedfc265eff74601f')
        version('1.2.0rc1', '2046cfd30c3046945bca570acafb9e6b')
        version('1.1.4', '1ba56a7a6deee19fd88c90920f9403cc')
        version('1.1.3', '97848eceee4926eb158e27ecb9365380')
        version('1.1.2', '985cb616910f8debff22be2c0e7699fa')
        version('1.1.1', 'd2dd09220cd47af50b585278ed5d7e01')
        version('1.1.0', '60a74f3ea6b3c6cd89ffa2b759d95bef')
        version('1.0.5', 'f7cc2ec26d595fd9d1df5bf856f56927')
        version('1.0.4', '3954c0675ead43398cadb73cbcffd8e4')
        version('1.0.3', '4aed2fe16057fbefafe9902c73ad56a7')
        version('1.0.2', '5105ffbeb1d88658663ea2e7d5865231')
        version('1.0.1', '72e9d92057f2b88483c27aca78c53316')
        version('1.0.0', '34177fa00fcff9f75b7650b307276b07')
        version('0.9.2', '51f9c5c19523e61e3e035bad3099b173')
        version('0.9.1', '675a22afdc68250bca2d8600cd73ee1b')
        version('0.9'  , 'bc69ab1d1a506b4e7f994b5fabbeaee7')
        version('0.4'  , '372a435987ff343e68088c6339068506')
        version('0.2'  , '763c9b1347026e035a25ed3709fec4fd')
        version('0.1'  , '658c7a8a3ef53599fd197ab3c7127c20')

    version('svn-trunk', svn='svn://scm.gforge.inria.fr/svn/starpu/trunk')
    version('svn-1.1', svn='svn://scm.gforge.inria.fr/svn/starpu/branches/starpu-1.1')
    version('svn-1.2', svn='svn://scm.gforge.inria.fr/svn/starpu/branches/starpu-1.2')

    variant('debug', default=False, description='Enable debug symbols')
    variant('fxt', default=False, description='Enable FxT tracing support')
    variant('mpi', default=False, description='Enable MPI support')
    variant('cuda', default=False, description='Enable CUDA support')
    variant('opencl', default=False, description='Enable OpenCL support')
    variant('simu', default=False, description='Enable SimGrid support')

    depends_on("hwloc")
    depends_on("mpi", when='+mpi')
    depends_on("fxt", when='+fxt')
    depends_on("SimGrid", when='+simu')

    def setup(self):
        # do nothing in the default case
        pass

    @when('@svn')
    def setup(self):
        # execute autogen first if running the SVN version
        subprocess.check_call('./autogen.sh')

    def install(self, spec, prefix):

        self.setup()

        config_args = ["--prefix=" + prefix]

        if '+debug' in spec:
            config_args.append("--enable-debug")

        if '+fxt' in spec:
            fxt = spec['fxt'].prefix
            config_args.append("--with-fxt=%s" % fxt)
            #@when('@1.2')
            #config_args.append("--enable-paje-codelet-details")

        if '+simu' in spec:
            config_args.append("--enable-simgrid")

        if not '+mpi' in spec:
            config_args.append("--without-mpicc")

        if not '+cuda' in spec:
            config_args.append("--disable-cuda")

        if not '+opencl' in spec:
            config_args.append("--disable-opencl")

        configure(*config_args)
        make()
        make("install", parallel=False)
