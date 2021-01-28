# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBluepysnap(PythonPackage):
    """Pythonic Sonata circuits access API"""

    homepage = "https://github.com/BlueBrain/snap"
    git      = "https://github.com/BlueBrain/snap.git"
    url      = "https://pypi.io/packages/source/b/bluepysnap/bluepysnap-0.2.0.tar.gz"

    version('0.9.0', sha256='140e06b9a7cc90719ffaf4c71ffaa9320c13bdd8ef25ffb598fd348b850b6695')
    version('0.8.0', sha256='10337610cfb83121f2869cec53830de04eed8e90b2b27aba36b8799468fa9c0f')
    version('0.7.0', sha256='fa4d54539fdb98c5febdabf7f13786567fc8fbd5e86f95864b4de89f18fd97bd')
    version('0.6.1', sha256='f17cdd43a9f444e4825ab9578b3184fb17df76b1598852d3b74161647a096285')
    version('0.5.2', sha256='d97c3fcd05261ba68e855e828b88d37fa1a7302abd79163d2d8ee806b1aad9b3')
    version('0.5.1', sha256='81cbeab26b219b52f496ea55145e60f6b826c697265f4fe2d1effe5df249cabf')
    version('0.5.0', sha256='97a31644d1e1daccb708e92734dfb873bc0b7aa7f98939527b91cde895cdef74')
    version('0.4.1', sha256='cbb16a0cbd43ae4ad9e35b2fad0c986ebf9029e386087c0a934565da428ad558')
    version('0.2.0', sha256='95273bedee0ad0b9957aed40dadc94c4a0973ba014bbc215172a9c2e7144d64a')
    version('0.1.2', sha256='aa29c1344258c1ca0cf7f5f53f3080025b9d098e3366872369586ad7ccf334a2')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-functools32', type='run', when='^python@:3.1.99')
    depends_on('py-cached-property@1.0:', type='run')
    depends_on('py-h5py@2.2:', type='run')
    depends_on('py-libsonata@0.1.4:', type='run')
    depends_on('py-neurom@1.3:', type='run')
    depends_on('py-numpy@1.8:', type='run')
    depends_on('py-pandas@0.17:', type='run')
    depends_on('py-six@1.0:', type='run')

    depends_on('py-click@7.0:', type='run')
    depends_on('py-pathlib2@2.3:', type='run')
