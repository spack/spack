# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPillow(PythonPackage):
    """Pillow is a fork of the Python Imaging Library (PIL). It adds image
    processing capabilities to your Python interpreter. This library supports
    many file formats, and provides powerful image processing and graphics
    capabilities."""

    homepage = "https://python-pillow.org/"
    url      = "https://pypi.io/packages/source/P/Pillow/Pillow-7.0.0.tar.gz"

    maintainers = ['adamjstewart']
    import_modules = ['PIL']

    version('7.0.0', sha256='4d9ed9a64095e031435af120d3c910148067087541131e82b3e8db302f4c8946')
    version('6.2.2', sha256='db9ff0c251ed066d367f53b64827cc9e18ccea001b986d08c265e53625dab950')
    version('6.2.1', sha256='bf4e972a88f8841d8fdc6db1a75e0f8d763e66e3754b03006cbc3854d89f1cb1')
    version('6.2.0', sha256='4548236844327a718ce3bb182ab32a16fa2050c61e334e959f554cac052fb0df')
    version('6.0.0', sha256='809c0a2ce9032cbcd7b5313f71af4bdc5c8c771cb86eb7559afd954cab82ebb5')
    version('5.4.1', sha256='5233664eadfa342c639b9b9977190d64ad7aca4edc51a966394d7e08e7f38a9f')
    version('5.1.0', sha256='cee9bc75bff455d317b6947081df0824a8f118de2786dc3d74a3503fd631f4ef')
    version('3.2.0', sha256='64b0a057210c480aea99406c9391180cd866fc0fd8f0b53367e3af21b195784a')
    version('3.0.0', sha256='ad50bef540fe5518a4653c3820452a881b6a042cb0f8bb7657c491c6bd3654bb')

    provides('pil')

    # These defaults correspond to Pillow defaults
    # https://pillow.readthedocs.io/en/stable/installation.html#external-libraries
    variant('tiff',     default=False, description='Compressed TIFF functionality')
    variant('freetype', default=False, description='Type related services')
    variant('lcms',     default=False, description='Color management')
    variant('webp',     default=False, description='WebP format')
    variant('webpmux',  default=False, description='WebP metadata')
    variant('jpeg2000', default=False, description='JPEG 2000 functionality')

    # Spack does not (yet) support these modes of building
    # variant('imagequant', default=False,
    #         description='Improved color quantization')

    # Required dependencies
    depends_on('python@2.6:2.8,3.2:', when='@3:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.3:', when='@4:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@5:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', when='@6:', type=('build', 'run'))
    depends_on('python@3.5:',         when='@7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('zlib')
    depends_on('jpeg')
    depends_on('py-pytest', type='test')
    depends_on('py-pytest-runner', type='test')

    # Optional dependencies
    depends_on('libtiff', when='+tiff')
    depends_on('freetype', when='+freetype')
    depends_on('lcms@2:', when='+lcms')
    depends_on('libwebp', when='+webp')
    depends_on('libwebp+libwebpmux+libwebpdemux', when='+webpmux')
    depends_on('openjpeg', when='+jpeg2000')
    depends_on('imagemagick', type='test')

    # Spack does not (yet) support these modes of building
    # depends_on('libimagequant', when='+imagequant')

    conflicts('+webpmux', when='~webp', msg='Webpmux relies on WebP support')

    phases = ['build_ext', 'install']

    def patch(self):
        """Patch setup.py to provide library and include directories
        for dependencies."""

        library_dirs = []
        include_dirs = []
        for dep in self.spec.dependencies(deptype='link'):
            query = self.spec[dep.name]
            library_dirs.extend(query.libs.directories)
            include_dirs.extend(query.headers.directories)

        setup = FileFilter('setup.py')
        setup.filter('library_dirs = []',
                     'library_dirs = {0}'.format(library_dirs), string=True)
        setup.filter('include_dirs = []',
                     'include_dirs = {0}'.format(include_dirs), string=True)

        def variant_to_cfg(setup):
            able = 'enable' if '+' + variant in self.spec else 'disable'
            return '{0}-{1}=1\n'.format(able, variant)

        with open('setup.cfg', 'a') as setup:
            # Default backend
            setup.write('[build_ext]\n')
            setup.write('enable-zlib=1\n')
            setup.write('enable-jpeg=1\n')
            variants = ['tiff', 'freetype', 'lcms', 'webp',
                        'webpmux', 'jpeg2000']
            for variant in variants:
                setup.write(variant_to_cfg(setup))

            # Spack does not (yet) support these modes of building
            setup.write('disable-imagequant=1\n')

            setup.write('rpath={0}\n'.format(':'.join(self.rpath)))
            setup.write('[install]\n')

    # Tests need to be re-added since `phases` was overridden
    run_after('build_ext')(
        PythonPackage._run_default_build_time_test_callbacks)
    run_after('install')(
        PythonPackage._run_default_install_time_test_callbacks)
    run_after('install')(PythonPackage.sanity_check_prefix)
