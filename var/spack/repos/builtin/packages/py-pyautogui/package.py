# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyautogui(PythonPackage):
    """PyAutoGUI lets your Python scripts control the mouse and
    keyboard to automate interactions with other
    applications."""

    homepage = "https://pyautogui.readthedocs.io/en/latest/"
    pypi     = "PyAutoGUI/PyAutoGUI-0.9.52.tar.gz"

    version('0.9.52', sha256='a486cb6b818bcbcdf98b48d010c7cee964134fa394b756e8ce6e50d43b58ecc8')

    depends_on('py-setuptools', type='build')
    depends_on('py-pymsgbox', type=('build', 'run'))
    depends_on('py-pytweening@1.0.1:', type=('build', 'run'))
    depends_on('py-pyscreeze@0.1.21:', type=('build', 'run'))
    depends_on('py-pygetwindow@0.0.5:', type=('build', 'run'))
    depends_on('py-mouseinfo', type=('build', 'run'))

    depends_on('py-python3-xlib', when='^python@3: platform=linux', type=('build', 'run'))
    depends_on('py-python-xlib', when='^python@:2 platform=linux', type=('build', 'run'))

    # Missing packages; commented out for now
    # depends_on('py-pyobjc-core', when='platform=darwin', type=('build', 'run'))
    # depends_on('py-pyobjc', when='platform=darwin', type=('build', 'run'))
    conflicts('platform=darwin')
