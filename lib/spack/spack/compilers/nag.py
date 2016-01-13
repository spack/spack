class Nag(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = []

    # Subclasses use possible names of C++ compiler
    cxx_names = []

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['nagfor']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['nagfor']

    @classmethod
    def default_version(self, comp):
        """The '-V' option works for nag compilers.
           Output looks like this::

               NAG Fortran Compiler Release 6.0(Hibiya) Build 1037
               Product NPL6A60NA for x86-64 Linux
               Copyright 1990-2015 The Numerical Algorithms Group Ltd., Oxford, U.K.
        """
        return get_compiler_version(
            comp, '-V', r'NAG Fortran Compiler Release ([0-9.]+)')
