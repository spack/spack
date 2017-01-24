#!/usr/bin/env python

import os
import requests
import glob
import argparse
import llnl.util.tty as tty
from spack.spec import Spec
import spack.cmd.install as install    
import spack.cmd.uninstall as uninstall
import spack.util.spack_yaml as yaml
import spack.compilers 
import spack

description = "Compiles a list of tests from a yaml file. Runs Spec and concretize then produces cdash format."

#not sure if I will use this later cdash or junit, spack.io or whereever or other flags
def setup_parser(subparser):
    subparser.add_argument(
        '-c', '--complete', action='store_true', dest='complete',
        help='using this option switches from simple cdash output to compelet: simple is only build, complete is configure, build and test xml output.')
    subparser.add_argument(
        'yamlFile', nargs=argparse.REMAINDER,
        help="yaml file that contains a list of tests, example yaml file can be found in /lib/spack/docs/tutorial/examples/test.yaml")

'''
fucntion Name: reduceCompilerList
parameters:
    masterList : list
returns:
    list
Get the list of compilers from spack found on the system.
Compares the spack list to test file.
If a compiler is found on both lists its returned.
'''
def reduceCompilerList(masterList):
    systemCompilers = []
    newMaster = []
    newList = []
    for item in masterList:
        newMaster.append(str(item))
    
    for compilers in spack.compilers.all_compilers(scope=None):
        systemCompilers.append(str(compilers))

    for compiler in systemCompilers:
        if compiler in newMaster:
            newList.append(compiler)
    return newList


'''
fucntion Name: removeTests
parameters:
    testList  : list
    exclusion : str
returns:
    list

Receieves a list of all tests and an excusion.
Depending on the type of exclusion it will remove tests matching.
Returns the list with the tests matching the excusion removed.

exclusions can be in this form:
pkg%compiler
pkg@version
compiler@version
pkg@version%compiler@version
pkg@version%compiler
pkg%compiler@version
pkg
compiler
'''
def removeTests(testList, exclusion):
    pkg = ""
    compiler=""
    teststoRemove = []
    if "%" in exclusion:
        pkg = exclusion.split('%')[0]
        compiler=exclusion.split('%')[1]
        if '@' in pkg and '@' in compiler:#pkg@version%compiler@version
            if exclusion in testList:
                teststoRemove.append(exclusion)
        elif '@' in pkg or '@' in compiler:#pkg@version%compiler or pkg%compiler@version
            for test in testList:
                if pkg in test and compiler in test:
                    teststoRemove.append(test)
        else:#pkg%compiler
            for test in testList:
                if pkg in test and compiler in test:
                    teststoRemove.append(test)
    elif '@' in exclusion: #pkg@version or compiler@version
        for test in testList:
            if exclusion in test:
                teststoRemove.append(test)
    else:#pkg or compiler
        remove=0
        for test in testList:
            if exclusion in str(test):
                teststoRemove.append(test)
    for test in teststoRemove: #remove tests from main test list
        testList.remove(test)
    return testList

def testsuite(parser, args):
    if not args.yamlFile:
        tty.die("spack testsuite requires a yaml file as argument.")
    if args.complete:
        args.log_format='cdash-complete' #use cdash-complete if you want configure, build and test output.
        cdash = '--log-format=cdash-complete'
    else:
        args.log_format='cdash-simple' #use cdash-complete if you want configure, build and test output.
        cdash = '--log-format=cdash-simple'
    print args.complete
    enabledTests = []
    compilers = []
    packages = []
    tests = []
    testPackages = []
    versions = []
    packageVersion = []
    compilerVersion = []
    path = ""
    dashboards = []
    #designed to use a single file and modify the enabled tests, thus requiring a single file modification.
    for files in args.yamlFile: #read yaml files which contains description of tests
        with open(files, 'r') as stream:
            try:
                yamlFile= yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

            enabledTests= yamlFile['enable']
            packages= yamlFile['packages'] # list of packages to test. Current libelf, libdwarf, bzip2
            compilers = yamlFile['compilers']
            
            try:
                path=yamlFile['path']
            except KeyError as e:
                tty.msg("Path not found, will use " + str(spack.prefix)+"/var/spack/cdash/")

            try:
                dashboards = yamlFile['dashboard']
            except KeyError as e:
                if path is "":
                    tty.msg("dashboard url was not found. xml files will be stored at " + str(spack.prefix)+"/var/spack/cdash/")
                else:
                    tty.msg("dashboard url was not found. xml files will be stored at path provided.")
    #creating a list of packages 
    for package in packages:
        for pkg in package:
            if pkg in enabledTests:
                versions = package[pkg][0]['versions']
                for version in versions:
                    # producing packages at available versions. Sample file contains only checksum'd
                    packageVersion.append(str(pkg)+"@"+str(version))

    #creating a list of compilers
    for compiler in compilers:
        for comp in compiler:
            versions = compiler[comp][0]['versions']
            for version in versions:
                # producing compilers at available versions. Sample file contains only checksum'd
                compilerVersion.append(str(comp)+"@"+str(version))
    #reducing compiler list to whats actually available on the system
    compilerVersion = reduceCompilerList(compilerVersion)
    #producing a list of tests with a combination of packages and compilers
    for pkg in packageVersion:
        for comp in compilerVersion:
            tests.append(str(pkg)+"%"+str(comp))

    #loading test excusions
    exclusions = yamlFile['exclusions']
    if len(exclusions) != 0:
        #remove test that match the exclusion
        for exclusion in exclusions:
            tests=removeTests(tests, exclusion)


    concreteTests = []
    
    #setting up tests for contretizing
    for test in tests:
        spec = Spec(test)
        #uninstall all packages before installing. This will reduce the number of skipped package installs.
        while (len(spack.store.db.query(spec)) > 0):
            spec.concretize()
            tty.msg("uninstalling " + str(spec))
            pkg = spack.repo.get(spec)
            pkg.do_uninstall()
        #concretize, failing can occur if the package uses the wrong compiler which would produce a failure for cdash
        try:
            spec.concretize()
            concreteTests.append(spec.to_yaml())
            parser = argparse.ArgumentParser()
            install.setup_parser(parser)
            args = parser.parse_args([cdash]) #use cdash-complete if you want configure, build and test output.
            args.package = test
            install.install(parser, args)
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            tty.msg(message)

    #Path contains xml files produced during the test run.
    if path is "": # if no path given in test yaml file. Uses default location.
        path = spack.prefix+"/var/spack/cdash/"
    for dashboard in dashboards:#allows for multiple dashboards
        files = [name for name in glob.glob(os.path.join(path,'*.*')) if os.path.isfile(os.path.join(path,name))]
        for file in files:
                if "dstore" not in file:
                        with open(file) as fh:
                                mydata = fh.read() #using a put request to send xml files to cdash.
                                response = requests.put(dashboard,
                                        data=mydata,
                                        headers={'content-type':'text/plain'},
                                        params={'file': path+file}
                                        )
                                tty.msg(file)
                                tty.msg(response.status_code)

