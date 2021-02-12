# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAlembic(PythonPackage):
    """Alembic is a database migrations tool."""

    pypi = "alembic/alembic-1.0.7.tar.gz"

    version('1.5.4',  sha256='e871118b6174681f7e9a9ea67cfcae954c6d18e05b49c6b17f662d2530c76bf5')
    version('1.5.3',  sha256='04608b6904a6e6bd1af83e1a48f73f50ba214aeddef44b92d498df33818654a8')
    version('1.5.2',  sha256='a4de8d3525a95a96d59342e14b95cab5956c25b0907dce1549bb4e3e7958f4c2')
    version('1.5.1',  sha256='52d1d48109f17959982779e3c4b5cdeca701e449897bacb75bab173bd6ba984e')
    version('1.5.0',  sha256='b7b3b43adc71447967b5f7bf55d5cc9113bb4e74840b6907d2705b34f2c0f898')
    version('1.4.3',  sha256='5334f32314fb2a56d86b4c4dd1ae34b08c03cae4cb888bc699942104d66bc245')
    version('1.4.2',  sha256='035ab00497217628bf5d0be82d664d8713ab13d37b630084da8e1f98facf4dbf')
    version('1.4.1',  sha256='791a5686953c4b366d3228c5377196db2f534475bb38d26f70eb69668efd9028')
    version('1.4.0',  sha256='2df2519a5b002f881517693b95626905a39c5faf4b5a1f94de4f1441095d1d26')
    version('1.3.3',  sha256='d412982920653db6e5a44bfd13b1d0db5685cbaaccaf226195749c706e1e862a')
    version('1.3.2',  sha256='3b0cb1948833e062f4048992fbc97ecfaaaac24aaa0d83a1202a99fb58af8c6d')
    version('1.3.1',  sha256='49277bb7242192bbb9eac58fed4fe02ec6c3a2a4b4345d2171197459266482b2')
    version('1.3.0',  sha256='e6c6a4243e89c8d3e2342a1562b2388f3b524c9cac2fccc4d2c461a1320cc1c1')
    version('1.2.1',  sha256='9f907d7e8b286a1cfb22db9084f9ce4fde7ad7956bb496dc7c952e10ac90e36a')
    version('1.2.0',  sha256='5609afbb2ab142a991b15ae436347c475f8a517f1610f2fd1b09cdca7c311f3f')
    version('1.1.0',  sha256='4a4811119efbdc5259d1f4c8f6de977b36ad3bcc919f59a29c2960c5ef9149e4')
    version('1.0.11', sha256='cdb7d98bd5cbf65acd38d70b1c05573c432e6473a82f955cdea541b5c153b0cc')
    version('1.0.10', sha256='828dcaa922155a2b7166c4f36ec45268944e4055c86499bd14319b4c8c0094b7')
    version('1.0.9',  sha256='40b9a619aa5f25ea1e1508adcda88b33704ef28e02c9cfa6471e5c772ecf0829')
    version('1.0.8',  sha256='505d41e01dc0c9e6d85c116d0d35dbb0a833dcb490bf483b75abeb06648864e8')
    version('1.0.7', sha256='16505782b229007ae905ef9e0ae6e880fddafa406f086ac7d442c1aaf712f8c2')

    depends_on('py-setuptools', type='build')
    depends_on('py-sqlalchemy@1.1.0:', type=('build', 'run'))
    depends_on('py-mako', type=('build', 'run'))
    depends_on('py-python-dateutil', type=('build', 'run'))
    depends_on('py-python-editor@0.3:', type=('build', 'run'))
