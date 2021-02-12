# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyTokenizers(PythonPackage):
    """Fast and Customizable Tokenizers."""

    homepage = "https://github.com/huggingface/tokenizers"
    pypi = "tokenizers/tokenizers-0.6.0.tar.gz"

    version('0.10.1', sha256='81c35b4bc9238c0b5d0af91a719e732a60ee0d87d8bf76615bfec8f3e3ba8f15')
    version('0.10.0', sha256='13e9971af25b39e6f355835dc192bcc6b6091c045869af4a99838cbbd4c8cb6c')
    version('0.9.4',  sha256='3ea3038008f1f74c8a1e1e2e73728690eed2d7fa4db0a51bcea391e644672426')
    version('0.9.3',  sha256='bacaeb3621055aba9b5158a21dc8b5d80f65724ff47f414f9d06f1e087668d61')
    version('0.9.2',  sha256='6ba1337b5decd5c49f3db97fd9b202f74c249aca6e65899062df9cb083fefa60')
    version('0.9.1',  sha256='d0bcfa45cfd66e6aa379c7362d56a77f66a195fd06bc38ec912ca3d63c03d3b8')
    version('0.9.0',  sha256='0bfa960345e114efd553e265e32eca6d79861abe24925fba903c925f8760f795')
    version('0.8.1',  sha256='e228ec9dcdced445124419219477ac4b4c4b0dc57b95b196a9ef37097d382559')
    version('0.8.0',  sha256='703101ffc1cce87e39a8fa9754126a5c29590b03817a73727e3268474dc716e6')
    version('0.7.0',  sha256='a3cb9be31e3be381ab3f9e9ea7f96d4ba83588c40c44fe63b535b7341cdf74fe')
    version('0.6.0', sha256='1da11fbfb4f73be695bed0d655576097d09a137a16dceab2f66399716afaffac')
    version('0.5.2', sha256='b5a235f9c71d04d4925df6c4fa13b13f1d03f9b7ac302b89f8120790c4f742bc')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-rust', type='build')
    depends_on('rust@nightly', type='build')

    # TODO: This package currently requires internet access to install.
    # Also, a nightly or dev version of rust is required to build.
    # https://github.com/huggingface/tokenizers/issues/176
    # https://github.com/PyO3/pyo3/issues/5
