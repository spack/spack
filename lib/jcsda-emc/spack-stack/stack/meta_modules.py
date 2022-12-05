#!/usr/bin/env python3

import copy
import logging
import os
import re
import sys

import spack
import spack.environment as ev

# logging.basicConfig(level=logging.INFO)
logging.basicConfig(format='%(message)s', level=logging.DEBUG)

# Get basic directory information
logging.info("Configuring basic directory information ...")
this_script_dir = os.path.realpath(os.path.split(__file__)[0])
base_dir = os.path.realpath(os.path.join(this_script_dir, '..'))
spack_dir = spack.paths.spack_root
logging.info("  ... script directory: {}".format(this_script_dir))
logging.info("  ... base directory: {}".format(base_dir))
logging.info("  ... spack directory: {}".format(spack_dir))

# Templates for creating compiler modules
COMPILER_TEMPLATES = {
    'lmod': os.path.join(this_script_dir, 'templates/compiler.lua'),
    'tcl': os.path.join(this_script_dir, 'templates/compiler'),
}
MPI_TEMPLATES = {
    'lmod': os.path.join(this_script_dir, 'templates/mpi.lua'),
    'tcl': os.path.join(this_script_dir, 'templates/mpi'),
}
PYTHON_TEMPLATES = {
    'lmod': os.path.join(this_script_dir, 'templates/python.lua'),
    'tcl': os.path.join(this_script_dir, 'templates/python')
}
MODULE_FILE_EXTENSION = {
    'lmod': '.lua',
    'tcl': '',
}

SUBSTITUTES_TEMPLATE = {
    'MODULELOADS': '',
    'MODULEPREREQS': '',
    'MODULEPATH': '',
    'CC': '',
    'CXX': '',
    'F77': '',
    'FC': '',
    'COMPFLAGS': '',
    'ENVVARS': '',
    'MPICC': '',
    'MPICXX': '',
    'MPIF77': '',
    'MPIFC': '',
    'MPIROOT': '',
    'PYTHONROOT': '',
}


def versiontuple(v):
    """Version comparison without relying on packaging module"""
    return tuple(map(int, (v.split("."))))


def get_name_and_version_from_spec(spec):
    """Extract the name and the version from a spec"""
    (spec_name, spec_version) = spec.split('@', 1)
    # Strip off any compiler/provider specification or variants from the spec version
    spec_version = spec_version.split('+')[0].split('~')[0].split('-')[0] \
        .split('%')[0].split('^')[0].strip()
    return (spec_name, spec_version)


def get_matched_dict(root_dir, candidate_list, sub_candidate_list=None):
    """Return a dictionary of package (compiler, mpi) versions that contains
    exact version matches for a list of candidates provided in candidate_list.
    This versions are identified by parsing the spack modulefile tree and
    matching the candidate names/versions (partially if incomplete) to the
    directory names. For packages with dependencies
    (e.g. mpi depends on compiler), a recursive search is performed
    for compiler versions based on sub_candidate_list."""

    matched_dict = {}
    dirs = [xdir for xdir in os.listdir(
        root_dir) if os.path.isdir(os.path.join(root_dir, xdir))]
    for candidate in candidate_list:
        matched_name = None
        matched_version = None
        for xdir in dirs:
            # Partial matches: name/version/
            if ('@' in candidate and xdir == candidate.split('@')[0]) or (xdir == candidate):
                candidate_dir = os.path.join(root_dir, xdir)
                # Now that we have the top-level compiler dir
                # check which versions are installed
                versions = [ydir for ydir in os.listdir(candidate_dir)
                            if os.path.isdir(os.path.join(candidate_dir, ydir))]
                # There must be a unique match with the compiler in the candidate list
                version_matches = [
                    x for x in versions if candidate in '{}@{}'.format(xdir, x)]
                if not version_matches:
                    raise Exception("No version match for {} in {}".format(
                        candidate, candidate_dir))
                elif len(version_matches) > 1:
                    raise Exception("Multiple version matches for {} in {}: {}".format(
                        candidate, candidate_dir, version_matches))
                # Each candidate must match exactly one entry
                if matched_name:
                    raise Exception("Multiple matches for {} in {}: {}@{} and {}@{}".format(
                        candidate, candidate_dir, matched_name, matched_version, xdir,
                        version_matches[0]))
                # Now we have an exact, unique match of mpi name and version
                matched_name = xdir
                matched_version = version_matches[0]
                if sub_candidate_list:
                    sub_matched_dict = get_matched_dict(
                        os.path.join(root_dir, matched_name, matched_version),
                        sub_candidate_list)
            # Partial matches: name-version/ or name-version-hash/ or ...
            elif '@' in candidate and xdir.startswith(candidate.replace('@','-')):
                matched_name = candidate.split('@')[0]
                matched_version = candidate.split('@')[1]
        if not matched_name or not matched_version:
            continue
        # Compilers for example do not depend on another package
        if not sub_candidate_list:
            if matched_name not in matched_dict.keys():
                matched_dict[matched_name] = [matched_version]
            else:
                matched_dict[matched_name].append(matched_version)
        # MPI providers or example depend on compilers
        else:
            if matched_name not in matched_dict.keys():
                matched_dict[matched_name] = {}
            if matched_version not in matched_dict[matched_name].keys():
                matched_dict[matched_name][matched_version] = {}
            matched_dict[matched_name][matched_version].update(sub_matched_dict)
    return matched_dict


