# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGitpython(PythonPackage):
    """GitPython is a python library used to interact with Git repositories."""

    homepage = "http://gitpython.readthedocs.org"
    url = "https://files.pythonhosted.org/packages/ec/4d/e6553122c85ec7c4c3e702142cc0f5ed02e5cf1b4d7ecea86a07e45725a0/GitPython-3.1.12.tar.gz"

    version('3.1.12',  sha256='42dbefd8d9e2576c496ed0059f3103dcef7125b9ce16f9d5f9c834aed44a1dac')
    version('3.1.11',  sha256='befa4d101f91bad1b632df4308ec64555db684c360bd7d2130b4807d49ce86b8')
    version('3.1.10',  sha256='f488d43600d7299567b59fe41497d313e7c1253a9f2a8ebd2df8af2a1151c71d')
    version('3.1.9',  sha256='a03f728b49ce9597a6655793207c6ab0da55519368ff5961e4a74ae475b9fa8e')
    version('3.1.8',  sha256='080bf8e2cf1a2b907634761c2eaefbe83b69930c94c66ad11b65a8252959f912')
    version('3.1.7',  sha256='2db287d71a284e22e5c2846042d0602465c7434d910406990d5b74df4afb0858')
    version('3.1.6',  sha256='b54969b3262d4647f80ace8e9dd4e3f99ac30cc0f3e766415b349208f810908f')
    version('3.1.5',  sha256='90400ecfa87bac36ac75dfa7b62e83a02017b51759f6eef4494e4de775b2b4be')
    version('3.1.4',  sha256='fa98ce1f05805d59bbc3adb16c0780e5ca43b5ea9422feecf1cd0949a61d947e')
    version('3.1.3',  sha256='e107af4d873daed64648b4f4beb89f89f0cfbe3ef558fc7821ed2331c2f8da1a')
    version('3.1.2',  sha256='864a47472548f3ba716ca202e034c1900f197c0fb3a08f641c20c3cafd15ed94')
    version('3.1.1',  sha256='6d4f10e2aaad1864bb0f17ec06a2c2831534140e5883c350d58b4e85189dab74')
    version('3.1.0',  sha256='e426c3b587bd58c482f0b7fe6145ff4ac7ae6c82673fc656f489719abca6f4cb')
    version('3.0.9',  sha256='7e5df21bfef38505115ad92544fb379e6fedb2753f3b709174c4358cecd0cb97')
    version('0.3.6',  sha256='e6599fcb939cb9b25a015a429702db39de10f2b493655ed5669c49c37707d233')

    depends_on('python@3.5:',   type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-gitdb@4.0.1:4.999', type=('build', 'run'))

    def url_for_version(self, version):
        url = ''
        if version == Version('3.1.12'):
            url = 'https://files.pythonhosted.org/packages/ec/4d/e6553122c85ec7c4c3e702142cc0f5ed02e5cf1b4d7ecea86a07e45725a0/GitPython-3.1.12.tar.gz'
        elif version == Version('3.1.11'):
            url = 'https://files.pythonhosted.org/packages/85/3d/ee9aa9c77a3c0e9074461d2d8da86c3564ed96abd28fa099dc3e05338a72/GitPython-3.1.11.tar.gz'
        elif version == Version('3.1.10'):
            url = 'https://files.pythonhosted.org/packages/bd/8a/0cfbc4b9f7b535891fe5c6592ee4233c296f2f0ec2542aa638ebaaaf949d/GitPython-3.1.10.tar.gz'
        elif version == Version('3.1.9'):
            url = 'https://files.pythonhosted.org/packages/72/ad/5cf16fd1307e0ec17fc2347475e732f64d396649c64ed358a29186f4ce74/GitPython-3.1.9.tar.gz'
        elif version == Version('3.1.8'):
            url = 'https://files.pythonhosted.org/packages/63/c7/639d7965f5c860ba0fec323fd3b80ba57f7c3eb90e58ca5b4ea467e50ba9/GitPython-3.1.8.tar.gz'
        elif version == Version('3.1.7'):
            url = 'https://files.pythonhosted.org/packages/53/ea/fc34cddaa30bfc5e283f13e754fb3e2648ccd9f7019eaa3518fb5350ae51/GitPython-3.1.7.tar.gz'
        elif version == Version('3.1.6'):
            url = 'https://files.pythonhosted.org/packages/a8/4f/31fcb591d71eb5aa7e6e65ece4f80320e48d0fa18f6fd687502780919439/GitPython-3.1.6.tar.gz'
        elif version == Version('3.1.5'):
            url = 'https://files.pythonhosted.org/packages/41/5d/acc4f00a53d6b5383bc04517bc8f7eed16df4a9c55db49abfcacbcd931de/GitPython-3.1.5.tar.gz'
        elif version == Version('3.1.4'):
            url = 'https://files.pythonhosted.org/packages/c4/10/855388aefec6b54f2ebba13929c524c0168dc8cbc02098078c9a379b7eda/GitPython-3.1.4.tar.gz'
        elif version == Version('3.1.3'):
            url = 'https://files.pythonhosted.org/packages/5b/ef/96dd6b06400821bbad3f7e275f4a4f88af324124c5c04958e2f2c14ce2c8/GitPython-3.1.3.tar.gz'
        elif version == Version('3.1.2'):
            url = 'https://files.pythonhosted.org/packages/36/5d/23c3f9a527a1e1c79e8622c7bb74704f6468351cd756e20f65f2ea7aba44/GitPython-3.1.2.tar.gz'
        elif version == Version('3.1.1'):
            url = 'https://files.pythonhosted.org/packages/ac/3d/9fe11d9cf14b49553e8e35a4dce360e18f25f964638b631dc5b9ca23a88f/GitPython-3.1.1.tar.gz'
        elif version == Version('3.1.0'):
            url = 'https://files.pythonhosted.org/packages/ee/bc/c8b6bc8b81b94f50bd46ed690e2677beec0071228e7f153981cb51f4d59a/GitPython-3.1.0.tar.gz'
        elif version == Version('3.0.9'):
            url = 'https://files.pythonhosted.org/packages/22/b1/f5a930bf89fcf9eee87f48e6dfa17106f319a316612714a0b7156ded5e84/GitPython-3.0.9.tar.gz'
        elif version == Version('0.3.6'):
            url = 'https://github.com/gitpython-developers/GitPython/archive/0.3.6.tar.gz'
        return url
