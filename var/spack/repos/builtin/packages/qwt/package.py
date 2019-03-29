# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Qwt(QMakePackage):
    """The Qwt library contains GUI Components and utility classes which are
    primarily useful for programs with a technical background. Beside a
    framework for 2D plots it provides scales, sliders, dials, compasses,
    thermometers, wheels and knobs to control or display values, arrays, or
    ranges of type double.
    """
    homepage = "http://qwt.sourceforge.net/"
    url      = "https://sourceforge.net/projects/qwt/files/qwt/6.1.3/qwt-6.1.3.tar.bz2"

    version('6.1.3', '19d1f5fa5e22054d22ee3accc37c54ba')
    version('5.2.2', '70d77e4008a6cc86763737f0f24726ca')

    variant('designer', default=False,
            description="Build extensions to QT designer")

    patch('no-designer.patch', when='~designer')

    depends_on('qt+opengl')
    depends_on('qt+tools', when='+designer')
    # Qwt 6.1.1 and older use a constant that was removed in Qt 5.4
    # https://bugs.launchpad.net/ubuntu/+source/qwt-qt5/+bug/1485213
    depends_on('qt@:5.3', when='@:6.1.1')

    def patch(self):
        # Subvert hardcoded prefix
        filter_file(r'/usr/local/qwt-\$\$(QWT_)?VERSION.*',
                    self.prefix, 'qwtconfig.pri')
