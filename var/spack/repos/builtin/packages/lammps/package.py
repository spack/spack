# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import datetime as dt

import archspec

from spack.package import *


class Lammps(CMakePackage, CudaPackage):
    """LAMMPS stands for Large-scale Atomic/Molecular Massively
    Parallel Simulator.
    """

    homepage = "https://www.lammps.org/"
    url = "https://github.com/lammps/lammps/archive/patch_1Sep2017.tar.gz"
    git = "https://github.com/lammps/lammps.git"

    tags = ["ecp", "ecp-apps"]

    maintainers("rbberger")

    # rules for new versions and deprecation
    # * new stable versions should be marked as preferred=True
    # * a stable version that has updates and any of its outdated update releases should be
    #   marked deprecated=True
    # * patch releases older than a stable release should be marked deprecated=True
    version("develop", branch="develop")
    version("20221103", sha256="d28517b84b157d4e46a1a64ed787b4662d8f2f5ade3f5a04bb0caed068f32f7e")
    version("20220915", sha256="392b8d35fc7919b0efaf8b389259a9b795a817e58e75e380467c63d03a0dab75")
    version("20220803", sha256="f37cb0b35c1682ffceae5826aadce47278aa7003099a1655fcea43acd7d37926")
    version(
        "20220623.2",
        sha256="8a560213e83919623525c4a7c4b5f0eda35cdf3b0c0e6548fd891379e04ca9e6",
        preferred=True,
    )
    version(
        "20220623.1",
        sha256="58e3b2b984f8935bb0db5631e143be2826c45ffd48844f7c394f36624a3e17a2",
        preferred=True,
        deprecated=True,
    )
    version(
        "20220623",
        sha256="d27ede095c9f00cd13a26f967a723d07cf8f4df65c700ed73573577bc173d5ce",
        preferred=True,
        deprecated=True,
    )
    version(
        "20220602",
        sha256="3e8f54453e53b3b387a68317277f832b8cf64a981e64b21e98bb37ea36ac4a60",
        deprecated=True,
    )
    version(
        "20220504",
        sha256="fe05bae8090fd0177b3c1b987cd32a9cb7cd05d790828ba954c764eb52e10b52",
        deprecated=True,
    )
    version(
        "20220324",
        sha256="d791cc93eedfc345fdf87bfa5b6f7e17e461f86ba197f9e9c3d477ce8657a7ef",
        deprecated=True,
    )
    version(
        "20220217",
        sha256="e5bd2bf325835fa98d1b95f0667c83076580916027df5b8109d5470d1b97da98",
        deprecated=True,
    )
    version(
        "20220107",
        sha256="fbf6c6814968ae0d772d7b6783079ff4f249a8faeceb39992c344969e9f1edbb",
        deprecated=True,
    )
    version(
        "20211214",
        sha256="9f7b1ee2394678c1a6baa2c158a62345680a952eee251783e3c246b3f12db4c9",
        deprecated=True,
    )
    version(
        "20211027",
        sha256="c06f682fcf9d5921ca90c857a104e90fba0fe65decaac9732745e4da49281938",
        deprecated=True,
    )
    version(
        "20210929.3",
        sha256="e4c274f0dc5fdedc43f2b365156653d1105197a116ff2bafe893523cdb22532e",
        preferred=True,
    )
    version(
        "20210929.2",
        sha256="9318ca816cde16a9a4174bf22a1966f5f2155cb32c0ad5a6757633276411fb36",
        preferred=True,
        deprecated=True,
    )
    version(
        "20210929.1",
        sha256="5000b422c9c245b92df63507de5aa2ea4af345ea1f00180167aaa084b711c27c",
        preferred=True,
        deprecated=True,
    )
    version(
        "20210929",
        sha256="2dff656cb21fd9a6d46c818741c99d400cfb1b12102604844663b655fb2f893d",
        preferred=True,
        deprecated=True,
    )
    version(
        "20210920",
        sha256="e3eba96933c1dd3177143c7ac837cae69faceba196948fbad2970425db414d8c",
        deprecated=True,
    )
    version(
        "20210831",
        sha256="532c42576a79d72682deaf43225ca773ed9f9e35deb484a82f91905b6cba23ec",
        deprecated=True,
    )
    version(
        "20210730",
        sha256="c5e998c8282a835d2bcba4fceffe3cecdf9aed9bdf79fa9c945af573e632f6e7",
        deprecated=True,
    )
    version(
        "20210728",
        sha256="6b844d2c3f7170a59d36fbf761483aa0c63d95eda254d00fe4d10542403abe36",
        deprecated=True,
    )
    version(
        "20210702",
        sha256="4fdd8ca2dbde8809c0048716650b73ae1f840e22ebe24b25f6f7a499377fea57",
        deprecated=True,
    )
    version(
        "20210514",
        sha256="74d9c4386f2181b15a024314c42b7a0b0aaefd3b4b947aeca00fe07e5b2f3317",
        deprecated=True,
    )
    version(
        "20210408",
        sha256="1645147b7777de4f616b8232edf0b597868084f969c777fa0a757949c3f71f56",
        deprecated=True,
    )
    version(
        "20210310",
        sha256="25708378dbeccf794bc5045aceb84380bf4a3ca03fc8e5d150a26ca88d371474",
        deprecated=True,
    )
    version(
        "20201029",
        sha256="759705e16c1fedd6aa6e07d028cc0c78d73c76b76736668420946a74050c3726",
        preferred=True,
    )
    version(
        "20200721",
        sha256="845bfeddb7b667799a1a5dbc166b397d714c3d2720316604a979d3465b4190a9",
        deprecated=True,
    )
    version(
        "20200630",
        sha256="413cbfabcc1541a339c7a4ab5693fbeb768f46bb1250640ba94686c6e90922fc",
        deprecated=True,
    )
    version(
        "20200505",
        sha256="c49d77fd602d28ebd8cf10f7359b9fc4d14668c72039028ed7792453d416de73",
        deprecated=True,
    )
    version(
        "20200303",
        sha256="a1a2e3e763ef5baecea258732518d75775639db26e60af1634ab385ed89224d1",
        preferred=True,
    )
    version(
        "20200227",
        sha256="1aabcf38bc72285797c710b648e906151a912c36b634a9c88ac383aacf85516e",
        deprecated=True,
    )
    version(
        "20200218",
        sha256="73bcf146660804ced954f6a0a8dce937482677778d46018ca5a688127bf97211",
        deprecated=True,
    )
    version(
        "20200204",
        sha256="3bf3de546ede34ffcd89f1fca5fd66aa78c662e7c8a76e30ce593e44a00d23ce",
        deprecated=True,
    )
    version(
        "20200124",
        sha256="443829560d760690e1ae21ad54922f56f34f640a81e817f5cc65d2a4af3a6a5d",
        deprecated=True,
    )
    version(
        "20200109",
        sha256="f2fd24f6c10837801f490913d73f672ec7c6becda08465d7e834a2bfbe3d7cd6",
        deprecated=True,
    )
    version(
        "20191120",
        sha256="fd146bf517a6c2fb8a69ecb3749dc352eef94414739cd7855c668c690af85d27",
        deprecated=True,
    )
    version(
        "20191030",
        sha256="5279567f731386ffdb87800b448903a63de2591064e13b4d5216acae25b7e541",
        deprecated=True,
    )
    version(
        "20190919",
        sha256="0f693203afe86bc70c084c55f29330bdeea3e3ad6791f81c727f7a34a7f6caf3",
        deprecated=True,
    )
    version(
        "20190807",
        sha256="895d71914057e070fdf0ae5ccf9d6552b932355056690bdb8e86d96549218cc0",
        deprecated=True,
    )
    version(
        "20190605",
        sha256="c7b35090aef7b114d2b47a7298c1e8237dd811da87995c997bf7639cca743152",
        deprecated=True,
    )
    version(
        "20181212",
        sha256="ccc5d2c21c4b62ce4afe7b3a0fe2f37b83e5a5e43819b7c2e2e255cce2ce0f24",
        deprecated=True,
    )
    version(
        "20181207",
        sha256="d92104d008a7f1d0b6071011decc5c6dc8b936a3418b20bd34b055371302557f",
        deprecated=True,
    )
    version(
        "20181127",
        sha256="c076b633eda5506f895de4c73103df8b995d9fec01be82c67c7608efcc345179",
        deprecated=True,
    )
    version(
        "20181115",
        sha256="3bc9c166e465cac625c4a8e4060e597003f4619dadd57d3bc8d25bcd930f286e",
        deprecated=True,
    )
    version(
        "20181109",
        sha256="dd30fe492fa147fb6f39bfcc79d8c786b9689f7fbe86d56de58cace53b6198c9",
        deprecated=True,
    )
    version(
        "20181024",
        sha256="a171dff5aff7aaa2c9606ab2abc9260f2b685a5c7f6d650e7f2b59cf4aa149d6",
        deprecated=True,
    )
    version(
        "20181010",
        sha256="bda762ee2d2dcefe0b4e36fb689c6b9f7ede49324444ccde6c59cba727b4b02d",
        deprecated=True,
    )
    version(
        "20180918",
        sha256="02f143d518d8647b77137adc527faa9725c7afbc538d670253169e2a9b3fa0e6",
        deprecated=True,
    )
    version(
        "20180905",
        sha256="ee0df649e33a9bf4fe62e062452978731548a56b7487e8e1ce9403676217958d",
        deprecated=True,
    )
    version(
        "20180831",
        sha256="6c604b3ebd0cef1a5b18730d2c2eb1e659b2db65c5b1ae6240b8a0b150e4dff3",
        deprecated=True,
    )
    version(
        "20180822",
        sha256="9f8942ca3f8e81377ae88ccfd075da4e27d0dd677526085e1a807777c8324074",
        deprecated=True,
    )
    version(
        "20180629",
        sha256="1acf7d9b37b99f17563cd4c8bb00ec57bb2e29eb77c0603fd6871898de74763b",
        deprecated=True,
    )
    version(
        "20180316",
        sha256="a81f88c93e417ecb87cd5f5464c9a2570384a48ff13764051c5e846c3d1258c1",
        deprecated=True,
    )
    version(
        "20180222",
        sha256="374254d5131b7118b9ab0f0e27d20c3d13d96b03ed2b5224057f0c1065828694",
        deprecated=True,
    )
    version(
        "20170922",
        sha256="f0bf6eb530d528f4d261d0a261e5616cbb6e990156808b721e73234e463849d3",
        deprecated=True,
    )
    version(
        "20170901",
        sha256="5d88d4e92f4e0bb57c8ab30e0d20de556830af820223778b9967bec2184efd46",
        deprecated=True,
    )

    def url_for_version(self, version):
        split_ver = str(version).split(".")
        vdate = dt.datetime.strptime(split_ver[0], "%Y%m%d")
        if len(split_ver) < 2:
            update = ""
        else:
            update = "_update{0}".format(split_ver[1])

        is_stable = (
            version in self.versions
            and "preferred" in self.versions[version]
            and self.versions[version]["preferred"]
        )

        return "https://github.com/lammps/lammps/archive/{0}_{1}{2}.tar.gz".format(
            "stable" if is_stable else "patch", vdate.strftime("%d%b%Y").lstrip("0"), update
        )

    # List of supported optional packages
    # Note: package `openmp` in this recipe is called `openmp-package`, to avoid clash
    # with the pre-existing `openmp` variant
    supported_packages = {
        "asphere": {},
        "body": {},
        "bpm": {"when": "@20220504:"},
        "class2": {},
        "colloid": {},
        "compress": {},
        "coreshell": {},
        "dielectric": {"when": "@20210702:"},
        "dipole": {},
        "electrode": {"when": "@20220504:"},
        "granular": {},
        "intel": {},
        "kspace": {},
        "kokkos": {},
        "latte": {},
        "manybody": {},
        "mc": {},
        "meam": {"when": "@20210728:"},
        "misc": {},
        "mliap": {"when": "@:20210702"},
        "ml-iap": {"when": "@20210728:"},
        "ml-snap": {"when": "@20210728:"},
        "ml-hdnnp": {"when": "@20210702:"},
        "molecule": {},
        "mpiio": {},
        "opt": {},
        "peri": {},
        "plugin": {"when": "@20210408:"},
        "poems": {},
        "python": {},
        "qeq": {},
        "replica": {},
        "rigid": {},
        "shock": {},
        "snap": {"when": "@:20210702"},
        "spin": {},
        "srd": {},
        "voronoi": {},
        "user-atc": {"when": "@:20210702"},
        "user-adios": {"when": "@:20210702"},
        "user-awpmd": {"when": "@:20210702"},
        "user-bocs": {"when": "@:20210702"},
        "user-brownian": {"when": "@20210514:20210702"},
        "user-cgsdk": {"when": "@:20210702"},
        "user-colvars": {"when": "@:20210702"},
        "user-diffraction": {"when": "@:20210702"},
        "user-dpd": {"when": "@:20210702"},
        "user-drude": {"when": "@:20210702"},
        "user-eff": {"when": "@:20210702"},
        "user-fep": {"when": "@:20210702"},
        "user-hdnnp": {"when": "@20210527"},
        "user-h5md": {"when": "@:20210702"},
        "user-intel": {"when": "@:20210702"},
        "user-lb": {"when": "@:20210702"},
        "user-manifold": {"when": "@:20210702"},
        "user-meamc": {"when": "@:20210702"},
        "user-mesodpd": {"when": "@:20210702"},
        "user-mesont": {"when": "@:20210702"},
        "user-mgpt": {"when": "@:20210702"},
        "user-misc": {"when": "@:20210702"},
        "user-mofff": {"when": "@:20210702"},
        "user-molfile": {"when": "@:20210702"},
        "user-netcdf": {"when": "@:20210702"},
        "user-omp": {"when": "@:20210702"},
        "user-phonon": {"when": "@:20210702"},
        "user-plumed": {"when": "@:20210702"},
        "user-ptm": {"when": "@:20210702"},
        "user-qtb": {"when": "@:20210702"},
        "user-reaction": {"when": "@:20210702"},
        "user-reaxc": {"when": "@:20210702"},
        "user-sdpd": {"when": "@:20210702"},
        "user-smd": {"when": "@:20210702"},
        "user-smtbq": {"when": "@:20210702"},
        "user-sph": {"when": "@:20210702"},
        "user-tally": {"when": "@:20210702"},
        "user-uef": {"when": "@:20210702"},
        "user-yaff": {"when": "@:20210702"},
        "atc": {"when": "@20210728:"},
        "adios": {"when": "@20210728:"},
        "awpmd": {"when": "@20210728:"},
        "bocs": {"when": "@20210728:"},
        "brownian": {"when": "@20210728:"},
        "cg-sdk": {"when": "@20210728:"},
        "colvars": {"when": "@20210728:"},
        "diffraction": {"when": "@20210728:"},
        "dpd-basic": {"when": "@20210728:"},
        "dpd-meso": {"when": "@20210728:"},
        "dpd-react": {"when": "@20210728:"},
        "dpd-smooth": {"when": "@20210728:"},
        "drude": {"when": "@20210728:"},
        "eff": {"when": "@20210728:"},
        "extra-compute": {"when": "@20210728:"},
        "extra-dump": {"when": "@20210728:"},
        "extra-fix": {"when": "@20210728:"},
        "extra-molecule": {"when": "@20210728:"},
        "extra-pair": {"when": "@20210728:"},
        "fep": {"when": "@20210728:"},
        "h5md": {"when": "@20210728:"},
        "interlayer": {"when": "@20210728:"},
        "latboltz": {"when": "@20210728:"},
        "machdyn": {"when": "@20210728:"},
        "manifold": {"when": "@20210728:"},
        "mesont": {"when": "@20210728:"},
        "mgpt": {"when": "@20210728:"},
        "mofff": {"when": "@20210728:"},
        "molfile": {"when": "@20210728:"},
        "netcdf": {"when": "@20210728:"},
        "openmp-package": {},
        "orient": {"when": "@20210728:"},
        "phonon": {"when": "@20210728:"},
        "plumed": {"when": "@20210728:"},
        "ptm": {"when": "@20210728:"},
        "qtb": {"when": "@20210728:"},
        "reaction": {"when": "@20210728:"},
        "reaxff": {"when": "@20210728:"},
        "smtbq": {"when": "@20210728:"},
        "sph": {"when": "@20210728:"},
        "tally": {"when": "@20210728:"},
        "uef": {"when": "@20210728:"},
        "yaff": {"when": "@20210728:"},
    }

    for pkg_name, pkg_options in supported_packages.items():
        variant(
            pkg_name,
            default=False,
            description="Activate the {} package".format(pkg_name.replace("-package", "")),
            when=pkg_options.get("when", None),
        )
    variant("lib", default=True, description="Build the liblammps in addition to the executable")
    variant("mpi", default=True, description="Build with mpi")
    variant("jpeg", default=True, description="Build with jpeg support")
    variant("png", default=True, description="Build with png support")
    variant("ffmpeg", default=True, description="Build with ffmpeg support")
    variant("kim", default=True, description="Build with KIM support")
    variant("openmp", default=True, description="Build with OpenMP")
    variant("opencl", default=False, description="Build with OpenCL")
    variant("exceptions", default=False, description="Build with lammps exceptions")
    variant(
        "cuda_mps",
        default=False,
        description="(CUDA only) Enable tweaks for running "
        + "with Nvidia CUDA Multi-process services daemon",
    )

    variant(
        "lammps_sizes",
        default="smallbig",
        description="LAMMPS integer sizes (smallsmall: all 32-bit, smallbig:"
        + "64-bit #atoms #timesteps, bigbig: also 64-bit imageint, 64-bit atom ids)",
        values=("smallbig", "bigbig", "smallsmall"),
        multi=False,
    )
    variant(
        "fftw_precision",
        default="double",
        when="+kspace",
        description="Select FFTW precision (used by Kspace)",
        values=("single", "double"),
        multi=False,
    )

    depends_on("mpi", when="+mpi")
    depends_on("mpi", when="+mpiio")
    depends_on("fftw-api@3", when="+kspace")
    depends_on("voropp+pic", when="+voronoi")
    depends_on("netcdf-c+mpi", when="+user-netcdf")
    depends_on("netcdf-c+mpi", when="+netcdf")
    depends_on("blas", when="+user-atc")
    depends_on("blas", when="+atc")
    depends_on("lapack", when="+user-atc")
    depends_on("lapack", when="+atc")
    depends_on("opencl", when="+opencl")
    depends_on("latte@1.0.1", when="@:20180222+latte")
    depends_on("latte@1.1.1:", when="@20180316:20180628+latte")
    depends_on("latte@1.2.1:", when="@20180629:20200505+latte")
    depends_on("latte@1.2.2:", when="@20200602:+latte")
    depends_on("blas", when="+latte")
    depends_on("lapack", when="+latte")
    depends_on("python", when="+python")
    depends_on("mpi", when="+user-lb")
    depends_on("mpi", when="+latboltz")
    depends_on("mpi", when="+user-h5md")
    depends_on("mpi", when="+h5md")
    depends_on("hdf5", when="+user-h5md")
    depends_on("hdf5", when="+h5md")
    depends_on("jpeg", when="+jpeg")
    depends_on("kim-api", when="+kim")
    depends_on("curl", when="@20190329:+kim")
    depends_on("libpng", when="+png")
    depends_on("ffmpeg", when="+ffmpeg")
    depends_on("kokkos+deprecated_code+shared@3.0.00", when="@20200303+kokkos")
    depends_on("kokkos+shared@3.1:", when="@20200505:+kokkos")
    depends_on("adios2", when="+user-adios")
    depends_on("adios2", when="+adios")
    depends_on("plumed", when="+user-plumed")
    depends_on("plumed", when="+plumed")
    depends_on("eigen@3:", when="+user-smd")
    depends_on("eigen@3:", when="+machdyn")
    depends_on("py-cython", when="+mliap+python")
    depends_on("py-cython", when="+ml-iap+python")
    depends_on("py-numpy", when="+mliap+python")
    depends_on("py-numpy", when="+ml-iap+python")
    depends_on("py-setuptools", when="@20220217:+python", type="build")
    depends_on("n2p2@2.1.4:", when="+user-hdnnp")
    depends_on("n2p2@2.1.4:", when="+ml-hdnnp")
    depends_on("n2p2+shared", when="+lib ^n2p2")

    depends_on("googletest", type="test")
    depends_on("libyaml", type="test")

    conflicts("+cuda", when="+opencl")
    conflicts("+body", when="+poems@:20180628")
    conflicts("+latte", when="@:20170921")
    conflicts("+python", when="~lib")
    conflicts("+qeq", when="~manybody")
    conflicts("+user-atc", when="~manybody")
    conflicts("+atc", when="~manybody")
    conflicts("+user-misc", when="~manybody")
    conflicts("+user-phonon", when="~kspace")
    conflicts("+phonon", when="~kspace")
    conflicts("%gcc@9:", when="@:20200303+openmp")
    conflicts("+kokkos", when="@:20200227")
    conflicts("+dielectric", when="~kspace")
    conflicts("+dielectric", when="@:20210702~user-misc")
    conflicts("+dielectric", when="@20210728:~extra-pair")
    conflicts(
        "+meam",
        when="@20181212:20210527",
        msg="+meam is removed between @20181212 and @20210527, use +user-meamc instead",
    )
    conflicts("+electrode", when="~kspace")
    conflicts("+mliap", when="~snap")
    conflicts("+ml-iap", when="~ml-snap")
    conflicts(
        "+user-adios +mpi",
        when="^adios2~mpi",
        msg="With +user-adios, mpi setting for adios2 and lammps must be the same",
    )
    conflicts(
        "+user-adios ~mpi",
        when="^adios2+mpi",
        msg="With +user-adios, mpi setting for adios2 and lammps must be the same",
    )
    conflicts(
        "+adios +mpi",
        when="^adios2~mpi",
        msg="With +adios, mpi setting for adios2 and lammps must be the same",
    )
    conflicts(
        "+adios ~mpi",
        when="^adios2+mpi",
        msg="With +adios, mpi setting for adios2 and lammps must be the same",
    )

    patch("lib.patch", when="@20170901")
    patch("660.patch", when="@20170922")
    patch("gtest_fix.patch", when="@:20210310 %aocc@3.2.0")
    patch(
        "https://github.com/lammps/lammps/commit/562300996285fdec4ef74542383276898555af06.patch?full_index=1",
        sha256="e6f1b62bbfdc79d632f4cea98019202d0dd25aa4ae61a70df1164cb4f290df79",
        when="@20200721 +cuda",
    )

    root_cmakelists_dir = "cmake"

    def cmake_args(self):
        spec = self.spec

        mpi_prefix = "ENABLE"
        pkg_prefix = "ENABLE"
        if spec.satisfies("@20180629:"):
            mpi_prefix = "BUILD"
            pkg_prefix = "PKG"

        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "lib"),
            self.define_from_variant("LAMMPS_EXCEPTIONS", "exceptions"),
            "-D{0}_MPI={1}".format(mpi_prefix, "ON" if "+mpi" in spec else "OFF"),
            self.define_from_variant("BUILD_OMP", "openmp"),
            self.define("ENABLE_TESTING", self.run_tests),
        ]
        if spec.satisfies("+cuda"):
            args.append("-DPKG_GPU=ON")
            args.append("-DGPU_API=cuda")
            cuda_arch = spec.variants["cuda_arch"].value
            if cuda_arch != "none":
                args.append("-DGPU_ARCH=sm_{0}".format(cuda_arch[0]))
            args.append(self.define_from_variant("CUDA_MPS_SUPPORT", "cuda_mps"))
        elif spec.satisfies("+opencl"):
            # LAMMPS downloads and bundles its own OpenCL ICD Loader by default
            args.append("-DUSE_STATIC_OPENCL_LOADER=OFF")
            args.append("-DPKG_GPU=ON")
            args.append("-DGPU_API=opencl")
        else:
            args.append("-DPKG_GPU=OFF")

        if spec.satisfies("@20180629:+lib"):
            args.append("-DBUILD_LIB=ON")

        if spec.satisfies("%aocc"):
            cxx_flags = "-Ofast -mfma -fvectorize -funroll-loops"
            args.append(self.define("CMAKE_CXX_FLAGS_RELEASE", cxx_flags))

        # Overwrite generic cpu tune option
        cmake_tune_flags = archspec.cpu.TARGETS[spec.target.name].optimization_flags(
            spec.compiler.name, spec.compiler.version
        )
        args.append(self.define("CMAKE_TUNE_FLAGS", cmake_tune_flags))

        args.append(self.define_from_variant("LAMMPS_SIZES", "lammps_sizes"))

        args.append(self.define_from_variant("WITH_JPEG", "jpeg"))
        args.append(self.define_from_variant("WITH_PNG", "png"))
        args.append(self.define_from_variant("WITH_FFMPEG", "ffmpeg"))

        for pkg in self.supported_packages.keys():
            opt = "-D{0}_{1}".format(pkg_prefix, pkg.replace("-package", "").upper())
            if "+{0}".format(pkg) in spec:
                args.append("{0}=ON".format(opt))
            else:
                args.append("{0}=OFF".format(opt))
        if "+kim" in spec:
            args.append("-DPKG_KIM=ON")
        if "+kspace" in spec:
            # If FFTW3 is selected, then CMake will try to detect, if threaded
            # FFTW libraries are available and enable them by default.
            if "^fftw" in spec:
                args.append("-DFFT=FFTW3")
            if "^mkl" in spec:
                args.append("-DFFT=MKL")
            if "^amdfftw" in spec:
                args.append(self.define("FFT", "FFTW3"))
            if "^armpl-gcc" in spec:
                args.append(self.define("FFT", "FFTW3"))
                args.append(self.define("FFTW3_LIBRARY", self.spec["fftw-api"].libs[0]))
                args.append(
                    self.define("FFTW3_INCLUDE_DIR", self.spec["fftw-api"].headers.directories[0])
                )
            if "^cray-fftw" in spec:
                args.append("-DFFT=FFTW3")
            # Using the -DFFT_SINGLE setting trades off a little accuracy
            # for reduced memory use and parallel communication costs
            # for transposing 3d FFT data.
            if spec.satisfies("fftw_precision=single"):
                args.append("-DFFT_SINGLE=True")
            else:
                args.append("-DFFT_SINGLE=False")

        if "+kokkos" in spec:
            args.append("-DEXTERNAL_KOKKOS=ON")
        if "+user-adios" in spec or "+adios" in spec:
            args.append("-DADIOS2_DIR={0}".format(self.spec["adios2"].prefix))
        if "+user-plumed" in spec or "+plumed" in spec:
            args.append("-DDOWNLOAD_PLUMED=no")
            if "+shared" in self.spec["plumed"]:
                args.append("-DPLUMED_MODE=shared")
            else:
                args.append("-DPLUMED_MODE=static")
        if "+user-smd" in spec or "+machdyn" in spec:
            args.append("-DDOWNLOAD_EIGEN3=no")
            args.append("-DEIGEN3_INCLUDE_DIR={0}".format(self.spec["eigen"].prefix.include))
        if "+user-hdnnp" in spec or "+ml-hdnnp" in spec:
            args.append("-DDOWNLOAD_N2P2=no")
            args.append("-DN2P2_DIR={0}".format(self.spec["n2p2"].prefix))

        return args

    def setup_run_environment(self, env):
        env.set("LAMMPS_POTENTIALS", self.prefix.share.lammps.potentials)
