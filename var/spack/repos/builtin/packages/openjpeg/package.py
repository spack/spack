# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openjpeg(CMakePackage):
    """OpenJPEG is an open-source JPEG 2000 codec written in C language.

    It has been developed in order to promote the use of JPEG 2000, a
    still-image compression standard from the Joint Photographic
    Experts Group (JPEG).
    Since April 2015, it is officially recognized by ISO/IEC and
    ITU-T as a JPEG 2000 Reference Software.
    """

    homepage = 'https://github.com/uclouvain/openjpeg'
    url = 'https://github.com/uclouvain/openjpeg/archive/v2.3.1.tar.gz'

    version('2.3.1', sha256='63f5a4713ecafc86de51bfad89cc07bb788e9bba24ebbf0c4ca637621aadb6a9')
    version('2.3.0', '6a1f8aaa1fe55d2088e3a9c942e0f698')
    version('2.2.0', '269bb0b175476f3addcc0d03bd9a97b6')
    version('2.1.2', '40a7bfdcc66280b3c1402a0eb1a27624')
    version('2.1.1', '0cc4b2aee0a9b6e9e21b7abcd201a3ec')
    version('2.1.0', '3e1c451c087f8462955426da38aa3b3d')
    version('2.0.1', '105876ed43ff7dbb2f90b41b5a43cfa5')
    version('2.0.0', 'cdf266530fee8af87454f15feb619609')
    version('1.5.2', '545f98923430369a6b046ef3632ef95c')
    version('1.5.1', 'd774e4b5a0db5f0f171c4fc0aabfa14e')

    # The problem with install name of the library on MacOs was fixed starting
    # version 2.1.1: https://github.com/uclouvain/openjpeg/commit/b9a247b559e62e55f5561624cf4a19aee3c8afdc
    # The solution works for the older versions (at least starting 1.5.1) too.
    patch('macos.patch', when='@:2.1.0 platform=darwin')

    def url_for_version(self, version):
        if version >= Version('2.1.1'):
            return super(Openjpeg, self).url_for_version(version)

        # Before version 2.2.0, release tarballs of the versions like x.y.0
        # did not have the ".0" in their names:
        if version[2] == 0:
            version = version.up_to(2)

        url_fmt = \
            'https://github.com/uclouvain/openjpeg/archive/version.{0}.tar.gz'

        return url_fmt.format(version)
