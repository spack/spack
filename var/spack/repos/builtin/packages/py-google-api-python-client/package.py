# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGoogleApiPythonClient(PythonPackage):
    """The Google API Client for Python is a client library for accessing the
    Plus, Moderator, and many other Google APIs."""

    homepage = "http://github.com/google/google-api-python-client/"
    pypi = "google-api-python-client/google-api-python-client-1.7.10.tar.gz"

    version('1.12.8', sha256='f3b9684442eec2cfe9f9bb48e796ef919456b82142c7528c5fd527e5224f08bb')
    version('1.12.7', sha256='df143f9d69a1458483d0a26add5f2fad22e1023f0593a7b2f1d49bfe5962062d')
    version('1.12.6', sha256='1f5cfcb92c8e3bd0a69cb2ff3cefa5ff16ffa1900af795a53f5bed93c8238951')
    version('1.12.5', sha256='1892cd490d164e5ec2f2168dc3b4fa0af68f36ca15a88b91bca1826b3d4f2829')
    version('1.12.4', sha256='d4b850e1aa107113339baf27670ae80d493f4e7758e455cee40100e13f07c2d6')
    version('1.12.3', sha256='844ef76bda585ea0ea2d5e7f8f9a0eb10d6e2eba66c4fea0210ec7843941cb1a')
    version('1.12.2', sha256='54a7d330833a2e7b0587446d7e4ae6d0244925a9a8e1dfe878f3f7e06cdedb62')
    version('1.12.1', sha256='ddadc243ce627512c2a27e11d369f5ddf658ef80dbffb247787499486ef1ea98')
    version('1.12.0', sha256='8d742d8809b32e4859bc406f9525bbbd351dc1ded02e5d72fd9b162c136b5425')
    version('1.11.0', sha256='caf4015800ef1a18d06d117f47f0219c0c0641f21978f6b1bb5ede7912fab97b')
    version('1.10.1', sha256='aa8740103774c2b7859f73ba6f55211e794ed7a374c5c427b583869b6bfe9e6c')
    version('1.10.0', sha256='fa24f07f6124ff2e91ee9b7550e240481bcb31b8f77a75e8d481be1c44a6ff07')
    version('1.9.3',  sha256='220349ce189a85229fc46875d467101318495a4a735c0ff2f165b9bdbc7511a0')
    version('1.9.2',  sha256='6b24022c75b38a1b323a74129d09af1131078b7c0d337ac8fa6461d5f8b2b0e9')
    version('1.9.1',  sha256='a230710c4a3709e00db6a8633865940d2a00d00da4d998ce91f1d0f18471d859')
    version('1.9.0',  sha256='6338a48d06866167998a613af738eb6a17e6b8140376d0eb5067fb5e993d2757')
    version('1.8.4',  sha256='bbe212611fdc05364f3d20271cae53971bf4d485056e6c0d40748eddeeda9a19')
    version('1.8.3',  sha256='be4e8dcf399d7d1dcaae004b7f18694907f740bf6e6cebda91da8ebd968c5481')
    version('1.8.2',  sha256='bf482c13fb41a6d01770f9d62be6b33fdcd41d68c97f2beb9be02297bdd9e725')
    version('1.8.1',  sha256='ffd6bf6310bc4be45483149f782d4569030a1a77109239f8c5ebd0ae5338a791')
    version('1.8.0',  sha256='0f5b42a14e2d2f7dee40f2e4514531dbe95ebde9c2173b1c4040a65c427e7900')
    version('1.7.12', sha256='9fd6a7b032b5e59975869a980655f49f27f1ad4dd51bdd3a9392bb2e46ad7409')
    version('1.7.11', sha256='a8a88174f66d92aed7ebbd73744c2c319b4b1ce828e565f9ec721352d2e2fb8c')
    version('1.7.10', sha256='2e55a5c7b56233c68945b6804c73e253445933f4d485d4e69e321b38772b9dd6')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-httplib2@0.9.2:', type=('build', 'run'))
    depends_on('py-google-auth@1.4.1:', type=('build', 'run'))
    depends_on('py-google-auth-httplib2@0.0.3:', type=('build', 'run'))
    depends_on('py-six@1.6.1:', type=('build', 'run'))
    depends_on('py-uritemplate@3.0.0:', type=('build', 'run'))
