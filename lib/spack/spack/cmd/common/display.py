# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from datetime import date

import llnl.util.tty as tty
import llnl.util.tty.color as color

import spack.spec

header_color = '@*b'
plain_format = '@.'


def section_title(s):
    return header_color + s + plain_format


def version(s):
    return spack.spec.version_color + s + plain_format


def variant(s):
    return spack.spec.enabled_variant_color + s + plain_format


def print_deps(spec, dependencies=True):
    """
    Print dependency or dependent information for the spec.

    Arguments:
        spec (Spec):  Spec whose information is being printed
        dependencies (bool): True if dependencies, False if dependents
    """
    deps = spec.dependencies_dict().items() if dependencies else \
        spec.dependents_dict().items()
    if not deps:
        return

    color.cprint('')
    title = 'Dependencies' if dependencies else 'Dependents'
    color.cprint(section_title('Recorded {0}:'.format(title)))
    for _, value in deps:
        dep_str = str(value).replace(spec.name, '') if dependencies \
            else str(value)
        dep_str = dep_str.replace('-->', ' dependencies on')
        color.cprint("    {0}".format(dep_str.strip()))


def print_installed_info(spec):
    """
    Print the installed spec's information

    Arguments:
        spec (Spec): Installed spec whose information will be printed
    """
    dag = spec.dag_hash()
    _, record = spack.store.db.query_by_spec_hash(dag)

    if not record.installed:
        tty.die("Spec is not installed.")

    pkg_vers = version('{0}@@{1}'.format(spec.name, spec.versions[0]))
    header = section_title(
        '{0}:   '
    ).format(spec.package.build_system_class) + pkg_vers
    color.cprint(header)

    color.cprint('')
    color.cprint(section_title('Hashes:'))
    color.cprint("    DAG  = {0}".format(dag))
    color.cprint("    full = {0}".format(spec.full_hash()))

    color.cprint('')
    how = 'Explicitly' if record.explicit else 'as Dependency'
    installation = 'Installed {0}:   '.format(how)
    when = date.fromtimestamp(record.installation_time).strftime("%A %d %B %Y")
    color.cprint(section_title(installation) + when)
    color.cprint("    architecture = {0}".format(spec.architecture))
    color.cprint("    prefix       = {0}".format(record.path))

    if spec.external:
        color.cprint('')
        color.cprint(section_title('External:'))
        color.cprint("    path             = {0}".format(spec.external_path))
        color.cprint("    module           = {0}".format(spec.external_modules))
        color.cprint("    extra_attributes = {0}".format(spec.extra_attributes))

    color.cprint('')
    compiler = '{0}@@{1}'.format(spec.compiler.name, spec.compiler.versions[0])
    color.cprint(section_title('Compiler:   ') + version(compiler))
    for flag, value in spec.compiler_flags.items():
        color.cprint("    {0} = {1}".format(flag, value))

    color.cprint('')
    color.cprint(section_title('Variant Settings:'))
    variants = spec.variants.items()
    if len(variants) > 1:
        for _, value in variants:
            color.cprint("    {0}".format(value))
    else:
        color.cprint("    None")

    print_deps(spec, dependencies=True)
    print_deps(spec, dependencies=False)
