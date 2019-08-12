# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPandas(PythonPackage):
    """pandas is a Python package providing fast, flexible, and expressive
       data structures designed to make working with relational or
       labeled data both easy and intuitive. It aims to be the
       fundamental high-level building block for doing practical, real
       world data analysis in Python. Additionally, it has the broader
       goal of becoming the most powerful and flexible open source data
       analysis / manipulation tool available in any language.

    """
    homepage = "http://pandas.pydata.org/"
    url = "https://pypi.io/packages/source/p/pandas/pandas-0.25.0.tar.gz"

    maintainers = ['adamjstewart']
    import_modules = [
        'pandas', 'pandas.compat', 'pandas.core', 'pandas.util', 'pandas.io',
        'pandas.tseries', 'pandas._libs', 'pandas.plotting', 'pandas.arrays',
        'pandas.api', 'pandas.errors', 'pandas._config', 'pandas.compat.numpy',
        'pandas.core.reshape', 'pandas.core.tools', 'pandas.core.util',
        'pandas.core.dtypes', 'pandas.core.groupby', 'pandas.core.internals',
        'pandas.core.computation', 'pandas.core.arrays', 'pandas.core.ops',
        'pandas.core.sparse', 'pandas.core.indexes', 'pandas.io.msgpack',
        'pandas.io.formats', 'pandas.io.excel', 'pandas.io.json',
        'pandas.io.sas', 'pandas.io.clipboard', 'pandas._libs.tslibs',
        'pandas.plotting._matplotlib', 'pandas.api.types',
        'pandas.api.extensions'
    ]

    version('0.25.0', sha256='914341ad2d5b1ea522798efa4016430b66107d05781dbfe7cf05eba8f37df995')
    version('0.24.2', sha256='4f919f409c433577a501e023943e582c57355d50a724c589e78bc1d551a535a2')
    version('0.24.1', sha256='435821cb2501eabbcee7e83614bd710940dc0cf28b5afbc4bdb816c31cec71af')
    version('0.23.4', sha256='5b24ca47acf69222e82530e89111dd9d14f9b970ab2cd3a1c2c78f0c4fbba4f4')
    version('0.21.1', '42ae7f81b81a86c3f91f663b66c525f7')
    version('0.20.0', sha256='54f7a2bb2a7832c0446ad51d779806f07ec4ea2bb7c9aea4b83669fa97e778c4')
    version('0.19.2', '26df3ef7cd5686fa284321f4f48b38cd')
    version('0.19.0', 'bc9bb7188e510b5d44fbdd249698a2c3')
    version('0.18.0', 'f143762cd7a59815e348adf4308d2cf6')
    version('0.16.1', 'fac4f25748f9610a3e00e765474bdea8')
    version('0.16.0', 'bfe311f05dc0c351f8955fbd1e296e73')

    # https://dev.pandas.io/install.html#dependencies
    # Required dependencies
    depends_on('python@3.5.3:', type=('build', 'run'), when='@0.25:')
    depends_on('py-setuptools@24.2.0:', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-numpy@1.13.3:', type=('build', 'run'), when='@0.25:')
    depends_on('py-python-dateutil', type=('build', 'run'))
    depends_on('py-python-dateutil@2.6.1:', type=('build', 'run'), when='@0.25:')
    depends_on('py-pytz@2017.2:', type=('build', 'run'))

    # Recommended dependencies
    depends_on('py-numexpr', type=('build', 'run'))
    depends_on('py-numexpr@2.6.2:', type=('build', 'run'), when='@0.25:')
    depends_on('py-bottleneck', type=('build', 'run'))
    depends_on('py-bottleneck@1.2.1:', type=('build', 'run'), when='@0.25:')

    # Optional dependencies
    # https://dev.pandas.io/install.html#optional-dependencies

    # Test dependencies
    # https://dev.pandas.io/install.html#running-the-test-suite
    depends_on('py-pytest@4.0.2:', type='test')
    depends_on('py-hypothesis@3.58:', type='test')
