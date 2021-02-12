# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMoreItertools(PythonPackage):
    """Additions to the standard Python itertools package."""

    homepage = "https://github.com/erikrose/more-itertools"
    pypi = "more-itertools/more-itertools-7.2.0.tar.gz"

    version('8.7.0', sha256='c5d6da9ca3ff65220c3bfd2a8db06d698f05d4d2b9be57e1deb2be5a45019713')
    version('8.6.0', sha256='b3a9005928e5bed54076e6e549c792b306fddfe72b2d1d22dd63d42d5d3899cf')
    version('8.5.0', sha256='6f83822ae94818eae2612063a5101a7311e68ae8002005b5e05f03fd74a86a20')
    version('8.4.0', sha256='68c70cc7167bdf5c7c9d8f6954a7837089c6a36bf565383919bb595efb8a17e5')
    version('8.3.0', sha256='558bb897a2232f5e4f8e2399089e35aecb746e1f9191b6584a151647e89267be')
    version('8.2.0', sha256='b1ddb932186d8a6ac451e1d95844b382f55e12686d51ca0c68b6f61f2ab7a507')
    version('8.1.0', sha256='c468adec578380b6281a114cb8a5db34eb1116277da92d7c46f904f0b52d3288')
    version('8.0.2', sha256='b84b238cce0d9adad5ed87e745778d20a3f8487d0f0cb8b8a586816c7496458d')
    version('8.0.1', sha256='a293dbdad9d4d22e1e70832b8dcab72aac20805f0fa0575aec27cab8841e09ff')
    version('8.0.0', sha256='53ff73f186307d9c8ef17a9600309154a6ae27f25579e80af4db8f047ba14bc2')
    version('7.2.0', sha256='409cd48d4db7052af495b09dec721011634af3753ae1ef92d2b32f73a745f832')
    version('7.0.0', sha256='c3e4748ba1aad8dba30a4886b0b1a2004f9a863837b8654e7059eebf727afa5a')
    version('5.0.0', sha256='38a936c0a6d98a38bcc2d03fdaaedaba9f412879461dd2ceff8d37564d6522e4')
    version('4.3.0', sha256='c476b5d3a34e12d40130bc2f935028b5f636df8f372dc2c1c01dc19681b2039e')
    version('4.1.0', sha256='c9ce7eccdcb901a2c75d326ea134e0886abfbea5f93e91cc95de9507c0816c44')
    version('2.2',   sha256='93e62e05c7ad3da1a233def6731e8285156701e3419a5fe279017c429ec67ce0')

    depends_on('python@3.5:', when='@7.1:', type=('build', 'run'))
    depends_on('python@3.4:', when='@6:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.2:', when='@2.3:', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.2:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-six@1.0.0:1.999', when='@:5', type=('build', 'run'))
