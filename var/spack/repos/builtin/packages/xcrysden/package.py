# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xcrysden(MakefilePackage):
    """a crystalline and molecular structure visualisation program
    aiming at display of isosurfaces and contours,
    which can be superimposed on crystalline structures
    and interactively rotated and manipulated."""

    homepage = "http://www.xcrysden.org"
    url      = homepage + "/download/xcrysden-1.6.2.tar.gz"

    version('1.6.2', sha256='811736ee598bec1a5b427fd10e4e063a30dd7cadae96a43a50b36ce90a4f503f')

    depends_on('tcl', type=('build', 'link', 'run'))
    depends_on('tk', type=('build', 'link', 'run'))
    depends_on('tcl-bwidget', type=('build', 'link', 'run'))
    depends_on('mesa', type=('build', 'link'))
    depends_on('mesa-glu', type=('build', 'link'))
    depends_on('fftw', type=('build', 'link'))
    depends_on('togl', type=('build', 'link'))

    parallel = False

    def setup_run_environment(self, env):
        env.set('XCRYSDEN_TOPDIR', join_path(self.prefix,
                'share', '-'.join([self.name, str(self.version)])))

        env.set('XCRYSDEN_SCRATCH', join_path('/', 'tmp', self.name))

    def edit(self, spec, prefix):
        copy('system/Make.sys-shared', 'Make.sys')

        # Otherwise it will download and install its own copy of bwidget
        remove_linked_tree(join_path(self.stage.source_path, 'external'))

        libs = {}
        incs = {}
        make_libs = {}
        make_incs = {}
        deps = ['tcl', 'tk', 'mesa-glu', 'fftw']

        make_libs['tcl'] = 'TCL_LIB'
        make_libs['tk'] = 'TK_LIB'
        make_libs['togl'] = 'TOGL_LIB'
        make_libs['mesa'] = 'GL_LIB'
        make_libs['mesa-glu'] = 'GLU_LIB'
        make_libs['fftw'] = 'FFTW3_LIB'
        make_libs['x11'] = 'X_LIB'

        make_incs['tcl'] = 'TCL_INCDIR'
        make_incs['tk'] = 'TK_INCDIR'
        make_incs['togl'] = 'TOGL_INCDIR'
        make_incs['mesa'] = 'GL_INCDIR'
        make_incs['fftw'] = 'FFTW3_INCDIR'

        for d in deps:
            libs[d] = spec[d].libs.ld_flags
            incs[d] = spec[d].headers.cpp_flags

        # These libraries' recipes do not have a '@libs' property :/
        xmulibs = find_libraries('libXmu', spec['libxmu'].prefix.lib)
        togllibs = find_libraries(
            'libTogl{0}'.format(spec['togl'].version.up_to(2)),
            spec['togl'].prefix.lib, recursive=True
        )
        mesalibs = find_libraries('libGL', spec['mesa'].prefix.lib)

        libs['libx11'] = (spec['libx11'].libs + xmulibs).ld_flags
        libs['togl'] = togllibs.ld_flags
        libs['mesa'] = mesalibs.ld_flags

        xmuincs = find_headers('Xmu', spec['libxmu'].prefix.include,
                               recursive=True)
        toglincs = find_headers('togl', spec['togl'].prefix.include,
                                recursive=True)
        mesaincs = find_headers('gl', spec['mesa'].prefix.include,
                                recursive=True)

        incs['libxmu'] = xmuincs.cpp_flags
        incs['togl'] = toglincs.cpp_flags
        incs['mesa'] = mesaincs.cpp_flags

        makesys = FileFilter('Make.sys')

        for key in make_libs.keys() or key in make_incs.keys():
            if key in libs.keys() and key in make_libs.keys():
                makesys.filter(
                    ''.join(['^', '{0}'.format(make_libs[key]), '.*$']),
                    '='.join([make_libs[key], libs[key]])
                )

            if key in incs.keys() and key in make_incs.keys():
                makesys.filter(
                    ''.join(['^', '{0}'.format(make_incs[key]), '.*$']),
                    '='.join([make_incs[key], incs[key]])
                )

    def install(self, spec, prefix):
        make('bindir', 'src-C', 'src-F', 'src-Tcl')

        make('install', 'prefix={0}'.format(prefix))
