##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""Tools to produce reports of spec installations"""
import collections
import functools
import itertools
import os.path
import platform
import re
import socket
import time
import traceback
import xml.sax.saxutils

import llnl.util.lang
import spack.build_environment
import spack.fetch_strategy
import spack.package
from spack.util.log_parse import parse_log_events


templates = {
    'junit': os.path.join('reports', 'junit.xml'),
    'cdash': os.path.join('reports', 'cdash')
}

#: Allowed report formats
valid_formats = list(templates.keys())

__all__ = [
    'valid_formats',
    'collect_info'
]


def fetch_package_log(pkg):
    try:
        with codecs.open(pkg.build_log_path, 'r', 'utf-8') as f:
            return ''.join(f.readlines())
    except Exception:
        return 'Cannot open build log for {0}'.format(
            pkg.spec.cshort_spec
        )


class InfoCollector(object):
    """Decorates PackageBase.do_install to collect information
    on the installation of certain specs.

    When exiting the context this change will be rolled-back.

    The data collected is available through the ``specs``
    attribute once exited, and it's organized as a list where
    each item represents the installation of one of the spec.

    Args:
        specs (list of Spec): specs whose install information will
           be recorded
    """
    #: Backup of PackageBase.do_install
    _backup_do_install = spack.package.PackageBase.do_install

    def __init__(self, specs):
        #: Specs that will be installed
        self.input_specs = specs
        #: This is where we record the data that will be included
        #: in our report.
        self.specs = []

    def __enter__(self):
        # Initialize the spec report with the data that is available upfront.
        for input_spec in self.input_specs:
            name_fmt = '{0}_{1}'
            name = name_fmt.format(input_spec.name,
                                   input_spec.dag_hash(length=7))

            spec = {
                'name': name,
                'nerrors': None,
                'nfailures': None,
                'npackages': None,
                'time': None,
                'timestamp': time.strftime(
                    "%a, %d %b %Y %H:%M:%S", time.gmtime()
                ),
                'properties': [],
                'packages': []
            }

            self.specs.append(spec)

            Property = collections.namedtuple('Property', ['name', 'value'])
            spec['properties'].append(
                Property('architecture', input_spec.architecture)
            )
            spec['properties'].append(
                Property('compiler', input_spec.compiler))

            # Check which specs are already installed and mark them as skipped
            for dep in filter(lambda x: x.package.installed,
                              input_spec.traverse()):
                package = {
                    'name': dep.name,
                    'id': dep.dag_hash(),
                    'elapsed_time': '0.0',
                    'result': 'skipped',
                    'message': 'Spec already installed'
                }
                spec['packages'].append(package)

        def gather_info(do_install):
            """Decorates do_install to gather useful information for
            a CI report.

            It's defined here to capture the environment and build
            this context as the installations proceed.
            """
            @functools.wraps(do_install)
            def wrapper(pkg, *args, **kwargs):

                # We accounted before for what is already installed
                installed_on_entry = pkg.installed

                package = {
                    'name': pkg.name,
                    'id': pkg.spec.dag_hash(),
                    'elapsed_time': None,
                    'result': None,
                    'message': None
                }

                start_time = time.time()
                value = None
                try:

                    value = do_install(pkg, *args, **kwargs)
                    package['result'] = 'success'
                    if installed_on_entry:
                        return

                except spack.build_environment.InstallError as e:
                    # An InstallError is considered a failure (the recipe
                    # didn't work correctly)
                    package['result'] = 'failure'
                    package['stdout'] = fetch_package_log(pkg)
                    package['message'] = e.message or 'Installation failure'
                    package['exception'] = e.traceback

                except (Exception, BaseException) as e:
                    # Everything else is an error (the installation
                    # failed outside of the child process)
                    package['result'] = 'error'
                    package['stdout'] = fetch_package_log(pkg)
                    package['message'] = str(e) or 'Unknown error'
                    package['exception'] = traceback.format_exc()

                finally:
                    package['elapsed_time'] = time.time() - start_time

                # Append the package to the correct spec report. In some
                # cases it may happen that a spec that is asked to be
                # installed explicitly will also be installed as a
                # dependency of another spec. In this case append to both
                # spec reports.
                for s in llnl.util.lang.dedupe([pkg.spec.root, pkg.spec]):
                    name = name_fmt.format(s.name, s.dag_hash(length=7))
                    try:
                        item = next((
                            x for x in self.specs
                            if x['name'] == name
                        ))
                        item['packages'].append(package)
                    except StopIteration:
                        pass

                return value

            return wrapper

        spack.package.PackageBase.do_install = gather_info(
            spack.package.PackageBase.do_install
        )

    def __exit__(self, exc_type, exc_val, exc_tb):

        # Restore the original method in PackageBase
        spack.package.PackageBase.do_install = InfoCollector._backup_do_install

        for spec in self.specs:
            spec['npackages'] = len(spec['packages'])
            spec['nfailures'] = len(
                [x for x in spec['packages'] if x['result'] == 'failure']
            )
            spec['nerrors'] = len(
                [x for x in spec['packages'] if x['result'] == 'error']
            )
            spec['time'] = sum([
                float(x['elapsed_time']) for x in spec['packages']
            ])


