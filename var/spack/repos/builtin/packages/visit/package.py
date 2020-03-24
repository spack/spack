# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Visit(CMakePackage):
    """VisIt is an Open Source, interactive, scalable, visualization,
       animation and analysis tool."""
    homepage = "https://wci.llnl.gov/simulation/computer-codes/visit/"
    url = "https://portal.nersc.gov/project/visit/releases/3.0.1/visit3.0.1.tar.gz"

    version('3.0.1', sha256='a506d4d83b8973829e68787d8d721199523ce7ec73e7594e93333c214c2c12bd')
    version('2.13.3', sha256='cf0b3d2e39e1cd102dd886d3ef6da892733445e362fc28f24d9682012cccf2e5')
    version('2.13.0', sha256='716644b8e78a00ff82691619d4d1e7a914965b6535884890b667b97ba08d6a0f')
    version('2.12.3', sha256='2dd351a291ee3e79926bc00391ca89b202cfa4751331b0fdee1b960c7922161f')
    version('2.12.2', sha256='55897d656ac2ea4eb87a30118b2e3963d6c8a391dda0790268426a73e4b06943')
    version('2.10.3', sha256='05018215c4727eb42d47bb5cc4ff937b2a2ccaca90d141bc7fa426a0843a5dbc')
    version('2.10.2', sha256='89ecdfaf197ef431685e31b75628774deb6cd75d3e332ef26505774403e8beff')
    version('2.10.1', sha256='6b53dea89a241fd03300a7a3a50c0f773e2fb8458cd3ad06816e9bd2f0337cd8')

    variant('gui',    default=True, description='Enable VisIt\'s GUI')
    variant('adios2', default=False, description='Enable ADIOS2 file format')
    variant('hdf5',   default=True, description='Enable HDF5 file format')
    variant('silo',   default=True, description='Enable Silo file format')
    variant('python', default=True, description='Enable Python support')
    variant('mpi',    default=True, description='Enable parallel engine')

    patch('spack-changes.patch')
    patch('nonframework-qwt.patch', when='^qt~framework platform=darwin')
    patch('parallel-hdf5.patch', when='+hdf5+mpi')

    depends_on('cmake@3.0:', type='build')
    depends_on('vtk@8.1.0:+opengl2', when='@3.0:3.0.1')
    depends_on('vtk@6.1.0~opengl2', when='@:2.999')
    depends_on('vtk+python', when='+python @3.0:')
    depends_on('vtk~mpi', when='~mpi')
    depends_on('vtk+qt', when='+gui')
    depends_on('qt@4.8.6:4.999', when='+gui @:2.999')
    depends_on('qt@5.10:', when='+gui @3.0:')
    depends_on('qwt', when='+gui')
    depends_on('python@2.6:2.8', when='+python')
    depends_on('silo+shared', when='+silo')
    depends_on('hdf5~mpi', when='+hdf5~mpi')
    depends_on('hdf5+mpi', when='+hdf5+mpi')
    depends_on('mpi', when='+mpi')
    depends_on('adios2', when='+adios2')

    conflicts('+adios2', when='@:2.999')
    conflicts('+hdf5', when='~gui @:2.999')
    conflicts('+silo', when='~gui @:2.999')

    root_cmakelists_dir = 'src'

    @when('@3.0.0:3.0.1')
    def patch(self):
        # Some of VTK's targets don't create explicit libraries, so there is no
        # 'vtktiff'. Instead, replace with the library variable defined from
        # VTK's module flies (e.g. lib/cmake/vtk-8.1/Modules/vtktiff.cmake)
        for filename in find('src', 'CMakeLists.txt'):
            filter_file(r'\bvtk(tiff|jpeg|png)', r'${vtk\1_LIBRARIES}',
                        filename)

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DVTK_MAJOR_VERSION=' + str(spec['vtk'].version[0]),
            '-DVTK_MINOR_VERSION=' + str(spec['vtk'].version[1]),
            '-DVISIT_VTK_DIR:PATH=' + spec['vtk'].prefix,
            '-DVISIT_ZLIB_DIR:PATH=' + spec['zlib'].prefix,
            '-DVISIT_USE_GLEW=OFF',
            '-DCMAKE_CXX_FLAGS=' + self.compiler.pic_flag,
            '-DCMAKE_C_FLAGS=' + self.compiler.pic_flag,
        ]

        if '+python' in spec:
            args.append('-DPYTHON_DIR:PATH={0}'.format(spec['python'].home))

        if '+gui' in spec:
            qt_bin = spec['qt'].prefix.bin
            args.extend([
                '-DVISIT_LOC_QMAKE_EXE:FILEPATH={0}/qmake'.format(qt_bin),
                '-DVISIT_QT_DIR:PATH=' + spec['qt'].prefix,
                '-DVISIT_QWT_DIR:PATH=' + spec['qwt'].prefix
            ])
        else:
            args.append('-DVISIT_SERVER_COMPONENTS_ONLY=ON')
            args.append('-DVISIT_ENGINE_ONLY=ON')

        if '+hdf5' in spec:
            args.append(
                '-DVISIT_HDF5_DIR:PATH={0}'.format(spec['hdf5'].prefix))
            if '+mpi' in spec:
                args.append('-DVISIT_HDF5_MPI_DIR:PATH={0}'.format(
                    spec['hdf5'].prefix))

        if '+silo' in spec:
            args.append(
                '-DVISIT_SILO_DIR:PATH={0}'.format(spec['silo'].prefix))

        if '+mpi' in spec:
            args.append('-DVISIT_PARALLEL=ON')
            args.append('-DVISIT_C_COMPILER={0}'.format(spec['mpi'].mpicc))
            args.append('-DVISIT_CXX_COMPILER={0}'.format(spec['mpi'].mpicxx))
            args.append('-DVISIT_MPI_COMPILER={0}'.format(spec['mpi'].mpicxx))

        return args
