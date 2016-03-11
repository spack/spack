from spack import *

class Octave(Package):
    """GNU Octave is a high-level language, primarily intended for numerical
    computations. It provides a convenient command line interface for solving
    linear and nonlinear problems numerically, and for performing other
    numerical experiments using a language that is mostly compatible with
    Matlab. It may also be used as a batch-oriented language."""

    homepage = "https://www.gnu.org/software/octave/"
    url      = "ftp://ftp.gnu.org/gnu/octave/octave-4.0.0.tar.gz"

    version('4.0.0' , 'a69f8320a4f20a8480c1b278b1adb799')

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
    variant('suiteparse', default=False)
    variant('zlib',       default=False)

    # Required dependencies
    depends_on('blas')
    depends_on('lapack')
    depends_on('pcre')

    # Strongly recommended dependencies
    depends_on('readline',    when='+readline')

    # Optional dependencies
    depends_on('arpack',      when='+arpack')
    depends_on('curl',        when='+curl')
    depends_on('fftw@3',      when='+fftw')
    depends_on('fltk',        when='+fltk')
    depends_on('fontconfig',  when='+fontconfig')
    depends_on('freetype',    when='+freetype')
    depends_on('glpk',        when='+glpk')
    depends_on('gl2ps',       when='+gl2ps')
    depends_on('gnuplot',     when='+gnuplot')
    depends_on('ImageMagick', when='+magick')
    depends_on('hdf5',        when='+hdf5')
    depends_on('jdk',         when='+jdk')
    depends_on('llvm',        when='+llvm')
    #depends_on('opengl',      when='+opengl')
    depends_on('qhull',       when='+qhull')
    depends_on('qrupdate',    when='+qrupdate')
    #depends_on('qscintilla',  when='+qscintilla)
    depends_on('qt',          when='+qt')
    depends_on('SuiteSparse', when='+suitesparse')
    depends_on('zlib',        when='+zlib')


    def install(self, spec, prefix):
        config_args = [
            "--prefix=%s" % prefix
        ]

        # Required dependencies
        config_args.extend([
            "--with-blas=%s"   % spec['blas'].prefix.lib,
            "--with-lapack=%s" % spec['lapack'].prefix.lib
        ])

        # Strongly recommended dependencies
        if '+readline' in spec:
            config_args.append('--enable-readline')
        else:
            config_args.append('--disable-readline')

        # Optional dependencies
        if '+arpack' in spec:
            config_args.extend([
                "--with-arpack-includedir=%s" % spec['arpack'].prefix.include,
                "--with-arpack-libdir=%s"     % spec['arpack'].prefix.lib
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
            config_args.append("--with-magick=%s" % spec['ImageMagick'].prefix.lib)

        if '+hdf5' in spec:
            config_args.extend([
                "--with-hdf5-includedir=%s" % spec['hdf5'].prefix.include,
                "--with-hdf5-libdir=%s"     % spec['hdf5'].prefix.lib
            ])
        else:
            config_args.append("--without-hdf5")

        if '+jdk' in spec:
            config_args.extend([
                "--with-java-homedir=%s"    % spec['jdk'].prefix,
                "--with-java-includedir=%s" % spec['jdk'].prefix.include,
                "--with-java-libdir=%s"     % spec['jdk'].prefix.lib
            ])

        #if '~opengl' in spec:
        #    config_args.extend([
        #        "--without-opengl",
        #        "--without-framework-opengl"
        #    ])

        if '+qhull' in spec:
            config_args.extend([
                "--with-qhull-includedir=%s" % spec['qhull'].prefix.include,
                "--with-qhull-libdir=%s"     % spec['qhull'].prefix.lib
            ])
        else:
            config_args.append("--without-qhull")

        if '+qrupdate' in spec:
            config_args.extend([
                "--with-qrupdate-includedir=%s" % spec['qrupdate'].prefix.include,
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

        configure(*config_args)

        make()
        make("install")
