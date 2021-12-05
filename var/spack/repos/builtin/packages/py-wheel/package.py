# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWheel(Package):
    """A built-package format for Python."""

    homepage = "https://github.com/pypa/wheel"
    url = "https://files.pythonhosted.org/packages/source/w/wheel/wheel-0.34.2.tar.gz"
    list_url = "https://pypi.org/simple/wheel/"

    version('0.37.0', sha256='e2ef7239991699e3355d54f8e968a21bb940a1dbf34a4d226741e64462516fad')
    version('0.36.2', sha256='e11eefd162658ea59a60a0f6c7d493a7190ea4b9a85e335b33489d9f17e0245e')
    version('0.35.1', sha256='99a22d87add3f634ff917310a3d87e499f19e663413a52eb9232c447aa646c9f')
    version('0.34.2', sha256='8788e9155fe14f54164c1b9eb0a319d98ef02c160725587ad60f14ddc57b6f96')
    version('0.33.6', sha256='10c9da68765315ed98850f8e048347c3eb06dd81822dc2ab1d4fde9dc9702646')
    version('0.33.4', sha256='62fcfa03d45b5b722539ccbc07b190e4bfff4bb9e3a4d470dd9f6a0981002565')
    version('0.33.1', sha256='66a8fd76f28977bb664b098372daef2b27f60dc4d1688cfab7b37a09448f0e9d')
    version('0.32.3', sha256='029703bf514e16c8271c3821806a1c171220cc5bdd325cbf4e7da1e056a01db6')
    version('0.29.0', sha256='1ebb8ad7e26b448e9caa4773d2357849bf80ff9e313964bcaf79cbf0201a1648')
    version('0.26.0', sha256='eaad353805c180a47545a256e6508835b65a8e830ba1093ed8162f19a50a530c')

    extends('python')
    depends_on('python@2.7:2.8,3.5:', when='@0.34:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@0.30:', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.2:', type=('build', 'run'))
    depends_on('py-pip', type='build')

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

    conflicts(
        '^python@:2.6,3.0:3.3',
        msg='An older version of setuptools is required to bootstrap '
        'this package, use a newer Python or contact @adamjstewart to fix this'
    )

    def setup_build_environment(self, env):
        # Setuptools is required to build wheel from source
        env.prepend_path('PYTHONPATH', join_path(self.stage.source_path, 'setuptools'))

    def install(self, spec, prefix):
        pip('install', '--no-deps', '--prefix', prefix, '--ignore-installed',
            '--no-build-isolation', '--no-index', '--no-warn-script-location', '.')
