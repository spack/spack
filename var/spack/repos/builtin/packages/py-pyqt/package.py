# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyqt(Package):
    """PyQt is a set of Python v2 and v3 bindings for Digia's Qt
       application framework and runs on all platforms supported by Qt
       including Windows, MacOS/X and Linux."""
    homepage = "http://www.riverbankcomputing.com/software/pyqt/intro"
    url      = "http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.3/PyQt-x11-gpl-4.11.3.tar.gz"

    version('4.11.3', '997c3e443165a89a559e0d96b061bf70')

    extends('python')
    depends_on('py-sip', type=('build', 'run'))

    # TODO: Fix version matching so that @4 works like @:4
    depends_on('qt@:4+phonon+dbus', when='@:4.99.99')
    depends_on('qt@5:+phonon+dbus', when='@5:')

    def url_for_version(self, version):
        """Handle version-based custom URLs."""
        url = 'http://sourceforge.net/projects/pyqt/files'
        if version.up_to(1).string <= '4': 
            return url + '/PyQt%s/PyQt-%s/PyQt-x11-gpl-%s.tar.gz' % (version.up_to(1), version, version)
        # url is different for 5.5.1 or less vs higher (note the '_' before 'gpl...')
        elif int(version.string.split('.')[1]) <= 5 and version.string != '5.5.1':
            return url + '/PyQt5/PyQt-%s/PyQt5-gpl-%s.tar.gz' % (version, version)
        else:
            return url + '/PyQt5/PyQt-%s/PyQt5_gpl-%s.tar.gz' % (version, version)


    def install(self, spec, prefix):
        python('configure.py',
               '--confirm-license',
               '--destdir=%s' % site_packages_dir)
        make()
        make('install')
