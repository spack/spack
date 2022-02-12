# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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

    version('21.7.0',    sha256='c9849afc2eafdce60efa210049ee7a94e7ef6cf3a7afa14a69b3bf0447825977')
    version('20.13.0',   sha256='ce5e881c13dc56f21a243804f90bc3c507af93c380f505c00e392c823968e4de')
    version('19.15.0',   sha256='08c93f300a9837104282ecc81458b903a56444c5c1ec3d990d237557312af47f')
    version('18.20.0',   sha256='0c72d00e7883375bd39ae99758425f5e6cb86388417cf7cc84305c211b2192cf')
    version('17.17.0',   sha256='c69b318696ba797dcf63eb928a8d4370c52319f4140023c502d7dfdf2080eb79')
    version('12.0.1',    sha256='ec52ea01d52e2ec3da255992f7e859f3a76f2bdb51cf65ba8cd71dfc309d8daa')
    version('12.0.0',    sha256='72f095a1cd593401ff26b3b8d71749340394ca6d8413770ea28ce18efd5bcf4c')
    version('11.0.0',    sha256='1a2472f8b01bc6aa87e3a34781f859bded5a5c8ff791a53d889a8bd6cc550430')
    version('10.1.0',    sha256='85a767d04f17d6d317374b6c35e09eb168a6bfd9276f0b3177cc206376bad968')
    version('10.0.1',    sha256='3770a496663396ad1def665eeadb947b3f45217a08b64b10c01a57e981ac8592')
    version('9.0.0',     sha256='a8b0aed55ba946faea660712595a52ae53a8854df773d96f47a63fa0c9d4e3bf')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-certifi@14.05.14:', type=('build', 'run'))
    depends_on('py-six@1.9.0:', type=('build', 'run'))
    depends_on('py-python-dateutil@2.5.3:', type=('build', 'run'))
    depends_on('py-setuptools@21.0.0:', type=('build'))
    depends_on('py-pyyaml@3.12:', when='@:18.19', type=('build', 'run'))
    depends_on('py-pyyaml@5.4.1:', when='@18.20.0:', type=('build', 'run'))
    depends_on('py-google-auth@1.0.1:', type=('build', 'run'))
    depends_on('py-ipaddress@1.0.17:', when='^python@:2.8', type=('build', 'run'))
    depends_on('py-websocket-client@0.32:0.39,0.43:', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-requests-oauthlib', type=('build', 'run'))
    depends_on('py-urllib3@1.24.2:', type=('build', 'run'))
