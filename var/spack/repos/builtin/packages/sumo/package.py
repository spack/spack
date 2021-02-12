# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sumo(CMakePackage):
    """Eclipse SUMO is an open source, highly portable, microscopic and
    continuous road traffic simulation package designed to handle large road
    networks. It allows for intermodal simulation including pedestrians and
    comes with a large set of tools for scenario creation."""

    homepage = "http://projects.eclipse.org/projects/technology.sumo"
    url      = "https://github.com/eclipse/sumo/archive/v1_5_0.tar.gz"

    version('1_8_0', sha256='c70a802509c354c222e40926c71314e05c04652b1759f50e581d8d95d2f1d836')
    version('1_7_0', sha256='db0868318f2a602475a15ba8b83d30b686e6283b3ff753b9d112217529f2893b')
    version('1_6_0', sha256='95d48b40a796e51db5dff91c316426262e6d6577347cc7a4e9a03c1b302a84ef')
    version('1.5.0', sha256='be6ba0361b487a5e71c81e60b4c07a67826d5e170500c10c37374c1086ac2cb6')

    variant('gdal',
            default=True,
            description='gdal support, for arcgis')
    variant('ffmpeg',
            default=False,
            description='ffmpeg support, for video output')
    variant('openscenegraph',
            default=False,
            description='openscenegraph support, for experimental 3D GUI')
    variant('gl2ps',
            default=False,
            description='gl2ps support')
    variant('eigen',
            default=False,
            description='eigen support')

    extends('python')
    depends_on('py-setuptools', type='build')
    depends_on('googletest', type='test')
    depends_on('xerces-c')
    depends_on('proj')
    depends_on('fox@1.6.57+opengl')
    depends_on('swig', type='build')
    depends_on('java', type=('build', 'run'))
    depends_on('gdal', when='+gdal')
    depends_on('ffmpeg', when='+ffmpeg')
    depends_on('openscenegraph', when='+openscenegraph')
    depends_on('gl2ps', when='+gl2ps')
    depends_on('eigen', when='+eigen')

    def url_for_version(self, version):
        url = "https://github.com/eclipse/sumo/archive/v{0}.tar.gz"
        return url.format(version.underscored)

    def setup_run_environment(self, env):
        env.set('SUMO_HOME', self.prefix)
