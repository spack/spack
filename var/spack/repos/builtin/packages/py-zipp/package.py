# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyZipp(PythonPackage):
    """Backport of pathlib-compatible object wrapper for zip files."""

    homepage = "https://github.com/jaraco/zipp"
    pypi = "zipp/zipp-0.6.0.tar.gz"

    version('3.4.0', sha256='ed5eee1974372595f9e416cc7bbeeb12335201d8081ca8a0743c954d4446e5cb')
    version('3.3.2', sha256='adf8f2ed8f614ced567d849cae9d183cef6cfd27c77a5cae7a28029be0c2b7a7')
    version('3.3.1', sha256='c1532a8030c32fd52ff6a288d855fe7adef5823ba1d26a29a68fd6314aa72baa')
    version('3.3.0', sha256='64ad89efee774d1897a58607895d80789c59778ea02185dd846ac38394a8642b')
    version('3.2.0', sha256='b52f22895f4cfce194bc8172f3819ee8de7540aa6d873535a8668b730b8b411f')
    version('3.1.0', sha256='c599e4d75c98f6798c509911d08a22e6c021d074469042177c8c86fb92eefd96')
    version('3.0.0', sha256='7c0f8e91abc0dc07a5068f315c52cb30c66bfbc581e5b50704c8a2f6ebae794a')
    version('2.2.1', sha256='fddb41c555ab338cdf27bc1d92cc6e3c05db8d1f1e7ba89d9646976702367333')
    version('2.2.0', sha256='5c56e330306215cd3553342cfafc73dda2c60792384117893f3a83f8a1209f50')
    version('2.1.0', sha256='feae2f18633c32fc71f2de629bfb3bd3c9325cd4419642b1f1da42ee488d9b98')
    version('2.0.1', sha256='b338014b9bc7102ca69e0fb96ed07215a8954d2989bc5d83658494ab2ba634af')
    version('2.0.0', sha256='7ae5ccaca427bafa9760ac3cd8f8c244bfc259794b5b6bb9db4dda2241575d09')
    version('1.2.0', sha256='c70410551488251b0fee67b460fb9a536af8d6f9f008ad10ac51f615b6a521b1')
    version('1.1.1', sha256='bc3eb6cc0b61029825f4ff8de5b20a75f11639d75aad95ea0e11500e37534923')
    version('1.1.0', sha256='d9d2efe11d3a3fb9184da550d35bd1319dc8e30a63255927c82bb42fca1f4f7c')
    version('1.0.0', sha256='d38fbe01bbf7a3593a32bc35a9c4453c32bc42b98c377f9bff7e9f8da157786c')
    version('0.6.0', sha256='3718b1cbcd963c7d4c5511a8240812904164b7f381b647143a89d3b98f9bcd8e')
    version('0.5.1', sha256='ca943a7e809cc12257001ccfb99e3563da9af99d52f261725e96dfe0f9275bc3')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm@1.15.0:', type='build')
    depends_on('py-more-itertools', type=('build', 'run'), when='@0.6.0:')
