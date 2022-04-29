# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class SstElements(AutotoolsPackage):
    """SST Elements implements a range of components for performing
       architecture simulation from node-level to system-level using
       the SST discrete event core.
    """

    homepage = "https://github.com/sstsimulator"
    git = "https://github.com/sstsimulator/sst-elements.git"
    url = "https://github.com/sstsimulator/sst-elements/releases/download/v11.0.0_Final/sstelements-11.0.0.tar.gz"

    maintainers = ['sknigh']

    version('11.0.0', sha256="bf265cb25afc041b74422cc5cddc8e3ae1e7c3efa3e37e699dac4e3f7629be6e")
    version('10.1.0', sha256="a790561449795dac48a84c525b8e0b09f05d0b0bff1a0da1aa2e903279a03c4a")
    version('10.0.0', sha256="ecf28ef97b27ea75be7e64cb0acb99d36773a888c1b32ba16034c62174b02693")
    version('9.1.0', sha256="e19b05aa6e59728995fc059840c79e476ba866b67887ccde7eaf52a18a1f52ca")

    version('develop',   branch='devel')
    version('master',  branch='master')

    # Contact SST developers (https://github.com/sstsimulator)
    # if your use case requires support for:
    #   - balar
    #   - OTF2
    #   - stake (riscv simulator)

    variant("pin",          default=False,
            description="Enable the Ariel CPU model")
    variant("dramsim2",     default=False,
            description="Build with DRAMSim2 support")
    variant("dramsim3",     default=False,
            description="Build with DRAMSim3 support")
    variant("dumpi",        default=False,
            description="Build with Dumpi support")
    variant("flashdimmsim", default=False,
            description="Build with FlashDIMMSim support")
    variant("nvdimmsim",    default=False,
            description="Build with NVDimmSim support")
    variant("hybridsim",    default=False,
            description="Build with HybridSim support")
    variant("goblin",       default=False,
            description="Build with GoblinHMCSim support")
    variant("hbm",          default=False,
            description="Build with HBM DRAMSim2 support")
    variant("ramulator",    default=False,
            description="Build with Ramulator support")
    variant("otf",          default=False,
            description="Build with OTF")
    variant("otf2",         default=False,
            description="Build with OTF2")

    depends_on("python", type=('build', 'run'))
    depends_on("sst-core")
    depends_on("sst-core@develop",  when="@develop")
    depends_on("sst-core@master", when="@master")

    depends_on("intel-pin",        when="+pin")
    depends_on("dramsim2@2:",      when="+dramsim2")
    depends_on("dramsim3@master",  when="+dramsim3")
    depends_on("sst-dumpi@master",     when="+dumpi")
    depends_on("flashdimmsim",     when="+flashdimmsim")
    depends_on("hybridsim@2.0.1",  when="+hybridsim")
    depends_on("dramsim3@master",  when="+hybridsim")
    depends_on("nvdimmsim@2.0.0",  when="+hybridsim")
    depends_on("nvdimmsim@2.0.0",  when="+nvdimmsim")
    depends_on("goblin-hmc-sim",   when="+goblin")
    depends_on("ramulator@sst",    when="+ramulator")
    depends_on("hbm-dramsim2",     when="+hbm")
    depends_on("otf",              when="+otf")
    depends_on("otf2",             when="+otf2")
    depends_on("gettext")
    depends_on("zlib")

    depends_on('autoconf@1.68:', type='build')
    depends_on('automake@1.11.1:', type='build')
    depends_on('libtool@1.2.4:', type='build')
    depends_on('m4', type='build')

    conflicts('+dumpi', msg='Dumpi not currently supported, contact SST Developers for help')
    conflicts('+otf', msg='OTF not currently supported, contact SST Developers for help')
    conflicts('+otf2', msg='OTF2 not currently supported, contact SST Developers for help')
    conflicts('~dramsim2', when='+hybridsim', msg='hybridsim requires dramsim2, spec should include +dramsim2')
    conflicts('~nvdimmsim', when='+hybridsim', msg='hybridsim requires nvdimmsim, spec should include +nvdimmsim')

    # force out-of-source builds
    build_directory = 'spack-build'

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('autogen.sh')

    def configure_args(self):
        spec = self.spec
        args = []

        if '+pdes_mpi' in spec["sst-core"]:
            env['CC'] = spec['mpi'].mpicc
            env['CXX'] = spec['mpi'].mpicxx
            env['F77'] = spec['mpi'].mpif77
            env['FC'] = spec['mpi'].mpifc

        if "+pin" in spec:
            args.append("--with-pin=%s" % spec["intel-pin"].prefix)

        if "+dramsim2" in spec or "+hybridsim" in spec:
            args.append("--with-dramsim=%s" % spec["dramsim2"].prefix)

        if "+dramsim3" in spec:
            args.append("--with-dramsim3=%s" % spec["dramsim3"].prefix)

        if "+dumpi" in spec:
            args.append("--with-dumpi=%s" % spec["sst-dumpi"].prefix)

        if "+flashdimmsim" in spec:
            args.append("--with-fdsim=%s" % spec["flashdimmsim"].prefix)

        if "+nvdimmsim" in spec or "+hybridsim" in spec:
            args.append("--with-nvdimmsim=%s" % spec["nvdimmsim"].prefix)

        if "+hybridsim" in spec:
            args.append("--with-hybridsim=%s" % spec["hybridsim"].prefix)

        if "+goblin" in spec:
            args.append("--with-goblin-hmcsim=%s" %
                        spec["goblin-hmc-sim"].prefix)

        if "+hbm" in spec:
            args.append("--with-hbmdramsim=%s" %
                        spec["hbm-dramsim2"].prefix)

        if "+ramulator" in spec:
            args.append("--with-ramulator=%s" % spec["ramulator"].prefix)

        if "+otf2" in spec:
            args.append("--with-otf2=%s" % spec["otf2"].prefix)

        if "+otf" in spec:
            args.append("--with-otf=%s" % spec["otf"].prefix)

        args.append("--with-sst-core=%s" % spec["sst-core"].prefix)
        return args
