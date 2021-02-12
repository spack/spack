# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyPlac(PythonPackage):
    """The smartest command line arguments parser in the world."""

    homepage = "https://github.com/micheles/plac"
    pypi = "plac/plac-1.1.3.tar.gz"

    version('1.3.1', sha256='9ebe589ae371c0f863848cebffbfa1394e814a9b8b5a5a42ea373572d29d856d')
    version('1.3.0', sha256='2e6422d966ca2cbe30353ad13f1c44fddfa71f8445fb54fff0169d3c982101be')
    version('1.2.0', sha256='ca03587234e5bdd2a3fa96f19a04a01ebb5b0cd66d48ecb5a54d42bc9b287320')
    version('1.1.3', sha256='398cb947c60c4c25e275e1f1dadf027e7096858fb260b8ece3b33bcff90d985f')

    depends_on('py-setuptools', type='build')
    depends_on('py-argparse', when='^python@:2.6', type=('build', 'run'))
