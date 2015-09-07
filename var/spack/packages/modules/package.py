#------------------------------------------------------------------------------
# Author: Justin Too <justin@doubleotoo.com>
# Date: September 6, 2015
#------------------------------------------------------------------------------

from spack import *

import os

class Modules(Package):
    """The Environment Modules package provides for the dynamic modification
       of a user's environment via modulefiles."""
    homepage = "http://modules.sourceforge.net/"
    url      = "http://sourceforge.net/projects/modules/files/Modules/modules-3.2.10/modules-3.2.10.tar.gz/download"

    version('3.2.10', '8b097fdcb90c514d7540bb55a3cb90fb')

    depends_on("tcl@8.6.4: +threads")

    # TODO: Add tclx package
    #depends_on("tclx@8.4.1: +threads")

    def install(self, spec, prefix):
        tcl  = spec['tcl']
        #tclx = spec['tclx']

        os.environ['CPPFLAGS'] = "-DUSE_INTERP_ERRORLINE"
        configure('--prefix=%s' % prefix,
            '--with-tcl-lib=%s/lib' % tcl.prefix,
            '--with-tcl-inc=%s/include' % tcl.prefix,
            '--with-tcl-ver=8.6',
            '--without-tclx',
            # Modules' autoconf requires this option T_T
            '--with-tclx-ver=8.4')
        #configure('--prefix=%s' % prefix,
        #    '--with-tcl-lib=%s/lib' % tcl.prefix,
        #    '--with-tcl-inc=%s/include' % tcl.prefix,
        #    '--with-tcl-ver=8.6',
        #    '--with-tclx-lib=%s/lib' % tcl.prefix,
        #    '--with-tclx-inc=%s/include' % tcl.prefix,
        #    '--with-tclx-ver=8.4')

        make()
        make("install")
