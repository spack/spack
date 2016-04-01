from spack import *
import os

class Nag(Package):
    """The NAG Fortran Compiler."""
    homepage = "http://www.nag.com/nagware/np.asp"

    version('6.1', '1e29d9d435b7ccc2842a320150b28ba4',
            url='http://www.nag.com/downloads/impl/npl6a61na_amd64.tgz')

    # Licensing
    license_required = True
    license_files    = ['lib/nag.key',
                        'lib/nag.licence',
                        'lib/nagware.licence']
    license_vars     = ['NAG_KUSARI_FILE']
    license_url      = 'http://www.nag.com/doc/inun/np61/lin-mac/klicence.txt'

    def install(self, spec, prefix):
        # Set installation directories
        os.environ['INSTALL_TO_BINDIR'] = prefix.bin
        os.environ['INSTALL_TO_LIBDIR'] = prefix.lib
        os.environ['INSTALL_TO_MANDIR'] = prefix + '/share/man/man'

        # Run install script
        os.system('./INSTALLU.sh')
