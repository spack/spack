# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class PyPip(Package):
    """The PyPA recommended tool for installing Python packages."""

    homepage = "https://pip.pypa.io/"
    url = "https://files.pythonhosted.org/packages/source/p/pip/pip-20.2.tar.gz"
    list_url = "https://pypi.org/simple/pip/"

    version('21.3.1', sha256='fd11ba3d0fdb4c07fbc5ecbba0b1b719809420f25038f8ee3cd913d3faa3033a')
    version('21.1.2', sha256='eb5df6b9ab0af50fe1098a52fd439b04730b6e066887ff7497357b9ebd19f79b')
    version('20.2',   sha256='912935eb20ea6a3b5ed5810dde9754fde5563f5ca9be44a8a6e5da806ade970b')
    version('19.3',   sha256='324d234b8f6124846b4e390df255cacbe09ce22791c3b714aa1ea6e44a4f2861')
    version('19.1.1', sha256='44d3d7d3d30a1eb65c7e5ff1173cdf8f7467850605ac7cc3707b6064bddd0958')
    version('19.0.3', sha256='6e6f197a1abfb45118dbb878b5c859a0edbdd33fd250100bc015b67fded4b9f2')
    version('18.1',   sha256='c0a292bd977ef590379a3f05d7b7f65135487b67470f6281289a94e015650ea1')
    version('10.0.1', sha256='f2bd08e0cd1b06e10218feaf6fef299f473ba706582eb3bd9d52203fdbd7ee68')
    version('9.0.1',  sha256='09f243e1a7b461f654c26a725fa373211bb7ff17a9300058b205c61658ca940d')

    extends('python')
    depends_on('python@3.6:', when='@21:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', when='@19.2:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@18:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.3:', when='@10:', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))

    # This bootstrapping procedure is similar to the one used by Nix:
    # https://github.com/NixOS/nixpkgs/blob/master/pkgs/development/python-modules/bootstrapped-pip/default.nix
    # Also see further discussion in:
    # https://discuss.python.org/t/bootstrapping-a-specific-version-of-pip/12306

    # Latest version, should be updated from time to time
    resource(
        name='setuptools',
        url='https://pypi.io/packages/source/s/setuptools/setuptools-59.4.0.tar.gz',
        sha256='b4c634615a0cf5b02cf83c7bedffc8da0ca439f00e79452699454da6fbd4153d',
        placement='setuptools',
        when='^python@3.6:',
    )
    # Latest version that supports Python 3.5
    resource(
        name='setuptools',
        url='https://pypi.io/packages/source/s/setuptools/setuptools-50.3.2.zip',
        sha256='ed0519d27a243843b05d82a5e9d01b0b083d9934eaa3d02779a23da18077bd3c',
        placement='setuptools',
        when='^python@3.5',
    )
    # Latest version that supports Python 2.7
    resource(
        name='setuptools',
        url='https://pypi.io/packages/source/s/setuptools/setuptools-44.1.1.zip',
        sha256='c67aa55db532a0dadc4d2e20ba9961cbd3ccc84d544e9029699822542b5a476b',
        placement='setuptools',
        when='^python@2.7',
    )
    # Latest version that supports Python 3.4
    resource(
        name='setuptools',
        url='https://pypi.io/packages/source/s/setuptools/setuptools-43.0.0.zip',
        sha256='db45ebb4a4b3b95ff0aca3ce5fe1e820ce17be393caf8902c78aa36240e8c378',
        placement='setuptools',
        when='^python@3.4',
    )

    # Latest version, should be updated from time to time
    resource(
        name='wheel',
        url='https://files.pythonhosted.org/packages/source/w/wheel/wheel-0.37.0.tar.gz',
        sha256='e2ef7239991699e3355d54f8e968a21bb940a1dbf34a4d226741e64462516fad',
        placement='wheel',
        when='^python@2.7,3.5:',
    )
    # Latest version that supports Python 3.4
    resource(
        name='wheel',
        url='https://files.pythonhosted.org/packages/source/w/wheel/wheel-0.33.6.tar.gz',
        sha256='10c9da68765315ed98850f8e048347c3eb06dd81822dc2ab1d4fde9dc9702646',
        placement='wheel',
        when='^python@3.4',
    )

    conflicts(
        '^python@:2.6,3.0:3.3',
        msg='An older version of setuptools/wheel is required to bootstrap '
        'this package, use a newer Python or contact @adamjstewart to fix this'
    )

    def setup_build_environment(self, env):
        # Use pip to bootstrap itself
        env.prepend_path('PYTHONPATH', 'src')

        # Setuptools and wheel are required to build pip from source
        env.prepend_path('PYTHONPATH', join_path(self.stage.source_path, 'setuptools'))
        env.prepend_path(
            'PYTHONPATH', join_path(self.stage.source_path, 'wheel', 'src')
        )

    def install(self, spec, prefix):
        args = ['-m', 'pip'] + std_pip_args + ['--prefix=' + prefix]
        python(*args)

    @property
    def command(self):
        """Returns the pip command, which may vary depending
        on the version of Python and how it was installed.

        Returns:
            Executable: the pip command
        """
        # We need to be careful here. If the user is using an externally
        # installed python, several different commands could be located
        # in the same directory. Be as specific as possible. Search for:
        #
        # * pip3.6
        # * pip3
        # * pip
        #
        # in that order if using python@3.6.5, for example.
        version = self.spec['python'].version
        for ver in [version.up_to(2), version.up_to(1), '']:
            path = os.path.join(self.prefix.bin, 'pip{0}'.format(ver))
            if os.path.exists(path):
                return Executable(path)
        else:
            msg = 'Unable to locate pip command in {1}'
            raise RuntimeError(msg.format(self.prefix.bin))

    def setup_dependent_package(self, module, dependent_spec):
        setattr(module, 'pip', self.command)
