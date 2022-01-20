# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMouseinfo(PythonPackage):
    """An application to display XY position and RGB color
    information for the pixel currently under the mouse. Works
    on Python 2 and 3. This is useful for GUI automation
    planning."""

    homepage = "https://github.com/asweigart/mouseinfo"
    pypi     = "MouseInfo/MouseInfo-0.1.3.tar.gz"

    version('0.1.3', sha256='2c62fb8885062b8e520a3cce0a297c657adcc08c60952eb05bc8256ef6f7f6e7')

    depends_on('python@2.7,3.2:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    # rubicon-objc;platform_system=="Darwin"',
    # 'python3-Xlib;platform_system=="Linux" and python_version>="3.0"',
    # 'Xlib;platform_system=="Linux" and python_version<"3.0"',
    # Conflicting until rubicon-objc exists
    conflicts('platform=darwin')
    depends_on('py-python3-xlib', when='^python@3 platform=linux', type=('build', 'run'))
    depends_on('py-python-xlib',  when='^python@2 platform=linux', type=('build', 'run'))

    depends_on('py-pyperclip', type=('build', 'run'))
    depends_on('pil@5.2.0:', when='^python@3.7:', type=('build', 'run'))
    depends_on('pil@4.0.0:', when='^python@3.6', type=('build', 'run'))
    depends_on('pil@3.2.0:', when='^python@3.5', type=('build', 'run'))
    depends_on('pil@2.5.0:5.4.1', when='^python@3.4', type=('build', 'run'))
    depends_on('pil@2.0.0:4.3.0', when='^python@3.3', type=('build', 'run'))
    depends_on('pil@2.0.0:3.4.2', when='^python@3.2', type=('build', 'run'))
    depends_on('pil@2.0.0:', when='^python@2.7', type=('build', 'run'))