class collect_info(object):
    """Collects information to build a report while installing
    and dumps it on exit.

    If the format name is not ``None``, this context manager
    decorates PackageBase.do_install when entering the context
    and unrolls the change when exiting.

    Within the context, only the specs that are passed to it
    on initialization will be recorded for the report. Data from
    other specs will be discarded.

    Examples:

        .. code-block:: python

            # The file 'junit.xml' is written when exiting
            # the context
            specs = [Spec('hdf5').concretized()]
            with collect_info(specs, 'junit', 'junit.xml'):
                # A report will be generated for these specs...
                for spec in specs:
                    spec.do_install()
                # ...but not for this one
                Spec('zlib').concretized().do_install()

    Args:
        specs (list of Spec): specs to be installed
        format_name (str or None): one of the supported formats
        filename (str or None): name of the file where the report wil
            be eventually written

    Raises:
        ValueError: when ``format_name`` is not in ``valid_formats``
    """
    def __init__(self, format_name, install_command):
        self.format_name = format_name
        # Consider setting these properties in a more CDash specific place.
        self.install_command = install_command
        self.hostname = socket.gethostname()
        self.osname = platform.system()
        self.starttime = int(time.time())
        # TODO: remove hardcoded use of Experimental here.
        #       Make the submission model configurable.
        self.buildstamp = time.strftime("%Y%m%d-%H%M-Experimental",
                                        time.localtime(self.starttime))

        # Check that the format is valid
        if format_name not in itertools.chain(valid_formats, [None]):
            raise ValueError('invalid report type: {0}'.format(format_name))

    def __enter__(self):
        if self.format_name:
            # Start the collector and patch PackageBase.do_install
            self.collector = InfoCollector(self.specs)
            self.collector.__enter__()

    def cdash_initialize_report(self, report_data):
        if not os.path.exists(self.filename):
            os.mkdir(self.filename)
        report_data['install_command'] = self.install_command
        report_data['buildstamp'] = self.buildstamp
        report_data['hostname'] = self.hostname
        report_data['osname'] = self.osname

    def cdash_build_report(self, report_data):
        self.cdash_initialize_report(report_data)

        # Mapping Spack phases to the corresponding CTest/CDash phase.
        map_phases_to_cdash = {
            'autoreconf': 'configure',
            'cmake':      'configure',
            'configure':  'configure',
            'edit':       'configure'
        }

        # Initialize data structures common to each phase's report.
        cdash_phases = set(map_phases_to_cdash.values())
        for phase in cdash_phases:
            report_data[phase] = {}
            report_data[phase]['log'] = ""
            report_data[phase]['status'] = 0
            report_data[phase]['starttime'] = self.starttime
            report_data[phase]['endtime'] = self.starttime

        # Track the phases we perform so we know what reports to create.
        phases_encountered = []

        # Parse output phase-by-phase.
        phase_regexp = re.compile(r"Executing phase: '(.*)'")
        for spec in self.collector.specs:
            for package in spec['packages']:
                if 'stdout' in package:
                    current_phase = ''
                    for line in package['stdout'].splitlines():
                        match = phase_regexp.search(line)
                        if match:
                            current_phase = match.group(1)
                            if current_phase not in map_phases_to_cdash:
                                current_phase = ''
                                continue
                            beginning_of_phase = True
                        else:
                            if beginning_of_phase:
                                cdash_phase = \
                                    map_phases_to_cdash[current_phase]
                                if cdash_phase not in phases_encountered:
                                    phases_encountered.append(cdash_phase)
                                report_data[cdash_phase]['log'] += \
                                    text_type("{0} output for {1}:\n".format(
                                        cdash_phase, package['name']))
                                beginning_of_phase = False
                            report_data[cdash_phase]['log'] += \
                                xml.sax.saxutils.escape(line) + "\n"

        for phase in phases_encountered:
            errors, warnings = parse_log_events(
                report_data[phase]['log'].splitlines())
            nerrors = len(errors)

            if phase == 'configure' and nerrors > 0:
                report_data[phase]['status'] = 1

            # Write the report.
            report_name = phase.capitalize() + ".xml"
            phase_report = os.path.join(self.filename, report_name)

            with open(phase_report, 'w') as f:
                env = spack.tengine.make_environment()
                site_template = os.path.join(templates[self.format_name],
                                             'Site.xml')
                t = env.get_template(site_template)
                f.write(t.render(report_data))

                phase_template = os.path.join(templates[self.format_name],
                                              report_name)
                t = env.get_template(phase_template)
                f.write(t.render(report_data))

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.format_name:
            # Close the collector and restore the
            # original PackageBase.do_install
            self.collector.__exit__(exc_type, exc_val, exc_tb)

            report_data = {'specs': self.collector.specs}

            if self.format_name == 'cdash':
                # CDash reporting results are split across multiple files.
                self.cdash_build_report(report_data)
            else:
                # Write the report
                with open(self.filename, 'w') as f:
                    env = spack.tengine.make_environment()
                    t = env.get_template(templates[self.format_name])
                    f.write(t.render(report_data))
