# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyTokenizers(PythonPackage):
    """Fast and Customizable Tokenizers."""

    homepage = "https://github.com/huggingface/tokenizers"
    url      = "https://pypi.io/packages/source/t/tokenizers/tokenizers-0.6.0.tar.gz"

    version('0.6.0', sha256='1da11fbfb4f73be695bed0d655576097d09a137a16dceab2f66399716afaffac')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-rust', type='build')
