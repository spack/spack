##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import sys


class Octave(AutotoolsPackage):
    """GNU Octave is a high-level language, primarily intended for numerical
    computations. It provides a convenient command line interface for solving
    linear and nonlinear problems numerically, and for performing other
    numerical experiments using a language that is mostly compatible with
    Matlab. It may also be used as a batch-oriented language."""

    homepage = "https://www.gnu.org/software/octave/"
    url      = "https://ftpmirror.gnu.org/octave/octave-4.0.0.tar.gz"

    extendable = True

    version('4.2.1', '80c28f6398576b50faca0e602defb9598d6f7308b0903724442c2a35a605333b')
    version('4.2.0', '443ba73782f3531c94bcf016f2f0362a58e186ddb8269af7dcce973562795567')
    version('4.0.2', 'c2a5cacc6e4c52f924739cdf22c2c687')
    version('4.0.0', 'a69f8320a4f20a8480c1b278b1adb799')

    # patches
    # see https://savannah.gnu.org/bugs/?50234
    patch('patch_4.2.1_inline.diff', when='@4.2.1')

    # Variants
    variant('readline',   default=True)
    variant('arpack',     default=False)
    variant('curl',       default=False)
    variant('fftw',       default=False)
    variant('fltk',       default=False)
    variant('fontconfig', default=False)
    variant('freetype',   default=False)
    variant('glpk',       default=False)
    variant('gl2ps',      default=False)
    variant('gnuplot',    default=False)
    variant('magick',     default=False)
    variant('hdf5',       default=False)
    variant('jdk',        default=False)
    variant('llvm',       default=False)
    variant('opengl',     default=False)
    variant('qhull',      default=False)
    variant('qrupdate',   default=False)
    variant('qscintilla', default=False)
    variant('qt',         default=False)
    variant('suitesparse', default=False)
    variant('zlib',       default=False)

    # Required dependencies
    depends_on('blas')
    depends_on('lapack')
    # Octave does not configure with sed from darwin:
    depends_on('sed', when=sys.platform == 'darwin', type='build')
    depends_on('pcre')
    depends_on('pkgconfig', type='build')

    # Strongly recommended dependencies
    depends_on('readline',     when='+readline')

    # Optional dependencies
    depends_on('arpack-ng',    when='+arpack')
    depends_on('curl',         when='+curl')
    depends_on('fftw',         when='+fftw')
    depends_on('fltk',         when='+fltk')
    depends_on('fontconfig',   when='+fontconfig')
    depends_on('freetype',     when='+freetype')
    depends_on('glpk',         when='+glpk')
    depends_on('gl2ps',        when='+gl2ps')
    depends_on('gnuplot',      when='+gnuplot')
    depends_on('image-magick',  when='+magick')
    depends_on('hdf5',         when='+hdf5')
    depends_on('java',          when='+jdk')        # TODO: requires Java 6 ?
    depends_on('llvm',         when='+llvm')
    # depends_on('opengl',      when='+opengl')    # TODO: add package
    depends_on('qhull',        when='+qhull')
    depends_on('qrupdate',     when='+qrupdate')
    # depends_on('qscintilla',  when='+qscintilla) # TODO: add package
    depends_on('qt+opengl',    when='+qt')
    depends_on('suite-sparse', when='+suitesparse')
    depends_on('zlib',         when='+zlib')

    def configure_args(self):
        # See
        # https://github.com/macports/macports-ports/blob/master/math/octave/
        # https://github.com/Homebrew/homebrew-science/blob/master/octave.rb

        spec = self.spec
        config_args = []

        # Required dependencies
        config_args.extend([
            "--with-blas=%s" % spec['blas'].libs.ld_flags,
            "--with-lapack=%s" % spec['lapack'].libs.ld_flags
        ])

        # Strongly recommended dependencies
        if '+readline' in spec:
            config_args.append('--enable-readline')
        else:
            config_args.append('--disable-readline')

        # Optional dependencies
        if '+arpack' in spec:
            sa = spec['arpack-ng']
            config_args.extend([
                "--with-arpack-includedir=%s" % sa.prefix.include,
                "--with-arpack-libdir=%s"     % sa.prefix.lib
            ])
        else:
            config_args.append("--without-arpack")

        if '+curl' in spec:
            config_args.extend([
                "--with-curl-includedir=%s" % spec['curl'].prefix.include,
                "--with-curl-libdir=%s"     % spec['curl'].prefix.lib
            ])
        else:
            config_args.append("--without-curl")

        if '+fftw' in spec:
            config_args.extend([
                "--with-fftw3-includedir=%s"  % spec['fftw'].prefix.include,
                "--with-fftw3-libdir=%s"      % spec['fftw'].prefix.lib,
                "--with-fftw3f-includedir=%s" % spec['fftw'].prefix.include,
                "--with-fftw3f-libdir=%s"     % spec['fftw'].prefix.lib
            ])
        else:
            config_args.extend([
                "--without-fftw3",
                "--without-fftw3f"
            ])

        if '+fltk' in spec:
            config_args.extend([
                "--with-fltk-prefix=%s"      % spec['fltk'].prefix,
                "--with-fltk-exec-prefix=%s" % spec['fltk'].prefix
            ])
        else:
            config_args.append("--without-fltk")

        if '+glpk' in spec:
            config_args.extend([
                "--with-glpk-includedir=%s" % spec['glpk'].prefix.include,
                "--with-glpk-libdir=%s"     % spec['glpk'].prefix.lib
            ])
        else:
            config_args.append("--without-glpk")

        if '+magick' in spec:
            config_args.append("--with-magick=%s"
                               % spec['image-magick'].prefix.lib)
        else:
            config_args.append("--without-magick")

        if '+hdf5' in spec:
            config_args.extend([
                "--with-hdf5-includedir=%s" % spec['hdf5'].prefix.include,
                "--with-hdf5-libdir=%s"     % spec['hdf5'].prefix.lib
            ])
        else:
            config_args.append("--without-hdf5")

        if '+jdk' in spec:
            config_args.extend([
                "--with-java-homedir=%s"    % spec['java'].home,
                "--with-java-includedir=%s" % spec['java'].home.include,
                "--with-java-libdir=%s"     % spec['java'].libs.directories[0]
            ])
        else:
            config_args.append("--disable-java")

        if '~opengl' in spec:
            config_args.extend([
                "--without-opengl",
                "--without-framework-opengl"
            ])
        # TODO:  opengl dependency and package is missing?

        if '+qhull' in spec:
            config_args.extend([
                "--with-qhull-includedir=%s" % spec['qhull'].prefix.include,
                "--with-qhull-libdir=%s"     % spec['qhull'].prefix.lib
            ])
        else:
            config_args.append("--without-qhull")

        if '+qrupdate' in spec:
            config_args.extend([
                "--with-qrupdate-includedir=%s"
                % spec['qrupdate'].prefix.include,
                "--with-qrupdate-libdir=%s"     % spec['qrupdate'].prefix.lib
            ])
        else:
            config_args.append("--without-qrupdate")

        if '+zlib' in spec:
            config_args.extend([
                "--with-z-includedir=%s" % spec['zlib'].prefix.include,
                "--with-z-libdir=%s"     % spec['zlib'].prefix.lib
            ])
        else:
            config_args.append("--without-z")

        return config_args

    # ========================================================================
    # Set up environment to make install easy for Octave extensions.
    # ========================================================================

    def setup_dependent_package(self, module, dependent_spec):
        """Called before Octave modules' install() methods.

        In most cases, extensions will only need to have one line:
            octave('--eval', 'pkg install %s' % self.stage.archive_file)
        """
        # Octave extension builds can have a global Octave executable function
        module.octave = Executable(join_path(self.spec.prefix.bin, 'octave'))
