# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySentrySdk(PythonPackage):
    """The new Python SDK for Sentry.io"""

    homepage = "https://github.com/getsentry/sentry-python"
    pypi = "sentry-sdk/sentry-sdk-0.17.6.tar.gz"

    version('0.20.1', sha256='3693cb47ba8d90c004ac002425770b32aaf0c83a846ec48e2d1364e7db1d072d')
    version('0.20.0', sha256='31871a1c18547cafa7b75064c6391aa517b15468fda7b644ccb149decccb9d44')
    version('0.19.5', sha256='737a094e49a529dd0fdcaafa9e97cf7c3d5eb964bd229821d640bc77f3502b3f')
    version('0.19.4', sha256='1052f0ed084e532f66cb3e4ba617960d820152aee8b93fc6c05bd53861768c1c')
    version('0.19.3', sha256='fd48f627945511c140546939b4d73815be4860cd1d2b9149577d7f6563e7bd60')
    version('0.19.2', sha256='17b725df2258354ccb39618ae4ead29651aa92c01a92acf72f98efe06ee2e45a')
    version('0.19.1', sha256='5cf36eb6b1dc62d55f3c64289792cbaebc8ffa5a9da14474f49b46d20caa7fc8')
    version('0.19.0', sha256='a3716e98a1285a74eeaea7418a5b8fb2d7568fa11b5fba389946f465876a4d44')
    version('0.18.0', sha256='1d91a0059d2d8bb980bec169578035c2f2d4b93cd8a4fb5b85c81904d33e221a')
    version('0.17.8', sha256='e159f7c919d19ae86e5a4ff370fccc45149fab461fbeb93fb5a735a0b33a9cb1')
    version('0.17.7', sha256='a698993f3abbe06e88e8a3c8b61c8a79c12f62e503f1a23eda30c3921f0525a9')
    version('0.17.6', sha256='1a086486ff9da15791f294f6e9915eb3747d161ef64dee2d038a4d0b4a369b24')

    depends_on('python@2.7,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-urllib3@1.10.0:', type=('build', 'run'))
    depends_on('py-certifi', type=('build', 'run'))
    depends_on('py-flask@0.11:', type=('build', 'run'))
    depends_on('py-bottle@0.12.13:', type=('build', 'run'))
    depends_on('py-falcon@1.4:', type=('build', 'run'))
    depends_on('py-django@1.8:', type=('build', 'run'))
    depends_on('py-sanic@0.8:', type=('build', 'run'))
    depends_on('py-celery@3:', type=('build', 'run'))
    depends_on('py-apache-beam@2.12:', type=('build', 'run'))
    depends_on('py-rq@0.6:', type=('build', 'run'))
    depends_on('py-aiohttp@3.5:', type=('build', 'run'))
    depends_on('py-tornado@5:', type=('build', 'run'))
    depends_on('py-sqlalchemy@1.2:', type=('build', 'run'))
    depends_on('py-pyspark@2.4.4:', type=('build', 'run'))
    depends_on('py-pure-eval', type=('build', 'run'))
    depends_on('py-chalice@1.16.0:', type=('build', 'run'))
