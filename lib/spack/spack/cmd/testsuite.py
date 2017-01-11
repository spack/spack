#!/usr/bin/env python

import os
import requests
import glob
import argparse
import llnl.util.tty as tty
import spack.cmd
from spack.spec import Spec
import spack.build_environment as build_env
import spack.cmd.install as install    
import spack.cmd.uninstall as uninstall
import spack.util.spack_yaml as yaml

description = "Compiles a list of tests from a yaml file. Runs Spec and concretize then produces cdash format."

#not sure if I will use this later cdash or junit, spack.io or whereever or other flags
def setup_parser(subparser):
    subparser.add_argument(
        'yamlFile', nargs=argparse.REMAINDER,
        help="Compiles a list of tests from a yaml file. Runs Spec and concretize then produces cdash format.")


def testsuite(parser, args):
    if not args.yamlFile:
        tty.die("spack testsuite requires a yaml file as argument.")

    args.log_format='cdash'
    compilers = []
    packages = []
    tests = []
    testsAll = []
    testPackages = []
    testPackagesAll = []
    for files in args.yamlFile: #read yaml files which contains description of tests
        with open(files, 'r') as stream:
            try:
                yamlFile= yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
            packages = yamlFile['packages'] # list of packages to test. Current libelf, libdwarf, bzip2
            compilers = yamlFile['aws_compilers'] # contains local compilers to my system. Use #yamlFile['compilers'] if you want all possible compilers
            #produces the combinations of packages with compilers.
            for package in packages:
                for versions in  yamlFile[package]:
                    testPackages.append(str(package)+"@"+str(versions))
                    testPackagesAll.append(str(package)+"@"+str(versions))
                    if len(yamlFile[package+"_noCheckSum"]) != 0:
                        for noSumVersions in yamlFile[package+"_noCheckSum"]:
                            testPackagesAll.append(str(package)+"@"+str(noSumVersions))


            #compiling a list of packages with and without checksums. This will be used later to widen the scope of tests            
            for package in testPackages:
                for compiler in compilers:
                    tests.append(package+'%'+compiler)

            for package in testPackagesAll:
                for compiler in compilers:
                    testsAll.append(package+'%'+compiler)


            #tty.msg("tests with checksum:\n")
            tty.msg(tests)
            #tty.msg("\n\n\ntests with no checksum:\n")
            #tty.msg(testsAll)

            exclusions = yamlFile['exclusion']
            if len(exclusions) != 0:
                for exclusion in exclusions:
                    if exclusion in tests:
                        tests.remove(exclusion)
                        testsAll.remove(exclusion)

            concreteTests = []

        for test in tests:
                spec = Spec(test)
                spec.concretize()
                #uninstall all packages before installing. This will reduce the number of skipped package installs.
                try:
                    uninstall.do_uninstall(spec, "True")
                except Exception:
                    print Exception
       
                try:
                    concreteTests.append(spec.to_yaml())
                    parser = argparse.ArgumentParser()
                    install.setup_parser(parser)
                    args = parser.parse_args(['--log-format=cdash'])
                    args.package = test
                    install.install(parser, args)
                except Exception:
                    continue
                
    #path used for testing. Path contains xml files produced during the cmd run.
    path = "/Users/friedt2/var/spack/cdash/"

    files = [name for name in glob.glob(os.path.join(path,'*.*')) if os.path.isfile(os.path.join(path,name))]
    for file in files:
            if "dstore" not in file:
                    with open(file) as fh:
                            mydata = fh.read() #using a put request to send xml files to cdash.
                            response = requests.put('https://spack.io/cdash/submit.php?project=Spack',
                                    data=mydata,
                                    #auth=('friedt2@llnl.gov', 'b01ad0ce'), #dont think I need this
                                    headers={'content-type':'text/plain'},
                                    params={'file': path+file}
                                    )
                            tty.msg(file)
                            tty.msg(response.status_code)

                



