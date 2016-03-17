from spack import *

class Luarocks(Package):
    """LuaRocks is the package manager for Lua modules"""
    homepage = "http://luarocks.org"
    url      = "http://luarocks.org/releases/luarocks-2.2.2.tar.gz"

    version('2.3.0', 'a38126684cf42b7d0e7a3c7cf485defb')
    version('2.2.2', '5a830953d27715cc955119609f8096e6')
    version('2.2.1', '718a0e8c257aace3ec16ebc2cfe9c696')
    version('2.2.0', 'eb142e0f0891ea4243ef3b7582cfbbaa')
    version('2.1.2', '0afc5fd6ee6ec6128fccda1bc559f41e')

    depends_on("lua")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)
        make("bootstrap")

        # luarocks = which("luarocks")
        # luarocks("install", "posix")
        # luarocks("install", "lfs")
