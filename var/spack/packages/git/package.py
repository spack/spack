from spack import *

class Git(Package):
    """Git is a free and open source distributed version control
       system designed to handle everything from small to very large
       projects with speed and efficiency."""
    homepage = "http://git-scm.com"
    url      = "https://www.kernel.org/pub/software/scm/git/git-2.2.1.tar.xz"

    version('2.2.1', '43e01f9d96ba8c11611e0eef0d9f9f28')

    # Use system openssl.
    # depends_on("openssl")

    # Use system perl for now.
    # depends_on("perl")
    # depends_on("pcre")

    depends_on("zlib")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--without-pcre",
                  "--without-python")

        make()
        make("install")
