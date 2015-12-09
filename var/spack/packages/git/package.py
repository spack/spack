from spack import *

class Git(Package):
    """Git is a free and open source distributed version control
       system designed to handle everything from small to very large
       projects with speed and efficiency."""
    homepage = "http://git-scm.com"
    url      = "https://www.kernel.org/pub/software/scm/git/git-2.2.1.tar.xz"

    version('2.6.3', '5a6375349c3f13c8dbbabfc327bae429')
    version('2.6.2', '32ae5ad29763fc927bfcaeab55385fd9')
    version('2.6.1', 'dd4a3a7fe96598c553edd39d40c9c290')
    version('2.6.0', '6b7d43d615fb3f0dfecf4d131e23f438')
    version('2.5.4', 'ec118fcd1cf984edc17eb6588b78e81b')
    version('2.2.1', '43e01f9d96ba8c11611e0eef0d9f9f28')


    # Git compiles with curl support by default on but if your system
    # does not have it you will not be able to clone https repos
    variant("curl", default=False, description="Add the internal support of curl for https clone")

    # Git compiles with expat support by default on but if your system
    # does not have it you will not be able to push https repos
    variant("expat", default=False, description="Add the internal support of expat for https push")

    depends_on("openssl")
    depends_on("curl", when="+curl")
    depends_on("expat", when="+expat")

    # Use system perl for now.
    # depends_on("perl")
    # depends_on("pcre")

    depends_on("zlib")

    def install(self, spec, prefix):
        configure_args = [
            "--prefix=%s" % prefix,
            "--without-pcre",
            "--with-openssl=%s" % spec['openssl'].prefix,
            "--with-zlib=%s" % spec['zlib'].prefix
            ]

        if '+curl' in spec:
            configure_args.append("--with-curl=%s" % spec['curl'].prefix)

        if '+expat' in spec:
            configure_args.append("--with-expat=%s" % spec['expat'].prefix)

        configure(*configure_args)
        make()
        make("install")







