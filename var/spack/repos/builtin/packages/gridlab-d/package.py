# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
#     spack install gridlab-d
#
# You can edit this file again by typing:
#
#     spack edit gridlab-d
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class GridlabD(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://www.gridlabd.org/"
    git      = "https://github.com/gridlab-d/gridlab-d"

    maintainers = ['0t1s1', 'yee29', 'afisher1']

    # Using only develop as other branches and releases did not build properly.
    version('develop', branch='develop')

    variant("mysql", default=False, description="Enable MySQL support for Gridlab-D.")
    variant('helics', default=False, description='Enable Helics support for Gridlab-D.')

    # Add dependencies.
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on("xerces-c")
    depends_on("superlu-mt")
    depends_on('helics', when='+helics')

    def configure_args(self):
        args = []

        if '+helics' in self.spec:
            # Taken from https://github.com/GMLC-TDC/HELICS-Tutorial/tree/master/setup
            args.append('--with-helics=' + self.spec['helics'].prefix)
            args.append('CFLAGS=-g -O0 -w')
            args.append('CXXFLAGS=-g -O0 -w -std=c++14')
            args.append('LDFLAGS=-g -O0 -w')

        return args

    def setup_run_environment(self, env):
        # Need to add GLPATH otherwise Gridlab-D will not run.
        env.set('GLPATH', join_path(self.prefix, 'lib', 'gridlabd'))
        env.prepend_path('GLPATH', join_path(self.prefix, 'share', 'gridlabd'))
