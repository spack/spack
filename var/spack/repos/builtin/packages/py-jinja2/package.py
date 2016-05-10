from spack import *

class PyJinja2(Package):
    """
    Jinja2 is a template engine written in pure Python. It provides
    a Django inspired non-XML syntax but supports inline expressions 
    and an optional sandboxed environment.
    """

    homepage = "http://jinja.pocoo.org/"
    url      = "https://github.com/pallets/jinja/archive/2.8.tar.gz"

    version('2.8'  , '4114200650d7630594e3bc70af23f59e')
    version('2.7.3', '55b87bdc8e585b8b5b86734eefce2621')
    version('2.7.2', '8e8f226809ae6363009b9296e30adf30')
    version('2.7.1', '69b6675553c81b1087f95cae7f2179bb')
    version('2.7'  , 'ec70433f325051dcedacbb2465028a35')

    extends("python")
    depends_on("py-setuptools")
    depends_on("py-markupsafe")
    
    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)