def merge_dicts(dictA, dictB):
    """Merge two dictionaries and remove duplicates"""
    for key in dictB.keys():
        if not key in dictA.keys():
            dictA[key] = copy.deepcopy(dictB[key])
        else:
            dictA[key] = list(set(dictA[key] + dictB[key]))
    return dictA


def setenv_command(module_choice, key, value):
    if module_choice == 'lmod':
        return 'setenv("{}", "{}")\n'.format(key, value)
    else:
        return 'setenv {{{}}} {{{}}}\n'.format(key, value)


def prepend_path_command(module_choice, key, value):
    if module_choice == 'lmod':
        return 'prepend_path("{}", "{}")\n'.format(key, value)
    else:
        return 'prepend-path {{{}}} {{{}}}\n'.format(key, value)


def module_load_command(module_choice, module):
    if module_choice == 'lmod':
        return 'load("{}")\n'.format(module)
    else:
        return """if {{ [ module-info mode load ] && ![ is-loaded {0} ] }} {{
    module load {0}
}}\n""".format(module)


def module_prereq_command(module_choice, module):
    if module_choice == 'lmod':
        return 'prereq("{}")\n'.format(module)
    else:
        return ''


def substitute_config_vars(config_str):
    """
    Substitute spack-specific and environment variables that may be present
    in configuration files. See:
    https://spack.readthedocs.io/en/latest/configuration.html#config-file-variables
    """
    spack_vars = {'ENV': ev.active_environment().path,
                  'SPACK': os.getenv('SPACK_ROOT'),
                  'TEMPDIR': None,
                  'USER': os.getenv('HOME'),
                  'USER_CACHE_PATH': os.path.join(os.getenv('HOME'), '.spack')
                  }

    if config_str.startswith('~'):
        config_str = config_str.replace('~', os.getenv('HOME'))

    # Get var as it appears in the string (e.g. ${env}), and its name (e.g. env)
    matches = re.findall(r'(\$(\w+))|(\${(\w+)})', config_str)
    for match in matches:
        if match[0]:
            pair = (match[0], match[1])
        else:
            pair = (match[2], match[3])

        var_string = pair[0]
        var_name = pair[1].upper()

        sub_value = spack_vars[var_name] if spack_vars[var_name] else os.getenv(
            var_name)
        config_str = config_str.replace(var_string, sub_value)

    return config_str


