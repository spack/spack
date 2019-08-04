# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyqt5(SIPPackage):
    """PyQt is a set of Python v2 and v3 bindings for The Qt Company's Qt
    application framework and runs on all platforms supported by Qt including
    Windows, OS X, Linux, iOS and Android. PyQt5 supports Qt v5."""

    homepage = "https://www.riverbankcomputing.com/software/pyqt/intro"
    url      = "https://www.riverbankcomputing.com/static/Downloads/PyQt5/5.13.0/PyQt5_gpl-5.13.0.tar.gz"
    list_url = "https://www.riverbankcomputing.com/software/pyqt/download5"
    import_modules = ['PyQt5']

    version('5.13.0', sha256='0cdbffe5135926527b61cc3692dd301cd0328dd87eeaf1313e610787c46faff9')

    depends_on('py-sip@4.19.14:')
    # Without opengl support, I got the following error:
    # sip: QOpenGLFramebufferObject is undefined
    depends_on('qt@5:+opengl')
    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-enum34', type=('build', 'run'), when='^python@:3.3')

    # https://www.riverbankcomputing.com/static/Docs/PyQt5/installation.html
    def configure_args(self):
        return ['--pyuic5-interpreter', self.spec['python'].command.path]
