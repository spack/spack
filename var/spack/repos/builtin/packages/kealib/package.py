from spack import *

class Kealib(Package):
    """An HDF5 Based Raster File Format
    
    KEALib provides an implementation of the GDAL data model.
    The format supports raster attribute tables, image pyramids,
    meta-data and in-built statistics while also handling very
    large files and compression throughout.
    
    Based on the HDF5 standard, it also provides a base from which
    other formats can be derived and is a good choice for long
    term data archiving. An independent software library (libkea)
    provides complete access to the KEA image format and a GDAL
    driver allowing KEA images to be used from any GDAL supported software.
    
    Development work on this project has been funded by Landcare Research.
    """
    homepage = "http://kealib.org/"
    url      = "https://bitbucket.org/chchrsc/kealib/get/kealib-1.4.5.tar.gz"

    version('1.4.5', '112e9c42d980b2d2987a3c15d0833a5d')

    depends_on("hdf5")

    def install(self, spec, prefix):
        with working_dir('trunk', create=False):
            cmake_args = []
            cmake_args.append("-DCMAKE_INSTALL_PREFIX=%s" % prefix)
            cmake_args.append("-DHDF5_INCLUDE_DIR=%s" % spec['hdf5'].prefix.include)
            cmake_args.append("-DHDF5_LIB_PATH=%s" % spec['hdf5'].prefix.lib)
            cmake('.', *cmake_args)

            make()
            make("install")
