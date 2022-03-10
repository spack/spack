# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyPandas(PythonPackage):
    """pandas is a fast, powerful, flexible and easy to use open source
    data analysis and manipulation tool, built on top of the Python
    programming language."""

    homepage = "https://pandas.pydata.org/"
    pypi = "pandas/pandas-1.2.0.tar.gz"

    maintainers = ['adamjstewart']

    version('1.4.1',  sha256='8db93ec98ac7cb5f8ac1420c10f5e3c43533153f253fe7fb6d891cf5aa2b80d2')
    version('1.4.0',  sha256='cdd76254c7f0a1583bd4e4781fb450d0ebf392e10d3f12e92c95575942e37df5')
    version('1.3.5',  sha256='1e4285f5de1012de20ca46b188ccf33521bff61ba5c5ebd78b4fb28e5416a9f1')
    version('1.3.4',  sha256='a2aa18d3f0b7d538e21932f637fbfe8518d085238b429e4790a35e1e44a96ffc')
    version('1.3.3',  sha256='272c8cb14aa9793eada6b1ebe81994616e647b5892a370c7135efb2924b701df')
    version('1.3.2',  sha256='cbcb84d63867af3411fa063af3de64902665bb5b3d40b25b2059e40603594e87')
    version('1.3.1',  sha256='341935a594db24f3ff07d1b34d1d231786aa9adfa84b76eab10bf42907c8aed3')
    version('1.3.0',  sha256='c554e6c9cf2d5ea1aba5979cc837b3649539ced0e18ece186f055450c86622e2')
    version('1.2.5',  sha256='14abb8ea73fce8aebbb1fb44bec809163f1c55241bcc1db91c2c780e97265033')
    version('1.2.4',  sha256='649ecab692fade3cbfcf967ff936496b0cfba0af00a55dfaacd82bdda5cb2279')
    version('1.2.3',  sha256='df6f10b85aef7a5bb25259ad651ad1cc1d6bb09000595cab47e718cbac250b1d')
    version('1.2.2',  sha256='14ed84b463e9b84c8ff9308a79b04bf591ae3122a376ee0f62c68a1bd917a773')
    version('1.2.1',  sha256='5527c5475d955c0bc9689c56865aaa2a7b13c504d6c44f0aadbf57b565af5ebd')
    version('1.2.0',  sha256='e03386615b970b8b41da6a68afe717626741bb2431cec993640685614c0680e4')
    version('1.1.5',  sha256='f10fc41ee3c75a474d3bdf68d396f10782d013d7f67db99c0efbfd0acb99701b')
    version('1.1.4',  sha256='a979d0404b135c63954dea79e6246c45dd45371a88631cdbb4877d844e6de3b6')
    version('1.1.3',  sha256='babbeda2f83b0686c9ad38d93b10516e68cdcd5771007eb80a763e98aaf44613')
    version('1.1.2',  sha256='b64ffd87a2cfd31b40acd4b92cb72ea9a52a48165aec4c140e78fd69c45d1444')
    version('1.1.1',  sha256='53328284a7bb046e2e885fd1b8c078bd896d7fc4575b915d4936f54984a2ba67')
    version('1.1.0',  sha256='b39508562ad0bb3f384b0db24da7d68a2608b9ddc85b1d931ccaaa92d5e45273')
    version('1.0.5',  sha256='69c5d920a0b2a9838e677f78f4dde506b95ea8e4d30da25859db6469ded84fa8')
    version('1.0.4',  sha256='b35d625282baa7b51e82e52622c300a1ca9f786711b2af7cbe64f1e6831f4126')
    version('1.0.3',  sha256='32f42e322fb903d0e189a4c10b75ba70d90958cc4f66a1781ed027f1a1d14586')
    version('1.0.2',  sha256='76334ba36aa42f93b6b47b79cbc32187d3a178a4ab1c3a478c8f4198bcd93a73')
    version('1.0.1',  sha256='3c07765308f091d81b6735d4f2242bb43c332cc3461cae60543df6b10967fe27')
    version('1.0.0',  sha256='3ea6cc86931f57f18b1240572216f09922d91b19ab8a01cf24734394a3db3bec')
    version('0.25.3', sha256='52da74df8a9c9a103af0a72c9d5fdc8e0183a90884278db7f386b5692a2220a4')
    version('0.25.2', sha256='ca91a19d1f0a280874a24dca44aadce42da7f3a7edb7e9ab7c7baad8febee2be')
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

    # Required dependencies
    # https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html#dependencies
    depends_on('python@3.8:', type=('build', 'run'), when='@1.4:')
    depends_on('python@3.7.1:', type=('build', 'run'), when='@1.2:')
    depends_on('python@3.6.1:', type=('build', 'run'), when='@1:')
    depends_on('python@3.5.3:', type=('build', 'run'), when='@0.25:')
    # https://pandas.pydata.org/docs/whatsnew/v1.0.0.html#build-changes
    depends_on('py-cython@0.29.13:2', type='build', when='@1:')
    depends_on('py-cython@0.29.16:2', type='build', when='@1.1:')
    depends_on('py-cython@0.29.21:2', type='build', when='@1.1.3:')
    depends_on('py-cython@0.29.24:2', type='build', when='@1.3.4:')
    depends_on('py-setuptools@24.2.0:', type='build')
    depends_on('py-setuptools@38.6.0:', type='build', when='@1.3:')
    depends_on('py-setuptools@51.0.0:', type='build', when='@1.3.2:')
    depends_on('py-numpy', type=('build', 'run'))
    # 'NUMPY_IMPORT_ARRAY_RETVAL' was removed in numpy@1.19
    depends_on('py-numpy@:1.18', type=('build', 'run'), when='@:0.25')
    depends_on('py-numpy@1.13.3:', type=('build', 'run'), when='@0.25:')
    depends_on('py-numpy@1.15.4:', type=('build', 'run'), when='@1.1:')
    depends_on('py-numpy@1.16.5:', type=('build', 'run'), when='@1.2:')
    depends_on('py-numpy@1.17.3:', type=('build', 'run'), when='@1.3:')
    depends_on('py-numpy@1.18.5:', type=('build', 'run'), when='@1.4:')
    depends_on('py-python-dateutil', type=('build', 'run'))
    depends_on('py-python-dateutil@2.6.1:', type=('build', 'run'), when='@0.25:')
    depends_on('py-python-dateutil@2.7.3:', type=('build', 'run'), when='@1.1:')
    depends_on('py-python-dateutil@2.8.1:', type=('build', 'run'), when='@1.4:')
    depends_on('py-pytz@2017.2:', type=('build', 'run'))
    depends_on('py-pytz@2017.3:', type=('build', 'run'), when='@1.2:')
    depends_on('py-pytz@2020.1:', type=('build', 'run'), when='@1.4:')

    # Recommended dependencies
    # https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html#recommended-dependencies
    depends_on('py-numexpr', type=('build', 'run'))
    depends_on('py-numexpr@2.6.2:', type=('build', 'run'), when='@0.25:')
    depends_on('py-numexpr@2.6.8:', type=('build', 'run'), when='@1.2:')
    depends_on('py-numexpr@2.7.0:', type=('build', 'run'), when='@1.3:')
    depends_on('py-numexpr@2.7.1:', type=('build', 'run'), when='@1.4:')
    depends_on('py-bottleneck', type=('build', 'run'))
    depends_on('py-bottleneck@1.2.1:', type=('build', 'run'), when='@0.25:')
    depends_on('py-bottleneck@1.3.1:', type=('build', 'run'), when='@1.4:')

    # Optional dependencies
    # https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html#optional-dependencies

    @property
    def import_modules(self):
        modules = super(__class__, self).import_modules

        ignored_imports = [
            "pandas.tests",
            "pandas.plotting._matplotlib",
            "pandas.core._numba.kernels"
        ]

        return [i for i in modules
                if not any(map(i.startswith, ignored_imports))]
