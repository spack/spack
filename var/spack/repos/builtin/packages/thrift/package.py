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

    extends("python")

    depends_on("autoconf")
    depends_on("automake")
    depends_on("bison")
    depends_on("boost")
    depends_on("flex")
    depends_on("jdk")
    depends_on("libtool")
    depends_on("openssl")
    depends_on("python")

    # Compilation fails for most languages, fortunately cpp installs fine
    # All other languages (yes, including C) are omitted until someone needs them
    def install(self, spec, prefix):
        env["PY_PREFIX"]   = prefix
        env["JAVA_PREFIX"] = prefix

        configure("--prefix=%s" % prefix,
                  "--with-boost=%s" % spec['boost'].prefix,
                  "--with-c=no",
                  "--with-go=no",
                  "--with-python=yes",
                  "--with-lua=no",
                  "--with-php=no",
                  "--with-qt4=no",
                  "--enable-tests=no")

        make()
        make("install")
