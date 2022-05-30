# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys

from llnl.util.lang import dedupe

from spack.package import *
from spack.util.environment import filter_system_paths


class Gdal(CMakePackage):
    """GDAL: Geospatial Data Abstraction Library.

    GDAL is a translator library for raster and vector geospatial data formats that
    is released under an MIT style Open Source License by the Open Source Geospatial
    Foundation. As a library, it presents a single raster abstract data model and
    single vector abstract data model to the calling application for all supported
    formats. It also comes with a variety of useful command line utilities for data
    translation and processing.
    """

    homepage   = "https://www.gdal.org/"
    url        = "https://download.osgeo.org/gdal/3.2.0/gdal-3.2.0.tar.xz"
    list_url   = "https://download.osgeo.org/gdal/"
    list_depth = 1

    maintainers = ['adamjstewart']

    version('3.5.0', sha256='d49121e5348a51659807be4fb866aa840f8dbec4d1acba6d17fdefa72125bfc9')
    version('3.4.3', sha256='02a27b35899e1c4c3bcb6007da900128ddd7e8ab7cd6ccfecf338a301eadad5a')
    version('3.4.2', sha256='16baf03dfccf9e3f72bb2e15cd2d5b3f4be0437cdff8a785bceab0c7be557335')
    version('3.4.1', sha256='332f053516ca45101ef0f7fa96309b64242688a8024780a5d93be0230e42173d')
    version('3.4.0', sha256='ac7bd2bb9436f3fc38bc7309704672980f82d64b4d57627d27849259b8f71d5c')
    version('3.3.3', sha256='1e8fc8b19c77238c7f4c27857d04857b65d8b7e8050d3aac256d70fa48a21e76')
    version('3.3.2', sha256='630e34141cf398c3078d7d8f08bb44e804c65bbf09807b3610dcbfbc37115cc3')
    version('3.3.1', sha256='48ab00b77d49f08cf66c60ccce55abb6455c3079f545e60c90ee7ce857bccb70')
    version('3.3.0', sha256='190c8f4b56afc767f43836b2a5cd53cc52ee7fdc25eb78c6079c5a244e28efa7')
    version('3.2.3', sha256='d9ec8458fe97fd02bf36379e7f63eaafce1005eeb60e329ed25bb2d2a17a796f')
    version('3.2.2', sha256='a7e1e414e5c405af48982bf4724a3da64a05770254f2ce8affb5f58a7604ca57')
    version('3.2.1', sha256='6c588b58fcb63ff3f288eb9f02d76791c0955ba9210d98c3abd879c770ae28ea')
    version('3.2.0', sha256='b051f852600ffdf07e337a7f15673da23f9201a9dbb482bd513756a3e5a196a6')
    version('3.1.4', sha256='7b82486f71c71cec61f9b237116212ce18ef6b90f068cbbf9f7de4fc50b576a8')
    version('3.1.3', sha256='161cf55371a143826f1d76ce566db1f0a666496eeb4371aed78b1642f219d51d')
    version('3.1.2', sha256='767c8d0dfa20ba3283de05d23a1d1c03a7e805d0ce2936beaff0bb7d11450641')
    version('3.1.1', sha256='97154a606339a6c1d87c80fb354d7456fe49828b2ef9a3bc9ed91771a03d2a04')
    version('3.1.0', sha256='e754a22242ccbec731aacdb2333b567d4c95b9b02d3ba1ea12f70508d244fcda')
    version('3.0.4', sha256='5569a4daa1abcbba47a9d535172fc335194d9214fdb96cd0f139bb57329ae277')
    version('3.0.3', sha256='e20add5802265159366f197a8bb354899e1693eab8dbba2208de14a457566109')
    version('3.0.2', sha256='c3765371ce391715c8f28bd6defbc70b57aa43341f6e94605f04fe3c92468983')
    version('3.0.1', sha256='45b4ae25dbd87282d589eca76481c426f72132d7a599556470d5c38263b09266')
    version('3.0.0', sha256='ad316fa052d94d9606e90b20a514b92b2dd64e3142dfdbd8f10981a5fcd5c43e')

    variant(
        'raster',
        default='cog,derived,gtiff,hfa,mem,vrt',
        values=(
            'aaigrid',  # Arc/Info ASCII Grid
            'ace2',  # ACE2
            'adrg',  # ADRG/ARC Digitized Raster Graphics (.gen/.thf)
            'aig',  # Arc/Info Binary Grid
            'airsar',  # AIRSAR Polarimetric Format
            'arg',  # Azavea Raster Grid
            'bag',  # Bathymetry Attributed Grid
            'blx',  # Magellan BLX Topo File Format
            'bmp',  # Microsoft Windows Device Independent Bitmap
            'bsb',  # Maptech/NOAA BSB Nautical Chart Format
            'bt',  # VTP .bt Binary Terrain Format
            'byn',  # Natural Resources Canada's Geoid file format (.byn)
            'cad',  # AutoCAD DWG raster layer
            'cals',  # CALS Type 1
            'ceos',  # CEOS Image
            'coasp',  # DRDC COASP SAR Processor Raster
            'cog',  # Cloud Optimized GeoTIFF generator
            'cosar',  # TerraSAR-X Complex SAR Data Product
            'cpg',  # Convair PolGASP data
            'ctable2',  # CTable2 Datum Grid Shift
            'ctg',  # USGS LULC Composite Theme Grid
            'daas',  # DAAS (Airbus DS Intelligence Data As A Service driver)
            'dds',  # DirectDraw Surface
            'derived',  # Derived subdatasets driver
            'dimap',  # Spot DIMAP
            'dipex',  # ELAS DIPEx
            'doq1',  # First Generation USGS DOQ
            'doq2',  # New Labelled USGS DOQ
            'dted',  # Military Elevation Data
            'ecrgtoc',  # ECRG Table Of Contents (TOC.xml)
            'ecw',  # Enhanced Compressed Wavelets (.ecw)
            'eedai',  # Google Earth Engine Data API Image
            'ehdr',  # ESRI .hdr Labelled
            'eir',  # Erdas Imagine Raw
            'elas',  # Earth Resources Laboratory Applications Software
            'envi',  # ENVI .hdr Labelled Raster
            'ers',  # ERMapper .ERS
            'esat',  # Envisat Image Product
            'esric',  # Esri Compact Cache
            'exr',  # Extended Dynamic Range Image File Format
            'fast',  # EOSAT FAST Format
            'fit',  # FIT
            'fits',  # Flexible Image Transport System
            'genbin',  # Generic Binary (.hdr labelled)
            'georaster',  # Oracle Spatial GeoRaster
            'gff',  # Sandia National Laboratories GSAT File Format
            'gif',  # Graphics Interchange Format
            'gpkg',  # GeoPackage raster
            'grassasciigrid',  # GRASS ASCII Grid
            'grib',  # WMO General Regularly-distributed Information in Binary form
            'gs7bg',  # Golden Software Surfer 7 Binary Grid File Format
            'gsag',  # Golden Software ASCII Grid File Format
            'gsbg',  # Golden Software Binary Grid File Format
            'gsc',  # GSC Geogrid
            'gta',  # Generic Tagged Arrays
            'gtiff',  # GeoTIFF File Format
            'gtx',  # NOAA .GTX Vertical Datum Grid Shift Format
            'gxf',  # Grid eXchange File
            'hdf4',  # Hierarchical Data Format Release 4 (HDF4)
            'hdf5',  # Hierarchical Data Format Release 5 (HDF5)
            'heif',  # ISO/IEC 23008-12:2017 High Efficiency Image File Format
            'hf2',  # HF2/HFZ heightfield raster
            'hfa',  # Erdas Imagine .img
            'rst',  # Idrisi Raster Format
            'ilwis',  # Raster Map
            'iris',  # Vaisala’s weather radar software format
            'isce',  # ISCE
            'isg',  # International Service for the Geoid
            'isis2',  # USGS Astrogeology ISIS Cube (Version 2)
            'isis3',  # USGS Astrogeology ISIS Cube (Version 3)
            'jdem',  # Japanese DEM (.mem)
            'jp2ecw',  # ERDAS JPEG2000 (.jp2)
            'jp2kak',  # JPEG-2000 (based on Kakadu)
            'jp2lura',  # JPEG2000 driver based on Lurawave library
            'jp2mrsid',  # JPEG2000 via MrSID SDK
            'jp2openjpeg',  # JPEG2000 driver based on OpenJPEG library
            'jpeg',  # JPEG JFIF File Format
            conditional('jpegxl', when='@3.6:'),  # JPEG-XL File Format
            'jpipkak',  # JPIP Streaming
            'kea',  # KEA
            'kmlsuperoverlay',  # KMLSuperoverlay
            'kro',  # KOLOR Raw format
            'l1b',  # NOAA Polar Orbiter Level 1b Data Set (AVHRR)
            'lan',  # Erdas 7.x .LAN and .GIS
            'lcp',  # FARSITE v.4 LCP Format
            'leveller',  # Daylon Leveller Heightfield
            'loslas',  # NADCON .los/.las Datum Grid Shift
            'map',  # OziExplorer .MAP
            'mrf',  # Meta Raster Format
            'mbtiles',  # MBTiles
            'mem',  # In Memory Raster
            'mff',  # Vexcel MFF Raster
            'mff2',  # Vexcel MFF2 Image
            'mrsid',  # Multi-resolution Seamless Image Database
            'msg',  # Meteosat Second Generation
            'msgn',  # Meteosat Second Generation (MSG) Native Archive Format (.nat)
            'ndf',  # NLAPS Data Format
            'netcdf',  # NetCDF: Network Common Data Form
            'ngsgeoid',  # NOAA NGS Geoid Height Grids
            'ngw',  # NextGIS Web
            'nitf',  # National Imagery Transmission Format
            'ntv2',  # NTv2 Datum Grid Shift
            'nwt_grd',  # Northwood/Vertical Mapper File Format
            'nwt_grc',  # Northwood/Vertical Mapper File Format
            'ogcapi',  # OGC API Tiles / Maps / Coverage
            'ozi',  # OZF2/OZFX3 raster
            'jaxapalsar',  # JAXA PALSAR Processed Products
            'paux',  # PCI .aux Labelled Raw Format
            'pcidsk',  # PCI Geomatics Database File
            'pcraster',  # PCRaster raster file format
            'pdf',  # Geospatial PDF
            'pds',  # Planetary Data System v3
            'pds4',  # NASA Planetary Data System (Version 4)
            'plmosaic',  # PLMosaic (Planet Labs Mosaics API)
            'plscenes',  # PLScenes (Planet Labs Scenes/Catalog API)
            'png',  # Portable Network Graphics
            'pnm',  # Netpbm (.pgm, .ppm)
            'postgisraster',  # PostGIS Raster drive
            'prf',  # PHOTOMOD Raster File
            'r',  # R Object Data Store
            'rasdaman',  # Rasdaman GDAL driver
            'rasterlite',  # Rasters in SQLite DB
            'sqlite',  # Rasters in SQLite DB
            'rdb',  # RIEGL Database
            'rik',  # Swedish Grid Maps
            'rmf',  # Raster Matrix Format
            'roi_pac',  # ROI_PAC
            'rpftoc',  # Raster Product Format/RPF (a.toc)
            'rraster',  # R Raster
            'rs2',  # RadarSat 2 XML Product
            'safe',  # Sentinel-1 SAFE XML Product
            'sar_ceos',  # CEOS SAR Image
            'saga',  # SAGA GIS Binary Grid File Format
            'sdts',  # USGS SDTS DEM
            'sentinel2',  # Sentinel-2 Products
            'sgi',  # SGI Image Format
            'sigdem',  # Scaled Integer Gridded DEM
            'snodas',  # Snow Data Assimilation System
            'srp',  # Standard Product Format (ASRP/USRP) (.gen)
            'srtmhgt',  # SRTM HGT Format
            'stacit',  # Spatio-Temporal Asset Catalog Items
            'stacta',  # Spatio-Temporal Asset Catalog Tiled Assets
            'terragen',  # Terragen Terrain File
            'tga',  # TARGA Image File Format
            'til',  # EarthWatch/DigitalGlobe .TIL
            'tiledb',  # TileDB
            'tsx',  # TerraSAR-X Product
            'usgsdem',  # USGS ASCII DEM (and CDED)
            'vicar',  # VICAR
            'vrt',  # GDAL Virtual Format
            'wcs',  # OGC Web Coverage Service
            'webp',  # WEBP
            'wms',  # Web Map Services
            'wmts',  # OGC Web Map Tile Service
            'xpm',  # X11 Pixmap
            'xyz',  # ASCII Gridded XYZ
            'zarr',  # Zarr
            'zmap',  # ZMap Plus Grid
        ),
        multi=True,
        description='GDAL raster drivers: https://gdal.org/drivers/raster/index.html',
    )

    raster_driver_to_flag = {
        # Drivers grouped together under a single flag
        'ace2': 'raw',
        'bt': 'raw',
        'byn': 'raw',
        'cpg': 'raw',
        'ctable2': 'raw',
        'dipex': 'raw',
        'doq1': 'raw',
        'doq2': 'raw',
        'ehdr': 'raw',
        'eir': 'raw',
        'envi': 'raw',
        'fast': 'raw',
        'genbin': 'raw',
        'gsc': 'raw',
        'gtx': 'raw',
        'mff2': 'raw',
        'isce': 'raw',
        'kro': 'raw',
        'mff': 'raw',
        'lan': 'raw',
        'lcp': 'raw',
        'loslas': 'raw',
        'ndf': 'raw',
        'ntv2': 'raw',
        'paux': 'raw',
        'pnm': 'raw',
        'roi_pac': 'raw',
        'rraster': 'raw',
        'snodas': 'raw',
        'pds4': 'pds',
        'isis2': 'pds',
        'isis3': 'pds',
        'vicar': 'pds',
        'grassasciigrid': 'aaigrid',
        'isg': 'aaigrid',
        'jp2ecw': 'ecw',
        'eedai': 'eeda',
        'gsag': 'gsg',
        'gsbg': 'gsg',
        'gs7bg': 'gsg',
        'bag': 'hdf5',
        'jp2mrsid': 'mrsid',
        'rpftoc': 'nitf',
        'ecrgtoc': 'nitf',
        'nwt_grd': 'northwood',
        'nwt_grc': 'northwood',
        'srp': 'adrg',
        # Drivers whose flags differ from their short names
        'aig': 'aigrid',
        'esat': 'envisat',
        'georaster': 'geor',
        'rst': 'idrisi',
        # Drivers with both raster and vector components but only a single flag
        'cad': None,
        'gpkg': None,
        'ngw': None,
        'plscenes': None,
        'sqlite': None,
        # Non-optional drivers without a flag
        'cog': None,
        'derived': None,
    }

    depends_on('hdf5', when='raster=bag')
    depends_on('hdf5@:1.12', when='@:3.4.1 raster=bag')
    # depends_on('libopencad', when='raster=cad')
    depends_on('curl', when='raster=daas')
    # depends_on('crunch', when='raster=dds')
    # depends_on('ecw@3.3,5.5', when='raster=ecw')
    depends_on('curl', when='raster=eedai')
    depends_on('cryptopp', when='raster=eedai')
    depends_on('openssl', when='raster=eedai')
    depends_on('openexr@2.2:', when='raster=exr')
    depends_on('cfitsio', when='raster=fits')
    depends_on('oracle-instant-client', when='raster=georaster')
    depends_on('giflib', when='raster=gif')
    depends_on('sqlite@3:', when='raster=gpkg')
    depends_on('libpng', when='raster=gpkg')
    depends_on('jpeg', when='raster=gpkg')
    depends_on('libwebp', when='raster=gpkg')
    # depends_on('libgta', when='raster=gta')
    depends_on('hdf', when='raster=hdf4')
    depends_on('hdf5', when='raster=hdf5')
    depends_on('hdf5@:1.12', when='@:3.4.1 raster=hdf5')
    # depends_on('libheif@1.1:+libde265', when='raster=heif')
    # depends_on('ecw@3.3,5.5', when='raster=ecw')
    # depends_on('kadaku', when='raster=jp2kak')
    # depends_on('lurawave', when='raster=jp2lura')
    # depends_on('mrsid', when='raster=jp2mrsid')
    depends_on('openjpeg@2.1:', when='raster=jp2openjpeg')
    depends_on('jpeg', when='raster=jpeg')
    # depends_on('libjxl', when='raster=jpegxl')
    # depends_on('kadaku', when='raster=jpipkak')
    depends_on('kealib', when='raster=kea')
    depends_on('hdf5+cxx', when='raster=kea')
    depends_on('hdf5@:1.12', when='@:3.4.1 raster=kea')
    # depends_on('brunsli', when='raster=mrf')
    depends_on('jpeg', when='raster=mrf')
    depends_on('sqlite@3:', when='raster=mbtiles')
    # depends_on('mrsid', when='raster=mrsid')
    # depends_on('msg', when='raster=msg')
    depends_on('netcdf-c', when='raster=netcdf')
    depends_on('curl', when='raster=ngw')
    depends_on('curl', when='raster=ogcapi')
    # depends_on('libcf', when='raster=pcraster')
    depends_on('libxml2', when='raster=pdf')
    depends_on('poppler@0.24:', when='raster=pdf')
    depends_on('poppler@:21', when='@:3.4.1 raster=pdf')
    depends_on('curl', when='raster=plmosaic')
    depends_on('curl', when='raster=plscenes')
    depends_on('postgresql', when='raster=postgisraster')
    # depends_on('raslib', when='raster=rasdaman')
    depends_on('sqlite@3:', when='raster=rasterlite')
    depends_on('sqlite@3:', when='raster=sqlite')
    # depends_on('librasterlite2@1.1:', when='raster=sqlite')
    depends_on('libspatialite', when='raster=sqlite')
    depends_on('pcre2', when='raster=sqlite')
    # depends_on('rdblib@2.2:', when='raster=rdb')
    depends_on('zlib', when='raster=rik')
    # depends_on('tiledb', when='raster=tiledb')
    depends_on('curl', when='raster=wcs')
    depends_on('libwebp', when='raster=webp')
    depends_on('curl@7.28:', when='raster=wms')
    depends_on('curl', when='raster=wmts')
    depends_on('lz4', when='raster=zarr')
    depends_on('xz', when='raster=zarr')
    depends_on('zstd', when='raster=zarr')
    depends_on('c-blosc', when='raster=zarr')

    variant(
        'vector',
        default='esrijson,esri_shapefile,geojson,geojsonseq,kml,mapinfo_file,memory,topojson,vrt',  # noqa: E501
        values=(
            'amigocloud',  # AmigoCloud
            'arrow',  # (Geo)Arrow IPC File Format / Stream
            'avcbin',  # Arc/Info Binary Coverage
            'avce00',  # Arc/Info E00 (ASCII) Coverage
            'cad',  # AutoCAD DWG
            'carto',  # Carto
            'csv',  # Comma Separated Value (.csv)
            'csw',  # OGC CSW (Catalog Service for the Web)
            'dgn',  # Microstation DGN
            'dgnv8',  # Microstation DGN v8
            'dwg',  # AutoCAD DWG
            'dxf',  # AutoCAD DXF
            'edigeo',  # EDIGEO
            'eeda',  # Google Earth Engine Data API
            'elasticsearch',  # Geographically Encoded Objects for Elasticsearch
            'esrijson',  # ESRIJSON / FeatureService driver
            'esri_shapefile',  # ESRI Shapefile / DBF
            'filegdb',  # ESRI File Geodatabase (FileGDB)
            'flatgeobuf',  # FlatGeobuf
            'geoconcept',  # GeoConcept text export
            'geojson',  # GeoJSON
            'geojsonseq',  # GeoJSONSeq: sequence of GeoJSON features
            'georss',  # GeoRSS: Geographically Encoded Objects for RSS feeds
            'gml',  # Geography Markup Language
            'gmlas',  # Geography Markup Language (GML) driven by application schemas
            'gmt',  # GMT ASCII Vectors (.gmt)
            'gpkg',  # GeoPackage vector
            'gpsbabel',  # GPSBabel
            'gpx',  # GPS Exchange Format
            'hana',  # SAP HANA
            'idb',  # IDB
            'idrisi',  # Idrisi Vector (.VCT)
            'interlis_1',  # INTERLIS 1 driver
            'interlis_2',  # INTERLIS 2 driver
            'jml',  # JML: OpenJUMP JML format
            'kml',  # Keyhole Markup Language
            'libkml',  # LIBKML Driver (.kml .kmz)
            'lvbag',  # Dutch Kadaster LV BAG 2.0 Extract
            'mapinfo_file',  # MapInfo TAB and MIF/MID
            'mapml',  # MapML
            'mbtiles',  # MBTiles
            'memory',  # Memory
            'mongodbv3',  # MongoDBv3
            'mssqlspatial',  # Microsoft SQL Server Spatial Database
            'mvt',  # MVT: Mapbox Vector Tiles
            'mysql',  # MySQL
            'nas',  # ALKIS
            'netcdf',  # Vector
            'ngw',  # NextGIS Web
            'uk_ntf',  # UK .NTF
            'oapif',  # OGC API - Features
            'oci',  # Oracle Spatial
            'odbc',  # ODBC RDBMS
            'ods',  # Open Document Spreadsheet
            'ogcapi',  # OGC API Tiles / Maps / Coverage
            'ogdi',  # OGDI Vectors
            'openfilegdb',  # ESRI File Geodatabase (OpenFileGDB)
            'osm',  # OpenStreetMap XML and PBF
            'parquet',  # (Geo)Parquet
            'pdf',  # Geospatial PDF
            'pds',  # Planetary Data Systems TABLE
            'postgresql',  # PostgreSQL / PostGIS
            'pgdump',  # PostgreSQL SQL Dump
            'pgeo',  # ESRI Personal GeoDatabase
            'plscenes',  # PLScenes (Planet Labs Scenes/Catalog API)
            's57',  # IHO S-57 (ENC)
            'sdts',  # SDTS
            'selafin',  # Selafin files
            'sosi',  # Norwegian SOSI Standard
            'sqlite',  # SQLite / Spatialite RDBMS
            'svg',  # Scalable Vector Graphics
            'sxf',  # SXF
            'tiger',  # U.S. Census TIGER/Line
            'topojson',  # TopoJSON driver
            'vdv',  # VDV-451/VDV-452/INTREST Data Format
            'vfk',  # Czech Cadastral Exchange Data Format
            'vicar',  # VICAR
            'vrt',  # Virtual Format
            'wasp',  # WAsP .map format
            'wfs',  # OGC WFS service
            'xls',  # MS Excel format
            'xlsx',  # MS Office Open XML spreadsheet
        ),
        multi=True,
        description='OGR vector drivers: https://gdal.org/drivers/vector/index.html',
    )

    vector_driver_to_flag = {
        # Drivers grouped together under a single flag
        'interlis_1': 'ili',
        'interlis_2': 'ili',
        'oapif': 'wfs',
        'avcbin': 'avc',
        'avce00': 'avc',
        'dgnv8': 'dwg',
        'vicar': 'pds',
        # Drivers whose flags differ from their short names
        'elasticsearch': 'elastic',
        'postgresql': 'pg',
        'uk_ntf': 'ntf',
        # Drivers with both raster and vector components but only a single flag
        'eeda': None,
        'mbtiles': None,
        'netcdf': None,
        'ogcapi': None,
        'pdf': None,
        # Non-optional drivers without a flag
        'esrijson': 'geojson',
        'esri_shapefile': 'shape',
        'geojsonseq': 'geojson',
        'mapinfo_file': 'tab',
        'memory': 'mem',
        'topojson': 'geojson',
    }

    depends_on('curl', when='vector=amigocloud')
    depends_on('arrow', when='vector=arrow')
    # depends_on('libopencad', when='vector=cad')
    depends_on('curl', when='vector=carto')
    depends_on('curl', when='vector=csw')
    # depends_on('teigha', when='vector=dgnv8')
    # depends_on('teigha', when='vector=dwg')
    depends_on('curl', when='vector=eeda')
    depends_on('curl', when='vector=elasticsearch')
    # depends_on('filegdb', when='vector=filegdb')
    depends_on('expat', when='vector=georss')
    depends_on('expat', when='vector=gml')
    depends_on('libxml2', when='vector=gml')
    depends_on('libxml2', when='vector=gmlas')
    depends_on('xerces-c@3.1:', when='vector=gmlas')
    depends_on('sqlite@3:', when='vector=gpkg')
    depends_on('expat', when='vector=gpsbabel')
    depends_on('expat', when='vector=gpx')
    depends_on('unixodbc', when='vector=hana')
    # depends_on('informix-datablade', when='vector=idb')
    depends_on('xerces-c', when='vector=interlis_1')
    depends_on('xerces-c', when='vector=interlis_2')
    depends_on('expat', when='vector=jml')
    depends_on('expat', when='vector=kml')
    depends_on('libkml@1.3:', when='vector=libkml')
    depends_on('expat', when='vector=lvbag')
    depends_on('sqlite@3:', when='vector=mbtiles')
    depends_on('mongo-cxx-driver@3.4:', when='vector=mongodbv3')
    # depends_on('mssql_odbc', when='vector=mssqlspatial')
    depends_on('unixodbc', when='vector=mssqlspatial')
    depends_on('sqlite@3:', when='vector=mvt')
    depends_on('geos', when='vector=mvt')
    depends_on('mysql', when='vector=mysql')
    depends_on('xerces-c', when='vector=nas')
    depends_on('netcdf-c', when='vector=netcdf')
    depends_on('curl', when='vector=ngw')
    depends_on('curl', when='vector=oapif')
    # depends_on('oci', when='vector=oci')
    depends_on('unixodbc', when='vector=odbc')
    depends_on('expat', when='vector=ods')
    depends_on('curl', when='vector=ogcapi')
    # depends_on('ogdi', when='vector=ogdi')
    depends_on('sqlite@3:', when='vector=osm')
    depends_on('expat', when='vector=osm')
    depends_on('arrow+parquet', when='vector=parquet')
    depends_on('poppler@0.24:', when='vector=pdf')
    depends_on('poppler@:21', when='@:3.4.1 vector=pdf')
    depends_on('postgresql', when='vector=postgresql')
    depends_on('unixodbc', when='vector=pgeo')
    depends_on('curl', when='vector=plscenes')
    depends_on('fyba', when='vector=sosi')
    depends_on('sqlite@3:', when='vector=sqlite')
    depends_on('expat', when='vector=svg')
    depends_on('sqlite@3:', when='vector=vfk')
    depends_on('curl', when='vector=wfs')
    depends_on('expat', when='vector=wfs')
    depends_on('freexl', when='vector=xls')
    depends_on('expat', when='vector=xlsx')

    # Language bindings
    variant('python', default=False, description='Build Python bindings')
    variant('java', default=False, description='Build Java bindings')
    variant('csharp', default=False, description='Build C# bindings')

    # FIXME: Allow packages to extend multiple packages
    # See https://github.com/spack/spack/issues/987
    # FIXME: Allow packages to extend virtual dependencies
    # See https://github.com/spack/spack/issues/17475
    extends('python', when='+python')
    # extends('openjdk', when='+java')

    # see gdal_version_and_min_supported_python_version
    # in swig/python/osgeo/__init__.py
    depends_on('python@3.6:', when='@3.3:+python', type=('build', 'link', 'run'))
    depends_on('python@2.7:', when='+python', type=('build', 'link', 'run'))
    # swig/python/setup.py
    depends_on('py-setuptools', when='+python', type='build')
    depends_on('py-setuptools@:57', when='@:3.2+python', type='build')  # needs 2to3
    depends_on('py-numpy@1.0.1:', when='+python', type=('build', 'run'))
    depends_on('java@7:', when='@3.2:+java', type=('build', 'link', 'run'))
    depends_on('java@6:', when='+java', type=('build', 'link', 'run'))
    depends_on('swig', when='+python', type='build')
    depends_on('swig', when='+java', type='build')
    depends_on('swig', when='+csharp', type='build')

    # Optional dependencies
    variant('armadillo', default=False, description='Speed up computations related to the Thin Plate Spline transformer')
    variant('geos', default=False, description='Use GEOS for geometry processing operations in OGR')
    variant('hdfs', default=False, description='Add support for /vsihdfs/ virtual file system')
    variant('iconv', default=False, description='Use iconv to convert text between encodings')
    variant('lerc', default=False, description='Add LERC compression/decompression support')
    variant('opencl', default=False, description='Use OpenCL to accelerate warping computations on GPU')
    variant('qhull', default=False, description='Use QHULL for linear interpolation of gdal_grid')
    variant('sfcgal', default=False, description='Use SFCGAL for ISO 19107:2013 and OGC Simple Features Access 1.2 for 3D operations')

    depends_on('armadillo', when='+armadillo')
    depends_on('blas', when='+armadillo')
    depends_on('lapack', when='+armadillo')
    depends_on('geos', when='+geos')
    depends_on('hadoop', when='+hdfs')
    depends_on('libiconv', when='+iconv')
    depends_on('lerc', when='+lerc')
    depends_on('opencl', when='+opencl')
    depends_on('qhull', when='+qhull')
    depends_on('sfcgal', when='+sfcgal')

    # Required dependencies
    depends_on('cmake@3.9:', when='@3.5:', type='build')
    depends_on('ninja', when='@3.5:', type='build')
    depends_on('gmake', when='@:3.4', type='build')
    depends_on('proj@6:')
    depends_on('zlib')
    depends_on('libtiff@4:')
    depends_on('libgeotiff@1.5:')
    depends_on('json-c')

    # https://trac.osgeo.org/gdal/wiki/SupportedCompilers
    msg = 'GDAL requires C++11 support'
    conflicts('%gcc@:4.8.0', msg=msg)
    conflicts('%clang@:3.2', msg=msg)
    conflicts('%intel@:12',  msg=msg)
    conflicts('%xl@:13.0',   msg=msg)
    conflicts('%xl_r@:13.0', msg=msg)

    # https://github.com/OSGeo/gdal/issues/3782
    patch('https://github.com/OSGeo/gdal/pull/3786.patch?full_index=1', when='@3.3.0', level=2,
          sha256='9f9824296e75b34b3e78284ec772a5ac8f8ba92c17253ea9ca242caf766767ce')

    generator = 'Ninja'
    executables = ['^gdal-config$']

    @classmethod
    def determine_version(cls, exe):
        return Executable(exe)('--version', output=str, error=str).rstrip()

    @classmethod
    def determine_variants(cls, exes, version_str):
        bin_dir = os.path.dirname(exes[0])
        pattern = re.compile(r'^\s*(.*)\s-(raster|vector)')

        # GDAL raster drivers
        gdalinfo = Executable(os.path.join(bin_dir, 'gdalinfo'))
        rasters = []
        for line in gdalinfo('--formats', output=str, error=str).split('\n'):
            m = pattern.match(line)
            if m:
                driver = m.group(1).lower().replace(' ', '_').replace('.', '')
                if driver in cls.variants['raster'][0].values:
                    rasters.append(driver)
                else:
                    print('Unknown driver:', line)
                    print('Please open an issue at:')
                    print('https://github.com/spack/spack/issues/new')
                    print('and tag', ' '.join(cls.maintainers))

        # OGR vector drivers
        ogrinfo = Executable(os.path.join(bin_dir, 'ogrinfo'))
        vectors = []
        for line in ogrinfo('--formats', output=str, error=str).split('\n'):
            m = pattern.match(line)
            if m:
                driver = m.group(1).lower().replace(' ', '_').replace('.', '')
                if driver in cls.variants['vector'][0].values:
                    vectors.append(driver)
                else:
                    print('Unknown driver:', line)
                    print('Please open an issue at:')
                    print('https://github.com/spack/spack/issues/new')
                    print('and tag', ' '.join(cls.maintainers))

        return 'raster=' + ','.join(rasters) + ' vector=' + ','.join(vectors)

    @property
    def import_modules(self):
        modules = ['osgeo']
        if self.spec.satisfies('@3.3:'):
            modules.append('osgeo_utils')
        else:
            modules.append('osgeo.utils')
        return modules

    @when('@:3.4')
    def setup_build_environment(self, env):
        # Needed to install Python bindings to GDAL installation
        # prefix instead of Python installation prefix.
        # See swig/python/GNUmakefile for more details.
        env.set('PREFIX', self.prefix)
        env.set('DESTDIR', '/')

    def setup_run_environment(self, env):
        if '+java' in self.spec:
            class_paths = find(self.prefix, '*.jar')
            classpath = os.pathsep.join(class_paths)
            env.prepend_path('CLASSPATH', classpath)

        # `spack test run gdal+python` requires these for the Python bindings
        # to find the correct libraries
        libs = []
        for dep in self.spec.dependencies(deptype='link'):
            query = self.spec[dep.name]
            libs.extend(filter_system_paths(query.libs.directories))
        if sys.platform == 'darwin':
            env.prepend_path('DYLD_FALLBACK_LIBRARY_PATH', ':'.join(libs))
        else:
            env.prepend_path('LD_LIBRARY_PATH', ':'.join(libs))

    def patch(self):
        if '+java platform=darwin' in self.spec:
            filter_file('linux', 'darwin', 'swig/java/java.opt', string=True)

    def cmake_args(self):
        # https://gdal.org/build_hints.html
        args = [
            # Only use Spack-installed dependencies
            self.define('GDAL_USE_INTERNAL_LIBS', False),
            # Only build optional drivers when explicitly requested
            self.define('GDAL_BUILD_OPTIONAL_DRIVERS', False),
            self.define('OGR_BUILD_OPTIONAL_DRIVERS', False),
        ]

        # GDAL raster drivers
        for driver in self.variants['raster'][0].values:
            # Only needed because conditional values are Value not str
            # FIXME: self.variants['raster'][0].values includes conditionals that
            # should not exist in that version
            driver = str(driver)
            flag = driver
            if driver in self.raster_driver_to_flag:
                flag = self.raster_driver_to_flag[driver]
            if flag:
                args.append(self.define(
                    'GDAL_ENABLE_DRIVER_' + flag.upper(),
                    'raster=' + driver in self.spec
                ))

        # OGR vector drivers
        for driver in self.variants['vector'][0].values:
            driver = str(driver)
            flag = driver
            if driver in self.vector_driver_to_flag:
                flag = self.vector_driver_to_flag[driver]
            if flag:
                args.append(self.define(
                    'OGR_ENABLE_DRIVER_' + flag.upper(),
                    'vector=' + driver in self.spec
                ))

        # Language bindings
        for lang in ['python', 'java', 'csharp']:
            args.append(self.define_from_variant(
                'BUILD_{}_BINDINGS'.format(lang.upper()), lang))

        # TODO: explicit control over whether or not a dependency is used if found

        # Some drivers are grouped under a single flag
        args = dedupe(args)

        return args

    def configure_args(self):
        # https://trac.osgeo.org/gdal/wiki/BuildHints
        args = [
            '--prefix=' + self.prefix,
            # Only build optional drivers when explicitly requested
            '--disable-all-optional-drivers',
            # https://trac.osgeo.org/gdal/wiki/TIFF
            '--with-libtiff={0}'.format(self.spec['libtiff'].prefix),
            '--with-geotiff={0}'.format(self.spec['libgeotiff'].prefix),
            '--with-libjson-c={0}'.format(self.spec['json-c'].prefix),
        ]

        # GDAL raster drivers
        for driver in self.variants['raster'][0].values:
            driver = str(driver)
            flag = driver
            if driver in self.raster_driver_to_flag:
                flag = self.raster_driver_to_flag[driver]
            if flag:
                if 'raster=' + driver in self.spec:
                    args.append('--enable-driver-' + flag)
                else:
                    args.append('--disable-driver-' + flag)

        # OGR vector drivers
        for driver in self.variants['vector'][0].values:
            driver = str(driver)
            flag = driver
            if driver in self.vector_driver_to_flag:
                flag = self.vector_driver_to_flag[driver]
            if flag:
                if 'vector=' + driver in self.spec:
                    args.append('--enable-driver-' + flag)
                else:
                    args.append('--disable-driver-' + flag)

        # TODO: explicit control over whether or not a dependency is used if found
        # Likely causing the build to fail due to internal deps that won't compile

        # TODO: handle differences in driver/flag names better

        # Some drivers are grouped under a single flag
        args = dedupe(args)

        return args

    @when('@:3.4')
    def cmake(self, spec, prefix):
        configure(*self.configure_args())

    @when('@:3.4')
    def build(self, spec, prefix):
        # https://trac.osgeo.org/gdal/wiki/GdalOgrInJavaBuildInstructionsUnix
        make()
        if '+java' in spec:
            with working_dir('swig/java'):
                make()

    @when('@:3.4')
    def check(self):
        # no top-level test target
        if '+java' in self.spec:
            with working_dir('swig/java'):
                make('test')

    @when('@:3.4')
    def install(self, spec, prefix):
        make('install')
        if '+java' in spec:
            with working_dir('swig/java'):
                make('install')
                install('*.jar', prefix)

    @run_after('install')
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        if self.spec.satisfies('@:3.4 platform=darwin'):
            fix_darwin_install_name(self.prefix.lib)

    def test(self):
        """Attempts to import modules of the installed package."""

        if '+python' in self.spec:
            # Make sure we are importing the installed modules,
            # not the ones in the source directory
            for module in self.import_modules:
                self.run_test(self.spec['python'].command.path,
                              ['-c', 'import {0}'.format(module)],
                              purpose='checking import of {0}'.format(module),
                              work_dir='spack-test')
