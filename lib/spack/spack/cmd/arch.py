from spack import *
import spack.version as version

import multiprocessing
import platform

def arch(args):
    print multiprocessing.cpu_count()
    print platform.mac_ver()


    print version.canonical(platform.mac_ver()[0])
