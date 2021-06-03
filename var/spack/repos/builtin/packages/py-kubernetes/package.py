# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyKubernetes(PythonPackage):
    """Official Python client library for kubernetes. """

    homepage = "https://kubernetes.io"
    git      = "https://github.com/kubernetes-client/python.git"
    pypi = "kubernetes/kubernetes-17.17.0.tar.gz"

    maintainers = ['vvolkl']

    version('17.17.0',   sha256='c69b318696ba797dcf63eb928a8d4370c52319f4140023c502d7dfdf2080eb79')
    version('12.0.1',    sha256='ec52ea01d52e2ec3da255992f7e859f3a76f2bdb51cf65ba8cd71dfc309d8daa')
    version('12.0.0',    sha256='72f095a1cd593401ff26b3b8d71749340394ca6d8413770ea28ce18efd5bcf4c')
    version('11.0.0',    sha256='1a2472f8b01bc6aa87e3a34781f859bded5a5c8ff791a53d889a8bd6cc550430')
    version('10.1.0',    sha256='85a767d04f17d6d317374b6c35e09eb168a6bfd9276f0b3177cc206376bad968')
    version('10.0.1',    sha256='3770a496663396ad1def665eeadb947b3f45217a08b64b10c01a57e981ac8592')
    version('9.0.0',     sha256='a8b0aed55ba946faea660712595a52ae53a8854df773d96f47a63fa0c9d4e3bf')

    depends_on('py-certifi@14.05.14:', type=('build', 'run'))
    depends_on('py-six@1.9.0:', type=('build', 'run'))
    depends_on('py-python-dateutil@2.5.3:', type=('build', 'run'))
    depends_on('py-setuptools@21.0.0:', type=('build'))
    depends_on('py-pyyaml@3.12:', type=('build', 'run'))
    depends_on('py-google-auth@1.0.1:', type=('build', 'run'))
    depends_on('py-ipaddress@1.0.17:', when='^python@:2.8', type=('build', 'run'))
    depends_on('py-websocket-client@0.32:0.39,0.43:', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-requests-oauthlib', type=('build', 'run'))
    depends_on('py-urllib3@1.24.2:', type=('build', 'run'))
