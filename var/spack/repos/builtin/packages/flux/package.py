from spack import *
import os

class Flux(Package):
    """ A next-generation resource manager (pre-alpha) """

    homepage = "https://github.com/flux-framework/flux-core"
    url      = "https://github.com/flux-framework/flux-core"

    version('master', branch='master', git='https://github.com/flux-framework/flux-core')

    # Also needs autotools, but should use the system version if available
    depends_on("zeromq@4.0.4:")
    depends_on("czmq@2.2:")
    depends_on("hwloc")
    depends_on("lua@5.1:5.1.99")
    depends_on("munge")
    depends_on("libjson-c")
    depends_on("libxslt")
    depends_on("python")
    depends_on("py-cffi")

    # TODO: This provides a catalog, hacked with environment below for now
    depends_on("docbook-xml")
    depends_on("asciidoc")

    def install(self, spec, prefix):
        # Bootstrap with autotools
        bash = which('bash')
        bash('./autogen.sh')
        bash('./autogen.sh') #yes, twice, intentionally

        # Fix asciidoc dependency on xml style sheets and whatnot
        os.environ['XML_CATALOG_FILES'] = os.path.join(spec['docbook-xml'].prefix,
                                                       'catalog.xml')
        # Configure, compile & install
        configure("--prefix=" + prefix)
        make("install", "V=1")

