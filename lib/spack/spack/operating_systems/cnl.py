import re
import os

from spack.architecture import OperatingSystem
from spack.util.executable import *
import spack.spec
from spack.util.multiproc import parmap
import spack.compilers

class Cnl(OperatingSystem):
    """ Compute Node Linux (CNL) is the operating system used for the Cray XC
    series super computers. It is a very stripped down version of GNU/Linux.
    Any compilers found through this operating system will be used with
    modules. If updated, user must make sure that version and name are 
    updated to indicate that OS has been upgraded (or downgraded)
    """
    def __init__(self):
        name = 'CNL'
        version = '10'
        super(Cnl, self).__init__(name, version)


    def find_compilers(self, *paths):
        types = spack.compilers.all_compiler_types()
        compiler_lists = parmap(lambda cmp_cls: self.find_compiler(cmp_cls, *paths), types)

        # ensure all the version calls we made are cached in the parent
        # process, as well.  This speeds up Spack a lot.
        clist = reduce(lambda x,y: x+y, compiler_lists)
        return clist


    def find_compiler(self, cmp_cls, *paths):
        compilers = []
        if cmp_cls.PrgEnv:
            if not cmp_cls.PrgEnv_compiler:
                tty.die('Must supply PrgEnv_compiler with PrgEnv')

            modulecmd = which('modulecmd')
            modulecmd.add_default_arg('python')

            # Save the environment variable to restore later
            old_modulepath = os.environ['MODULEPATH']
            # if given any explicit paths, search them for module files too
            if paths:
                module_paths = ':' + ':'.join(p for p in paths)
                os.environ['MODULEPATH'] = module_paths
        
            output = modulecmd('avail', cmp_cls.PrgEnv_compiler, output=str, error=str)
            matches = re.findall(r'(%s)/([\d\.]+[\d])' % cmp_cls.PrgEnv_compiler, output)
            for name, version in matches:
                v = version
                comp = cmp_cls(spack.spec.CompilerSpec(name + '@' + v), self,
                           ['cc', 'CC', 'ftn'], [cmp_cls.PrgEnv, name +'/' + v])

                compilers.append(comp)

            # Restore modulepath environment variable
            if paths:
                os.environ['MODULEPATH'] = old_modulepath

        return compilers
