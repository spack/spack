from spack import *

class Paraview(Package):
    homepage = 'http://www.paraview.org'
    url      = 'http://www.paraview.org/files/v4.4/ParaView-v4.4.0-source.tar.gz'

    version('4.4.0', 'fa1569857dd680ebb4d7ff89c2227378', url='http://www.paraview.org/files/v4.4/ParaView-v4.4.0-source.tar.gz')

    variant('python', default=False, description='Enable Python support')

    variant('tcl', default=False, description='Enable TCL support')

    variant('mpi', default=False, description='Enable MPI support')

    variant('osmesa', default=False, description='Enable OSMesa support')
    variant('qt', default=False, description='Enable Qt support')

    depends_on('python', when='+python')
    depends_on('py-numpy', when='+python')
    depends_on('py-matplotlib', when='+python')
    depends_on('tcl', when='+tcl')
    depends_on('mpi', when='+mpi')
    depends_on('qt@:4', when='+qt')

    depends_on('bzip2')
    depends_on('freetype')
    depends_on('hdf5') # drags in mpi
    depends_on('jpeg')
    depends_on('libpng')
    depends_on('libtiff')
    depends_on('libxml2')
    depends_on('netcdf')
    #depends_on('protobuf') # version mismatches?
    #depends_on('sqlite') # external version not supported
    depends_on('zlib')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            def feature_to_bool(feature, on='ON', off='OFF'):
                if feature in spec:
                    return on
                return off

            def nfeature_to_bool(feature):
                return feature_to_bool(feature, on='OFF', off='ON')

            feature_args = std_cmake_args[:]
            feature_args.append('-DPARAVIEW_BUILD_QT_GUI:BOOL=%s' % feature_to_bool('+qt'))
            feature_args.append('-DPARAVIEW_ENABLE_PYTHON:BOOL=%s' % feature_to_bool('+python'))
            if '+python' in spec:
                feature_args.append('-DPYTHON_EXECUTABLE:FILEPATH=%s/bin/python' % spec['python'].prefix)
            feature_args.append('-DPARAVIEW_USE_MPI:BOOL=%s' % feature_to_bool('+mpi'))
            if '+mpi' in spec:
                feature_args.append('-DMPIEXEC:FILEPATH=%s/bin/mpiexec' % spec['mpi'].prefix)
            feature_args.append('-DVTK_ENABLE_TCL_WRAPPING:BOOL=%s' % feature_to_bool('+tcl'))
            feature_args.append('-DVTK_OPENGL_HAS_OSMESA:BOOL=%s' % feature_to_bool('+osmesa'))
            feature_args.append('-DVTK_USE_X:BOOL=%s' % nfeature_to_bool('+osmesa'))
            feature_args.append('-DVTK_RENDERING_BACKEND:STRING=%s' % feature_to_bool('+opengl2', 'OpenGL2', 'OpenGL'))

            feature_args.extend(std_cmake_args)

            cmake('..',
                '-DCMAKE_INSTALL_PREFIX:PATH=%s' % prefix,
                '-DBUILD_TESTING:BOOL=OFF',
                '-DVTK_USER_SYSTEM_FREETYPE:BOOL=ON',
                '-DVTK_USER_SYSTEM_HDF5:BOOL=ON',
                '-DVTK_USER_SYSTEM_JPEG:BOOL=ON',
                '-DVTK_USER_SYSTEM_LIBXML2:BOOL=ON',
                '-DVTK_USER_SYSTEM_NETCDF:BOOL=ON',
                '-DVTK_USER_SYSTEM_TIFF:BOOL=ON',
                '-DVTK_USER_SYSTEM_ZLIB:BOOL=ON',
                *feature_args)
            make()
            make('install')
