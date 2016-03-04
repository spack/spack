from spack import *

class NetcdfFortran(Package):
    """Fortran interface for NetCDF4"""

    homepage = "http://www.unidata.ucar.edu/downloads/netcdf/netcdf-cxx/index.jsp"
    url      = "http://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-fortran-4.4.3.tar.gz"

    version('4.4.3', 'bfd4ae23a34635b273d3eb0d91cbde9e')

    variant('mpi', default=True, description='Enables MPI parallelism')

    depends_on('netcdf')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")




# netcdf-fortran configure parameters are below
# ---------------------------------------------
#
# `configure' configures netCDF-Fortran 4.4.3 to adapt to many kinds of systems.
# 
# Usage: ./configure [OPTION]... [VAR=VALUE]...
# 
# To assign environment variables (e.g., CC, CFLAGS...), specify them as
# VAR=VALUE.  See below for descriptions of some of the useful variables.
# 
# Defaults for the options are specified in brackets.
# 
# Configuration:
#   -h, --help              display this help and exit
#       --help=short        display options specific to this package
#       --help=recursive    display the short help of all the included packages
#   -V, --version           display version information and exit
#   -q, --quiet, --silent   do not print `checking ...' messages
#       --cache-file=FILE   cache test results in FILE [disabled]
#   -C, --config-cache      alias for `--cache-file=config.cache'
#   -n, --no-create         do not create output files
#       --srcdir=DIR        find the sources in DIR [configure dir or `..']
# 
# Installation directories:
#   --prefix=PREFIX         install architecture-independent files in PREFIX
#                           [/usr/local]
#   --exec-prefix=EPREFIX   install architecture-dependent files in EPREFIX
#                           [PREFIX]
# 
# By default, `make install' will install all the files in
# `/usr/local/bin', `/usr/local/lib' etc.  You can specify
# an installation prefix other than `/usr/local' using `--prefix',
# for instance `--prefix=$HOME'.
# 
# For better control, use the options below.
# 
# Fine tuning of the installation directories:
#   --bindir=DIR            user executables [EPREFIX/bin]
#   --sbindir=DIR           system admin executables [EPREFIX/sbin]
#   --libexecdir=DIR        program executables [EPREFIX/libexec]
#   --sysconfdir=DIR        read-only single-machine data [PREFIX/etc]
#   --sharedstatedir=DIR    modifiable architecture-independent data [PREFIX/com]
#   --localstatedir=DIR     modifiable single-machine data [PREFIX/var]
#   --libdir=DIR            object code libraries [EPREFIX/lib]
#   --includedir=DIR        C header files [PREFIX/include]
#   --oldincludedir=DIR     C header files for non-gcc [/usr/include]
#   --datarootdir=DIR       read-only arch.-independent data root [PREFIX/share]
#   --datadir=DIR           read-only architecture-independent data [DATAROOTDIR]
#   --infodir=DIR           info documentation [DATAROOTDIR/info]
#   --localedir=DIR         locale-dependent data [DATAROOTDIR/locale]
#   --mandir=DIR            man documentation [DATAROOTDIR/man]
#   --docdir=DIR            documentation root [DATAROOTDIR/doc/netcdf-fortran]
#   --htmldir=DIR           html documentation [DOCDIR]
#   --dvidir=DIR            dvi documentation [DOCDIR]
#   --pdfdir=DIR            pdf documentation [DOCDIR]
#   --psdir=DIR             ps documentation [DOCDIR]
# 
# Program names:
#   --program-prefix=PREFIX            prepend PREFIX to installed program names
#   --program-suffix=SUFFIX            append SUFFIX to installed program names
#   --program-transform-name=PROGRAM   run sed PROGRAM on installed program names
# 
# System types:
#   --build=BUILD     configure for building on BUILD [guessed]
#   --host=HOST       cross-compile to build programs to run on HOST [BUILD]
#   --target=TARGET   configure for building compilers for TARGET [HOST]
# 
# Optional Features:
#   --disable-option-checking  ignore unrecognized --enable/--with options
#   --disable-FEATURE       do not include FEATURE (same as --enable-FEATURE=no)
#   --enable-FEATURE[=ARG]  include FEATURE [ARG=yes]
#   --enable-silent-rules   less verbose build output (undo: "make V=1")
#   --disable-silent-rules  verbose build output (undo: "make V=0")
#   --enable-maintainer-mode
#                           enable make rules and dependencies not useful (and
#                           sometimes confusing) to the casual installer
#   --enable-valgrind-tests build with valgrind-tests (valgrind is required,
#                           static builds only)
#   --enable-parallel-tests Run extra parallel IO tests. Ignored if netCDF-4 is
#                           not enabled, or built on a system without parallel
#                           I/O support.
#   --enable-extra-tests    run some extra tests that may not pass because of
#                           known issues
#   --enable-doxygen        Enable generation of documentation with doxygen.
#   --enable-dot            Use dot (provided by graphviz) to generate charts
#                           and graphs in the doxygen-based documentation.
#   --enable-internal-docs  Include documentation of library internals. This is
#                           of interest only to those developing the netCDF
#                           library.
#   --enable-dependency-tracking
#                           do not reject slow dependency extractors
#   --disable-dependency-tracking
#                           speeds up one-time build
#   --disable-f03-compiler-check
#                           disable check of ISO_C_BINDING support in Fortran
#                           compiler
#   --disable-f03           suppress netCDF Fortran 2003 native code
#   --disable-fortran-type-check
#                           cause the Fortran type sizes checks to be skipped
#   --enable-large-file-tests
#                           Run tests which create very large data files (~13 GB
#                           disk space required, but it will be recovered when
#                           tests are complete). See option --with-temp-large to
#                           specify temporary directory
#   --enable-benchmarks     Run benchmarks. This is an experimental feature.
#   --enable-shared[=PKGS]  build shared libraries [default=yes]
#   --enable-static[=PKGS]  build static libraries [default=yes]
#   --enable-fast-install[=PKGS]
#                           optimize for fast installation [default=yes]
#   --disable-libtool-lock  avoid locking (might break parallel builds)
#   --disable-largefile     omit support for large files
#   --enable-extra-example-tests
#                           Run extra example tests; requires GNU sed. Ignored
#                           if netCDF-4 is not enabled.
#   --enable-dll            build a win32 DLL (only works on mingw)
# 
# Optional Packages:
#   --with-PACKAGE[=ARG]    use PACKAGE [ARG=yes]
#   --without-PACKAGE       do not use PACKAGE (same as --with-PACKAGE=no)
#   --with-temp-large=<directory>
#                           specify directory where large files (i.e. >2 GB)
#                           will be written, if large files tests are run with
#                           --enable-large-file-tests
#   --with-pic[=PKGS]       try to use only PIC/non-PIC objects [default=use
#                           both]
#   --with-gnu-ld           assume the C compiler uses GNU ld [default=no]
#   --with-sysroot=DIR Search for dependent libraries within DIR
#                         (or the compiler's sysroot if not specified).
# 
# Some influential environment variables:
#   CC          C compiler command
#   CFLAGS      C compiler flags
#   LDFLAGS     linker flags, e.g. -L<lib dir> if you have libraries in a
#               nonstandard directory <lib dir>
#   LIBS        libraries to pass to the linker, e.g. -l<library>
#   CPPFLAGS    (Objective) C/C++ preprocessor flags, e.g. -I<include dir> if
#               you have headers in a nonstandard directory <include dir>
#   FC          Fortran compiler command
#   FCFLAGS     Fortran compiler flags
#   F77         Fortran 77 compiler command
#   FFLAGS      Fortran 77 compiler flags
#   CPP         C preprocessor
# 
# Use these variables to override the choices made by `configure' or to help
# it to find libraries and programs with nonstandard names/locations.
# 
# Report bugs to <support-netcdf@unidata.ucar.edu>.
# 
# from spack import *
