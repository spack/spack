from spack import *

class Icedtea(Package):
    """The IcedTea project provides a harness to build the source code from
       http://openjdk.java.net using Free Software build tools and adds a number
       of key features to the upstream OpenJDK codebase."""

    homepage = "http://icedtea.classpath.org"
    url = "http://icedtea.wildebeest.org/download/source/icedtea-3.2.0.tar.xz"

    version('3.2.0', 'f2a197734cc1f820f14a6ba0aef0f198c24c77e9f026d14ddf185b684b178f80')

    resource(name='corba', placement='spack-resource/corba',
             md5='19a12dc608da61a6878f4614a91156af',
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.2.0/corba.tar.xz')
    resource(name='hotspot', placement='spack-resource/hotspot',
             md5='cc5f423ed2949ee8a7e25d43f0cb425f',
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.2.0/hotspot.tar.xz')
    resource(name='jaxp', placement='spack-resource/jaxp',
             md5='8b1171ec1060517fc1c4eee162c78b33',
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.2.0/jaxp.tar.xz')
    resource(name='jaxws', placement='spack-resource/jaxws',
             md5='ca6bbcdb0f87399bd0a5481ad55939c8',
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.2.0/jaxws.tar.xz')
    resource(name='jdk', placement='spack-resource/jdk',
             md5='5f5d90b7036f1e8561f6943308528e80',
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.2.0/jdk.tar.xz')
    resource(name='langtools', placement='spack-resource/langtools',
             md5='9d105ca8e4de3936fe1a4916ec30ad7f',
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.2.0/langtools.tar.xz')
    resource(name='nashorn', placement='spack-resource/nashorn',
             md5='05fa4f0110a5c9c18828a3e359b1adde',
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.2.0/nashorn.tar.xz')
    resource(name='openjdk', placement='spack-resource/openjdk',
             md5='c7a7681fff0afda6a897b135820a1440',
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.2.0/openjdk.tar.xz')
    resource(name='shenandoah', placement='spack-resource/shenandoah',
             md5='1c42ff1802a6f10645a3e76b7d6fe9da',
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.2.0/shenandoah.tar.xz')

    depends_on('wget')
    depends_on('gawk')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  '--with-corba-src-zip=%s'      % self.stage[1].archive_file,
                  '--with-corba-checksum=no',
                  '--with-hotspot-src-zip=%s'    % self.stage[2].archive_file,
                  '--with-hotspot-checksum=no',
                  '--with-jaxp-src-zip=%s'       % self.stage[3].archive_file,
                  '--with-jaxp-checksum=no',
                  '--with-jaxws-src-zip=%s'      % self.stage[4].archive_file,
                  '--with-jaxws-checksum=no',
                  '--with-jdk-src-zip=%s'        % self.stage[5].archive_file,
                  '--with-jdk-checksum=no',
                  '--with-langtools-src-zip=%s'  % self.stage[6].archive_file,
                  '--with-langtools-checksum=no',
                  '--with-nashorn-src-zip=%s'    % self.stage[7].archive_file,
                  '--with-nashorn-checksum=no',
                  '--with-openjdk-src-zip=%s'    % self.stage[8].archive_file,
                  '--with-openjdk-checksum=no',
                  '--with-shenandoah-src-zip=%s' % self.stage[9].archive_file,
                  '--with-shenandoah-checksum=no')

        make()
        make("install")
