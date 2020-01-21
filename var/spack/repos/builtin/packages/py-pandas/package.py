# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    url = "https://pypi.io/packages/source/p/pandas/pandas-0.25.1.tar.gz"

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

    version('0.25.1', sha256='cb2e197b7b0687becb026b84d3c242482f20cbb29a9981e43604eb67576da9f6')
    version('0.25.0', sha256='914341ad2d5b1ea522798efa4016430b66107d05781dbfe7cf05eba8f37df995')
    version('0.24.2', sha256='4f919f409c433577a501e023943e582c57355d50a724c589e78bc1d551a535a2')
    version('0.24.1', sha256='435821cb2501eabbcee7e83614bd710940dc0cf28b5afbc4bdb816c31cec71af')
    version('0.23.4', sha256='5b24ca47acf69222e82530e89111dd9d14f9b970ab2cd3a1c2c78f0c4fbba4f4')
    version('0.21.1', sha256='c5f5cba88bf0659554c41c909e1f78139f6fce8fa9315a29a23692b38ff9788a')
    version('0.20.0', sha256='54f7a2bb2a7832c0446ad51d779806f07ec4ea2bb7c9aea4b83669fa97e778c4')
    version('0.19.2', sha256='6f0f4f598c2b16746803c8bafef7c721c57e4844da752d36240c0acf97658014')
    version('0.19.0', sha256='4697606cdf023c6b7fcb74e48aaf25cf282a1a00e339d2d274cf1b663748805b')
    version('0.18.0', sha256='c975710ce8154b50f39a46aa3ea88d95b680191d1d9d4b5dd91eae7215e01814')
    version('0.16.1', sha256='570d243f8cb068bf780461b9225d2e7bef7c90aa10d43cf908fe541fc92df8b6')
    version('0.16.0', sha256='4013de6f8796ca9d2871218861823bd9878a8dfacd26e08ccf9afdd01bbad9f1')

    # https://pandas.pydata.org/pandas-docs/stable/install.html#dependencies
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
    # https://pandas.pydata.org/pandas-docs/stable/install.html#optional-dependencies

    # Test dependencies
    # https://pandas.pydata.org/pandas-docs/stable/development/contributing.html#running-the-test-suite
    depends_on('py-pytest@4.0.2:', type='test')
    depends_on('py-hypothesis@3.58:', type='test')
    depends_on('py-pyarrow@0.10.0:', type='test')