def setup_meta_modules():
    # Find currently active spack environment, activate here
    logging.info("Configuring active spack environment ...")
    env_dir = ev.active_environment().path
    if not env_dir:
        raise Exception("No active spack environment")
    env = spack.environment.Environment(env_dir)
    spack.environment.environment.activate(env)
    logging.info("  ... environment directory: {}".format(env_dir))

    # Parse spack main config from environment
    logging.info("Parsing spack environment main config ...")
    main_config = spack.config.get('config')
    install_dir = substitute_config_vars(main_config['install_tree']['root'])

    if not os.path.isabs(install_dir):
        install_dir = os.path.realpath(os.path.join(env_dir, install_dir))
    else:
        install_dir = os.path.realpath(install_dir)
    logging.info("  ... install directory: {}".format(install_dir))

    ##################################################################
    # Parse the modulefile directory to determine the combinations   #
    # of compiler and mpi providers for which to create meta modules #
    ##################################################################

    # Parse spack module config from environment
    logging.info("Parsing spack environment modules config ...")
    module_config = spack.config.get('modules')

    # Check which modules are used - tcl or lmod (can only be one)
    if len(module_config['default']['enable']) > 1:
        raise Exception("Can use either lmod or tcl modules, not both")
    module_choice = module_config['default']['enable'][0]
    logging.info("  ... configured to use {} modules".format(module_choice))

    # Prevent the use of tcl modules on macOS because sed syntax is different
    if module_choice == 'tcl' and sys.platform == "darwin":
        raise Exception(
            "Use of tcl modules on macOS not supported - sed syntax differs")

    # Top-level module directory
    module_dir = substitute_config_vars(
        module_config['default']['roots'][module_choice])
    if not os.path.isabs(module_dir):
        module_dir = os.path.realpath(os.path.join(env_dir, module_dir))
    else:
        module_dir = os.path.realpath(module_dir)
    logging.info("  ... module directory: {}".format(module_dir))

    # Parse spack package config from environment
    logging.info("Parsing spack environment package config ...")
    package_config = spack.config.get('packages')
    compiler_candidate_list = package_config['all']['compiler']
    logging.debug("  ... list of possible compilers: '{}'".format(
        compiler_candidate_list))
    mpi_candidate_list = package_config['all']['providers']['mpi']
    logging.debug(
        "  ... list of possible mpi providers: '{}'".format(mpi_candidate_list))

    # Sanity checks: compiler_candidate_list and mpi_candidate_list must be unique
    if not len(compiler_candidate_list) == len(set(compiler_candidate_list)):
        raise Exception("Compiler candidate list is not unique: {}".format(
            compiler_candidate_list))
    if not len(mpi_candidate_list) == len(set(mpi_candidate_list)):
        raise Exception(
            "Compiler candidate list is not unique: {}".format(mpi_candidate_list))

    # Parse the directory tree under the top-level module directory
    logging.debug(os.listdir(module_dir))
    # First, check for compilers
    compiler_dict = get_matched_dict(module_dir, compiler_candidate_list)
    logging.info(" ... stack compilers: '{}'".format(compiler_dict))
    # Then, check for mpi providers - recursively for compilers
    mpi_dict = get_matched_dict(module_dir, mpi_candidate_list, compiler_candidate_list)
    logging.info(" ... stack mpi providers: '{}'".format(mpi_dict))

    # For some environments, there are only compiler+mpi-dependent modules,
    # and therefore the compiler itself is not recorded in compiler_dict.
    for mpi_provider_name in mpi_dict.keys():
        for mpi_provider_version in mpi_dict[mpi_provider_name].keys():
            compiler_dict_tmp = get_matched_dict(
                os.path.join(module_dir, mpi_provider_name, mpi_provider_version),
                compiler_candidate_list)
            compiler_dict = merge_dicts(compiler_dict, compiler_dict_tmp)

    # For future use, we need a flattened list of all compilers
    flattened_compiler_list = [
        '{}@{}'.format(name, version) for name in compiler_dict.keys()
                       for version in compiler_dict[name]]

    core_compilers = module_config['default'][module_choice]['core_compilers']
    logging.info("  ... core compilers: {}".format(core_compilers))
    # Check that none of the compilers used for the stack is a core compiler
    for core_compiler in core_compilers:
        if any(core_compiler in x for x in flattened_compiler_list):
            raise Exception(
                """Not supported: compiler used for environment
                is in list of core compilers""")

    # Prepare meta module directory
    logging.info("Preparing meta module directory ...")
    meta_module_dir = os.path.join(module_dir, 'Core')
    if not os.path.isdir(meta_module_dir):
        os.mkdir(meta_module_dir)
    logging.info("  ... meta module directory : {}".format(meta_module_dir))

    # Create compiler modules
    logging.info("Creating compiler modules ...")
    compiler_config = spack.config.get('compilers')
    for compiler in compiler_config:
        if compiler['compiler']['spec'] in flattened_compiler_list:
            (compiler_name, compiler_version) = compiler['compiler']['spec'].split('@')
            logging.info(
                "  ... configuring stack compiler {}@{}"
                .format(compiler_name, compiler_version))
            compiler_module_dir = os.path.join(
                meta_module_dir, 'stack-' + compiler_name)
            compiler_module_file = os.path.join(
                compiler_module_dir, compiler_version +
                MODULE_FILE_EXTENSION[module_choice])
            substitutes = SUBSTITUTES_TEMPLATE.copy()

            # Compiler environment variables; names are lowercase in spack
            substitutes['CC'] = compiler['compiler']['paths']['cc']
            substitutes['CXX'] = compiler['compiler']['paths']['cxx']
            substitutes['F77'] = compiler['compiler']['paths']['f77']
            substitutes['FC'] = compiler['compiler']['paths']['fc']
            logging.debug("  ... ... CC  : {}".format(substitutes['CC']))
            logging.debug("  ... ... CXX : {}".format(substitutes['CXX']))
            logging.debug("  ... ... F77 : {}".format(substitutes['F77']))
            logging.debug("  ... ... FC' : {}".format(substitutes['FC']))

            # Compiler flags; names are lowercase in spack
            for flag_name in compiler['compiler']['flags']:
                flag_values = compiler['compiler']['flags'][flag_name]
                substitutes['COMPFLAGS'] += setenv_command(
                    module_choice, flag_name.upper(), flag_values)
            substitutes['COMPFLAGS'] = substitutes['COMPFLAGS'].rstrip('\n')
            logging.debug("  ... ... COMPFLAGS: {}".format(substitutes['COMPFLAGS']))

            # Existing non-spack modules to load
            for module in compiler['compiler']['modules']:
                substitutes['MODULELOADS'] += module_load_command(
                                                                 module_choice, module)
                substitutes['MODULEPREREQS'] += module_prereq_command(
                    module_choice, module)
            substitutes['MODULELOADS'] = substitutes['MODULELOADS'].rstrip('\n')
            substitutes['MODULEPREREQS'] = substitutes['MODULEPREREQS'].rstrip('\n')
            logging.debug("  ... ... MODULELOADS: {}".format(
                substitutes['MODULELOADS']))
            logging.debug("  ... ... MODULEPREREQS: {}".format(
                substitutes['MODULEPREREQS']))

            # Environment variables; case-sensitive in spack
            if 'environment' in compiler['compiler'].keys() and compiler['compiler']['environment']:
                # prepend_path
                if 'prepend_path' in compiler['compiler']['environment'].keys():
                    for env_name in compiler['compiler']['environment']['prepend_path']:
                        env_values = compiler['compiler']['environment']['prepend_path'][env_name]
                        substitutes['ENVVARS'] += prepend_path_command(
                            module_choice, env_name, env_values)
                # set
                if 'set' in compiler['compiler']['environment'].keys():
                    for env_name in compiler['compiler']['environment']['set']:
                        env_values = compiler['compiler']['environment']['set'][env_name]
                        substitutes['ENVVARS'] += setenv_command(
                            module_choice, env_name, env_values)
                substitutes['ENVVARS'] = substitutes['ENVVARS'].rstrip('\n')
                logging.debug("  ... ... ENVVARS  : {}".format(substitutes['ENVVARS']))

            # Spack compiler module hierarchy
            substitutes['MODULEPATH'] = os.path.join(
                module_dir, compiler_name, compiler_version)
            logging.debug("  ... ... MODULEPATH  : {}".format(
                substitutes['MODULEPATH']))
            # If the environment doesn't have compiler-only dependent modules
            # then simply create the placeholder directory
            if not os.path.isdir(substitutes['MODULEPATH']):
                os.makedirs(substitutes['MODULEPATH'])

            # For tcl modules remove the compiler prefices from the module contents
            if module_choice == 'tcl':
                logging.info("  ... ... removing compiler prefices from tcl modulefiles in {}".format(
                    substitutes['MODULEPATH']))
                for root, ddir, files in os.walk(substitutes['MODULEPATH']):
                    for ffile in files:
                        filepath = os.path.join(root, ffile)
                        logging.debug(
                            "  ... ... ... removing compiler prefices in {}".format(filepath))
                        cmd = "sed -i 's#is-loaded {}/{}/#is-loaded #g' {}".format(
                            compiler_name, compiler_version, filepath)
                        status = os.system(cmd)
                        if not status == 0:
                            raise Exception("Error while calling '{}'".format(cmd))
                        cmd = "sed -i 's#load {}/{}/#load #g' {}".format(
                            compiler_name, compiler_version, filepath)
                        status = os.system(cmd)
                        if not status == 0:
                            raise Exception("Error while calling '{}'".format(cmd))

            # Read compiler template into module_content string
            with open(COMPILER_TEMPLATES[module_choice]) as f:
                module_content = f.read()

            # Substitute variables in module_content
            for key in substitutes.keys():
                module_content = module_content.replace(
                    "@{}@".format(key), substitutes[key])

            # Write compiler lua module
            if not os.path.isdir(compiler_module_dir):
                os.makedirs(compiler_module_dir)
            with open(compiler_module_file, 'w') as f:
                f.write(module_content)
            logging.info("  ... writing {}".format(compiler_module_file))

    # Create mpi modules
    for mpi_name in mpi_dict.keys():
        for mpi_version in mpi_dict[mpi_name].keys():
            package_found = False
            external_mpi_package_config = None
            for package_name in package_config.keys():
                if package_name == mpi_name:
                    # mpi provider was supplied as an external package
                    if 'externals' in package_config[package_name].keys():
                        for i in range(len(package_config[package_name]['externals'])):
                            (package_name_dummy, package_version) = get_name_and_version_from_spec(
                                package_config[package_name]['externals'][i]['spec'])
                            if package_version == mpi_version:
                                package_found = True
                                external_mpi_package_config = package_config[package_name]['externals'][i]
                                break
                    # mpi provider was built by spack
                    elif 'version' in package_config[package_name].keys() and \
                            len(package_config[package_name]['version']) == 1 and \
                            package_config[package_name]['version'][0] == mpi_version:
                        package_found = True
                        break
                    # mpi provider was built by spack, we don't have enough
                    # information, just hope we will be lucky
                    elif 'version' not in package_config[package_name].keys():
                        package_found = True
                        break
                    else:
                        raise Exception("Package with matching name is incompatible: {}".format(
                            package_config[package_name]))
                if package_found:
                    break
            if not package_found:
                raise Exception(
                    "Could not find a spack package for {}@{}:".format(mpi_name, mpi_version))

            for compiler_name in mpi_dict[mpi_name][mpi_version].keys():
                for compiler_version in mpi_dict[mpi_name][mpi_version][compiler_name]:
                    logging.info("  ... configuring stack mpi library {}@{} for compiler {}@{}".format(
                        mpi_name, mpi_version, compiler_name, compiler_version))

                    # Path and name for lua module file
                    mpi_module_dir = os.path.join(module_dir, compiler_name,
                                                  compiler_version, 'stack-' + mpi_name)
                    mpi_module_file = os.path.join(
                        mpi_module_dir, mpi_version + MODULE_FILE_EXTENSION[module_choice])
                    substitutes = SUBSTITUTES_TEMPLATE.copy()
                    #
                    if external_mpi_package_config and 'modules' in external_mpi_package_config.keys():
                        # Existing non-spack modules to load
                        for module in external_mpi_package_config['modules']:
                            substitutes['MODULELOADS'] += module_load_command(
                                module_choice, module)
                            substitutes['MODULEPREREQS'] += module_prereq_command(
                                module_choice, module)
                        substitutes['MODULELOADS'] = substitutes['MODULELOADS'].rstrip(
                            '\n')
                        substitutes['MODULEPREREQS'] = substitutes['MODULEPREREQS'].rstrip(
                            '\n')
                        logging.debug("  ... ... MODULELOADS: {}".format(
                            substitutes['MODULELOADS']))
                        logging.debug("  ... ... MODULEPREREQS: {}".format(
                            substitutes['MODULEPREREQS']))
                        # mpi_name_ROOT - replace "-" in mpi_name with "_" for environment variables
                        if 'prefix' in external_mpi_package_config.keys():
                            prefix = external_mpi_package_config['prefix']
                            substitutes['MPIROOT'] = setenv_command(
                                module_choice, mpi_name.replace('-', '_') + '_ROOT', prefix)
                            logging.debug("  ... ... MPIROOT: {}".format(
                                substitutes['MPIROOT']).rstrip('\n'))
                    elif external_mpi_package_config and 'prefix' in external_mpi_package_config.keys():
                        prefix = external_mpi_package_config['prefix']
                        # PATH and compiler wrapper environment variables
                        bindir = os.path.join(prefix, 'bin')
                        if os.path.isdir(bindir):
                            substitutes['ENVVARS'] += prepend_path_command(
                                module_choice, "PATH", bindir)
                        # LD_LIBRARY_PATH AND PKG_CONFIG_PATH - do we need to worry about DYLD_LIBRARY_PATH for macOS?
                        libdir = os.path.join(prefix, 'lib')
                        if os.path.isdir(libdir):
                            substitutes['ENVVARS'] += prepend_path_command(
                                module_choice, "LD_LIBRARY_PATH", libdir)
                        pkgconfigdir = os.path.join(libdir, 'pkgconfig')
                        if os.path.isdir(pkgconfigdir):
                            substitutes['ENVVARS'] += prepend_path_command(
                                module_choice, "PKG_CONFIG_PATH", pkgconfigdir)
                        lib64dir = os.path.join(prefix, 'lib64')
                        if os.path.isdir(lib64dir):
                            substitutes['ENVVARS'] += prepend_path_command(
                                module_choice, "LD_LIBRARY_PATH", lib64dir)
                        pkgconfig64dir = os.path.join(lib64dir, 'pkgconfig')
                        if os.path.isdir(pkgconfig64dir):
                            substitutes['ENVVARS'] += prepend_path_command(
                                module_choice, "PKG_CONFIG_PATH", pkgconfig64dir)
                        # MANPATH
                        mandir = os.path.join(prefix, 'share/man')
                        if os.path.isdir(mandir):
                            substitutes['ENVVARS'] += prepend_path_command(
                                module_choice, "MANPATH", mandir)
                        # ACLOCAL_PATH
                        aclocaldir = os.path.join(prefix, 'share/aclocal')
                        if os.path.isdir(aclocaldir):
                            substitutes['ENVVARS'] += prepend_path_command(
                                module_choice, "ACLOCAL_PATH", aclocaldir)
                        # mpi_name_ROOT - replace "-" in mpi_name with "_" for environment variables
                        substitutes['MPIROOT'] = setenv_command(
                            module_choice, mpi_name.replace('-', '_') + '_ROOT', prefix)
                        logging.debug("  ... ... MPIROOT: {}".format(
                            substitutes['MPIROOT']).rstrip('\n'))
                    else:
                        # Simple workaround for now - depend on spack building the mpi module
                        # and load it with the wrapper, don't set any of the other substitutes
                        module = '{}/{}'.format(mpi_name, mpi_version)
                        substitutes['MODULELOADS'] += module_load_command(
                            module_choice, module).rstrip('\n')
                        substitutes['MODULEPREREQS'] += module_prereq_command(
                            module_choice, module).rstrip('\n')
                        logging.debug("  ... ... MODULELOADS: {}".format(
                            substitutes['MODULELOADS']))
                        logging.debug("  ... ... MODULEPREREQS: {}".format(
                            substitutes['MODULEPREREQS']))

                    # Compiler wrapper environment variables
                    if 'intel' in mpi_name:
                        substitutes['MPICC']    = os.path.join('mpiicc')
                        substitutes['MPICXX']   = os.path.join('mpiicpc')
                        substitutes['MPIF77']   = os.path.join('mpiifort')
                        substitutes['MPIF90']   = os.path.join('mpiifort')
                    else:
                        substitutes['MPICC']    = os.path.join('mpicc')
                        substitutes['MPICXX']   = os.path.join('mpic++')
                        substitutes['MPIF77']   = os.path.join('mpif77')
                        substitutes['MPIF90']   = os.path.join('mpif90')

                    # Spack compiler module hierarchy
                    substitutes['MODULEPATH'] = os.path.join(module_dir, mpi_name, mpi_version,
                                                             compiler_name, compiler_version)
                    logging.debug("  ... ... MODULEPATH  : {}".format(
                        substitutes['MODULEPATH']))
                    # If the environment doesn't have mpi dependent modules
                    # then simply create the placeholder directory
                    if not os.path.isdir(substitutes['MODULEPATH']):
                        os.makedirs(substitutes['MODULEPATH'])

                    # For tcl modules remove the compiler/mpi prefices from the module contents
                    if module_choice == 'tcl':
                        logging.info(
                            "  ... ... removing compiler/mpi prefices from tcl modulefiles in {}".format(substitutes['MODULEPATH']))
                        for root, ddir, files in os.walk(substitutes['MODULEPATH']):
                            for ffile in files:
                                filepath = os.path.join(root, ffile)
                                logging.debug(
                                    "  ... ... ... removing compiler/mpi prefices in {}".format(filepath))
                                # First, compiler-only dependent modules
                                cmd = "sed -i 's#is-loaded {}/{}/#is-loaded #g' {}".format(
                                    compiler_name, compiler_version, filepath)
                                status = os.system(cmd)
                                if not status == 0:
                                    raise Exception(
                                        "Error while calling '{}'".format(cmd))
                                cmd = "sed -i 's#load {}/{}/#load #g' {}".format(
                                    compiler_name, compiler_version, filepath)
                                status = os.system(cmd)
                                if not status == 0:
                                    raise Exception(
                                        "Error while calling '{}'".format(cmd))
                                # Then, compiler+mpi-dependent modules
                                cmd = "sed -i 's#is-loaded {}/{}/{}/{}/#is-loaded #g' {}".format(mpi_name, mpi_version,
                                                                                                 compiler_name, compiler_version, filepath)
                                status = os.system(cmd)
                                if not status == 0:
                                    raise Exception(
                                        "Error while calling '{}'".format(cmd))
                                cmd = "sed -i 's#load {}/{}/{}/{}/#load #g' {}".format(mpi_name, mpi_version,
                                                                                       compiler_name, compiler_version, filepath)
                                status = os.system(cmd)
                                if not status == 0:
                                    raise Exception(
                                        "Error while calling '{}'".format(cmd))

                    # Read compiler lua template into module_content string
                    with open(MPI_TEMPLATES[module_choice]) as f:
                        module_content = f.read()

                    # Substitute variables in module_content
                    for key in substitutes.keys():
                        module_content = module_content.replace(
                            "@{}@".format(key), substitutes[key])

                    # Write mpi lua module
                    if not os.path.isdir(mpi_module_dir):
                        os.makedirs(mpi_module_dir)
                    with open(mpi_module_file, 'w') as f:
                        f.write(module_content)
                    logging.info("  ... writing {}".format(mpi_module_file))

    del package_name
    # Create python modules. Need to accommodate both external
    # Python distributions and spack-built Python distributions.
    # If there is no package config info for Python, then we are
    # using a spack-built Python without knowing the version - not supported.
    if not 'python' in package_config.keys():
        raise Exception("""No information on Python in package config. For external
Python distributions, specify complete specifications. For spack-built
Python, list the correct version in the package config""")
    else:
        package_name = 'python'
        if 'externals' in package_config[package_name].keys():
            # Loop through all external specs and find the
            # latest version, this is what spack is using
            spack_python_build = False
            python_version = None
            for i in range(len(package_config[package_name]['externals'])):
                (python_name, python_version_test) = get_name_and_version_from_spec(
                    package_config[package_name]['externals'][i]['spec'])
                if not python_version or \
                        versiontuple(python_version_test) > versiontuple(python_version):
                    python_version = python_version_test
                    python_package_config = package_config[python_name]['externals'][i]
            logging.debug(
                "  ... using external python version {}".format(python_version))
        else:
            spack_python_build = True
            python_name = 'python'
            python_version = None
            python_package_config = None
            # Loop through versions, pick the most-recent
            for python_version_test in package_config[package_name]['version']:
                if not python_version or \
                        versiontuple(python_version_test) > versiontuple(python_version):
                    python_version = python_version_test
            logging.debug(
                "  ... using spack-built python version {}".format(python_version))
            # Check that the Python version we determined is indeed what's installed
            python_candidate_list = ['python@{}'.format(python_version)]
            for compiler_name in compiler_dict.keys():
                for compiler_version in compiler_dict[compiler_name]:
                    compiler_install_dir = os.path.join(install_dir, compiler_name, compiler_version)
                    python_dict = get_matched_dict(compiler_install_dir, python_candidate_list)
            logging.info(" ... stack python providers: '{}'".format(python_dict))
            if not python_dict:
                raise Exception("""No matching Python version found. Make sure that the
Python version in the package config matches what spack installed.""")

    for compiler_name in compiler_dict.keys():
        for compiler_version in compiler_dict[compiler_name]:
            logging.info("  ... configuring stack python interpreter {}@{} for compiler {}@{}".format(
                python_name, python_version, compiler_name, compiler_version))

            # Path and name for lua module file
            python_module_dir = os.path.join(
                module_dir, compiler_name, compiler_version, 'stack-' + python_name)
            python_module_file = os.path.join(
                python_module_dir, python_version + MODULE_FILE_EXTENSION[module_choice])

            substitutes = SUBSTITUTES_TEMPLATE.copy()
            #
            if spack_python_build:
                module = 'python/{}'.format(python_version)
                # Load spack python module
                substitutes['MODULELOADS'] += module_load_command(
                    module_choice, module)
            elif 'modules' in python_package_config.keys():
                # Existing non-spack modules to load
                for module in python_package_config['modules']:
                    substitutes['MODULELOADS'] += module_load_command(
                        module_choice, module)
                    substitutes['MODULEPREREQS'] += module_prereq_command(
                        module_choice, module)
                substitutes['MODULELOADS'] = substitutes['MODULELOADS'].rstrip(
                    '\n')
                substitutes['MODULEPREREQS'] = substitutes['MODULEPREREQS'].rstrip(
                    '\n')
                logging.debug("  ... ... MODULELOADS: {}".format(
                    substitutes['MODULELOADS']))
                logging.debug("  ... ... MODULEPREREQS: {}".format(
                    substitutes['MODULEPREREQS']))
                # python_name_ROOT - replace "-" in python_name with "_" for environment variables
                if 'prefix' in python_package_config.keys():
                    prefix = python_package_config['prefix']
                    substitutes['PYTHONROOT'] = setenv_command(
                        module_choice, python_name.replace('-', '_') + "_ROOT", prefix)
                    logging.debug("  ... ... PYTHONROOT: {}".format(
                        substitutes['PYTHONROOT']))
            elif 'prefix' in python_package_config.keys():
                prefix = python_package_config['prefix']
                # PATH
                bindir = os.path.join(prefix, 'bin')
                if os.path.isdir(bindir):
                    substitutes['ENVVARS'] += prepend_path_command(
                        module_choice, "PATH", bindir)
                # LD_LIBRARY_PATH AND PKG_CONFIG_PATH - do we need to worry about DYLD_LIBRARY_PATH for macOS?
                # Also: PYTHONPATH = check site-packages and dist-packages
                libdir = os.path.join(prefix, 'lib')
                if os.path.isdir(libdir):
                    substitutes['ENVVARS'] += prepend_path_command(
                        module_choice, "LD_LIBRARY_PATH", libdir)
                pkgconfigdir = os.path.join(libdir, 'pkgconfig')
                if os.path.isdir(pkgconfigdir):
                    substitutes['ENVVARS'] += prepend_path_command(
                        module_choice, "PKG_CONFIG_PATH", pkgconfigdir)
                # Python version for constructing PYTHONPATH is X.Y (major.minor, no patch-level)
                python_version_for_pythonpath = python_version[:python_version.rfind(
                    '.')]
                # Check site-packages and dist-packages
                pythonpathdir = os.path.join(libdir, 'python{}'.format(
                    python_version_for_pythonpath), 'site-packages')
                if os.path.isdir(pythonpathdir):
                    substitutes['ENVVARS'] += prepend_path_command(
                        module_choice, "PYTHONPATH", pythonpathdir)
                pythonpathdir = os.path.join(libdir, 'python{}'.format(
                    python_version_for_pythonpath), 'dist-packages')
                if os.path.isdir(pythonpathdir):
                    substitutes['ENVVARS'] += prepend_path_command(
                        module_choice, "PYTHONPATH", pythonpathdir)
                lib64dir = os.path.join(prefix, 'lib64')
                if os.path.isdir(lib64dir):
                    substitutes['ENVVARS'] += prepend_path_command(
                        module_choice, "LD_LIBRARY_PATH", lib64dir)
                pkgconfig64dir = os.path.join(lib64dir, 'pkgconfig')
                if os.path.isdir(pkgconfig64dir):
                    substitutes['ENVVARS'] += prepend_path_command(
                        module_choice, "PKG_CONFIG_PATH", pkgconfig64dir)
                pythonpath64dir = os.path.join(lib64dir, 'python{}'.format(
                    python_version_for_pythonpath), 'site-packages')
                if os.path.isdir(pythonpath64dir):
                    substitutes['ENVVARS'] += prepend_path_command(
                        module_choice, "PYTHONPATH", pythonpath64dir)
                pythonpath64dir = os.path.join(lib64dir, 'python{}'.format(
                    python_version_for_pythonpath), 'dist-packages')
                if os.path.isdir(pythonpath64dir):
                    substitutes['ENVVARS'] += prepend_path_command(
                        module_choice, "PYTHONPATH", pythonpath64dir)
                # MANPATH
                mandir = os.path.join(prefix, 'share/man')
                if os.path.isdir(mandir):
                    substitutes['ENVVARS'] += prepend_path_command(
                        module_choice, "MANPATH", mandir)
                # ACLOCAL_PATH
                aclocaldir = os.path.join(prefix, 'share/aclocal')
                if os.path.isdir(aclocaldir):
                    substitutes['ENVVARS'] += prepend_path_command(
                        module_choice, "ACLOCAL_PATH", aclocaldir)
                # python_name_ROOT - replace "-" in 
                # python_name with "_" for environment variables
                substitutes['PYTHONROOT'] = setenv_command(
                    module_choice, python_name.replace('-', '_') + "_ROOT", prefix)
            else:
                raise Exception(
                    "External packages must have 'prefix' and/or 'modules'")

            # Read compiler lua template into module_content string
            with open(PYTHON_TEMPLATES[module_choice]) as f:
                module_content = f.read()

            # Substitute variables in module_content
            for key in substitutes.keys():
                module_content = module_content.replace(
                    "@{}@".format(key), substitutes[key])

            # Write python lua module
            if not os.path.isdir(python_module_dir):
                os.makedirs(python_module_dir)
            with open(python_module_file, 'w') as f:
                f.write(module_content)
            logging.info("  ... writing {}".format(python_module_file))

    logging.info(
        "Metamodule generation completed successfully in {}".format(meta_module_dir))
