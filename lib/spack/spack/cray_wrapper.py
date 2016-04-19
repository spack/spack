from spack.compiler import *
from spack.util.executable import *
import re

class CrayWrapper(object):
    # Subclasses set the vendor name for the wrapper to use
    cray_wrapper_config = {
        'vendor_module': 'PrgEnv-vendor',
        'compiler_module': 'vendorcc',
        'libsci_overrides': {
            'vendorcc/old': 'cray-libsci/13.0.0',
            'vendorcc/super-old': 'cray-libsci/12.0.0'
        },
        'mpich_overrides': {
            'vendorcc/old': 'cray-mpich/7.0.0',
            'vendorcc/super-old': 'cray-mpich/6.0.0'
        }
    }

    @property
    def cray_wrapper_module(self):
        conf = self.cray_wrapper_config
        return "%s/%s" % (conf['compiler_module'], self.version)

    @property
    def cray_libsci_module(self):
        conf = self.cray_wrapper_config
        if self.cray_wrapper_module in conf['libsci_overrides']:
            return conf['libsci_overrides'][self.cray_wrapper_module]
        else:
            return "cray-libsci" #default

    @property
    def cray_mpich_module(self):
        conf = self.cray_wrapper_config
        if self.cray_wrapper_module in conf['mpich_overrides']:
            return conf['mpich_overrides'][self.cray_wrapper_module]
        else:
            return "cray-mpich" #default

    @property
    def prelude(self):
        conf = self.cray_wrapper_config
        prelude_tcl =  "module unload PrgEnv-pgi PrgEnv-gnu PrgEnv-intel PrgEnv-cray PrgEnv-nag PrgEnv-pathscale; "
        prelude_tcl += "module load %s; " % conf['vendor_module']
        prelude_tcl += "module swap %s %s; " % (conf['compiler_module'], self.cray_wrapper_module)
        prelude_tcl += "module swap cray-libsci %s; " % self.cray_libsci_module
        prelude_tcl += "module swap cray-mpich %s" % self.cray_mpich_module
        return prelude_tcl
        
    cc_names = ['cc']
    cxx_names = ['CC']
    f77_names = ['ftn']
    fc_names = ['ftn']

    # Named wrapper links within spack.build_env_path
    link_paths = { 'cc'  : 'craype/cc',
                   'cxx' : 'case-insensitive/CC',
                   'f77' : 'craype/ftn',
                   'fc'  : 'craype/ftn' }
    @classmethod
    def _detect_wrapper(cls, comp, regex):
        """The '-help' option gets information about the cray wrapper, 
           not the underlying compiler
           Output looks like this::

           Usage: cc [options] file...
        """
        compiler = Executable(comp)
        output = compiler('-help', output=str, error=str)
        match = re.match(regex, output)
        return (match.group(0) is not None)
    
    @classmethod
    def cc_version(cls, comp):
        if cls._detect_wrapper(comp, r'(Usage: cc \[options\] file)\.*'):
            return super(CrayWrapper, cls).cc_version(comp)
    
    @classmethod
    def cxx_version(cls, comp):
        if cls._detect_wrapper(comp, r'(Usage: CC \[options\] file)\.*'):
            return super(CrayWrapper, cls).cxx_version(comp)
    
    @classmethod
    def fc_version(cls, comp):
        if cls._detect_wrapper(comp, r'(Usage: ftn \[options\] file)\.*'):
            return super(CrayWrapper, cls).fc_version(comp)
    
    @classmethod
    def f77_version(cls, comp):
        if cls._detect_wrapper(comp, r'(Usage: ftn \[options\] file)\.*'):
            return super(CrayWrapper, cls).f77_version(comp)
