# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPip(PythonPackage):
    """The PyPA recommended tool for installing Python packages."""

    homepage = "https://pip.pypa.io/"
    pypi = "pip/pip-20.2.tar.gz"

    version('21.0.1', sha256='99bbde183ec5ec037318e774b0d8ae0a64352fe53b2c7fd630be1d07e94f41e5')
    version('21.0',   sha256='b330cf6467afd5d15f4c1c56f5c95e56a2bfb941c869bed4c1aa517bcb16de25')
    version('20.3.4', sha256='6773934e5f5fc3eaa8c5a44949b5b924fc122daa0a8aa9f80c835b4ca2a543fc')
    version('20.3.3', sha256='79c1ac8a9dccbec8752761cb5a2df833224263ca661477a2a9ed03ddf4e0e3ba')
    version('20.3.2', sha256='aa1516c1c8f6f634919cbd8a58fc81432b0fa96f421a97d05a205ee86b07c43d')
    version('20.3.1', sha256='43f7d3811f05db95809d39515a5111dd05994965d870178a4fe10d5482f9d2e2')
    version('20.3',   sha256='9ae7ca6656eac22d2a9b49d024fc24e00f68f4c4d4db673d2d9b525c3dea6e0e')
    version('20.2.4', sha256='85c99a857ea0fb0aedf23833d9be5c40cf253fe24443f0829c7b472e23c364a1')
    version('20.2.3', sha256='30c70b6179711a7c4cf76da89e8a0f5282279dfb0278bec7b94134be92543b6d')
    version('20.2.2', sha256='58a3b0b55ee2278104165c7ee7bc8e2db6f635067f3c66cf637113ec5aa71584')
    version('20.2.1', sha256='c87c2b2620f2942dfd5f3cf1bb2a18a99ae70de07384e847c8e3afd1d1604cf2')
    version('20.2',   sha256='912935eb20ea6a3b5ed5810dde9754fde5563f5ca9be44a8a6e5da806ade970b')
    version('19.3',   sha256='324d234b8f6124846b4e390df255cacbe09ce22791c3b714aa1ea6e44a4f2861')
    version('19.1.1', sha256='44d3d7d3d30a1eb65c7e5ff1173cdf8f7467850605ac7cc3707b6064bddd0958')
    version('19.0.3', sha256='6e6f197a1abfb45118dbb878b5c859a0edbdd33fd250100bc015b67fded4b9f2')
    version('18.1',   sha256='c0a292bd977ef590379a3f05d7b7f65135487b67470f6281289a94e015650ea1')
    version('10.0.1', sha256='f2bd08e0cd1b06e10218feaf6fef299f473ba706582eb3bd9d52203fdbd7ee68')
    version('9.0.1',  sha256='09f243e1a7b461f654c26a725fa373211bb7ff17a9300058b205c61658ca940d')

    depends_on('python@3.5:', when='@21:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', when='@19.2:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@18:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.3:', when='@10:', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))

    # Most Python packages only require setuptools as a build dependency.
    # However, pip requires setuptools during runtime as well.
    depends_on('py-setuptools', type=('build', 'run'))
