#!/usr/bin/env python

import os
import requests
import glob
import argparse
import llnl.util.tty as tty
from spack.spec import Spec
import spack.cmd.install as install    
import spack.cmd.uninstall as uninstall
import spack.util.spack_yaml as syaml
import spack.compilers 
import spack
from yaml.error import MarkedYAMLError
import jsonschema
from jsonschema import Draft4Validator, validators
from spack.error import SpackError
import re
import sys

description = "Compiles a list of tests from a yaml file. Runs Spec and concretize then produces cdash format."

def setup_parser(subparser):
    subparser.add_argument(
        '-c', '--complete', action='store_true', dest='complete',
        help='using this option switches from simple cdash output to compelet: simple is only build, complete is configure, build and test xml output.')
    subparser.add_argument(
        'yamlFile', nargs=argparse.REMAINDER,
        help="yaml file that contains a list of tests, example yaml file can be found in /lib/spack/docs/tutorial/examples/test.yaml")

def _mark_overrides(data):
    if isinstance(data, list):
        return [_mark_overrides(elt) for elt in data]

    elif isinstance(data, dict):
        marked = {}
        for key, val in data.iteritems():
            if isinstance(key, basestring) and key.endswith(':'):
                key = syaml.syaml_str(key[:-1])
                key.override = True
            marked[key] = _mark_overrides(val)
        return marked

    else:
        return data

def extend_with_default(validator_class):
    """Add support for the 'default' attr for properties and patternProperties.

       jsonschema does not handle this out of the box -- it only
       validates.  This allows us to set default values for configs
       where certain fields are `None` b/c they're deleted or
       commented out.

    """
    validate_properties = validator_class.VALIDATORS["properties"]
    validate_pattern_properties = validator_class.VALIDATORS[
        "patternProperties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.iteritems():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])
        for err in validate_properties(
                validator, properties, instance, schema):
            yield err

    def set_pp_defaults(validator, properties, instance, schema):
        for property, subschema in properties.iteritems():
            if "default" in subschema:
                if isinstance(instance, dict):
                    for key, val in instance.iteritems():
                        if re.match(property, key) and val is None:
                            instance[key] = subschema["default"]

        for err in validate_pattern_properties(
                validator, properties, instance, schema):
            yield err

    return validators.extend(validator_class, {
        "properties": set_defaults,
        "patternProperties": set_pp_defaults
    })


DefaultSettingValidator = extend_with_default(Draft4Validator)


def validate_section(data, schema):
    """Validate data read in from a Spack YAML file.

    This leverages the line information (start_mark, end_mark) stored
    on Spack YAML structures.

    """
    try:
        DefaultSettingValidator(schema).validate(data)
    except jsonschema.ValidationError as e:
        raise ConfigFormatError(e, data)

def test_suite(parser, args):
    #pdb.set_trace()
    """Compiles a list of tests from a yaml file. Runs Spec and concretize then produces cdash format."""
    if not args.yamlFile:
        tty.die("spack testsuite requires a yaml file as argument.")
    if args.complete:
        args.log_format='cdash-complete' #use cdash-complete if you want configure, build and test output.
        cdash = '--log-format=cdash-complete'
    else:
        args.log_format='cdash-simple' #use cdash-complete if you want configure, build and test output.
        cdash = '--log-format=cdash-simple'
    
    cdash_root = "/var/spack/cdash/"
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
    data = ""
    schema = spack.schema.test.schema
    all_specs = spack.store.layout.all_specs()
    #designed to use a single file and modify the enabled tests, thus requiring a single file modification.
    for filename in args.yamlFile: #read yaml files which contains description of tests
        try:
            tty.debug("Reading config file %s" % filename)
            with open(filename) as f:
                data = _mark_overrides(syaml.load(f))

            if data:
                validate_section(data, schema)
            try:
                enabledTests= data['enable']
                packages= data['packages'] # list of packages to test. Current libelf, libdwarf, bzip2
                compilers = data['compilers']
            except:
                tty.msg("Testing yaml files must contain atleast enable, packages and compilers to produce results.")
                ssy.exit(1)
            try:    
                dashboards  = data['dashboard']
            except:
                tty.msg("dashboard tag not found. Results will be create in " + str(cdash_root))
                pass
        except MarkedYAMLError as e:
            raise ConfigFileError(
                "Error parsing yaml%s: %s" % (str(e.context_mark), e.problem))

        except IOError as e:
            raise ConfigFileError(
                "Error reading configuration file %s: %s" % (filename, str(e)))
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
                    if bool([s for s in all_specs if s.satisfies("%"+str(comp)+"@"+str(version))]):
                        compilerVersion.append(str(comp)+"@"+str(version))
    #reducing compiler list to whats actually available on the system
    
    #producing a list of tests with a combination of packages and compilers
    for pkg in packageVersion:
        for comp in compilerVersion:
            tests.append(str(pkg)+"%"+str(comp))
    #loading test excusions
    removeTests = []
    exclusions = data['exclusions']
    if len(exclusions) != 0:
        #remove test that match the exclusion
        #setting up tests for contretizing
        for test in tests:
            spec = Spec(test)
            for exclusion in exclusions:
            #for exclusion in exclusions:
                if bool(spec.satisfies(exclusion)):
                    removeTests.append(test)
        for test in removeTests:
            tests.remove(test)

    concreteTests = []
    #setting up tests for contretizing
    for test in tests:
        spec = Spec(test)
        if len(spack.store.db.query(spec)) != 0:
            tty.msg(spack.store.db.query(spec))
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
        path = spack.prefix+cdash_root
    if len(dashboards) != 0:
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

class ConfigError(SpackError):
    pass

class ConfigFileError(ConfigError):
    pass

    
class ConfigFormatError(ConfigError):
    """Raised when a configuration format does not match its schema."""

    def __init__(self, validation_error, data):
        # Try to get line number from erroneous instance and its parent
        instance_mark = getattr(validation_error.instance, '_start_mark', None)
        parent_mark = getattr(validation_error.parent, '_start_mark', None)
        path = [str(s) for s in getattr(validation_error, 'path', None)]

        # Try really hard to get the parent (which sometimes is not
        # set) This digs it out of the validated structure if it's not
        # on the validation_error.
        if path and not parent_mark:
            parent_path = list(path)[:-1]
            parent = get_path(parent_path, data)
            if path[-1] in parent:
                if isinstance(parent, dict):
                    keylist = parent.keys()
                elif isinstance(parent, list):
                    keylist = parent
                idx = keylist.index(path[-1])
                parent_mark = getattr(keylist[idx], '_start_mark', None)

        if instance_mark:
            location = '%s:%d' % (instance_mark.name, instance_mark.line + 1)
        elif parent_mark:
            location = '%s:%d' % (parent_mark.name, parent_mark.line + 1)
        elif path:
            location = 'At ' + ':'.join(path)
        else:
            location = '<unknown line>'

        message = '%s: %s' % (location, validation_error.message)
        super(ConfigError, self).__init__(message)
