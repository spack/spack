from spack import *
import re
import sys

class Cactus(Package):

    """
    Cactus is an open source problem solving environment designed for scientists
    and engineers. Its modular structure easily enables parallel computation
    across different architectures and collaborative code development between
    different groups. Cactus originated in the academic research community,
    where it was developed and used over many years by a large international
    collaboration of physicists and computational scientists.
    """

    homepage = "http://cactuscode.org"

    version(
        'ET_2015_11_v0',
        git='https://bitbucket.org/cactuscode/cactus.git',
        tag='ET_2015_11_v0')

    variant('debug', default=False, description="Compile with run-time checks (runs very slowly")
    variant('optimize', default=True, description="Optimize")

    variant('fortran', default=True, description="Enable Fortran code")
    variant('openmp', default=True, description="Use OpenMP multi-threading")

    variant('carpet', default=True, description="Provide Carpet AMR")
    variant('ctthorns', default=True, description="Include CTThorns")
    variant('einsteintoolkit', default=True, description="Include Einstein Toolkit")
    variant('f5', default=True, description="Provide F5 library")
    variant('lorene', default=True, description="Provide LORENE library")
    variant('pittnullcode', default=True, description="Include PITTNullCode")
    variant('wvuthorns', default=True, description="Include WVUThorns")

    variant('fftw', default=True, description="Use FFTW")
    variant('gsl', default=True, description="Use GSL")
    variant('hdf5', default=True, description="Support HDF5 I/O")
    variant('hwloc', default=True, description="Use hwloc")
    variant('lapack', default=True, description="Use BLAS and LAPACK")
    variant('mpi', default=True, description="Use MPI")
    variant('papi', default=True, description="Use PAPI")
    variant('petsc', default=True, description="Use PETSc")

    depends_on('fftw +float -mpi', when='+fftw -mpi')
    depends_on('fftw +float +mpi', when='+fftw +mpi')
    depends_on('gsl', when='+gsl')
    depends_on('hdf5', when='+hdf5')
    depends_on('hwloc', when='+hwloc')
    depends_on('lapack', when='+lapack')
    depends_on('mpi', when='+mpi')
    depends_on('papi', when='+papi')
    depends_on('petsc', when='+petsc')
    depends_on('zlib', when='+hdf5')

    # Cactus
    resource(
        name='CactusBase',
        git='https://bitbucket.org/cactuscode/cactusbase.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='CactusBase')
    resource(
        name='CactusConnect',
        git='https://bitbucket.org/cactuscode/cactusconnect.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='CactusConnect')
    resource(
        name='CactusElliptic',
        git='https://bitbucket.org/cactuscode/cactuselliptic.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='CactusElliptic')
    resource(
        name='CactusExamples',
        git='https://bitbucket.org/cactuscode/cactusexamples.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='CactusExamples')
    resource(
        name='CactusIO',
        git='https://bitbucket.org/cactuscode/cactusio.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='CactusIO')
    resource(
        name='CactusNumerical',
        git='https://bitbucket.org/cactuscode/cactusnumerical.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='CactusNumerical')
    resource(
        name='CactusPUGH',
        git='https://bitbucket.org/cactuscode/cactuspugh.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='CactusPUGH')
    resource(
        name='CactusPUGHIO',
        git='https://bitbucket.org/cactuscode/cactuspughio.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='CactusPUGHIO')
    resource(
        name='CactusTest',
        git='https://bitbucket.org/cactuscode/cactustest.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='CactusTest')
    resource(
        name='CactusUtils',
        git='https://bitbucket.org/cactuscode/cactusutils.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='CactusUtils')
    resource(
        name='CactusWave',
        git='https://bitbucket.org/cactuscode/cactuswave.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='CactusWave')

    resource(
        name='CoreDoc',
        git='https://bitbucket.org/cactuscode/coredoc.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='CoreDoc')
    resource(
        name='Kranc',
        git='https://github.com/ianhinder/Kranc.git',
        tag='ET_2015_11_v0',
        destination='repos')
    resource(
        name='Numerical',
        git='https://bitbucket.org/cactuscode/numerical.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='Numerical')

    # Utilities
    resource(
        name='examples',
        git='https://bitbucket.org/einsteintoolkit/einsteinexamples.git',
        tag='ET_2015_11_v0',
        destination='.',
        subdir='examples',
        when='+einsteintoolkit')
    resource(
        name='manifest',
        git='https://bitbucket.org/einsteintoolkit/manifest.git',
        tag='ET_2015_11_v0',
        destination='.',
        subdir='manifest',
        when='+einsteintoolkit')
    resource(
        name='simfactory',
        git='https://bitbucket.org/simfactory/simfactory2.git',
        tag='ET_2015_11_v0',
        destination='.',
        subdir='simfactory')
    resource(
        name='utils',
        git='https://bitbucket.org/cactuscode/utilities.git',
        tag='ET_2015_11_v0',
        destination='.',
        subdir='utils')

    # Carpet
    resource(
        name='Carpet',
        git='https://bitbucket.org/eschnett/carpet.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='Carpet',
        when='+carpet')

    # Einstein Toolkit
    resource(
        name='EinsteinAnalysis',
        git='https://bitbucket.org/einsteintoolkit/einsteinanalysis.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='EinsteinAnalysis',
        when='+einsteintoolkit')
    resource(
        name='EinsteinBase',
        git='https://bitbucket.org/einsteintoolkit/einsteinbase.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='EinsteinBase',
        when='+einsteintoolkit')
    resource(
        name='EinsteinEOS',
        git='https://bitbucket.org/einsteintoolkit/einsteineos.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='EinsteinEOS',
        when='+einsteintoolkit')
    resource(
        name='EinsteinEvolve',
        git='https://bitbucket.org/einsteintoolkit/einsteinevolve.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='EinsteinEvolve',
        when='+einsteintoolkit')
    resource(
        name='EinsteinInitialData',
        git='https://bitbucket.org/einsteintoolkit/einsteininitialdata.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='EinsteinInitialData',
        when='+einsteintoolkit')
    resource(
        name='EinsteinUtils',
        git='https://bitbucket.org/einsteintoolkit/einsteinutils.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='EinsteinUtils',
        when='+einsteintoolkit')

    resource(
        name='CTThorns',
        git='https://bitbucket.org/eloisa/ctthorns.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='CTThorns',
        when='+ctthorns')
    resource(
        name='EinsteinExact',
        git='https://github.com/barrywardell/EinsteinExact.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='EinsteinExact',
        when='+einsteintoolkit')
    resource(
        name='McLachlan',
        git='https://bitbucket.org/einsteintoolkit/mclachlan.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='McLachlan',
        when='+einsteintoolkit')
    resource(
        name='PITTNullCode',
        git='https://bitbucket.org/einsteintoolkit/pittnullcode.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='PITTNullCode',
        when='+pittnullcode')
    resource(
        name='WVUThorns',
        git='https://bitbucket.org/zach_etienne/wvuthorns.git',
        tag='ET_2015_11_v0',
        destination='arrangements',
        subdir='WVUThorns',
        when='+wvuthorns')

    # External Libraries
    resource(
        name='BLAS',
        svn='https://svn.cactuscode.org/projects/ExternalLibraries/BLAS/tags/ET_2015_11_v0',
        destination='arrangements/ExternalLibraries',
        subdir='BLAS',
        when='+lapack')
    resource(
        name='F5',
        svn='https://svn.cactuscode.org/projects/ExternalLibraries/F5/trunk',
        destination='arrangements/ExternalLibraries',
        subdir='F5',
        when='+f5')
    resource(
        name='FFTW3',
        svn='https://svn.cactuscode.org/projects/ExternalLibraries/FFTW3/tags/ET_2015_11_v0',
        destination='arrangements/ExternalLibraries',
        subdir='FFTW3',
        when='+fftw')
    resource(
        name='GSL',
        svn='https://svn.cactuscode.org/projects/ExternalLibraries/GSL/tags/ET_2015_11_v0',
        destination='arrangements/ExternalLibraries',
        subdir='GSL',
        when='+gsl')
    resource(
        name='HDF5',
        svn='https://svn.cactuscode.org/projects/ExternalLibraries/HDF5/tags/ET_2015_11_v0',
        destination='arrangements/ExternalLibraries',
        subdir='HDF5',
        when='+hdf5')
    resource(
        name='hwloc',
        svn='https://svn.cactuscode.org/projects/ExternalLibraries/hwloc/tags/ET_2015_11_v0',
        destination='arrangements/ExternalLibraries',
        subdir='hwloc',
        when='+hwloc')
    resource(
        name='LAPACK',
        svn='https://svn.cactuscode.org/projects/ExternalLibraries/LAPACK/tags/ET_2015_11_v0',
        destination='arrangements/ExternalLibraries',
        subdir='LAPACK',
        when='+lapack')
    resource(
        name='LORENE',
        svn='https://svn.cactuscode.org/projects/ExternalLibraries/LORENE/tags/ET_2015_11_v0',
        destination='arrangements/ExternalLibraries',
        subdir='LORENE',
        when='+lorene')
    resource(
        name='MPI',
        svn='https://svn.cactuscode.org/projects/ExternalLibraries/MPI/tags/ET_2015_11_v0',
        destination='arrangements/ExternalLibraries',
        subdir='MPI',
        when='+mpi')
    resource(
        name='PAPI',
        svn='https://svn.cactuscode.org/projects/ExternalLibraries/PAPI/tags/ET_2015_11_v0',
        destination='arrangements/ExternalLibraries',
        subdir='PAPI',
        when='+papi')
    resource(
        name='PETSc',
        svn='https://svn.cactuscode.org/projects/ExternalLibraries/PETSc/tags/ET_2015_11_v0',
        destination='arrangements/ExternalLibraries',
        subdir='PETSc',
        when='+petsc')
    resource(
        name='zlib',
        svn='https://svn.cactuscode.org/projects/ExternalLibraries/zlib/tags/ET_2015_11_v0',
        destination='arrangements/ExternalLibraries',
        subdir='zlib',
        when='+hdf5')

    def mkOptionList(self, spec, prefix):
        optionlist = []
        if '+fortran' in spec:
            optionlist += [
                '# Fortran',
                'FPPFLAGS = -traditional',
                'F90FLAGS = -fcray-pointer',
                'LIBS = gfortran',
                '']
        if '+debug' in spec:
            if '+optimize' in spec:
                tty.error("Cannot combine +debug and +optimize")
            optionlist += [
                'DEBUG = yes',
                'CPP_DEBUG_FLAGS = -DCARPET_DEBUG',
                'FPP_DEBUG_FLAGS = -DCARPET_DEBUG',
                '']
        else:
            optionlist += [
                'DEBUG = no',
                '']
        if '+optimize' in spec:
            optionlist += [
                'OPTIMISE = yes',
                '']
        else:
            optionlist += [
                'OPTIMISE = no',
                '']
        optionlist += [
            'WARN = yes',
            '']
        if '+openmp' in spec:
            optionlist += [
                'OPENMP = yes',
                'CPP_OPENMP_FLAGS = -fopenmp',
                'FPP_OPENMP_FLAGS = -fopenmp',
                'C_OPENMP_FLAGS = -fopenmp',
                'CXX_OPENMP_FLAGS = -fopenmp',
                'F90_OPENMP_FLAGS = -fopenmp',
                '']

        if '+carpet' in spec and '+mpi' not in spec:
            tty.error("Variant +carpet requires +mpi")
        if '+f5' in spec and ('+hdf5' not in spec or '+mpi' not in spec):
            tty.error("Variant +f5 requires both +hdf5 and +mpi")

        if '+fftw' in spec:
            if '+mpi' in spec['fftw'] and '+mpi' not in spec:
                tty.error("FFTW variant +mpi requires Cactus variant +mpi")
            optionlist += [
                '# FFTW',
                'FFTW3_DIR = %s' % spec['fftw'].prefix,
                '']
        if '+gsl' in spec:
            optionlist += [
                '# GSL',
                'GSL_DIR = %s' % spec['gsl'].prefix,
                '']
        if '+hdf5' in spec:
            if '+mpi' in spec['hdf5'] and '+mpi' not in spec:
                tty.error("HDF5 variant +mpi requires Cactus variant +mpi")
            optionlist += [
                '# HDF5',
                'HDF5_DIR = %s' % spec['hdf5'].prefix,
                'ZLIB_DIR = %s' % spec['zlib'].prefix,
                '']
        if '+hwloc' in spec:
            optionlist += [
                '# hwloc',
                'HWLOC_DIR = %s' % spec['hwloc'].prefix,
                '']
        if '+lapack' in spec:
            optionlist += [
                '# LAPACK',
                'BLAS_DIR = %s' % spec['lapack'].prefix,
                'LAPACK_DIR = %s' % spec['lapack'].prefix,
                '']
        if '+mpi' in spec:
            optionlist += [
                '# MPI',
                'MPI_DIR = %s' % spec['mpi'].prefix,
                '']
        if '+papi' in spec:
            optionlist += [
                '# PAPI',
                'PAPI_DIR = %s' % spec['papi'].prefix,
                '']
        if '+petsc' in spec:
            optionlist += [
                '# PETSc',
                'PETSC_DIR = %s' % spec['petsc'].prefix,
                '']
        optionlist += [
            'PTHREADS = yes',
            '']

        return optionlist

    def mkThornList(self, spec, prefix):
        thornlist = [
            '# Cactus',
            '',
            'CactusBase/Boundary',
            'CactusBase/CartGrid3D',
            'CactusBase/CoordBase',
            'CactusBase/Fortran',
            'CactusBase/InitBase',
            'CactusBase/IOASCII',
            'CactusBase/IOBasic',
            'CactusBase/IOUtil',
            'CactusBase/SymBase',
            'CactusBase/Time',
            '',
            'CactusConnect/HTTPD',
            'CactusConnect/HTTPDExtra',
            'CactusConnect/Socket',
            '',
            'CactusElliptic/EllBase',
            '#[+petsc] CactusElliptic/EllPETSc',
            'CactusElliptic/EllSOR',
            'CactusElliptic/TATelliptic',
            '#[+petsc] CactusElliptic/TATPETSc',
            '',
            'CactusExamples/DemoInterp',
            'CactusExamples/FleshInfo',
            'CactusExamples/HelloWorld',
            '#DISABLED CactusExamples/HelloWorldCUDA',
            '#DISABLED CactusExamples/HelloWorldOpenCL',
            'CactusExamples/IDWaveMoL',
            '#[+carpet] CactusExamples/Poisson',
            'CactusExamples/SampleBoundary',
            'CactusExamples/SampleIO',
            'CactusExamples/TimerInfo',
            'CactusExamples/WaveMoL',
            'CactusExamples/WaveToy1DF77',
            'CactusExamples/WaveToy2DF77',
            '#DISABLED CactusExamples/WaveToyOpenCL',
            '',
            '#TODO CactusIO/IOJpeg',
            '',
            'CactusNumerical/Cartoon2D',
            'CactusNumerical/Dissipation',
            'CactusNumerical/InterpToArray',
            'CactusNumerical/LocalInterp',
            'CactusNumerical/LocalInterp2',
            'CactusNumerical/LocalReduce',
            'CactusNumerical/MoL',
            'CactusNumerical/Noise',
            'CactusNumerical/Norms',
            'CactusNumerical/Periodic',
            'CactusNumerical/ReflectionSymmetry',
            'CactusNumerical/RotatingSymmetry180',
            'CactusNumerical/RotatingSymmetry90',
            'CactusNumerical/Slab',
            'CactusNumerical/SlabTest',
            'CactusNumerical/SpaceMask',
            'CactusNumerical/SphericalSurface',
            'CactusNumerical/SummationByParts',
            'CactusNumerical/TensorTypes',
            'CactusNumerical/TestLocalInterp2',
            'CactusNumerical/TestLocalReduce',
            '',
            'CactusPUGH/PUGH',
            'CactusPUGH/PUGHInterp',
            'CactusPUGH/PUGHReduce',
            'CactusPUGH/PUGHSlab',
            '',
            '#[+hdf5] CactusPUGHIO/IOHDF5',
            '#[+hdf5] CactusPUGHIO/IOHDF5Util',
            '',
            '#DISABLED CactusTest/TestAllTypes',
            'CactusTest/TestArrays',
            'CactusTest/TestComplex',
            'CactusTest/TestCoordinates',
            'CactusTest/TestFortranCrayPointers',
            'CactusTest/TestFortranDependencies1',
            'CactusTest/TestFortranDependencies2',
            'CactusTest/TestFpointerNULL',
            'CactusTest/TestFreeF90',
            'CactusTest/TestGlobalReduce',
            'CactusTest/TestInclude1',
            'CactusTest/TestInclude2',
            'CactusTest/TestLoop',
            'CactusTest/TestMath',
            'CactusTest/TestMoL',
            'CactusTest/TestPar',
            'CactusTest/TestReduce',
            'CactusTest/TestSchedule',
            'CactusTest/TestStrings',
            'CactusTest/TestTable',
            'CactusTest/TestTimers',
            'CactusTest/TestTypes',
            '',
            '#DISABLED CactusUtils/Accelerator',
            'CactusUtils/Formaline',
            '#[+hwloc] #[+mpi] CactusUtils/MemSpeed',
            'CactusUtils/NaNCatcher',
            'CactusUtils/NaNChecker',
            'CactusUtils/Nice',
            'CactusUtils/NoMPI',
            '#DISABLED CactusUtils/OpenCLRunTime',
            'CactusUtils/SystemStatistics',
            '#[+hwloc] #[+mpi] CactusUtils/SystemTopology',
            'CactusUtils/TerminationTrigger',
            'CactusUtils/TimerReport',
            'CactusUtils/Trigger',
            'CactusUtils/Vectors',
            '',
            '#[+fortran] CactusWave/IDScalarWave',
            'CactusWave/IDScalarWaveC',
            'CactusWave/IDScalarWaveCXX',
            'CactusWave/IDScalarWaveElliptic',
            'CactusWave/WaveBinarySource',
            'CactusWave/WaveToyC',
            'CactusWave/WaveToyCXX',
            'CactusWave/WaveToyExtra',
            '#[+fortran] CactusWave/WaveToyF77',
            '#[+fortran] CactusWave/WaveToyF90',
            '#[+fortran] CactusWave/WaveToyFreeF90',
            '',
            '# Kranc',
            'KrancNumericalTools/GenericFD',
            '',
            '# Numerical',
            'Numerical/AEILocalInterp',
            '',
            '# Einstein Toolkit'
            '',
            '#[+einsteintoolkit] EinsteinAnalysis/ADMAnalysis',
            '#[+einsteintoolkit] EinsteinAnalysis/ADMMass',
            '#[+einsteintoolkit] EinsteinAnalysis/AHFinder',
            '#[+einsteintoolkit] EinsteinAnalysis/AHFinderDirect',
            '#[+einsteintoolkit] EinsteinAnalysis/CalcK',
            '#[+einsteintoolkit] EinsteinAnalysis/EHFinder',
            '#[+einsteintoolkit] EinsteinAnalysis/Extract',
            '#[+einsteintoolkit] EinsteinAnalysis/Hydro_Analysis',
            '#[+einsteintoolkit] EinsteinAnalysis/Multipole',
            '#[+einsteintoolkit] EinsteinAnalysis/Outflow',
            '#[+einsteintoolkit] EinsteinAnalysis/PunctureTracker',
            '#[+einsteintoolkit] EinsteinAnalysis/QuasiLocalMeasures',
            '#[+einsteintoolkit] EinsteinAnalysis/WeylScal4',
            '',
            '#[+einsteintoolkit] EinsteinBase/ADMBase',
            '#[+einsteintoolkit] EinsteinBase/ADMCoupling',
            '#[+einsteintoolkit] EinsteinBase/ADMMacros',
            '#[+einsteintoolkit] EinsteinBase/Constants',
            '#[+einsteintoolkit] EinsteinBase/CoordGauge',
            '#[+einsteintoolkit] EinsteinBase/EOS_Base',
            '#[+einsteintoolkit] EinsteinBase/HydroBase',
            '#[+einsteintoolkit] EinsteinBase/StaticConformal',
            '#[+einsteintoolkit] EinsteinBase/TmunuBase',
            '',
            '#[+einsteintoolkit] EinsteinEOS/EOS_Hybrid',
            '#[+einsteintoolkit] EinsteinEOS/EOS_IdealFluid',
            '#[+einsteintoolkit] EinsteinEOS/EOS_Omni',
            '#[+einsteintoolkit] EinsteinEOS/EOS_Polytrope',
            '',
            '#[+einsteintoolkit] EinsteinEvolve/GRHydro',
            '#[+einsteintoolkit] EinsteinEvolve/GRHydro_InitData',
            '#[+einsteintoolkit] EinsteinEvolve/NewRad',
            '',
            '#[+einsteintoolkit] EinsteinInitialData/DistortedBHIVP',
            '#[+einsteintoolkit] EinsteinInitialData/Exact',
            '#[+einsteintoolkit] EinsteinInitialData/Hydro_InitExcision',
            '#[+einsteintoolkit] EinsteinInitialData/IDAnalyticBH',
            '#[+einsteintoolkit] EinsteinInitialData/IDAxiBrillBH',
            '#[+einsteintoolkit] EinsteinInitialData/IDAxiOddBrillBH',
            '#[+einsteintoolkit] EinsteinInitialData/IDBrillData',
            '#[+einsteintoolkit] EinsteinInitialData/IDConstraintViolate',
            '#[+einsteintoolkit] EinsteinInitialData/IDFileADM',
            '#[+einsteintoolkit] EinsteinInitialData/IDLinearWaves',
            '#[+einsteintoolkit] EinsteinInitialData/Meudon_Bin_BH',
            '#[+einsteintoolkit] EinsteinInitialData/Meudon_Bin_NS',
            '#[+einsteintoolkit] EinsteinInitialData/Meudon_Mag_NS',
            '#[+einsteintoolkit] EinsteinInitialData/NoExcision',
            '#[+einsteintoolkit] EinsteinInitialData/RotatingDBHIVP',
            '#[+einsteintoolkit] EinsteinInitialData/TOVSolver',
            '#[+einsteintoolkit] EinsteinInitialData/TwoPunctures',
            '',
            '#[+einsteintoolkit] EinsteinUtils/SetMask_SphericalSurface',
            '#[+einsteintoolkit] EinsteinUtils/TGRtensor',
            '',
            '# EinsteinExact',
            '#[+einsteintoolkit] EinsteinExact/EinsteinExact_Test',
            '#[+einsteintoolkit] EinsteinExact/GaugeWave',
            '#[+einsteintoolkit] EinsteinExact/KerrSchild',
            '#[+einsteintoolkit] EinsteinExact/Minkowski',
            '#[+einsteintoolkit] EinsteinExact/ModifiedSchwarzschildBL',
            '#[+einsteintoolkit] EinsteinExact/ShiftedGaugeWave',
            '#[+einsteintoolkit] EinsteinExact/Vaidya2',
            '',
            '# McLachlan',
            '#[+einsteintoolkit] McLachlan/ML_ADMConstraints',
            '#[+einsteintoolkit] McLachlan/ML_ADMQuantities',
            '#[+einsteintoolkit] McLachlan/ML_BSSN',
            '#[+einsteintoolkit] McLachlan/ML_BSSN_Helper',
            '#[+einsteintoolkit] McLachlan/ML_BSSN_Test',
            '#[+einsteintoolkit] McLachlan/ML_CCZ4',
            '#[+einsteintoolkit] McLachlan/ML_CCZ4_Helper',
            '#[+einsteintoolkit] McLachlan/ML_CCZ4_Test',
            '#[+einsteintoolkit] McLachlan/ML_WaveToy',
            '#[+einsteintoolkit] #DISABLED McLachlan/ML_WaveToy_CL',
            '#[+einsteintoolkit] McLachlan/ML_WaveToy_Test',
            '',
            '# Carpet',
            '#[+carpet] #[+mpi] Carpet/Carpet',
            '#[+carpet] #[+mpi] Carpet/CarpetEvolutionMask',
            '#[+carpet] #[+mpi] Carpet/CarpetIOASCII',
            '#[+carpet] #[+mpi] Carpet/CarpetIOBasic',
            '#[+carpet] #[+mpi] #[+f5] Carpet/CarpetIOF5',
            '#[+carpet] #[+mpi] #[+hdf5] Carpet/CarpetIOHDF5',
            '#[+carpet] #[+mpi] Carpet/CarpetIOScalar',
            '#[+carpet] #[+mpi] Carpet/CarpetIntegrateTest',
            '#[+carpet] #[+mpi] Carpet/CarpetInterp',
            '#[+carpet] #[+mpi] Carpet/CarpetInterp2',
            '#[+carpet] #[+mpi] Carpet/CarpetLib',
            '#[+carpet] #[+mpi] Carpet/CarpetMask',
            '#[+carpet] #[+mpi] Carpet/CarpetProlongateTest',
            '#[+carpet] #[+mpi] Carpet/CarpetReduce',
            '#[+carpet] #[+mpi] Carpet/CarpetRegrid',
            '#[+carpet] #[+mpi] Carpet/CarpetRegrid2',
            '#[+carpet] #[+mpi] Carpet/CarpetRegridTest',
            '#[+carpet] #[+mpi] Carpet/CarpetSlab',
            '#[+carpet] #[+mpi] Carpet/CarpetTracker',
            '#[+carpet] #[+mpi] Carpet/CycleClock',
            '#[+carpet] #[+mpi] Carpet/HighOrderWaveTest',
            '#[+carpet] #[+mpi] Carpet/LoopControl',
            '#[+carpet] #[+mpi] Carpet/PeriodicCarpet',
            '#[+carpet] #[+mpi] #TODO Carpet/ReductionTest',
            '#[+carpet] #[+mpi] Carpet/ReductionTest2',
            '#[+carpet] #[+mpi] Carpet/ReductionTest3',
            '#[+carpet] #[+mpi] Carpet/RegridSyncTest',
            '#[+carpet] #[+mpi] Carpet/TestCarpetGridInfo',
            '#[+carpet] #[+mpi] Carpet/TestLoopControl',
            '#[+carpet] #[+mpi] Carpet/Timers',
            '',
            '# CTThorns',
            '#[+ctthorns] CTThorns/CT_Analytic',
            '#[+ctthorns] CTThorns/CT_MultiLevel',
            '',
            '# PITTNullCode',
            '#[+pittnullcode] PITTNullCode/NullConstr',
            '#[+pittnullcode] PITTNullCode/NullDecomp',
            '#[+pittnullcode] PITTNullCode/NullEvolve',
            '#[+pittnullcode] PITTNullCode/NullExact',
            '#[+pittnullcode] PITTNullCode/NullGrid',
            '#[+pittnullcode] PITTNullCode/NullInterp',
            '#[+pittnullcode] PITTNullCode/NullNews',
            '#[+pittnullcode] PITTNullCode/NullPsiInt',
            '#[+pittnullcode] PITTNullCode/NullSHRExtract',
            '#[+pittnullcode] PITTNullCode/NullVars',
            '#[+pittnullcode] PITTNullCode/SphericalHarmonicDecomp',
            '#[+pittnullcode] PITTNullCode/SphericalHarmonicRecon',
            '#[+pittnullcode] PITTNullCode/SphericalHarmonicReconGen',
            '',
            '# WVUThorns',
            '#[+wvuthorns] WVUThorns/IllinoisGRMHD',
            '#[+wvuthorns] WVUThorns/Convert_to_HydroBase',
            '#[+wvuthorns] WVUThorns/ID_converter_ILGRMHD',
            '#[+wvuthorns] WVUThorns/Seed_Magnetic_Fields',
            '',
            '# External Libraries',
            '#[+lapack] ExternalLibraries/BLAS',
            '#[+f5] ExternalLibraries/F5',
            '#[+fftw] ExternalLibraries/FFTW3',
            '#[+gsl] ExternalLibraries/GSL',
            '#[+hdf5] ExternalLibraries/HDF5',
            '#[+hwloc] ExternalLibraries/hwloc',
            '#[+lapack] ExternalLibraries/LAPACK',
            '#TODO ExternalLibraries/libjpeg',
            '#[+lorene] #[+fortran] ExternalLibraries/LORENE',
            '#[+mpi] ExternalLibraries/MPI',
            '#DISABLED ExternalLibraries/OpenBLAS',
            '#DISABLED ExternalLibraries/OpenCL',
            '#TODO ExternalLibraries/OpenSSL',
            '#[+papi] ExternalLibraries/PAPI',
            '#DISABLED ExternalLibraries/pciutils',
            '#[+petsc] ExternalLibraries/PETSc',
            '#[+hdf5] ExternalLibraries/zlib',
            '']
        # Enable thorns according to spec
        for v in [
            '+debug', '+fortran', '+openmp', '+optimize',
            '+carpet', '+ctthorns', '+einsteintoolkit', '+f5', '+lorene',
            '+pittnullcode', '+wvuthorns',
            '+fftw', '+gsl', '+hdf5', '+hwloc', '+lapack', '+mpi', '+papi',
            '+petsc']:
            if v in spec:
                # Escape '+' in variant specification
                v = re.sub(r'\+', r'\\+', v)
                thornlist = [re.sub(r'#\[%s\]' % v, '', t) for t in thornlist]
        # Remove leading spaces
        thornlist = [re.sub(r'^ *', '', t) for t in thornlist]
        return thornlist

    def install(self, spec, prefix):
        mkdirp("arrangements/KrancNumericalTools")
        force_symlink(
            "../../repos/Kranc/Auxiliary/Cactus/KrancNumericalTools/GenericFD",
            "arrangements/KrancNumericalTools/GenericFD")

        with open('OptionList', 'w') as f:
            f.write('\n'.join(self.mkOptionList(spec, prefix)))
        with open('ThornList', 'w') as f:
            f.write('\n'.join(self.mkThornList(spec, prefix)))

        make('sim-config', 'PROMPT=no',
            'options=OptionList', 'THORNLIST=ThornList')

        mkdirp(prefix.bin)
        install(join_path('exe', 'cactus_sim'),
            join_path(prefix.bin, 'cactus_sim'))
