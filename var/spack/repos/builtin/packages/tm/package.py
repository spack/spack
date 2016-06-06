from spack import *

class Tm(Package):
    """This is Torque / PBS"""
    homepage = "http://www.adaptivecomputing.com/"
    url      = "http://www.adaptivecomputing.com/download/torque/torque-6.0.1-1456945733_daea91b.tar.gz"

    version('6.0.1', '2b958e9f5d200641e6fc9564977aecc5')

    def install(self, spec, prefix):
        print "install not implemented"
        #configure("--prefix=%s" % prefix)
        #make()
        #make("install")
##############################################################
# these lines should be added to etc/spack/packages.yaml
#  tm:
#    version: [system]
#    paths:
#      tm@system: /cineca/sysprod/pbs/12.3.0.143517
#    buildable: false

