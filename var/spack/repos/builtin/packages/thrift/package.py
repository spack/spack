from spack import *

class Thrift(Package):
    """The Apache Thrift software framework, for scalable cross-language services
    development, combines a software stack with a code generation engine to build
    services that work efficiently and seamlessly between C++, Java, Python, PHP,
    Ruby, Erlang, Perl, Haskell, C#, Cocoa, JavaScript, Node.js, Smalltalk, OCaml
     and Delphi and other languages."""

    homepage = "http://thrift.apache.org"
    url      = "http://apache.mirrors.ionfish.org/thrift/0.9.2/thrift-0.9.2.tar.gz"

    version('0.9.2', '89f63cc4d0100912f4a1f8a9dee63678')

    # Currently only support for c-family and python
    variant('c', default=True, description="Build support for C-family languages")
    variant('python', default=True, description="Build support for python")

    depends_on('jdk')
    depends_on('autoconf')
    depends_on('automake')
    depends_on('libtool')
    depends_on('boost@1.53:')
    depends_on('bison')
    depends_on('flex')
    depends_on('openssl')

    # Variant dependencies
    extends('python', when='+python')

    depends_on('zlib', when='+c')
    depends_on('libevent', when='+c')

    def install(self, spec, prefix):
        env['PY_PREFIX'] = prefix
        env['JAVA_HOME'] = spec['jdk'].prefix

        # configure options
        options = ['--prefix=%s' % prefix]

        options.append('--with-boost=%s' % spec['boost'].prefix)
        options.append('--enable-tests=no')

        options.append('--with-c=%s' % ('yes' if '+c' in spec else 'no'))
        options.append('--with-python=%s' % ('yes' if '+python' in spec else 'no'))
        options.append('--with-java=%s' % ('yes' if '+java' in spec else 'no'))
        options.append('--with-go=%s' % ('yes' if '+go' in spec else 'no'))
        options.append('--with-lua=%s' % ('yes' if '+lua' in spec else 'no'))
        options.append('--with-php=%s' % ('yes' if '+php' in spec else 'no'))
        options.append('--with-qt4=%s' % ('yes' if '+qt4' in spec else 'no'))

        configure(*options)

        make()
        make("install")
