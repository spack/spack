from spack import *

class Intltool(Package):
    """intltool is a set of tools to centralize translation of many different file formats using GNU gettext-compatible PO files."""
    homepage  = 'https://freedesktop.org/wiki/Software/intltool/'

    version('0.51.0',    '12e517cac2b57a0121cda351570f1e63')

    def url_for_version(self, version):
        """Handle version-based custom URLs."""
        return 'https://launchpad.net/intltool/trunk/%s/+download/intltool-%s.tar.gz' % (version, version)

    def install(self, spec, prefix):

        # configure, build, install:
        options = ['--prefix=%s' % prefix ]
        configure(*options)
        make()
        make('install')
