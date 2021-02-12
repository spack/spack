# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCodecov(PythonPackage):
    """Hosted coverage reports for Github, Bitbucket and Gitlab."""

    homepage = "https://github.com/codecov/codecov-python"
    pypi = "codecov/codecov-2.0.15.tar.gz"

    version('2.1.11', sha256='6cde272454009d27355f9434f4e49f238c0273b216beda8472a65dc4957f473b')
    version('2.1.10', sha256='d30ad6084501224b1ba699cbf018a340bb9553eb2701301c14133995fdd84f33')
    version('2.1.9',  sha256='355fc7e0c0b8a133045f0d6089bde351c845e7b52b99fec5903b4ea3ab5f6aab')
    version('2.1.8',  sha256='0be9cd6358cc6a3c01a1586134b0fb524dfa65ccbec3a40e9f28d5f976676ba2')
    version('2.1.7',  sha256='491938ad774ea94a963d5d16354c7299e90422a33a353ba0d38d0943ed1d5091')
    version('2.1.6',  sha256='5bf4e752844566087c287cb7c43522210c28ac5db089005966109f58cbcbe135')
    version('2.1.5',  sha256='46ea90211df4991a449cf6d3bb56175292ce4136186976aa5d3ec738261b5209')
    version('2.1.4',  sha256='bf30a41f65e747b159e2a749d1f9c92042d358bba0905fd94d3def3a368e592c')
    version('2.1.3',  sha256='2ebd639d8f621aabcce399e475b0302e436cb7e00e7724d1b2224bbf3f215a0c')
    version('2.1.1',  sha256='520ab0ef447d695a9f71e83f9fa65eedbd2d6d1022ff88836e27b9eb82fbdc7b')
    version('2.1.0',  sha256='43ad6cb3e7de073d911aa3ab6a754db88d270fcb0e0d8e2062b964098a51d69b')
    version('2.0.22', sha256='aeeefa3a03cac8a78e4f988e935b51a4689bb1f17f20d4e827807ee11135f845')
    version('2.0.21', sha256='52bb893ebf391a145e4702b36d120b7012f42d8956ea6451e64d52bb84e0c977')
    version('2.0.20', sha256='2dff9cf7c0421d776fe7b3cf05dd0d612a46c7170115d7ba3713e1e7d8ad0c38')
    version('2.0.19', sha256='31a0cfc39e8aaedfb0899296371637d21b27b104d698f772e6aa11d0529d249e')
    version('2.0.18', sha256='2c22451c8dea97c77c8325f6acd0b984c414ff8b5ce8a854ef7fc0f103bb0691')
    version('2.0.17', sha256='df81781dfae3a033ffcca5b340c7bba36c5a3091a02e710955fb748684528225')
    version('2.0.16', sha256='4cf93c30cc1ddb6d7414fce0a45816889499c3febc8bbbc24f1cd1936a804087')
    version('2.0.15', sha256='8ed8b7c6791010d359baed66f84f061bba5bd41174bf324c31311e8737602788')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-requests@2.7.9:', type=('build', 'run'))
    depends_on('py-coverage', type=('build', 'run'))
    depends_on('py-argparse', when='^python@:2.6', type=('build', 'run'))
