from spack import *
import os

class Lmod(Package):
    """
    Lmod is a Lua based module system that easily handles the MODULEPATH
    Hierarchical problem. Environment Modules provide a convenient way to
    dynamically change the users' environment through modulefiles. This
    includes easily adding or removing directories to the PATH environment
    variable. Modulefiles for Library packages provide environment variables
    that specify where the library and header files can be found.
    """
    homepage = "https://www.tacc.utexas.edu/research-development/tacc-projects/lmod"
    url      = "http://sourceforge.net/projects/lmod/files/Lmod-6.0.1.tar.bz2/download"

    version('6.0.1', '91abf52fe5033bd419ffe2842ebe7af9')

    depends_on("lua@5.2:")

    def install(self, spec, prefix):
        # Add our lua to PATH
        os.environ['PATH'] = spec['lua'].prefix.bin + ';' + os.environ['PATH']
        
        configure('--prefix=%s' % prefix)
        make()
        make("install")
