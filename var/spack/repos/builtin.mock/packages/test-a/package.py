from spack import *

import os

mydir = os.path.dirname(__file__)
source = os.path.join(mydir,'test-a-0.0.tar.gz')

class TestA(Package):
    """The test-a package"""

    url = 'file://'+source
    homepage = "http://www.example.com/"

    version('0.0', '4e823d0af4154fcf52b75dad41b7fd63')

    variant('nom', default=True, description='Nominal variant')
    variant('var', default=False, description='Variant variant')
  
    def install(self, spec, prefix):
        bindir = os.path.join(prefix,'bin')
        os.makedirs(bindir)
        script = os.path.join(bindir, 'test-a')
        with open(script,'w') as fp:
            fp.write("""#!/bin/bash
echo 'name: %s'
echo 'prefix: %s'
echo 'spec: %s'
            """ % (spec.name, prefix, spec))
        
        os.chmod(script, 0555)
