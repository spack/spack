# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import datetime as dt


class Lammps(CMakePackage):
    """LAMMPS stands for Large-scale Atomic/Molecular Massively
    Parallel Simulator. This package uses patch releases, not
    stable release.
    See https://github.com/spack/spack/pull/5342 for a detailed
    discussion.
    """
    homepage = "http://lammps.sandia.gov/"
    url      = "https://github.com/lammps/lammps/archive/patch_1Sep2017.tar.gz"
    git      = "https://github.com/lammps/lammps.git"

    tags = ['ecp', 'ecp-apps']

    version('develop', branch='master')
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
    version('20180629', '6d5941863ee25ad2227ff3b7577d5e7c')
    version('20180316', '25bad35679583e0dd8cb8753665bb84b')
    version('20180222', '4d0513e3183bd57721814d217fdaf957')
    version('20170922', '4306071f919ec7e759bda195c26cfd9a')
    version('20170901', '767e7f07289663f033474dfe974974e7')

    def url_for_version(self, version):
        vdate = dt.datetime.strptime(str(version), "%Y%m%d")
        return "https://github.com/lammps/lammps/archive/patch_{0}.tar.gz".format(
            vdate.strftime("%d%b%Y").lstrip('0'))

    supported_packages = ['asphere', 'body', 'class2', 'colloid', 'compress',
                          'coreshell', 'dipole', 'granular', 'kspace', 'latte',
                          'manybody', 'mc', 'meam', 'misc', 'molecule',
                          'mpiio', 'peri', 'poems', 'python', 'qeq', 'reax',
                          'replica', 'rigid', 'shock', 'snap', 'srd',
                          'user-atc', 'user-h5md', 'user-lb', 'user-misc',
                          'user-netcdf', 'user-omp', 'voronoi']

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
    variant('openmp', default=True, description='Build with OpenMP')
    variant('exceptions', default=False,
            description='Build with lammps exceptions')

    depends_on('mpi', when='+mpi')
    depends_on('mpi', when='+mpiio')
    depends_on('fftw', when='+kspace')
    depends_on('voropp+pic', when='+voronoi')
    depends_on('netcdf+mpi', when='+user-netcdf')
    depends_on('blas', when='+user-atc')
    depends_on('lapack', when='+user-atc')
    depends_on('latte@1.0.1', when='@:20180222+latte')
    depends_on('latte@1.1.1:', when='@20180316:20180628+latte')
    depends_on('latte@1.2.1:', when='@20180629:+latte')
    depends_on('blas', when='+latte')
    depends_on('lapack', when='+latte')
    depends_on('python', when='+python')
    depends_on('mpi', when='+user-lb')
    depends_on('mpi', when='+user-h5md')
    depends_on('hdf5', when='+user-h5md')
    depends_on('jpeg', when='+jpeg')
    depends_on('libpng', when='+png')
    depends_on('ffmpeg', when='+ffmpeg')

    conflicts('+body', when='+poems@:20180628')
    conflicts('+latte', when='@:20170921')
    conflicts('+python', when='~lib')
    conflicts('+qeq', when='~manybody')
    conflicts('+user-atc', when='~manybody')
    conflicts('+user-misc', when='~manybody')
    conflicts('+user-phonon', when='~kspace')
    conflicts('+user-misc', when='~manybody')
    conflicts('%gcc@9:', when='+openmp')

    patch("lib.patch", when="@20170901")
    patch("660.patch", when="@20170922")

    root_cmakelists_dir = 'cmake'

    def cmake_args(self):
        spec = self.spec

        mpi_prefix = 'ENABLE'
        pkg_prefix = 'ENABLE'
        if spec.satisfies('@20180629:'):
            mpi_prefix = 'BUILD'
            pkg_prefix = 'PKG'

        args = [
            '-DBUILD_SHARED_LIBS={0}'.format(
                'ON' if '+lib' in spec else 'OFF'),
            '-DLAMMPS_EXCEPTIONS={0}'.format(
                'ON' if '+exceptions' in spec else 'OFF'),
            '-D{0}_MPI={1}'.format(
                mpi_prefix,
                'ON' if '+mpi' in spec else 'OFF'),
            '-DBUILD_OMP={0}'.format(
                'ON' if '+openmp' in spec else 'OFF'),
        ]

        if spec.satisfies('@20180629:+lib'):
            args.append('-DBUILD_LIB=ON')

        args.append('-DWITH_JPEG={0}'.format(
            'ON' if '+jpeg' in spec else 'OFF'))
        args.append('-DWITH_PNG={0}'.format(
            'ON' if '+png' in spec else 'OFF'))
        args.append('-DWITH_FFMPEG={0}'.format(
            'ON' if '+ffmpeg' in spec else 'OFF'))

        for pkg in self.supported_packages:
            opt = '-D{0}_{1}'.format(pkg_prefix, pkg.upper())
            if '+{0}'.format(pkg) in spec:
                args.append('{0}=ON'.format(opt))
            else:
                args.append('{0}=OFF'.format(opt))
        if '+kspace' in spec:
            args.append('-DFFT=FFTW3')

        return args
