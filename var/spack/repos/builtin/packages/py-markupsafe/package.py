from spack import *

class PyMarkupsafe(Package):
    """
    MarkupSafe is a library for Python that implements a unicode 
    string that is aware of HTML escaping rules and can be used 
    to implement automatic string escaping. It is used by Jinja 2,
    the Mako templating engine, the Pylons web framework and many more.
    """
    
    homepage = "http://www.pocoo.org/projects/markupsafe/"
    url      = "https://github.com/pallets/markupsafe/archive/0.23.tar.gz"

    version('0.23', '1a0dadc95169832367c9dcf142155cde')
    version('0.22', '7a2ac7427b58def567628d06dc328396')
    version('0.21', 'aebcd93ee05269773c8b80bb6c86fc2f')
    version('0.20', '0c1fef97c8fd6a986d708f08d7f84a02')
    version('0.19', '64b05361adb92c11839fc470e308c593')

    extends("python")
    depends_on("py-setuptools")

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)

