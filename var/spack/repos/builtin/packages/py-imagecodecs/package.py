# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyImagecodecs(PythonPackage):
    """Imagecodecs is a Python library that provides block-oriented,
    in-memory buffer transformation, compression, and decompression
    functions for use in the tifffile, czifile, zarr, and other
    scientific image input/output modules.."""

    homepage = "https://www.lfd.uci.edu/~gohlke/"
    pypi     = "imagecodecs/imagecodecs-2022.2.22.tar.gz"

    version('2022.2.22', sha256='062bef6b003290a8163abed2744b406854238208dfdd41cf7165253c6e01c0bd')

    depends_on('python@3.8:', type=('build', 'run'))
    depends_on('py-numpy@1.19.2:', type=('build', 'run'))
    depends_on('py-setuptools@18.0:', type='build')
    depends_on('py-cython@0.29.27:', type='build')
    depends_on('py-bitshuffle@0.3.5:', type=('build', 'run'))

    depends_on('brotli@1.0.9:')
    # depends_on('brunsli@0.1:')
    # https://github.com/google/brunsli/tree/v0.1
    depends_on('bzip2@1.0.8:')
    depends_on('c-blosc@1.21.1:')
    depends_on('c-blosc2@2.0.4:')
    depends_on('cfitsio@3.49:')
    # depends_on('charls@2.3.4:')
    # https://github.com/team-charls/charls/tree/2.3.4
    depends_on('giflib@5.2.1:')
    # depends_on('jxrlib@1.1:')
    # https://packages.debian.org/source/sid/jxrlib
    depends_on('lcms@2.13.1:')
    depends_on('lerc@3.0:')
    depends_on('libaec@1.0.6:')
    # depends_on('libavif@0.9.3:')
    # https://github.com/AOMediaCodec/libavif
    depends_on('libdeflate@1.10:')
#    depends_on('libjpeg@9d:')
#    depends_on('libjpeg-turbo@2.1.2:') #  FIXME: Problem, normal solution didn't work
    depends_on('jpeg')
    # depends_on('libjxl@0.61:')
    # https://github.com/libjxl/libjxl
    depends_on('liblzf@3.6:')
    # depends_on('liblzma@5.2.5:')
    # https://github.com/xz-mirror/xz
    # py version on spack
    depends_on('libpng@1.6.37:')
    # depends_on('libpng-apng@1.6.37:')
    # https://sourceforge.net/projects/libpng-apng/
    # depends_on('libspng@0.7.2:')
    # https://github.com/randy408/libspng 
    depends_on('libtiff@4.3.0:')
    depends_on('libwebp@1.2.2:')
    depends_on('lz4@1.9.3:')
    # depends_on('mozjpeg@4.0.3:')
    # https://github.com/mozilla/mozjpeg
    depends_on('openjpeg@2.4.0:')
    depends_on('snappy@1.1.9:')
    depends_on('zfp@0.5.5:')
    depends_on('zlib@1.2.11:')
    depends_on('zlib-ng@2.0.6:')
    # depends_on('zopfli@1.0.3:')
    # https://github.com/google/zopfli
    depends_on('zstd@1.5.2:')

