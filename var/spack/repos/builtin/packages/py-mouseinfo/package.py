# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-mouseinfo
#
# You can edit this file again by typing:
#
#     spack edit py-mouseinfo
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyMouseinfo(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    pypi     = "MouseInfo/MouseInfo-0.1.3.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('0.1.3', sha256='2c62fb8885062b8e520a3cce0a297c657adcc08c60952eb05bc8256ef6f7f6e7')

    # FIXME: Add dependencies if required. Only add the python dependency
    # if you need specific versions. A generic python dependency is
    # added implicity by the PythonPackage class.
    depends_on('python@2.7,3.2:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    # rubicon-objc;platform_system=="Darwin"',
    # 'python3-Xlib;platform_system=="Linux" and python_version>="3.0"',
    # 'Xlib;platform_system=="Linux" and python_version<"3.0"',
    depends_on('py-python3-xlib', when='^python@3 platform=linux', type=('build', 'run'))

    depends_on('py-pyperclip', type=('build', 'run'))
    depends_on('py-pillow@5.2.0:', when='^python@3.7:', type=('build', 'run'))
    depends_on('py-pillow@4.0.0:', when='^python@3.6', type=('build', 'run'))
    depends_on('py-pillow@3.2.0:', when='^python@3.5', type=('build', 'run'))
    depends_on('py-pillow@2.5.0:5.4.1', when='^python@3.4', type=('build', 'run'))
    depends_on('py-pillow@2.0.0:4.3.0', when='^python@3.3', type=('build', 'run'))
    depends_on('py-pillow@2.0.0:3.4.2', when='^python@3.2', type=('build', 'run'))
    depends_on('py-pillow@2.0.0:', when='^python@2.7', type=('build', 'run'))
    # depends_on('py-foo',        type=('build', 'run'))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
