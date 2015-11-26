from spack import *
import os

class Lua(Package):
    """ The Lua programming language interpreter and library """
    homepage = "http://www.lua.org"
    url      = "http://www.lua.org/ftp/lua-5.1.5.tar.gz"

    version('5.3.1', '797adacada8d85761c079390ff1d9961')
    version('5.3.0', 'a1b0a7e92d0c85bbff7a8d27bf29f8af')
    version('5.2.4', '913fdb32207046b273fdb17aad70be13')
    version('5.2.3', 'dc7f94ec6ff15c985d2d6ad0f1b35654')
    version('5.2.2', 'efbb645e897eae37cad4344ce8b0a614')
    version('5.2.1', 'ae08f641b45d737d12d30291a5e5f6e3')
    version('5.2.0', 'f1ea831f397214bae8a265995ab1a93e')
    version('5.1.5', '2e115fe26e435e33b0d5c022e4490567')
    version('5.1.4', 'd0870f2de55d59c1c8419f36e8fac150')
    version('5.1.3', 'a70a8dfaa150e047866dc01a46272599')

    depends_on('ncurses')

    def install(self, spec, prefix):
        make('INSTALL_TOP=%s' % prefix,
             'MYLDFLAGS=-L%s/lib' % spec['ncurses'].prefix,
             'linux',
             'install')
