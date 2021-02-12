# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMako(PythonPackage):
    """A super-fast templating language that borrows the best
       ideas from the existing templating languages."""

    pypi = "Mako/Mako-1.0.1.tar.gz"

    version('1.1.4',  sha256='17831f0b7087c313c0ffae2bcbbd3c1d5ba9eeac9c38f2eb7b50e8c99fe9d5ab')
    version('1.1.3',  sha256='8195c8c1400ceb53496064314c6736719c6f25e7479cd24c77be3d9361cddc27')
    version('1.1.2',  sha256='3139c5d64aa5d175dbafb95027057128b5fbd05a40c53999f3905ceb53366d9d')
    version('1.1.1',  sha256='2984a6733e1d472796ceef37ad48c26f4a984bb18119bb2dbc37a44d8f6e75a4')
    version('1.1.0',  sha256='a36919599a9b7dc5d86a7a8988f23a9a3a3d083070023bab23d64f7f1d1e0a4b')
    version('1.0.14', sha256='f5a642d8c5699269ab62a68b296ff990767eb120f51e2e8f3d6afb16bdb57f4b')
    version('1.0.13', sha256='95ee720cc3453063788515d55bd7ce4a2a77b7b209e4ac70ec5c86091eb02541')
    version('1.0.12', sha256='0cfa65de3a835e87eeca6ac856b3013aade55f49e32515f65d999f91a2324162')
    version('1.0.11', sha256='889c7f16d5388092d4c585cf9def19cad089e9f848a7c40e03394553048362a6')
    version('1.0.10', sha256='7165919e78e1feb68b4dbe829871ea9941398178fa58e6beedb9ba14acf63965')
    version('1.0.9',  sha256='0728c404877cd4ca72c409c0ea372dc5f3b53fa1ad2bb434e1d216c0444ff1fd')
    version('1.0.8',  sha256='04092940c0df49b01f43daea4f5adcecd0e50ef6a4b222be5ac003d5d84b2843')
    version('1.0.7',  sha256='4e02fde57bd4abb5ec400181e4c314f56ac3e49ba4fb8b0d50bba18cb27d25ae')
    version('1.0.6',  sha256='48559ebd872a8e77f92005884b3d88ffae552812cdf17db6768e5c3be5ebbe0d')
    version('1.0.5',  sha256='e3e27cdd7abfd78337f33bd455f756c823c2d6224ad440a88f14bbd53a5ebc93')
    version('1.0.4', sha256='fed99dbe4d0ddb27a33ee4910d8708aca9ef1fe854e668387a9ab9a90cbf9059')
    version('1.0.1', sha256='45f0869febea59dab7efd256fb451c377cbb7947bef386ff0bb44627c31a8d1c')

    depends_on('py-setuptools', type='build')
    depends_on('py-markupsafe@0.9.2:', type=('build', 'run'))
