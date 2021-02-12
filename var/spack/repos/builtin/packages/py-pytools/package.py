# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytools(PythonPackage):
    """A collection of tools for Python"""

    pypi = "pytools/pytools-2019.1.1.tar.gz"

    version('2021.1',   sha256='073ae22a0ae946e2db97164f2eb24a599cd3a51430384aa40859dffd73056c40')
    version('2020.4.4', sha256='3645ed839cf4d79cb4bf030f37ddaeecd7fe5e2d6698438cc36c24a1d5168809')
    version('2020.4.3', sha256='21aa1fd942bc3bc54c8ae3b5e60c1f771e6db0817b7402fd802aa5964f20e629')
    version('2020.4.2', sha256='a1304b07cb9102d566123f87aa4b5ad55e65d4c55e0af9985906ad11b2ffbdce')
    version('2020.4',   sha256='37db39ff11a1b5fc8aec875ae4ddb3d6c21aa0e95bddc9c841aa98e1631ae460')
    version('2020.3.1', sha256='86ebb27e8d946b30bc4479f97862066eb26e305d5ad4327230b2b2f8cbf110f9')
    version('2020.3',   sha256='7b9004b9f113ad502485f6496940c35ca7c802edf6459433adf035c01cc56690')
    version('2020.2',   sha256='3cacefed54148aafb07502c7c907cae8d9327ea35df16e3366c883a706ed5601')
    version('2020.1',   sha256='c132d17855584ad61c6e00f3ff11146499755944afc400cce9eae0ecf03d04a6')
    version('2019.1.1', sha256='ce2d702ae4ef10a70197b00b93141461140d00578f2a862fa946ca1446a300db')
    version('2016.2.6', sha256='6dd49932b8f81a8b622685cff3dd515e351a9290aef0fd5d020e4df00c06aa95')

    depends_on('py-setuptools', type='build')
    depends_on('py-decorator@3.2.0:', type=('build', 'run'))
    depends_on('py-appdirs@1.4.0:', type=('build', 'run'))
    depends_on('py-six@1.8.0:', type=('build', 'run'))
    depends_on('py-numpy@1.6.0:', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.4:', type=('build', 'run'))
