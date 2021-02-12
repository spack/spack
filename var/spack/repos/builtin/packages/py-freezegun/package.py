# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFreezegun(PythonPackage):
    """FreezeGun is a library that allows your Python tests to travel
    through time by mocking the datetime module."""

    homepage = "https://github.com/spulec/freezegun"
    pypi = "freezegun/freezegun-0.3.12.tar.gz"

    version('1.1.0',  sha256='177f9dd59861d871e27a484c3332f35a6e3f5d14626f2bf91be37891f18927f3')
    version('1.0.0',  sha256='1cf08e441f913ff5e59b19cc065a8faa9dd1ddc442eaf0375294f344581a0643')
    version('0.3.15', sha256='e2062f2c7f95cc276a834c22f1a17179467176b624cc6f936e8bc3be5535ad1b')
    version('0.3.14', sha256='6262de2f4bab671f7189bb8a0b9d8751da69a53f0b9813fb8f412681662d872a')
    version('0.3.13', sha256='6125965e9bd268cff7da54e4f5c02101b713e2db94a123b20c3e3c0b1f5a991e')
    version('0.3.12', sha256='2a4d9c8cd3c04a201e20c313caf8b6338f1cfa4cda43f46a94cc4a9fd13ea5e7')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-python-dateutil@1.0:1.999', type=('build', 'run'), when='^python@:2')
    depends_on('py-python-dateutil@2:', type=('build', 'run'), when='^python@3:')
