# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHdfs(PythonPackage):
    """API and command line interface for HDFS"""
    homepage = "https://hdfscli.readthedocs.io/en/latest/"
    pypi = "hdfs/hdfs-2.1.0.tar.gz"

    version('2.5.8', sha256='1be117549fc1285571bc51aedc15df5a203138dba02f9adfa26761b69a949370')
    version('2.5.7', sha256='2b33124ed1b67add2d43d4bf2aee5cf86323a292bb8fa001ce886be22f1aa630')
    version('2.5.6', sha256='7ac9c9ef7a24f6275b41c003ae9808542ecf1a696a13e1ad337664e8ebb40a48')
    version('2.5.5', sha256='41e1a6f97f938fdc2ae74992c731a44f9781909ef5f8672b243187f9f566536e')
    version('2.5.4', sha256='f159ff72f526b21572b6a2904df26fbf8bb996cd61c536b94a2402a0376e7a4f')
    version('2.5.2', sha256='4faccafa381204914c24d557c10267c2d60e9341172959e3c977f28d7a48698c')
    version('2.5.1', sha256='3933cfe4ddef3077b57391d9d8c05207e107c2bd10ec9ce93f0333381b782a57')
    version('2.5.0', sha256='e798bc76c3cac41b65c6796c0c5063e3336e484073f78a9da8637a837c5c8709')
    version('2.4.0', sha256='1649109d08f003611e7f189b6e03abe7d13f3274cd3a26ded059ec96b141af4d')
    version('2.3.1', sha256='73e800b2f97b41d89a4ccf0f0359c62afde32b0e385c375f80664e2df173f767')
    version('2.3.0', sha256='31deda2473aa490dd8bc55111f6af55857ccc8791a315739d01cf80c0dba53ab')
    version('2.2.2', sha256='df8c99e359d7351c7ef70efaceea8238f8311035701c235a57ba98fbac26c932')
    version('2.2.1', sha256='92fdf7fc7203d5d20cab467fb37d6f347b56dbf82e4440b47a867dd3c20d10f0')
    version('2.2.0', sha256='c8d92284cf350827890ffb16d2b757b208453d17d97b48e8743c469c91406639')
    version('2.1.0', sha256='a40fe99ccb03b5c3247b33a4110eb21b57405dd7c3f1b775e362e66c19b44bc6')

    depends_on('py-setuptools', type='build')
    depends_on('py-docopt', type=('build', 'run'))
    depends_on('py-requests@2.7.0:', type=('build', 'run'))
    depends_on('py-six@1.9.0:', type=('build', 'run'))
