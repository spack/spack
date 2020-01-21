# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWxpython(PythonPackage):
    """Cross platform GUI toolkit for Python."""

    homepage = "https://www.wxpython.org/"
    url      = "https://pypi.io/packages/source/w/wxPython/wxPython-4.0.6.tar.gz"

    import_modules = [
        'wx', 'wx.tools', 'wx.py', 'wx.lib', 'wx.lib.analogclock',
        'wx.lib.floatcanvas', 'wx.lib.plot', 'wx.lib.mixins', 'wx.lib.gizmos',
        'wx.lib.art', 'wx.lib.pdfviewer', 'wx.lib.colourchooser',
        'wx.lib.masked', 'wx.lib.ogl', 'wx.lib.wxcairo', 'wx.lib.agw',
        'wx.lib.pubsub', 'wx.lib.editor', 'wx.lib.analogclock.lib_setup',
        'wx.lib.floatcanvas.Utilities', 'wx.lib.plot.examples',
        'wx.lib.agw.aui', 'wx.lib.agw.ribbon', 'wx.lib.agw.persist',
        'wx.lib.pubsub.core', 'wx.lib.pubsub.utils', 'wx.lib.pubsub.core.arg1',
        'wx.lib.pubsub.core.kwargs'
    ]

    version('4.0.6', sha256='35cc8ae9dd5246e2c9861bb796026bbcb9fb083e4d49650f776622171ecdab37')

    depends_on('wxwidgets')

    # Needed for the build.py script
    depends_on('py-setuptools', type='build')
    depends_on('py-pathlib2', type='build')

    # Needed at runtime
    depends_on('py-numpy', type='run')
    depends_on('py-pillow', type='run')
    depends_on('py-six', type='run')
