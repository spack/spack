from spack import *

class Git(Package):
    """Git is a free and open source distributed version control
       system designed to handle everything from small to very large
       projects with speed and efficiency."""
    homepage = "http://git-scm.com"
    url      = "https://www.kernel.org/pub/software/scm/git/git-2.2.1.tar.gz"

    version('2.6.3', 'b711be7628a4a2c25f38d859ee81b423')
    version('2.6.2', 'da293290da69f45a86a311ad3cd43dc8')
    version('2.6.1', '4c62ee9c5991fe93d99cf2a6b68397fd')
    version('2.6.0', 'eb76a07148d94802a1745d759716a57e')
    version('2.5.4', '3eca2390cf1fa698b48e2a233563a76b')
    version('2.2.1', 'ff41fdb094eed1ec430aed8ee9b9849c')


    # Git compiles with curl support by default on but if your system
    # does not have it you will not be able to clone https repos
    variant("curl", default=False, description="Add the internal support of curl for https clone")

    # Git compiles with expat support by default on but if your system
    # does not have it you will not be able to push https repos
    variant("expat", default=False, description="Add the internal support of expat for https push")

#    depends_on("openssl")
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
#            "--with-openssl=%s" % spec['openssl'].prefix,
            "--with-zlib=%s" % spec['zlib'].prefix
            ]

        if '+curl' in spec:
            configure_args.append("--with-curl=%s" % spec['curl'].prefix)

        if '+expat' in spec:
            configure_args.append("--with-expat=%s" % spec['expat'].prefix)

        configure(*configure_args)
        make()
        make("install")







