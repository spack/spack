from spack import *

class Silo(Package):
    """Silo is a library for reading and writing a wide variety of scientific
       data to binary, disk files."""

    homepage = "http://wci.llnl.gov/simulation/computer-codes/silo"
    base_url = "https://wci.llnl.gov/content/assets/docs/simulation/computer-codes/silo"

    version('4.10.2', '9ceac777a2f2469ac8cef40f4fab49c8')
    version('4.9', 'a83eda4f06761a86726e918fc55e782a')
    version('4.8', 'b1cbc0e7ec435eb656dc4b53a23663c9')

    variant('fortran', default=True, description='Enable Fortran support')
    variant('silex', default=False, description='Builds Silex, a GUI for viewing Silo files')

    depends_on('hdf5')
    depends_on('qt', when='+silex')

    def install(self, spec, prefix):
        config_args = [
            '--enable-fortran' if '+fortran' in spec else '--disable-fortran',
            '--enable-silex' if '+silex' in spec else '--disable-silex',
        ]

        if '+silex' in spec:
            config_args.append('--with-Qt-dir=%s' % spec['qt'].prefix)

        configure(
            '--prefix=%s' % prefix,
            '--with-hdf5=%s,%s' % (spec['hdf5'].prefix.include, spec['hdf5'].prefix.lib),
            '--with-zlib=%s,%s' % (spec['zlib'].prefix.include, spec['zlib'].prefix.lib),
            *config_args)

        make()
        make('install')

    def url_for_version(self, version):
        return '%s/silo-%s/silo-%s.tar.gz' % (Silo.base_url, version, version)
