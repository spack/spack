# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import datetime as dt

from spack.package import *


class Lammps(CMakePackage, CudaPackage):
    """LAMMPS stands for Large-scale Atomic/Molecular Massively
    Parallel Simulator. This package uses patch releases, not
    stable release.
    See https://github.com/spack/spack/pull/5342 for a detailed
    discussion.
    """
    homepage = "https://lammps.sandia.gov/"
    url      = "https://github.com/lammps/lammps/archive/patch_1Sep2017.tar.gz"
    git      = "https://github.com/lammps/lammps.git"

    tags = ['ecp', 'ecp-apps']

    version('master', branch='master')
    version('20220107', sha256='fbf6c6814968ae0d772d7b6783079ff4f249a8faeceb39992c344969e9f1edbb')
    version('20211214', sha256='9f7b1ee2394678c1a6baa2c158a62345680a952eee251783e3c246b3f12db4c9')
    version('20211027', sha256='c06f682fcf9d5921ca90c857a104e90fba0fe65decaac9732745e4da49281938')
    version('20210929.2', sha256='26586c1e82356b60e40359ee474818003c7788214bfe2bfe9128a3dbe5200b4d')
    version('20210929.1', sha256='3b792e20864bf88b855332486996f2c540deabb4e3507e48fa4ee96ad79615ec')
    version('20210929', sha256='5132f332b582be3006510562ef10bac9ef76d760f34fc08a2af556416c57cf4c')
    version('20210920', sha256='e3eba96933c1dd3177143c7ac837cae69faceba196948fbad2970425db414d8c')
    version('20210831', sha256='532c42576a79d72682deaf43225ca773ed9f9e35deb484a82f91905b6cba23ec')
    version('20210730', sha256='c5e998c8282a835d2bcba4fceffe3cecdf9aed9bdf79fa9c945af573e632f6e7')
    version('20210728', sha256='6b844d2c3f7170a59d36fbf761483aa0c63d95eda254d00fe4d10542403abe36')
    version('20210702', sha256='4fdd8ca2dbde8809c0048716650b73ae1f840e22ebe24b25f6f7a499377fea57')
    version('20210514', sha256='74d9c4386f2181b15a024314c42b7a0b0aaefd3b4b947aeca00fe07e5b2f3317')
    version('20210408', sha256='1645147b7777de4f616b8232edf0b597868084f969c777fa0a757949c3f71f56')
    version('20210310', sha256='25708378dbeccf794bc5045aceb84380bf4a3ca03fc8e5d150a26ca88d371474')
    version('20201029', sha256='759705e16c1fedd6aa6e07d028cc0c78d73c76b76736668420946a74050c3726')
    version('20200721', sha256='845bfeddb7b667799a1a5dbc166b397d714c3d2720316604a979d3465b4190a9')
    version('20200630', sha256='413cbfabcc1541a339c7a4ab5693fbeb768f46bb1250640ba94686c6e90922fc')
    version('20200505', sha256='c49d77fd602d28ebd8cf10f7359b9fc4d14668c72039028ed7792453d416de73')
    version('20200303', sha256='9aa56dfb8673a06e6c88588505ec1dfc01dd94f9d60e719ed0c605e48cc06c58')
    version('20200227', sha256='1aabcf38bc72285797c710b648e906151a912c36b634a9c88ac383aacf85516e')
    version('20200218', sha256='73bcf146660804ced954f6a0a8dce937482677778d46018ca5a688127bf97211')
    version('20200204', sha256='3bf3de546ede34ffcd89f1fca5fd66aa78c662e7c8a76e30ce593e44a00d23ce')
    version('20200124', sha256='443829560d760690e1ae21ad54922f56f34f640a81e817f5cc65d2a4af3a6a5d')
    version('20200109', sha256='f2fd24f6c10837801f490913d73f672ec7c6becda08465d7e834a2bfbe3d7cd6')
    version('20191120', sha256='fd146bf517a6c2fb8a69ecb3749dc352eef94414739cd7855c668c690af85d27')
    version('20191030', sha256='5279567f731386ffdb87800b448903a63de2591064e13b4d5216acae25b7e541')
    version('20190919', sha256='0f693203afe86bc70c084c55f29330bdeea3e3ad6791f81c727f7a34a7f6caf3')
    version('20190807', sha256='895d71914057e070fdf0ae5ccf9d6552b932355056690bdb8e86d96549218cc0')
    version('20190605', sha256='c7b35090aef7b114d2b47a7298c1e8237dd811da87995c997bf7639cca743152')
    version('20181212', sha256='ccc5d2c21c4b62ce4afe7b3a0fe2f37b83e5a5e43819b7c2e2e255cce2ce0f24')
    version('20181207', sha256='d92104d008a7f1d0b6071011decc5c6dc8b936a3418b20bd34b055371302557f')
    version('20181127', sha256='c076b633eda5506f895de4c73103df8b995d9fec01be82c67c7608efcc345179')
    version('20181115', sha256='3bc9c166e465cac625c4a8e4060e597003f4619dadd57d3bc8d25bcd930f286e')
    version('20181109', sha256='dd30fe492fa147fb6f39bfcc79d8c786b9689f7fbe86d56de58cace53b6198c9')
    version('20181024', sha256='a171dff5aff7aaa2c9606ab2abc9260f2b685a5c7f6d650e7f2b59cf4aa149d6')
    version('20181010', sha256='bda762ee2d2dcefe0b4e36fb689c6b9f7ede49324444ccde6c59cba727b4b02d')
    version('20180918', sha256='02f143d518d8647b77137adc527faa9725c7afbc538d670253169e2a9b3fa0e6')
    version('20180905', sha256='ee0df649e33a9bf4fe62e062452978731548a56b7487e8e1ce9403676217958d')
    version('20180831', sha256='6c604b3ebd0cef1a5b18730d2c2eb1e659b2db65c5b1ae6240b8a0b150e4dff3')
    version('20180822', sha256='9f8942ca3f8e81377ae88ccfd075da4e27d0dd677526085e1a807777c8324074')
    version('20180629', sha256='1acf7d9b37b99f17563cd4c8bb00ec57bb2e29eb77c0603fd6871898de74763b')
    version('20180316', sha256='a81f88c93e417ecb87cd5f5464c9a2570384a48ff13764051c5e846c3d1258c1')
    version('20180222', sha256='374254d5131b7118b9ab0f0e27d20c3d13d96b03ed2b5224057f0c1065828694')
    version('20170922', sha256='f0bf6eb530d528f4d261d0a261e5616cbb6e990156808b721e73234e463849d3')
    version('20170901', sha256='5d88d4e92f4e0bb57c8ab30e0d20de556830af820223778b9967bec2184efd46')

    def url_for_version(self, version):
        split_ver = str(version).split('.')
        vdate = dt.datetime.strptime(split_ver[0], "%Y%m%d")
        if len(split_ver) < 2:
            update = ""
        else:
            update = "_update{0}".format(split_ver[1])
        return "https://github.com/lammps/lammps/archive/patch_{0}{1}.tar.gz".format(
            vdate.strftime("%d%b%Y").lstrip('0'), update)

    supported_packages = ['asphere', 'body', 'class2', 'colloid', 'compress',
                          'coreshell', 'dipole', 'granular', 'kspace',
                          'kokkos', 'latte', 'manybody', 'mc', 'meam', 'misc',
                          'mliap', 'molecule', 'mpiio', 'opt', 'peri', 'poems',
                          'python', 'qeq', 'replica', 'rigid', 'shock', 'snap',
                          'spin', 'srd', 'user-atc', 'user-adios',
                          'user-awpmd', 'user-bocs', 'user-cgsdk',
                          'user-colvars', 'user-diffraction', 'user-dpd',
                          'user-drude', 'user-eff', 'user-fep', 'user-h5md',
                          'user-lb', 'user-manifold', 'user-meamc',
                          'user-mesodpd', 'user-mesont', 'user-mgpt',
                          'user-misc', 'user-mofff', 'user-netcdf', 'user-omp',
                          'user-phonon', 'user-plumed', 'user-ptm', 'user-qtb',
                          'user-reaction', 'user-reaxc', 'user-sdpd',
                          'user-smd', 'user-smtbq', 'user-sph', 'user-tally',
                          'user-uef', 'user-yaff', 'voronoi']

    for pkg in supported_packages:
        variant(pkg, default=False,
                description='Activate the {0} package'.format(pkg))
    variant('lib', default=True,
            description='Build the liblammps in addition to the executable')
    variant('mpi', default=True,
            description='Build with mpi')
    variant('jpeg', default=True,
            description='Build with jpeg support')
    variant('png', default=True,
            description='Build with png support')
    variant('ffmpeg', default=True,
            description='Build with ffmpeg support')
    variant('kim', default=True,
            description='Build with KIM support')
    variant('openmp', default=True, description='Build with OpenMP')
    variant('opencl', default=False, description='Build with OpenCL')
    variant('exceptions', default=False,
            description='Build with lammps exceptions')
    variant('cuda_mps', default=False,
            description='(CUDA only) Enable tweaks for running ' +
                        'with Nvidia CUDA Multi-process services daemon')

    depends_on('mpi', when='+mpi')
    depends_on('mpi', when='+mpiio')
    depends_on('fftw-api@3', when='+kspace')
    depends_on('voropp+pic', when='+voronoi')
    depends_on('netcdf-c+mpi', when='+user-netcdf')
    depends_on('blas', when='+user-atc')
    depends_on('lapack', when='+user-atc')
    depends_on('opencl', when='+opencl')
    depends_on('latte@1.0.1', when='@:20180222+latte')
    depends_on('latte@1.1.1:', when='@20180316:20180628+latte')
    depends_on('latte@1.2.1:', when='@20180629:20200505+latte')
    depends_on('latte@1.2.2:', when='@20200602:+latte')
    depends_on('blas', when='+latte')
    depends_on('lapack', when='+latte')
    depends_on('python', when='+python')
    depends_on('mpi', when='+user-lb')
    depends_on('mpi', when='+user-h5md')
    depends_on('hdf5', when='+user-h5md')
    depends_on('jpeg', when='+jpeg')
    depends_on('kim-api', when='+kim')
    depends_on('libpng', when='+png')
    depends_on('ffmpeg', when='+ffmpeg')
    depends_on('kokkos+deprecated_code+shared@3.0.00', when='@20200303+kokkos')
    depends_on('kokkos+shared@3.1:', when='@20200505:+kokkos')
    depends_on('adios2', when='+user-adios')
    depends_on('plumed', when='+user-plumed')
    depends_on('eigen@3:', when='+user-smd')

    conflicts('+cuda', when='+opencl')
    conflicts('+body', when='+poems@:20180628')
    conflicts('+latte', when='@:20170921')
    conflicts('+python', when='~lib')
    conflicts('+qeq', when='~manybody')
    conflicts('+user-atc', when='~manybody')
    conflicts('+user-misc', when='~manybody')
    conflicts('+user-phonon', when='~kspace')
    conflicts('+user-misc', when='~manybody')
    conflicts('%gcc@9:', when='@:20200303+openmp')
    conflicts('+kokkos', when='@:20200227')
    conflicts(
        '+meam', when='@20181212:',
        msg='+meam was removed after @20181212, use +user-meamc instead')
    conflicts(
        '+user-meamc', when='@:20181212',
        msg='+user-meamc only added @20181212, use +meam instead')
    conflicts(
        '+user-reaction', when='@:20200303',
        msg='+user-reaction only supported for version 20200505 and later')
    conflicts('+mliap', when='~snap')
    conflicts(
        '+user-adios +mpi', when='^adios2~mpi',
        msg='With +user-adios, mpi setting for adios2 and lammps must be the same')
    conflicts(
        '+user-adios ~mpi', when='^adios2+mpi',
        msg='With +user-adios, mpi setting for adios2 and lammps must be the same')

    patch("lib.patch", when="@20170901")
    patch("660.patch", when="@20170922")
    patch("gtest_fix.patch", when="@:20210310 %aocc@3.2.0")
    patch("https://github.com/lammps/lammps/commit/562300996285fdec4ef74542383276898555af06.patch?full_index=1",
          sha256="e6f1b62bbfdc79d632f4cea98019202d0dd25aa4ae61a70df1164cb4f290df79",
          when="@20200721 +cuda")

    root_cmakelists_dir = 'cmake'

    def cmake_args(self):
        spec = self.spec

        mpi_prefix = 'ENABLE'
        pkg_prefix = 'ENABLE'
        if spec.satisfies('@20180629:'):
            mpi_prefix = 'BUILD'
            pkg_prefix = 'PKG'

        args = [
            self.define_from_variant('BUILD_SHARED_LIBS', 'lib'),
            self.define_from_variant('LAMMPS_EXCEPTIONS', 'exceptions'),
            '-D{0}_MPI={1}'.format(
                mpi_prefix,
                'ON' if '+mpi' in spec else 'OFF'),
            self.define_from_variant('BUILD_OMP', 'openmp'),
            '-DENABLE_TESTING=ON'
        ]
        if spec.satisfies('+cuda'):
            args.append('-DPKG_GPU=ON')
            args.append('-DGPU_API=cuda')
            cuda_arch = spec.variants['cuda_arch'].value
            if cuda_arch != 'none':
                args.append('-DGPU_ARCH=sm_{0}'.format(cuda_arch[0]))
            args.append(self.define_from_variant('CUDA_MPS_SUPPORT', 'cuda_mps'))
        elif spec.satisfies('+opencl'):
            args.append('-DPKG_GPU=ON')
            args.append('-DGPU_API=opencl')
        else:
            args.append('-DPKG_GPU=OFF')

        if spec.satisfies('@20180629:+lib'):
            args.append('-DBUILD_LIB=ON')

        if spec.satisfies('%aocc'):
            cxx_flags = '-Ofast -mfma -fvectorize -funroll-loops'
            args.append(self.define('CMAKE_CXX_FLAGS_RELEASE', cxx_flags))

        args.append(self.define_from_variant('WITH_JPEG', 'jpeg'))
        args.append(self.define_from_variant('WITH_PNG', 'png'))
        args.append(self.define_from_variant('WITH_FFMPEG', 'ffmpeg'))

        for pkg in self.supported_packages:
            opt = '-D{0}_{1}'.format(pkg_prefix, pkg.upper())
            if '+{0}'.format(pkg) in spec:
                args.append('{0}=ON'.format(opt))
            else:
                args.append('{0}=OFF'.format(opt))
        if '+kim' in spec:
            args.append('-DPKG_KIM=ON')
        if '+kspace' in spec:
            if '^fftw' in spec:
                args.append('-DFFT=FFTW3')
            if '^mkl' in spec:
                args.append('-DFFT=MKL')
            if '^amdfftw' in spec:
                # If FFTW3 is selected, then CMake will try to detect, if threaded
                # FFTW libraries are available and enable them by default.
                args.append(self.define('FFT', 'FFTW3'))
                # Using the -DFFT_SINGLE setting trades off a little accuracy
                # for reduced memory use and parallel communication costs
                # for transposing 3d FFT data.
                args.append(self.define('FFT_SINGLE', True))

        if '+kokkos' in spec:
            args.append('-DEXTERNAL_KOKKOS=ON')
        if '+user-adios' in spec:
            args.append('-DADIOS2_DIR={0}'.format(self.spec['adios2'].prefix))
        if '+user-plumed' in spec:
            args.append('-DDOWNLOAD_PLUMED=no')
            if '+shared' in self.spec['plumed']:
                args.append('-DPLUMED_MODE=shared')
            else:
                args.append('-DPLUMED_MODE=static')
        if '+user-smd' in spec:
            args.append('-DDOWNLOAD_EIGEN3=no')
            args.append('-DEIGEN3_INCLUDE_DIR={0}'.format(
                self.spec['eigen'].prefix.include))

        return args

    def setup_run_environment(self, env):
        env.set('LAMMPS_POTENTIALS',
                self.prefix.share.lammps.potentials)
